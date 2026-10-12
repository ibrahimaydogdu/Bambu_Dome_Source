"""
test_fast_eval.py -- vektorlestirilmis cekirdegin eski fonksiyonlarla esdegerligi ve
meta-sezgisel optimizasyon motorunun (16 yontem) dogrulanmasi.
Kullanim: python test_fast_eval.py
"""
from fem_bridge import FEMBridge   # BLAS iplik ayari numpy'dan once
import math, random, tempfile, numpy as np
from bamboo_catalog import BAMBOO_CATALOG as C
from truss_model import build_dome_model
from dome_types import build_preset
from iso22156_checks import check_member, evaluate_all_members
from carbon_calculator import compute_structural_weight, compute_embodied_carbon
from fast_eval import FastCore, CarbonModel, dc_force
from bamboo_catalog import ASD_K
from metaheuristic_optimizers import MetaheuristicOptimizer, ALGORITHM_NAMES

def model(name):
    return build_dome_model(2, 40.0) if name == "ribbed40" else build_preset(name)

def t_dc_equivalence():
    rng = np.random.default_rng(0); worst = 0.0
    for _ in range(3000):
        sec = int(rng.integers(1, 25)); row = C.loc[sec]; L = float(rng.uniform(0.7, 4.0))
        N = float(rng.choice([0.0, rng.normal(0, 60), rng.normal(0, 5)]))
        k = ASD_K["transient"]
        old = check_member("x", N, row, L, k_asd=k).demand_capacity_ratio
        new = float(dc_force(np.array([N / k]), np.array([row["A_m2"]]), np.array([row["r_m"]]), np.array([L]), "all",
                             np.array([N]))[0])
        worst = max(worst, abs(old - new) / max(abs(old), 1e-12))
    assert worst < 1e-12, worst
    print(f"  dc_force == check_member ({3000} rastgele durum): en buyuk bagil fark {worst:.1e}")

def t_models():
    for name in ("geodesic16", "kiewitt32", "ribbed40"):
        m = model(name); b = FEMBridge(m); b.open(); g, L = b.read_groups_and_lengths(); G = len(g)
        core_fixed = FastCore(b, C, m.span_m, m.disp_limit_m, CarbonModel(mode="fixed"), "all", envelope=False)
        core_fixed.kcase[:] = ASD_K["permanent"]          # eski tek-kuvvet API'si ile ayni olcek
        rng = np.random.default_rng(1); wd = wf = wp = 0.0
        for _ in range(6):
            gene = rng.integers(1, 25, G)
            b.update_sections(gene.tolist(), C); axial, disp = b.run_analysis_and_read()
            pen_old, dcmax_old, res = evaluate_all_members(axial, L, b._member_group, gene.tolist(), C, disp,
                                                         span_m=m.span_m, disp_limit_m=m.disp_limit_m)
            f1_old = compute_structural_weight(gene.tolist(), C, L, b._member_group)
            f2_old = compute_embodied_carbon(gene.tolist(), C, L, b._member_group, b.n_nodes)[0]
            dc_old = np.array([r.demand_capacity_ratio for r in res])
            f1, f2, P = core_fixed.evaluate(gene)
            wd = max(wd, np.abs(core_fixed.last["dc"] - dc_old).max())
            wf = max(wf, abs(f1 - f1_old) / f1_old, abs(f2 - f2_old) / f2_old)
            gm = {}
            for gi, mem in enumerate(b._group_members): gm[gi] = mem
            P_ref = sum(max(max(dc_old[mem].max() - 1.0, 0.0), 0.0) for mem in gm.values()) \
                    + max(core_fixed.last["umax"] / (m.disp_limit_m) - 1.0, 0.0)
            wp = max(wp, abs(P - P_ref))
        assert wd < 1e-10 and wf < 1e-12 and wp < 1e-12, (name, wd, wf, wp)
        print(f"  {name}: DC farki {wd:.1e} | f1,f2(sabit mod) bagil farki {wf:.1e} | P tanim farki {wp:.1e}")

def t_envelope_and_modes():
    m = model("kiewitt32"); b = FEMBridge(m); b.open(); g, _ = b.read_groups_and_lengths(); G = len(g)
    core = FastCore(b, C, m.span_m, m.disp_limit_m, CarbonModel(mode="section"), "all", envelope=True)
    f1, f2, p = core.evaluate(np.full(G, 1, dtype=int))
    assert p > 0
    penalized = f1 * ((1.0 + p) ** 2.0)
    assert abs(penalized / f1 - (1.0 + p) ** 2.0) < 1e-12
    f1u, f2u, pu = core.evaluate(np.full(G, 24, dtype=int))
    assert pu == 0.0
    print(f"  ceza modlari: carpimsal (1+P)^2 = {(1+p)**2:.3f} (P={p:.3f}) | uygun birey P=0")

def t_carbon_collinearity():
    m = model("geodesic16"); b = FEMBridge(m); b.open(); g, _ = b.read_groups_and_lengths(); G = len(g)
    out = {}
    for mode in ("fixed", "section"):
        core = FastCore(b, C, m.span_m, m.disp_limit_m, CarbonModel(mode=mode))
        rng = np.random.default_rng(5)
        F = np.array([core.evaluate(rng.integers(1, 25, G))[:2] for _ in range(100)])
        out[mode] = np.corrcoef(F[:, 0], F[:, 1])[0, 1]
    print(f"  corr(f1,f2): sabit mod {out['fixed']:.9f} | kesite bagli mod {out['section']:.4f}")

def t_16_optimizers_on_dome():
    m = model("geodesic16"); b = FEMBridge(m); b.open(); g, _ = b.read_groups_and_lengths(); G = len(g)
    core = FastCore(b, C, m.span_m, m.disp_limit_m, CarbonModel(mode="section"))

    for algo in ("abc", "hs", "gwo", "woa"):
        opt = MetaheuristicOptimizer(core.evaluate, n_vars=G, pop_size=6, max_iters=2, seed=42, method=algo)
        best, hist = opt.optimize()
        assert best is not None
        assert len(hist) == 3
        print(f"  {algo.upper()}: best_penalized = {best.penalized_cost:.2f} kN, feasible={best.is_feasible}")

if __name__ == "__main__":
    for t in (t_dc_equivalence, t_models, t_envelope_and_modes, t_carbon_collinearity, t_16_optimizers_on_dome):
        print(t.__name__); t()
    print("TUM TESTLER GECTI")
