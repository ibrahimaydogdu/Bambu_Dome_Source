"""
joint_capacity_by_diameter.py
En hafif tasarimlarda her elemanin eksenel kuvvetini, kendi cap icin NSR-10 Tablo G.12.11-2'den
interpole edilen 4 civata kapasitesiyle (Cg = 0.93) karsilastirir (makale Bolum 4.3).
Kullanim (03_Code_Execution icinden): python joint_capacity_by_diameter.py [--results-dir ../campaign_data/full/results]
"""
import argparse, glob, json
import numpy as np
from run_full_campaign import build_model
from fem_bridge import FEMBridge
from fast_eval import FastCore
from bamboo_catalog import BAMBOO_CATALOG as C

DTAB = np.array([80, 90, 100, 110, 115, 120, 125, 130, 135, 140, 150.])
PTAB = np.array([11.540, 12.806, 13.250, 14.515, 15.185, 15.855, 16.525, 17.195, 17.865, 18.535, 19.800])  # kN, #5 civata
ap = argparse.ArgumentParser()
ap.add_argument("--results-dir", default="C:/BambuDome_campaign/full/results")
a = ap.parse_args()
for m in ("geodesic16", "kiewitt32", "ribbed40"):
    mod = build_model(m); b = FEMBridge(mod); b.open(); b.read_groups_and_lengths()
    core = FastCore(b, C, mod.span_m, mod.disp_limit_m)
    best = min([json.load(open(f)) for f in glob.glob(f"{a.results_dir}/{m}__*.json")],
               key=lambda r: (not r["is_feasible"], r["best_structural_weight_kN"]))
    gene = np.array(best["solution"]); core.evaluate(gene)
    N, _ = b.analyze_arrays(); Nmax = np.abs(N).max(axis=1)
    D = C["D_m"].to_numpy(float)[gene[core.gidx] - 1] * 1000
    cap = 4 * 0.93 * np.interp(D, DTAB, PTAB)       # 150 mm degeri 160 mm icin tutulur
    dc = Nmax / cap
    print(f"{m}: max D/C joint = {dc.max():.3f}; members with D/C > 1: {(dc > 1).sum()}; constant 49.3 kN: {(Nmax / 49.3).max():.3f}")
