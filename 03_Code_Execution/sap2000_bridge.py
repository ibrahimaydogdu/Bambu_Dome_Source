"""
sap2000_bridge.py
SAP2000 OAPI Bridge -- Bambu Geodezik Kubbe Optimizasyonu
=========================================================
VB.net BBO_API.vb referans alinarak Python 3.10 / comtypes ile yeniden yazildi.

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
    for pid in _SAP2000_PROGIDS:
        try:
            obj = comtypes.client.CreateObject(pid)
            obj.ApplicationExit(False)
            return pid
        except Exception:
            continue
    raise RuntimeError(
        "SAP2000 COM nesnesi olusturulamadi. "
        "SAP2000 yuklu ve COM kaydi yapilmis olmalidir."
    )


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
        self._sap_object = comtypes.client.CreateObject(self._progid)
        self._sap_object.ApplicationStart()
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
        BBO_API.vb'deki orijinal COM bellek sizinti onleme mekanizmasiyla ayni mantik.
        Watchdog tetiklendikten sonra grup ve load combo bilgileri otomatik yenilenir.
        """
        if iter_no > 0 and iter_no % self.restart_every == 0:
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
        # eMatType 8 = Other
        m.PropMaterial.AddMaterial(mat_name, 8, "", "", "")
        ret = m.PropMaterial.SetMPIsotropic(mat_name, E_kPa, nu, 0.0)
        self._check(ret, "PropMaterial.SetMPIsotropic")
        ret = m.PropMaterial.SetWeightAndMass(mat_name, rho_kN_m3, 0.0)
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
            # SetPipe(Name, MatProp, Thickness=t_m, OuterDiameter=D_m, ...)
            ret = m.PropFrame.SetPipe(sec_name, mat_name, t_m, D_m)
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
        num_groups = m.GroupDef.Count
        self._group_names = []
        self._member_lengths = {}
        self._member_group = {}

        for i in range(1, num_groups):  # 0 = "ALL" grubu
            gname = str(i)
            try:
                ret, num_items, obj_types, obj_names = (
                    m.GroupDef.GetAssignments(gname, 0, [], [])
                )
            except Exception:
                continue
            if ret != 0:
                continue
            self._group_names.append(gname)

            for k in range(num_items):
                if obj_types[k] != 2:   # 2 = Frame
                    continue
                mem_name = str(obj_names[k])
                try:
                    ret2, p1, p2 = m.FrameObj.GetPoints(mem_name, "", "")
                    _r3, x1, y1, z1 = m.PointObj.GetCoordCartesian(p1, 0.0, 0.0, 0.0)
                    _r4, x2, y2, z2 = m.PointObj.GetCoordCartesian(p2, 0.0, 0.0, 0.0)
                    L = math.sqrt(
                        (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
                    )
                except Exception:
                    L = 1.0  # Hatali okumada 1 m varsayilan
                self._member_lengths[mem_name] = L
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
        try:
            ret, _n, names = m.RespCombo.GetNameList(0, [])
            if ret == 0 and names:
                self._load_combos = list(names)
        except Exception:
            pass
        if not self._load_combos:
            try:
                ret2, _n2, lnames = m.LoadCases.GetNameList(0, [])
                if ret2 == 0 and lnames:
                    self._load_combos = list(lnames)
            except Exception:
                pass
        logger.info("Yuk durumu/kombo sayisi: %d", len(self._load_combos))
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
        for i, sec_idx in enumerate(group_section_indices):
            gname = str(i + 1)
            row = catalog_df.loc[int(sec_idx)]
            sec_name = str(row["name"])
            # Grup adi ile toplu atama dene
            ret = m.FrameObj.SetSection(gname, sec_name, 1)
            if ret != 0:
                # Yedek: elemanlari tek tek ata
                for mem_name, grp in self._member_group.items():
                    if grp == gname:
                        m.FrameObj.SetSection(mem_name, sec_name, 0)

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

        # Yuk durumu/kombo secimi
        m.Results.Setup.DeselectAllCasesAndCombosForOutput()
        for lc in self._load_combos:
            try:
                m.Results.Setup.SetCaseSelectedForOutput(lc)
            except Exception:
                pass
            try:
                m.Results.Setup.SetComboSelectedForOutput(lc)
            except Exception:
                pass

        # Analiz
        m.File.Save(self.sdb_path)
        ret = m.Analyze.RunAnalysis()
        self._check(ret, "Analyze.RunAnalysis")
        self._analysis_count += 1
        logger.debug("Analiz #%d tamamlandi.", self._analysis_count)

        # -- Eksenel kuvvetler (FrameForce) --
        axial: dict[str, float] = {}
        try:
            (ret, nres,
             obj_arr, obj_sta, elm_arr, elm_sta,
             lc_arr, stt, stn,
             P, V2, V3, T_, M2, M3) = m.Results.FrameForce(
                "ALL", 2, 0, [], [], [], [], [], [], [], [], [], [], [], []
            )
            if ret == 0:
                for j in range(nres):
                    mem = str(obj_arr[j])
                    pv = float(P[j])
                    if mem not in axial or abs(pv) > abs(axial[mem]):
                        axial[mem] = pv
        except Exception as exc:
            logger.error("FrameForce okuma hatasi: %s", exc)

        # -- Yer degistirmeler (JointDispl) --
        disp: dict[str, tuple[float, float, float]] = {}
        try:
            (ret2, nj,
             jo, je, jlc, jst, jsn,
             U1, U2, U3, R1, R2, R3) = m.Results.JointDispl(
                "ALL", 2, 0, [], [], [], [], [], [], [], [], [], []
            )
            if ret2 == 0:
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
        except Exception as exc:
            logger.error("JointDispl okuma hatasi: %s", exc)

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
