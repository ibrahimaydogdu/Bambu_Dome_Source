"""
sap_export.py
TrussModel + kesit atamasi (gen) -> SAP2000 .sdb dosyasi, ve FEM cozucusu ile
SAP2000 sonuclarinin karsilastirilmasi.

  export_model(model, gene, catalog, out_path)   -> .sdb yazar (analiz kosmaz)
  verify_with_sap(model, gene, catalog, ...)     -> SAP2000'de acip analiz eder,
                                                    FEM ile eksenel kuvvet / yer
                                                    degistirme / ISO 22156 D/C farkini doner

SAP2000 modeli: birimler kN-m; yalniz UX,UY,UZ aktif; cubuk uclarinda moment
serbest; yuk desenleri DEAD/SNOW/WIND_N/WIND_P (kendi agirlik carpani 0, yukler
dugum kuvveti); LRFD kombinasyonlari RespCombo olarak tanimli.
"""

from __future__ import annotations
import logging
import shutil
from pathlib import Path

import numpy as np

import sap2000_bridge as sb
from bamboo_catalog import MATERIAL_PROPERTIES as MP
from truss_model import TrussModel, LOAD_CASES

logger = logging.getLogger(__name__)

_PAT_TYPE = {"DEAD": 1, "SNOW": 7, "WIND_N": 6, "WIND_P": 6}   # eLoadPatternType
_TT = [True, True, True, False, False, False]
_FF = [False, False, False, False, False, False]
_REL_I = [False, False, False, True, True, True]    # burulma + 2 moment (I ucu)
_REL_J = [False, False, False, False, True, True]   # 2 moment (J ucu); iki uc burulma serbest olamaz


def _ok(res, what: str, allow=()) -> None:
    ret, _ = sb._split(res)
    if ret != 0 and ret not in allow:
        raise RuntimeError(f"SAP2000 OAPI hatasi [ret={ret}] -- {what}")


def export_model(model: TrussModel, gene, catalog, out_path, hidden: bool = True,
                 mat_name: str = "BAMBOO_GUADUA") -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gene = [int(g) for g in gene]
    if len(gene) != len(model.group_names):
        raise ValueError("Gen uzunlugu grup sayisina esit degil.")

    obj = sb._create_sap_object(sb._find_sap_progid())
    obj.ApplicationStart()
    if hidden:
        try:
            obj.Hide()
        except Exception:
            pass
    m = obj.SapModel
    try:
        _ok(m.InitializeNewModel(6), "InitializeNewModel(kN-m)")
        _ok(m.File.NewBlank(), "File.NewBlank")

        # Malzeme ve kesitler
        _ok(m.PropMaterial.SetMaterial(mat_name, 3), "SetMaterial")
        _ok(m.PropMaterial.SetMPIsotropic(mat_name, MP["E_mean"], MP["nu"], 0.0), "SetMPIsotropic")
        _ok(m.PropMaterial.SetWeightAndMass(mat_name, 1, MP["rho"] * 9.81 / 1000.0), "SetWeightAndMass")
        for _, row in catalog.iterrows():
            _ok(m.PropFrame.SetPipe(str(row["name"]), mat_name, float(row["D_m"]), float(row["t_m"])),
                f"SetPipe({row['name']})")

        # Dugumler (ad = model dugum adi) ve mesnetler
        for i, name in enumerate(model.joint_names):
            x, y, z = (float(v) for v in model.xyz[i])
            ret, (nm,) = sb._split(m.PointObj.AddCartesian(x, y, z, "", name))
            if ret != 0 or nm != name:
                raise RuntimeError(f"Dugum eklenemedi: {name} -> {nm} (ret={ret})")
            if model.fixed[3 * i: 3 * i + 3].all():
                _ok(m.PointObj.SetRestraint(name, _TT), f"SetRestraint({name})")

        # Cubuklar (gruba gore kesit) ve uc serbestlestirmeleri
        sec_of = {}
        for g, members in zip(model.group_names, model.group_members):
            sec = str(catalog.loc[gene[int(g) - 1]]["name"])
            for k in members:
                sec_of[int(k)] = sec
        for k, name in enumerate(model.frame_names):
            a, b = model.joint_names[model.fi[k]], model.joint_names[model.fj[k]]
            ret, (nm,) = sb._split(m.FrameObj.AddByPoint(a, b, "", sec_of[k], name))
            if ret != 0 or nm != name:
                raise RuntimeError(f"Cubuk eklenemedi: {name} -> {nm} (ret={ret})")
            _ok(m.FrameObj.SetReleases(name, _REL_I, _REL_J, [0.0] * 6, [0.0] * 6), f"SetReleases({name})")

        # Gruplar
        for g, members in zip(model.group_names, model.group_members):
            _ok(m.GroupDef.SetGroup(g), f"SetGroup({g})")
            for k in members:
                _ok(m.FrameObj.SetGroupAssign(model.frame_names[int(k)], g), f"SetGroupAssign({g})")

        # Yuk desenleri ve dugum yukleri
        for pat, F in model.patterns.items():
            ret = sb._split(m.LoadPatterns.Add(pat, _PAT_TYPE[pat], 0.0, True))[0]
            if ret != 0:                                  # DEAD bos modelde hazir gelir
                _ok(m.LoadPatterns.SetSelfWTMultiplier(pat, 0.0), f"SetSelfWTMultiplier({pat})")
            for i in np.flatnonzero(np.abs(F).sum(axis=1) > 0):
                _ok(m.PointObj.SetLoadForce(model.joint_names[i], pat,
                                            [float(F[i, 0]), float(F[i, 1]), float(F[i, 2]), 0, 0, 0]),
                    f"SetLoadForce({pat},{model.joint_names[i]})")
        _ok(m.LoadPatterns.SetSelfWTMultiplier("DEAD", 0.0), "DEAD selfwt=0")

        # LRFD kombinasyonlari
        for combo, terms in LOAD_CASES.items():
            _ok(m.RespCombo.Add(combo, 0), f"RespCombo.Add({combo})")
            for pat, f in terms.items():
                _ok(m.RespCombo.SetCaseList(combo, 0, pat, float(f)), f"SetCaseList({combo},{pat})")

        _ok(m.Analyze.SetActiveDOF(_TT), "SetActiveDOF")
        _ok(m.File.Save(str(out_path)), "File.Save")
        logger.info("SAP2000 modeli yazildi: %s", out_path)
    finally:
        try:
            obj.ApplicationExit(False)
        except Exception:
            pass
    return out_path


def verify_with_sap(model: TrussModel, gene, catalog, work_dir, tag: str = "verify",
                    span_m: float = 40.0, disp_limit_m: float = 0.111,
                    deliver_path=None):
    """Modeli SAP2000'e yazar, orada analiz eder; FEM ile karsilastirir.
    Doner: dict(err_axial, err_disp, dc_sap, dc_fem, pen_sap, pen_fem, sdb_path)"""
    from fem_bridge import FEMBridge
    from iso22156_checks import evaluate_all_members

    work_dir = Path(work_dir); work_dir.mkdir(parents=True, exist_ok=True)
    for stale in work_dir.glob(f"{tag}.*"):                  # eski sonuc dosyalari -> uyari penceresi
        stale.unlink()
    sdb = export_model(model, gene, catalog, work_dir / f"{tag}.sdb")
    if deliver_path is not None:                       # analizsiz, temiz model kopyasi
        Path(deliver_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sdb, deliver_path)

    fem = FEMBridge(model); fem.open()
    groups, lengths = fem.read_groups_and_lengths()
    fem.update_sections(gene, catalog)
    aF, dF = fem.run_analysis_and_read()

    sap = sb.SAP2000Bridge(sdb_path=sdb, hidden=True)
    sap.open()
    try:
        sap.read_groups_and_lengths(); sap.read_load_combos()
        aS, dS = sap.run_analysis_and_read()
        sap_groups = list(sap._group_names)
        by_case = {k: dict(v) for k, v in sap.axial_by_case.items()}
    finally:
        sap.close()
    if sap_groups != groups:
        raise RuntimeError(f"Grup sirasi uyusmuyor: {sap_groups[:3]} / {groups[:3]}")

    refN = max(abs(v) for v in aS.values()) or 1.0
    refU = max(abs(c) for v in dS.values() for c in v) or 1.0
    eN = max(abs(aF[k] - aS[k]) for k in aS) / refN
    eU = max(abs(a - b) for k in dS for a, b in zip(dF[k], dS[k])) / refU

    # ASD kontrolu (kampanyadakiyle ayni): kombinasyon bazli kuvvetler, yuk suresi carpani, grup-max ceza
    import numpy as np
    from fast_eval import FastCore, dc_force
    core = FastCore(fem, catalog, span_m, disp_limit_m)
    penF_core = core.evaluate(np.asarray(gene, dtype=int))[2]
    dcF = float(core.last["dc"].max())
    cases = fem._load_combos
    NS = np.array([[by_case[n][c] for c in cases] for n in fem._frame_names])
    sec = np.asarray(gene)[core.gidx] - 1
    A, r = core.A_sec[sec], core.r_sec[sec]
    Ns = NS / core.kcase[None, :]
    Nj = np.abs(NS).max(axis=1)
    dc = np.maximum(dc_force(Ns.max(axis=1), A, r, core.L, "all", Nj), dc_force(Ns.min(axis=1), A, r, core.L, "all", Nj))
    dcg = np.maximum.reduceat(dc[core.order], core.starts)
    uS = max(abs(c) for v in dS.values() for c in v)
    penS = float(np.maximum(dcg - 1.0, 0.0).sum()) + max(uS / core.limit - 1.0, 0.0)
    dcS = float(dc.max())
    return dict(err_axial=eN, err_disp=eU, dc_fem=dcF, dc_sap=dcS,
                pen_fem=penF_core, pen_sap=penS, max_axial_kN=refN, sdb_path=sdb)


def export_best(model: TrussModel, results: dict, catalog, out_dir, run_tag: str,
                work_dir, span_m: float = 40.0, disp_limit_m: float = 0.111) -> list[dict]:
    """Her algoritmanin arsivindeki en hafif (f1) uygulanabilir cozumu SAP2000 .sdb olarak
    kaydeder ve SAP2000 analizi ile FEM'i karsilastirir.
    results: {algo: (sols, objs)}  -- objs[i] = (f1, f2)"""
    import json
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for algo, (sols, objs) in results.items():
        if not objs:
            logger.warning("%s: uygulanabilir cozum yok -- SAP2000 dosyasi yazilmadi.", algo.upper())
            continue
        i = int(np.argmin([o[0] for o in objs]))
        gene = [int(round(g)) for g in sols[i]]
        tag = f"best_{algo}_{run_tag}"
        try:
            r = verify_with_sap(model, gene, catalog, work_dir, tag=tag, span_m=span_m,
                                disp_limit_m=disp_limit_m, deliver_path=out_dir / f"{tag}.sdb")
        except Exception as exc:                       # SAP2000 hatasi optimizasyon sonuclarini bozmasin
            logger.error("%s: SAP2000 dogrulamasi basarisiz: %s", algo.upper(), exc)
            continue
        r.update(algo=algo, f1_kN=float(objs[i][0]), f2_kgCO2e=float(objs[i][1]), gene=gene)
        r.pop("sdb_path", None)
        (out_dir / f"{tag}.json").write_text(json.dumps(r, indent=2), encoding="utf-8")
        logger.info("%s: en iyi cozum SAP2000'e yazildi (%s). Hata: eksenel %.1e, yer degistirme %.1e; "
                    "D/C FEM %.4f / SAP %.4f", algo.upper(), f"{tag}.sdb", r["err_axial"], r["err_disp"],
                    r["dc_fem"], r["dc_sap"])
        report.append(r)
    return report
