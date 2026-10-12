"""
steel_reference.py
Referans CELIK yapi: ayni aciklik, ayni geometri, ayni yuk desenleri ve ayni ASD kombinasyonlari,
yalniz malzeme/yonetmelik degisir. Bambu sonuclariyla malzeme etkisi karsilastirmasi icin (bkz. results_report.py).

Varsayimlar (HEPSI doğrulanacak; karsilastirma duyarliligi results_report.py'de taranir):
  * Profil: 24 elemanli tipik CHS (EN 10219 boyutlari, 33.7x2.6 ... 244.5x10; kucuk kesitler dahil ki alt sinir baglayici olmasin), S355 (Fy=355 MPa), E=210 GPa, rho=7850 kg/m3.
  * Yonetmelik: AISC 360 ASD: cekme 0.6 Fy; basinc Fcr/1.67 (E3), KL/r <= 200 (basinc), 300 (cekme); K=1.
    Baglanti (hub/civata) ayrica kontrol edilmez (celik dugum yeterli kabul edilir).
  * Yuk: bambu ile ayni DEAD/SNOW/WIND desenleri ve ASD kombinasyonlari (ozagirlik dahil degil, benchmark gibi).
  * Yer degistirme siniri: bambu ile ayni, aciklik/150.
  * Dugum/baglanti celigi: bambudaki ile ayni model (m_hub, c_s0), harc yok.

Kullanim:  python steel_reference.py run [--seeds 30] [--workers 7]
Cikti:     C:\\BambuDome_campaign\\steel_ref\\results\\<model>__abc__s<seed>.json
"""
from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(r"C:\BambuDome_campaign\steel_ref")
FY = 355.0e3            # kPa (S355)
E_S = 210.0e6           # kPa
RHO_S = 7850.0          # kg/m3
LAM_C, LAM_T = 200.0, 300.0
CODE = "aisc360"        # "aisc360" (AISC 360-16 ASD) | "asd89" (AISC-ASD 1989; literatur 354MemberDome.pdf ile ayni)
CATALOG = "chs24"       # "chs24" (EN 10219 CHS) | "aisc37" (literaturdeki 37 AISC boru; aisc_pipes.py)


def configure(code=None, catalog=None, fy_mpa=None, e_gpa=None):
    global CODE, CATALOG, FY, E_S
    if code: CODE = code
    if catalog: CATALOG = catalog
    if fy_mpa: FY = fy_mpa * 1e3
    if e_gpa: E_S = e_gpa * 1e6
OMEGA_C = 1.67
MODELS = ["ribbed354", "ribbed40", "kiewitt32", "geodesic16"]   # ribbed354 = orijinal 354 elemanli referans
CHS = [(33.7, 2.6), (42.4, 2.6), (48.3, 2.9), (48.3, 4.0), (60.3, 2.9), (60.3, 4.0), (76.1, 2.9), (76.1, 4.0),
       (88.9, 3.2), (88.9, 5.0), (114.3, 3.6), (114.3, 5.0), (114.3, 6.3), (139.7, 4.0), (139.7, 6.3), (168.3, 4.5),
       (168.3, 6.3), (168.3, 8.0), (193.7, 5.0), (193.7, 8.0), (219.1, 6.3), (219.1, 8.0), (244.5, 8.0), (244.5, 10.0)]


def steel_catalog() -> pd.DataFrame:
    if CATALOG == "aisc37":
        from aisc_pipes import aisc37_catalog
        return aisc37_catalog()
    rows = []
    for i, (D, t) in enumerate(CHS, start=1):
        D_m, t_m = D / 1000.0, t / 1000.0
        d = D_m - 2 * t_m
        A = math.pi / 4 * (D_m ** 2 - d ** 2)
        I = math.pi / 64 * (D_m ** 4 - d ** 4)
        rows.append(dict(idx=i, D_m=D_m, t_m=t_m, A_m2=A, r_m=math.sqrt(I / A)))
    return pd.DataFrame(rows).set_index("idx", drop=False)


def build_model(name: str):
    from run_full_campaign import build_model as bm
    if name == "ribbed354":
        from truss_model import build_dome_model
        return build_dome_model(1, 40.0)
    return bm(name)


def steel_dc(N, A, r, L):
    """ASD talep/kapasite (cekme +). N: kN (servis kuvveti). CODE: aisc360 | asd89."""
    lam = L / r
    ft = 0.6 * FY
    dct = np.where(N > 1e-9, N / A / ft, 0.0)
    if CODE == "asd89":
        from aisc_pipes import asd89_compression_allowable
        fa = asd89_compression_allowable(lam, FY, E_S)
    else:
        fe = math.pi ** 2 * E_S / np.maximum(lam, 1.0) ** 2
        lim = 4.71 * math.sqrt(E_S / FY)
        fa = np.where(lam <= lim, (0.658 ** (FY / fe)) * FY, 0.877 * fe) / OMEGA_C
    dcc = np.where(N < -1e-9, np.abs(N) / A / fa, 0.0)
    sl = np.where(N < -1e-9, lam / LAM_C, lam / LAM_T)
    return np.maximum(np.maximum(dct, dcc), sl)


class SteelCore:
    """FastCore ile ayni arayuz: evaluate(gene) -> (f1 agirlik kN, f2 karbon kgCO2e, P)."""

    def __init__(self, bridge, catalog, span_m, disp_limit_m, ec_tube=None, ec_conn=None, m_hub=2.0, c_s0=0.5):
        self.bridge = bridge
        self.gidx = bridge.group_index
        self.L = bridge.member_lengths_arr
        self.G = int(self.gidx.max()) + 1
        self.order = np.argsort(self.gidx, kind="stable")
        counts = np.bincount(self.gidx, minlength=self.G)
        self.starts = np.concatenate(([0], np.cumsum(counts)[:-1]))
        self.n_nodes = bridge.n_nodes
        self.limit = disp_limit_m
        self.A_sec = catalog["A_m2"].to_numpy(float)
        self.r_sec = catalog["r_m"].to_numpy(float)
        from bamboo_catalog import MATERIAL_PROPERTIES as _MP
        self.ec_tube = _MP["EC_steel_tube"] if ec_tube is None else ec_tube
        self.ec_conn = _MP["EC_steel"] if ec_conn is None else ec_conn
        self.conn_kg = self.n_nodes * m_hub + 2.0 * len(self.L) * c_s0
        self.last: dict = {}

    def evaluate(self, gene):
        sec = np.asarray(np.round(gene[self.gidx] - 1), dtype=int)
        A = self.A_sec[sec]; r = self.r_sec[sec]
        self.bridge.set_member_areas(A)
        N, umax = self.bridge.analyze_arrays()
        dc = np.maximum(steel_dc(N.max(axis=1), A, r, self.L), steel_dc(N.min(axis=1), A, r, self.L))
        dcg = np.maximum.reduceat(dc[self.order], self.starts)
        p = float(np.maximum(dcg - 1.0, 0.0).sum()) + max(umax / self.limit - 1.0, 0.0)
        mass = float((RHO_S * A * self.L).sum())
        f1 = mass * 9.81 / 1000.0
        f2 = self.ec_tube * mass + self.ec_conn * self.conn_kg
        self.last = dict(max_dc=float(dc.max()), umax=umax, dc=dc, mass_kg=mass)
        return f1, f2, p


def make_core(name: str):
    from fem_bridge import FEMBridge
    model = build_model(name)
    bridge = FEMBridge(model, E_kPa=E_S); bridge.open()
    groups, _ = bridge.read_groups_and_lengths()
    return model, bridge, SteelCore(bridge, steel_catalog(), model.span_m, model.disp_limit_m), len(groups)


def run_one(job: dict) -> dict:
    from metaheuristic_optimizers import MetaheuristicOptimizer
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    configure(code=job.get("code"), catalog=job.get("catalog"), fy_mpa=job.get("fy"), e_gpa=job.get("e"))
    model, bridge, core, G = make_core(job["model"])
    t0 = time.time()
    opt = MetaheuristicOptimizer(core.evaluate, G, 1, len(steel_catalog()), job["pop"], 10 ** 9, 2.0, job["seed"], "abc",
                                 max_evals=job["nfe_per_var"] * G)
    best, hist = opt.optimize()
    res = dict(job, n_groups=G, nfe=opt.n_evals, elapsed_s=time.time() - t0,
               best_structural_weight_kN=best.cost_value, best_embodied_carbon_kgCO2e=best.carbon_value,
               penalty=best.penalty, is_feasible=best.is_feasible, solution=best.design_variables.tolist(),
               history=hist)
    (Path(job.get("root", str(ROOT))) / "results" / f"{job['id']}.json").write_text(json.dumps(res), encoding="utf-8")
    return dict(id=job["id"], w=best.cost_value, feas=best.is_feasible, t=res["elapsed_s"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["run"])
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--pop", type=int, default=20)
    ap.add_argument("--nfe-per-var", type=int, default=1000)
    ap.add_argument("--code", default="aisc360", choices=["aisc360", "asd89"])
    ap.add_argument("--catalog", default="chs24", choices=["chs24", "aisc37"])
    ap.add_argument("--fy", type=float, default=355.0)
    ap.add_argument("--e", type=float, default=210.0)
    ap.add_argument("--out", default=None, help="sonuc klasoru (varsayilan C:\BambuDome_campaign\steel_ref)")
    ap.add_argument("--workers", type=int, default=max(1, min((os.cpu_count() or 2) - 1, 7)))
    a = ap.parse_args()
    global ROOT
    if a.out:
        ROOT = Path(a.out)
    (ROOT / "results").mkdir(parents=True, exist_ok=True)
    jobs = []
    for k in range(a.seeds):
        for m in MODELS:
            jid = f"{m}__abc__s{1001 + k}"
            if not (ROOT / "results" / f"{jid}.json").exists():
                jobs.append(dict(id=jid, model=m, seed=1001 + k, pop=a.pop, nfe_per_var=a.nfe_per_var, code=a.code,
                                 catalog=a.catalog, fy=a.fy, e=a.e, root=str(ROOT)))
    print(len(jobs), "kosu", flush=True)
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=mp.get_context("spawn")) as pool:
        futs = [pool.submit(run_one, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            r = f.result()
            print(f"[{i}/{len(jobs)}] {r['id']} W={r['w']:.2f} kN uygun={r['feas']} {r['t']:.0f}s", flush=True)


if __name__ == "__main__":
    main()
