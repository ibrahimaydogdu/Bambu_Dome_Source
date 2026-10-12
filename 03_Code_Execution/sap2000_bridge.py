"""
sap2000_bridge.py
SAP2000 OAPI Bridge -- Bambu Geodezik Kubbe Optimizasyonu
=========================================================
Python 3.10 / comtypes ile SAP2000 OAPI entegrasyonu.

Sorumluluklar:
  - SAP2000 COM baglantisi (ac, gizle, kapat)
  - Model kilit yonetimi (SetModelIsLocked)
  - Bamboo Pipe kesit tanimlama (PropFrame.SetPipe)
  - Her 100 analizde SAP2000'i yeniden baslatma (watchdog -- COM bellek hijyeni)
  - Eleman grubu, uzunluk ve yuk kombinasyonu dinamik okuma
  - Eksenel kuvvet (P) ve yer degistirme (U1/U2/U3) sonuc okuma
"""

from __future__ import annotations
import math
import time
import logging
from pathlib import Path

import comtypes.client

logger = logging.getLogger(__name__)

# SAP2000 birim kodu: kN - m - C
UNITS_KN_M = 6

# Desteklenen SAP2000 COM ProgID listesi (v16 -> v26)
_SAP2000_PROGIDS = [
    "CSI.SAP2000.API.SapObject",   # v24 / v25 / v26
    "SAP2000v1.SapObject",
    "SAP2000v16.SapObject",
]


def _find_sap_progid() -> str:
    """Sistemde kayitli SAP2000 COM ProgID'yi dondurur."""
    import comtypes
    for pid in _SAP2000_PROGIDS:
        try:
            comtypes.GUID.from_progid(pid)  # Sadece kayit kontrolu, surec baslatmaz
            return pid
        except Exception:
            continue
    raise RuntimeError(
        "SAP2000 COM nesnesi olusturulamadi. "
        "SAP2000 yuklu ve COM kaydi yapilmis olmalidir."
    )


def _split(res):
    """
    CSI OAPI + comtypes donus degerini ayristirir.
    ByRef parametreli cagrilar [out1, out2, ..., ret] listesi dondurur (ret SONDA).
    Doner: (ret, [out1, out2, ...])
    """
    if isinstance(res, (list, tuple)):
        return int(res[-1]), list(res[:-1])
    return int(res), []


def _find_sap_exe() -> str | None:
    """SAP2000_EXE ortam degiskeni veya en yeni kurulu SAP2000.exe yolunu dondurur."""
    import os
    env = os.environ.get("SAP2000_EXE")
    if env and Path(env).exists():
        return env
    root = Path(r"C:\Program Files\Computers and Structures")
    cands = sorted(root.glob("SAP2000 */SAP2000.exe"),
                   key=lambda p: int("".join(c for c in p.parent.name if c.isdigit()) or 0))
    return str(cands[-1]) if cands else None


def _create_sap_object(progid: str):
    """
    1. Varsa acik olan SAP2000 nesnesine baglanir (GetActiveObject).
    2. Yoksa SAP2000v1.Helper.CreateObjectProgID ile temiz bir sekilde baslatir.
    """
    try:
        obj = comtypes.client.GetActiveObject(progid)
        logger.info("Calisan mevcut SAP2000 oturumuna baglanildi (GetActiveObject).")
        return obj
    except Exception:
        pass

    try:
        helper = comtypes.client.CreateObject("SAP2000v1.Helper")
        logger.info("SAP2000v1.Helper ile yeni nesne olusturuluyor (%s)...", progid)
        return helper.CreateObjectProgID(progid)
    except Exception as exc:
        logger.warning("Helper yolu basarisiz (%s) -- dogrudan CreateObject deneniyor.", exc)
        return comtypes.client.CreateObject(progid)


class SAP2000Bridge:
    """
    SAP2000 ile Python arasindaki tekil iletisim koprusu.

    Kullanim:
        bridge = SAP2000Bridge(sdb_path="alara3v16.sdb", hidden=True)
        bridge.open()
        bridge.define_bamboo_material()
        bridge.define_bamboo_sections(BAMBOO_CATALOG)
        groups, lengths = bridge.read_groups_and_lengths()
        load_combos    = bridge.read_load_combos()

        for iter_no in range(1, max_iter + 1):
            bridge.update_sections(gene_vector, BAMBOO_CATALOG)
            axial, disp = bridge.run_analysis_and_read()
            bridge.watchdog(iter_no)   # Her 100 analizde SAP2000 restart

        bridge.close()
    """

    def __init__(
        self,
        sdb_path: str | Path,
        hidden: bool = True,
        restart_every: int = 100,
    ):
        self.sdb_path = str(Path(sdb_path).resolve())
        self.hidden = hidden
        self.restart_every = restart_every

        self._analysis_count: int = 0
        self._sap_object = None
        self._sap_model = None
        self._progid: str | None = None

        # Grup / eleman bilgileri (read_groups_and_lengths sonrasi dolar)
        self._group_names: list[str] = []
        self._member_lengths: dict[str, float] = {}
        self._member_group: dict[str, str] = {}
        self._load_combos: list[str] = []

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def open(self) -> None:
        """SAP2000 baslatir, model dosyasini acar ve kilidi kaldirir."""
        if self._progid is None:
            self._progid = _find_sap_progid()

        logger.info("SAP2000 baslatiliyor (%s)...", self._progid)
        self._sap_object = _create_sap_object(self._progid)
        try:
            self._sap_object.ApplicationStart()
        except Exception:
            pass
        self._sap_model = self._sap_object.SapModel

        if self.hidden:
            try:
                self._sap_object.Hide()
            except Exception:
                pass

        ret = self._sap_model.File.OpenFile(self.sdb_path)
        self._check(ret, "File.OpenFile")

        ret = self._sap_model.SetPresentUnits(UNITS_KN_M)
        self._check(ret, "SetPresentUnits(kN-m)")

        self._unlock_model()
        logger.info("SAP2000 acildi: %s", self.sdb_path)

    def close(self, save: bool = False) -> None:
        """SAP2000'i kapatir, COM nesnelerini temizler."""
        if self._sap_object is not None:
            try:
                self._sap_object.ApplicationExit(save)
            except Exception:
                pass
            self._sap_model = None
            self._sap_object = None
        logger.info("SAP2000 kapatildi.")

    def watchdog(self, iter_no: int) -> None:
        """
        Her `restart_every` iterasyonda SAP2000'i kapat-ac.
        COM bellek sizinti onleme mekanizmasi.
        Watchdog tetiklendikten sonra grup ve load combo bilgileri otomatik yenilenir.
        """
        if (iter_no > 0 and iter_no % self.restart_every == 0
                and iter_no != getattr(self, "_last_restart_at", -1)):
            self._last_restart_at = iter_no
            logger.warning(
                "WATCHDOG: iter=%d -- SAP2000 yeniden baslatiliyor "
                "(COM bellek hijyeni)...",
                iter_no,
            )
            self.close(save=False)
            time.sleep(2)
            self.open()
            self.read_groups_and_lengths()
            self.read_load_combos()

    # ------------------------------------------------------------------
    # Model Setup
    # ------------------------------------------------------------------

    def define_bamboo_material(
        self,
        mat_name: str = "BAMBOO_GUADUA",
        E_kPa: float = 11_000_000.0,   # 11,000 MPa -> kPa
        nu: float = 0.30,
        rho_kN_m3: float = 6.867,      # 700 kg/m3 * 9.81 / 1000
    ) -> None:
        """
        Bambu malzemesini SAP2000'e izotropik olarak tanimlar.
        Zaten varsa SetMPIsotropic ile guncellenir, hata verilmez.
        """
        m = self._sap_model
        # eMatType 3 = NoDesign (v2026'da 8 = Masonry; AddMaterial Region/Standard ister)
        ret = m.PropMaterial.SetMaterial(mat_name, 3)
        self._check(ret, "PropMaterial.SetMaterial")
        ret = m.PropMaterial.SetMPIsotropic(mat_name, E_kPa, nu, 0.0)
        self._check(ret, "PropMaterial.SetMPIsotropic")
        ret = m.PropMaterial.SetWeightAndMass(mat_name, 1, rho_kN_m3)  # 1 = agirlik/hacim
        self._check(ret, "PropMaterial.SetWeightAndMass")
        logger.info("Malzeme tanimlandi: %s", mat_name)

    def define_bamboo_sections(
        self, catalog_df, mat_name: str = "BAMBOO_GUADUA"
    ) -> None:
        """
        DataFrame'deki tum Pipe kesitlerini SAP2000'e PropFrame.SetPipe ile ekler.
        catalog_df: bamboo_catalog.py::BAMBOO_CATALOG
        """
        m = self._sap_model
        self._unlock_model()
        ok, fail = 0, 0
        for idx, row in catalog_df.iterrows():
            sec_name = str(row["name"])
            D_m = float(row["D_m"])
            t_m = float(row["t_m"])
            # SetPipe(Name, MatProp, T3=dis cap, Tw=et kalinligi)
            ret = m.PropFrame.SetPipe(sec_name, mat_name, D_m, t_m)
            if ret == 0:
                ok += 1
            else:
                logger.warning("SetPipe hatasi (ret=%d): %s", ret, sec_name)
                fail += 1
        logger.info("Kesit tanimlama: %d basarili, %d hatali.", ok, fail)

    # ------------------------------------------------------------------
    # Model Reading
    # ------------------------------------------------------------------

    def read_groups_and_lengths(self) -> tuple[list[str], dict[str, float]]:
        """
        SAP2000 modelindeki simetri gruplarini ve her eleman uzunlugunu okur.

        Donerler:
          group_names    : ['1', '2', ..., '22']
          member_lengths : {eleman_adi: uzunluk_m}
        """
        m = self._sap_model
        self._group_names = []
        self._member_lengths = {}
        self._member_group = {}

        ret, (_n, all_groups) = _split(m.GroupDef.GetNameList(0, []))
        self._check(ret, "GroupDef.GetNameList")
        names = [str(g) for g in all_groups if str(g).upper() != "ALL"]
        # Sayisal grup adlari (1..22) sayisal sirada; digerleri alfabetik sonda
        names.sort(key=lambda s: (0, int(s)) if s.isdigit() else (1, s))

        coord_cache: dict[str, tuple[float, float, float]] = {}

        def _xyz(pt: str) -> tuple[float, float, float]:
            if pt not in coord_cache:
                r, (x, y, z) = _split(m.PointObj.GetCoordCartesian(pt, 0.0, 0.0, 0.0))
                self._check(r, f"PointObj.GetCoordCartesian({pt})")
                coord_cache[pt] = (x, y, z)
            return coord_cache[pt]

        for gname in names:
            ret, (num_items, obj_types, obj_names) = _split(
                m.GroupDef.GetAssignments(gname, 0, [], [])
            )
            if ret != 0:
                continue
            frames = [str(obj_names[k]) for k in range(num_items) if obj_types[k] == 2]
            if not frames:          # Cubuk icermeyen gruplari (mesnet vb.) atla
                continue
            self._group_names.append(gname)
            for mem_name in frames:
                r2, (p1, p2) = _split(m.FrameObj.GetPoints(mem_name, "", ""))
                self._check(r2, f"FrameObj.GetPoints({mem_name})")
                (x1, y1, z1), (x2, y2, z2) = _xyz(p1), _xyz(p2)
                self._member_lengths[mem_name] = math.sqrt(
                    (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
                )
                self._member_group[mem_name] = gname

        logger.info(
            "Grup okuma tamam: %d grup, %d eleman.",
            len(self._group_names),
            len(self._member_lengths),
        )
        return self._group_names, self._member_lengths

    def read_load_combos(self) -> list[str]:
        """Tum yuk kombinasyonlarini (yoksa yuk durumlarini) okur."""
        m = self._sap_model
        self._load_combos = []
        self._combos_are_cases = False
        try:
            ret, (_n, names) = _split(m.RespCombo.GetNameList(0, []))
            if ret == 0 and names:
                self._load_combos = [str(x) for x in names]
        except Exception as exc:
            logger.warning("RespCombo.GetNameList hatasi: %s", exc)
        if not self._load_combos:
            try:
                ret2, (_n2, lnames) = _split(m.LoadCases.GetNameList(0, []))
                if ret2 == 0 and lnames:
                    self._load_combos = [str(x) for x in lnames]
                    self._combos_are_cases = True
            except Exception as exc:
                logger.warning("LoadCases.GetNameList hatasi: %s", exc)
        logger.info("Yuk durumu/kombo sayisi: %d -> %s",
                    len(self._load_combos), self._load_combos)
        return self._load_combos

    # ------------------------------------------------------------------
    # Optimization Loop
    # ------------------------------------------------------------------

    def update_sections(
        self, group_section_indices: list[int], catalog_df
    ) -> None:
        """
        Her simetri grubuna katalog kesiti atar.
        group_section_indices[i] = katalog ID (1-24) for i. grup (1-tabanli)
        """
        m = self._sap_model
        self._unlock_model()
        if len(group_section_indices) != len(self._group_names):
            raise ValueError(
                f"Gen uzunlugu ({len(group_section_indices)}) grup sayisina "
                f"({len(self._group_names)}) esit degil."
            )
        for gname, sec_idx in zip(self._group_names, group_section_indices):
            row = catalog_df.loc[int(sec_idx)]
            sec_name = str(row["name"])
            # Grup adi ile toplu atama (eItemType.Group = 1)
            ret = _split(m.FrameObj.SetSection(gname, sec_name, 1))[0]
            if ret != 0:
                # Yedek: elemanlari tek tek ata
                for mem_name, grp in self._member_group.items():
                    if grp == gname:
                        r = _split(m.FrameObj.SetSection(mem_name, sec_name, 0))[0]
                        self._check(r, f"FrameObj.SetSection({mem_name})")

    def run_analysis_and_read(
        self,
    ) -> tuple[dict[str, float], dict[str, tuple[float, float, float]]]:
        """
        Analiz calistirir; eksenel kuvvet ve yer degistirme sonuclarini okur.

        Donerler:
          axial : {eleman_adi: max_eksenel_kN}   (en kritik mutlak deger)
          disp  : {dugum_adi: (U1, U2, U3) [m]}  (en buyuk mutlak deger)
        """
        m = self._sap_model
        self._unlock_model()

        # Analiz (yerel calisma kopyasina kaydedilir; orijinal .sdb korunur)
        _split(m.File.Save(self.sdb_path))
        ret = _split(m.Analyze.RunAnalysis())[0]
        self._check(ret, "Analyze.RunAnalysis")
        self._analysis_count += 1
        logger.debug("Analiz #%d tamamlandi.", self._analysis_count)

        # Cikti secimi (analizden sonra)
        m.Results.Setup.DeselectAllCasesAndCombosForOutput()
        for lc in self._load_combos:
            if getattr(self, "_combos_are_cases", False):
                m.Results.Setup.SetCaseSelectedForOutput(lc)
            else:
                m.Results.Setup.SetComboSelectedForOutput(lc)

        # -- Eksenel kuvvetler (FrameForce) --
        axial: dict[str, float] = {}
        ret, out = _split(m.Results.FrameForce(
            "ALL", 2, 0, [], [], [], [], [], [], [], [], [], [], [], [], []
        ))
        if ret != 0:
            raise RuntimeError(f"Results.FrameForce ret={ret}")
        nres, obj_arr, P = out[0], out[1], out[8]
        case_arr = out[5]
        self.axial_by_case = {}                      # {eleman: {yuk durumu/kombinasyon: P}} (ASD zarfi icin)
        for j in range(nres):
            mem = str(obj_arr[j])
            pv = float(P[j])
            self.axial_by_case.setdefault(mem, {})[str(case_arr[j])] = pv
            if mem not in axial or abs(pv) > abs(axial[mem]):
                axial[mem] = pv

        # -- Yer degistirmeler (JointDispl) --
        disp: dict[str, tuple[float, float, float]] = {}
        ret2, out2 = _split(m.Results.JointDispl(
            "ALL", 2, 0, [], [], [], [], [], [], [], [], [], [], []
        ))
        if ret2 != 0:
            raise RuntimeError(f"Results.JointDispl ret={ret2}")
        nj, jo = out2[0], out2[1]
        U1, U2, U3 = out2[6], out2[7], out2[8]
        for j in range(nj):
            jn = str(jo[j])
            u1, u2, u3 = float(U1[j]), float(U2[j]), float(U3[j])
            if jn not in disp:
                disp[jn] = (u1, u2, u3)
            else:
                prev = disp[jn]
                disp[jn] = (
                    u1 if abs(u1) > abs(prev[0]) else prev[0],
                    u2 if abs(u2) > abs(prev[1]) else prev[1],
                    u3 if abs(u3) > abs(prev[2]) else prev[2],
                )

        return axial, disp

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _unlock_model(self) -> None:
        m = self._sap_model
        if m is None:
            return
        try:
            if m.GetModelIsLocked():
                ret = m.SetModelIsLocked(False)
                self._check(ret, "SetModelIsLocked(False)")
        except Exception:
            pass

    @staticmethod
    def _check(ret: int, context: str) -> None:
        if ret != 0:
            raise RuntimeError(f"SAP2000 OAPI hatasi [ret={ret}] -- {context}")
