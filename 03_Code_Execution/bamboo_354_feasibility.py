"""
bamboo_354_feasibility.py
Orijinal 354 elemanli (frekans-1) kubbe icin bambu kesit katalogu ile uygun tasarim var mi? (makale Bolum 3.1)
 1) Tum gruplarda en buyuk katalog kesiti: ceza toplami P ve en buyuk eleman kuvveti
 2) ABC (pop 20, NFE = 1000 N_g), tohum 1001-1003
Kullanim (03_Code_Execution icinden): python bamboo_354_feasibility.py [--config ../campaign_data/full/config.json]
"""
import argparse, json, logging, random
import numpy as np
from truss_model import build_dome_model
from fem_bridge import FEMBridge
from run_full_campaign import make_evaluator
from bamboo_catalog import BAMBOO_CATALOG
from metaheuristic_optimizers import MetaheuristicOptimizer

ap = argparse.ArgumentParser()
ap.add_argument("--config", default="C:/BambuDome_campaign/full/config.json")
a = ap.parse_args()
logging.getLogger().setLevel(logging.WARNING)
cfg = json.load(open(a.config))
mod = build_dome_model(1, 40.0)                     # freq 1 = 354 elemanli referans
b = FEMBridge(mod); b.open(); groups, lengths = b.read_groups_and_lengths()
core = make_evaluator(mod, b, lengths, cfg)
G = len(groups)
print(f"members {len(mod.fi)}, groups {G}, member length {min(lengths.values()):.2f}-{max(lengths.values()):.2f} m")
heavy = np.full(G, int(BAMBOO_CATALOG["A_m2"].values.argmax()) + 1)
res = core.evaluate(heavy)
print(f"largest section everywhere: weight {res[0]:.2f} kN, penalty sum P = {res[2]:.2f}")
N, _ = b.analyze_arrays(); Nmax = np.abs(N).max(axis=1)
print(f"largest member force {Nmax.max():.1f} kN; members above 49.3 kN: {(Nmax > 49.3).sum()}")
for seed in (1001, 1002, 1003):
    random.seed(seed); np.random.seed(seed)
    opt = MetaheuristicOptimizer(eval_fn=core.evaluate, n_vars=G, lb=1, ub=len(BAMBOO_CATALOG), pop_size=20, max_iters=10 ** 9,
                                 max_evals=1000 * G, penalty_exp=cfg["penalty_exp"], seed=seed, method="abc")
    best, _ = opt.optimize()
    print(f"seed {seed}: feasible {best.is_feasible}, weight {best.cost_value:.2f} kN, P = {best.penalty:.3f}")
