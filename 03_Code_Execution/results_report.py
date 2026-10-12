"""
results_report.py
Kampanya sonuclarindan makale tablo ve sekilleri (04_Results/figures, 04_Results/tables).
  1.1 en iyi cozumler ve kesit profilleri      1.2 yakinsama (en iyi / ortalama)
  1.3 kararlilik (box-plot; istatistik testleri statistical_analysis.py)
  1.4 sinirlayici dominasyonu (max D/C, hangi kontrol belirleyici)
  2.1-2.3 malzeme etkisi: celik referans (steel_reference.py) ile agirlik / maliyet / CO2 ve bambu bilesen dagilimi

Kullanim: python results_report.py [--campaign C:\\BambuDome_campaign\\full] [--steel C:\\BambuDome_campaign\\steel_ref]
Maliyet ve EC degerleri VARSAYIMDIR (PRICES / carbon modeli); duyarlilik tablolari ayrica uretilir.
"""
from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
OUT = BASE.parent / "04_Results"
FIG, TAB = OUT / "figures", OUT / "tables"
MODELS = ["geodesic16", "kiewitt32", "ribbed40"]
ALGO_COL = {"abc": "#1f77b4", "aco": "#d62728", "do": "#2ca02c"}
G = 9.81

# --- Maliyet varsayimlari (DOGRULANACAK) -----------------------------------------------------------
CULM_PRICE_D_MM = np.array([80.0, 100.0, 120.0, 140.0, 160.0])      # Tablo 1 (kullanici): USD/m
CULM_PRICE_USD_M = np.array([0.65, 1.10, 1.85, 3.15, 5.20])
PRICES = dict(steel_tube=1.50,       # USD/kg yapisal celik boru (VARSAYIM; 1.0-3.0 taranir)
              steel_conn=4.00,       # USD/kg baglanti celigi (hub, saplama)
              mortar=0.12)           # USD/kg harc


def culm_price(D_m):
    d = np.asarray(D_m) * 1000.0
    return np.exp(np.interp(np.log(d), np.log(CULM_PRICE_D_MM), np.log(CULM_PRICE_USD_M),
                            left=None, right=None))


def md_table(df: pd.DataFrame, floatfmt="{:.3f}") -> str:
    h = list(df.columns)
    lines = ["| " + " | ".join(map(str, h)) + " |", "|" + "---|" * len(h)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(floatfmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r) + " |")
    return "\n".join(lines)


def save_table(df: pd.DataFrame, name: str, title: str, floatfmt="{:.3f}") -> None:
    TAB.mkdir(parents=True, exist_ok=True)
    df.to_csv(TAB / f"{name}.csv", index=False)
    (TAB / f"{name}.md").write_text(f"### {title}\n\n" + md_table(df, floatfmt) + "\n", encoding="utf-8")


def load_results(d: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted((d / "results").glob("*.json"))]


def get_model(name):
    from run_full_campaign import build_model
    return build_model(name)


# ----------------------------------------------------------------------------------------------------
def bamboo_context(name):
    from fem_bridge import FEMBridge
    from fast_eval import FastCore, CarbonModel
    from bamboo_catalog import BAMBOO_CATALOG
    m = get_model(name)
    b = FEMBridge(m); b.open(); b.read_groups_and_lengths()
    core = FastCore(b, BAMBOO_CATALOG, m.span_m, m.disp_limit_m, CarbonModel(), "all", True)
    return m, b, core, BAMBOO_CATALOG


def bamboo_breakdown(core, cat, gene):
    """Kutle, karbon ve maliyet bilesenleri (bambu culm / baglanti celigi / harc)."""
    c = core.carbon
    sec = np.asarray(gene)[core.gidx] - 1
    A = core.A_sec[sec]; L = core.L; D = cat["D_m"].to_numpy(float)[sec]
    mass_b = float((700.0 * A * L).sum())
    m_steel = core.n_nodes * c.m_hub + 2.0 * float(core.steel_end[sec].sum())
    m_mortar = 2.0 * float(core.mortar_end[sec].sum())
    return dict(mass_bamboo=mass_b, mass_steel=m_steel, mass_mortar=m_mortar,
                co2_bamboo=c.ec_bamboo * mass_b, co2_steel=c.ec_steel * m_steel, co2_mortar=c.ec_mortar * m_mortar,
                cost_bamboo=float((culm_price(D) * L).sum()), cost_steel=PRICES["steel_conn"] * m_steel,
                cost_mortar=PRICES["mortar"] * m_mortar)


def steel_breakdown(core, gene):
    sec = np.asarray(gene)[core.gidx] - 1
    A = core.A_sec[sec]
    mass = float((7850.0 * A * core.L).sum())
    conn = core.conn_kg
    return dict(mass_tube=mass, mass_conn=conn, co2_tube=core.ec_tube * mass, co2_conn=core.ec_conn * conn,
                cost_tube=PRICES["steel_tube"] * mass, cost_conn=PRICES["steel_conn"] * conn)


def limit_breakdown(core, gene):
    """Bambu: her kontrolun en buyuk D/C degeri ve grup basina belirleyici kontrol."""
    from fast_eval import ylinen_fcr, F_T_K, F_J_RD, LAMBDA_MAX
    gene = np.asarray(gene)
    core.evaluate(gene)
    sec = gene[core.gidx] - 1
    A, r = core.A_sec[sec], core.r_sec[sec]
    N, umax = core.bridge.analyze_arrays()
    Ns = N / core.kcase[None, :]
    lam = core.L / r
    chk = {"tension": np.maximum(Ns.max(axis=1), 0.0) / A / F_T_K,
           "compression": np.maximum(-Ns.min(axis=1), 0.0) / A / ylinen_fcr(lam),
           "slenderness": lam / LAMBDA_MAX,
           "joint": np.abs(N).max(axis=1) / F_J_RD}
    names = list(chk)
    M = np.vstack([chk[k] for k in names])                       # (4, nmem)
    dc = M.max(axis=0)
    gov = {k: 0 for k in names}; active = 0
    for g in range(core.G):
        idx = np.flatnonzero(core.gidx == g)
        i = idx[np.argmax(dc[idx])]
        gov[names[int(np.argmax(M[:, i]))]] += 1
        active += int(dc[i] >= 0.95)
    return dict(max_dc={k: float(v.max()) for k, v in chk.items()}, disp_ratio=float(umax / core.limit),
                gov_groups=gov, active_groups=active, n_groups=core.G)


# ----------------------------------------------------------------------------------------------------
def part_performance(res: list[dict]) -> dict:
    df = pd.DataFrame([dict(model=r["model"], algo=r["algo"], seed=r["seed"], w=r["best_structural_weight_kN"],
                            co2=r["best_embodied_carbon_kgCO2e"], feas=r["is_feasible"], nfe=r["nfe"],
                            t=r["elapsed_s"]) for r in res])
    rows = []
    for (m, a), g in df.groupby(["model", "algo"]):
        w = g.w.to_numpy()
        rows.append({"Dome": m, "Algorithm": a.upper(), "Runs": len(g), "Feasible": int(g.feas.sum()),
                     "Best [kN]": w.min(), "Median [kN]": np.median(w), "Mean [kN]": w.mean(),
                     "Std [kN]": w.std(ddof=1), "Worst [kN]": w.max(), "CV [%]": 100 * w.std(ddof=1) / w.mean(),
                     "NFE": int(g.nfe.iloc[0]), "Time [min]": g.t.mean() / 60})
    t = pd.DataFrame(rows)
    save_table(t, "T1_optimization_results", "Table 1. Best-weight statistics over 30 independent runs (seeds 1001-1030)")
    # boxplot
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.6))
    for a_, m in zip(ax, MODELS):
        dm = df[df.model == m]
        algos = sorted(dm.algo.unique())
        data = [dm[dm.algo == a].w.to_numpy() for a in algos]
        bp = a_.boxplot(data, tick_labels=[x.upper() for x in algos], patch_artist=True, showmeans=True)
        for patch, a in zip(bp["boxes"], algos):
            patch.set_facecolor(ALGO_COL.get(a, "gray")); patch.set_alpha(0.5)
        for i, d in enumerate(data, 1):
            a_.scatter(np.random.default_rng(0).normal(i, 0.05, len(d)), d, s=6, c="k", alpha=0.5, zorder=3)
        a_.set_title(m); a_.set_ylabel("Structural weight [kN]"); a_.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "F3_boxplots.png", dpi=200); plt.close(fig)
    return dict(df=df, table=t)


def part_best_profiles(res):
    from bamboo_catalog import BAMBOO_CATALOG as C
    best_rows = []
    fig, ax = plt.subplots(3, 1, figsize=(10, 9))
    for a_, m in zip(ax, MODELS):
        rr = [r for r in res if r["model"] == m and r["is_feasible"]]
        b = min(rr, key=lambda r: r["best_structural_weight_kN"])
        gene = np.array(b["solution"])
        D = C["D_m"].to_numpy(float)[gene - 1] * 1000; t = C["t_m"].to_numpy(float)[gene - 1] * 1000
        best_rows.append({"Dome": m, "Best [kN]": b["best_structural_weight_kN"], "Algorithm": b["algo"].upper(),
                          "Seed": b["seed"], "Groups": len(gene), "Carbon [kgCO2e]": b["best_embodied_carbon_kgCO2e"]})
        pd.DataFrame(dict(group=np.arange(1, len(gene) + 1), section=gene, D_mm=D, t_mm=t, tD=t / D)).to_csv(
            TAB / f"T2_best_profile_{m}.csv", index=False)
        a_.bar(np.arange(1, len(gene) + 1), D, color="#8c6d31", alpha=0.8)
        a_.set_ylabel("D [mm]"); a_.set_xlabel("Design group"); a_.set_title(f"{m}: best design ({b['algo'].upper()}, seed {b['seed']}, {b['best_structural_weight_kN']:.2f} kN)")
        a2 = a_.twinx(); a2.plot(np.arange(1, len(gene) + 1), t, "ro-", ms=3); a2.set_ylabel("t [mm]", color="r")
        a_.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIG / "F1_best_profiles.png", dpi=200); plt.close(fig)
    save_table(pd.DataFrame(best_rows), "T2_best_solutions", "Table 2. Best solution per dome")
    return best_rows


def part_convergence(res):
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
    for a_, m in zip(ax, MODELS):
        for algo in sorted({r["algo"] for r in res}):
            rr = [r for r in res if r["model"] == m and r["algo"] == algo]
            budget = rr[0]["nfe"]
            grid = np.linspace(rr[0]["pop"], budget, 300)
            curves = []
            for r in rr:
                ev = np.array([h["evals"] for h in r["history"]]); bp = np.array([h["best_penalized"] for h in r["history"]])
                idx = np.searchsorted(ev, grid, side="right") - 1
                curves.append(bp[np.clip(idx, 0, None)])
            cur = np.array(curves)
            a_.plot(grid, cur.mean(axis=0), color=ALGO_COL.get(algo), lw=1.6, label=f"{algo.upper()} mean")
            a_.plot(grid, cur.min(axis=0), color=ALGO_COL.get(algo), lw=1.0, ls="--", label=f"{algo.upper()} best")
        a_.set_yscale("log"); a_.set_xlabel("NFE"); a_.set_title(m); a_.grid(alpha=0.3, which="both")
        lo = min(min(c) for c in [[h["best_penalized"] for h in r["history"]][-1:] for r in res if r["model"] == m])
        a_.set_ylim(lo * 0.9, lo * 4)
    ax[0].set_ylabel("Best penalized weight [kN]"); ax[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "F2_convergence.png", dpi=200); plt.close(fig)


def part_limits(res):
    rows, shares = [], []
    for m in MODELS:
        _, b, core, cat = bamboo_context(m)
        rr = [r for r in res if r["model"] == m and r["is_feasible"]]
        best = min(rr, key=lambda r: r["best_structural_weight_kN"])
        lb = limit_breakdown(core, best["solution"])
        rows.append({"Dome": m, "Design": "best", **{f"max D/C {k}": v for k, v in lb["max_dc"].items()},
                     "u/u_lim": lb["disp_ratio"], "Active groups (DC>=0.95)": f"{lb['active_groups']}/{lb['n_groups']}"})
        agg = {k: 0.0 for k in lb["gov_groups"]}; act = []
        mx = {k: [] for k in lb["max_dc"]}; us = []
        for r in rr:
            x = limit_breakdown(core, r["solution"])
            for k in agg:
                agg[k] += x["gov_groups"][k] / x["n_groups"] / len(rr)
            act.append(x["active_groups"] / x["n_groups"]); us.append(x["disp_ratio"])
            for k in mx:
                mx[k].append(x["max_dc"][k])
        rows.append({"Dome": m, "Design": f"mean of {len(rr)} runs", **{f"max D/C {k}": float(np.mean(v)) for k, v in mx.items()},
                     "u/u_lim": float(np.mean(us)), "Active groups (DC>=0.95)": f"{100 * np.mean(act):.0f}%"})
        shares.append((m, {k: lb["gov_groups"][k] / lb["n_groups"] for k in lb["gov_groups"]}, agg))
    save_table(pd.DataFrame(rows), "T4_limit_states", "Table 4. Maximum demand/capacity ratio per limit state (bamboo designs)")
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    cols = {"tension": "#1f77b4", "compression": "#d62728", "slenderness": "#2ca02c", "joint": "#ff7f0e"}
    for j, (title, pick) in enumerate((("Best design", 1), ("Mean of all runs", 2))):
        bottom = np.zeros(len(shares))
        for k in cols:
            v = np.array([s[pick][k] for s in shares]) * 100
            ax[j].bar([s[0] for s in shares], v, bottom=bottom, color=cols[k], label=k)
            bottom += v
        ax[j].set_ylabel("Groups governed by check [%]"); ax[j].set_title(title)
    ax[0].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "F4_governing_limit_states.png", dpi=200); plt.close(fig)


# ----------------------------------------------------------------------------------------------------
def part_material(res, steel_res, best_rows):
    from steel_reference import make_core as steel_core
    rows = []
    entries = []          # (label, group, breakdown dict)
    # celik referanslar: en iyi ve medyan
    for m in ["ribbed354", "ribbed40", "kiewitt32", "geodesic16"]:
        rr = [r for r in steel_res if r["model"] == m and r["is_feasible"]]
        if not rr:
            continue
        _, _, sc, G_ = steel_core(m)
        best = min(rr, key=lambda r: r["best_structural_weight_kN"])
        bd = steel_breakdown(sc, best["solution"])
        w_all = np.array([r["best_structural_weight_kN"] for r in rr])
        rows.append(dict(structure=f"Steel {m}", material="steel", dome=m, w_member=best["best_structural_weight_kN"],
                         w_total=(bd["mass_tube"] + bd["mass_conn"]) * G / 1000, w_member_med=float(np.median(w_all)),
                         co2=bd["co2_tube"] + bd["co2_conn"], cost=bd["cost_tube"] + bd["cost_conn"],
                         co2_parts=(bd["co2_tube"], bd["co2_conn"], 0.0), cost_parts=(bd["cost_tube"], bd["cost_conn"], 0.0),
                         n=len(rr), maxlen=float(sc.L.max()), nmem=len(sc.L)))
    for m in MODELS:
        rr = [r for r in res if r["model"] == m and r["is_feasible"]]
        _, _, core, cat = bamboo_context(m)
        best = min(rr, key=lambda r: r["best_structural_weight_kN"])
        bd = bamboo_breakdown(core, cat, best["solution"])
        w_all = np.array([r["best_structural_weight_kN"] for r in rr])
        rows.append(dict(structure=f"Bamboo {m}", material="bamboo", dome=m, w_member=best["best_structural_weight_kN"],
                         w_total=(bd["mass_bamboo"] + bd["mass_steel"] + bd["mass_mortar"]) * G / 1000,
                         w_member_med=float(np.median(w_all)),
                         co2=bd["co2_bamboo"] + bd["co2_steel"] + bd["co2_mortar"],
                         cost=bd["cost_bamboo"] + bd["cost_steel"] + bd["cost_mortar"],
                         co2_parts=(bd["co2_bamboo"], bd["co2_steel"], bd["co2_mortar"]),
                         cost_parts=(bd["cost_bamboo"], bd["cost_steel"], bd["cost_mortar"]),
                         n=len(rr), maxlen=float(core.L.max()), nmem=len(core.L)))
    S = pd.DataFrame(rows)
    ref = S[S.structure == "Steel ribbed354"].iloc[0] if (S.structure == "Steel ribbed354").any() else None
    tab = S[["structure", "nmem", "maxlen", "w_member", "w_total", "co2", "cost"]].copy()
    tab.columns = ["Structure", "Members", "Max member length [m]", "Member weight [kN]", "Total system weight [kN]",
                   "Embodied carbon [kgCO2e]", "Cost [USD]"]
    if ref is not None:
        for col, rc in (("Member weight [kN]", "w_member"), ("Embodied carbon [kgCO2e]", "co2"), ("Cost [USD]", "cost")):
            tab[f"{col.split(' [')[0]} / steel354"] = S[rc] / ref[rc]
    save_table(tab, "T5_material_comparison",
               "Table 5. Steel vs bamboo (same span and load patterns; best design of 30 runs; cost and EC are assumptions)")
    # ayni geometri: bambu / celik orani
    pair = []
    for m in MODELS:
        s = S[(S.dome == m) & (S.material == "steel")]; b = S[(S.dome == m) & (S.material == "bamboo")]
        if len(s) and len(b):
            s, b = s.iloc[0], b.iloc[0]
            pair.append({"Dome": m, "Steel member weight [kN]": s.w_member, "Bamboo member weight [kN]": b.w_member,
                         "Bamboo/Steel weight": b.w_member / s.w_member,
                         "Steel CO2e [t]": s.co2 / 1000, "Bamboo CO2e [t]": b.co2 / 1000, "Bamboo/Steel CO2e": b.co2 / s.co2,
                         "Steel cost [kUSD]": s.cost / 1000, "Bamboo cost [kUSD]": b.cost / 1000, "Bamboo/Steel cost": b.cost / s.cost})
    save_table(pd.DataFrame(pair), "T6_same_geometry_ratio", "Table 6. Same-geometry comparison (material effect only)")
    # bilesen dagilimi (bambu)
    br = []
    for _, r in S[S.material == "bamboo"].iterrows():
        for key, labels in (("co2_parts", ("culm", "steel connectors", "mortar")), ("cost_parts", ("culm", "steel connectors", "mortar"))):
            tot = sum(r[key])
            br.append({"Dome": r.dome, "Quantity": "CO2e" if key == "co2_parts" else "Cost",
                       **{f"{lab} [%]": 100 * v / tot for lab, v in zip(labels, r[key])}, "Total": tot})
    save_table(pd.DataFrame(br), "T7_bamboo_component_breakdown", "Table 7. Bamboo structure: component shares of CO2e and cost")
    # sekiller
    for qty, key, ylab, scale in (("weight", None, "Member weight [kN]", 1.0), ("co2", "co2_parts", "Embodied carbon [t CO2e]", 1e-3),
                                  ("cost", "cost_parts", "Cost [kUSD]", 1e-3)):
        fig, ax = plt.subplots(figsize=(9, 4))
        names = list(S.structure); x = np.arange(len(names))
        if key is None:
            ax.bar(x, S.w_member, color=["#7f7f7f" if mt == "steel" else "#8c6d31" for mt in S.material])
            for i, v in enumerate(S.w_member):
                ax.text(i, v, f"{v:.1f}", ha="center", va="bottom", fontsize=8)
        else:
            bottom = np.zeros(len(S))
            labs = [("tube/culm", "#8c6d31"), ("steel connectors", "#555555"), ("mortar", "#d9b38c")]
            for j, (lab, col) in enumerate(labs):
                v = np.array([p[j] for p in S[key]]) * scale
                ax.bar(x, v, bottom=bottom, color=col, label=lab if j else "tube (steel) / culm (bamboo)"); bottom += v
            for i, v in enumerate(bottom):
                ax.text(i, v, f"{v:.1f}", ha="center", va="bottom", fontsize=8)
            ax.legend(fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels(names, rotation=25, ha="right"); ax.set_ylabel(ylab); ax.grid(alpha=0.3, axis="y")
        if qty == "weight":
            ax.set_title("Member weight (steel tubes / bamboo culms), optimum designs")
        fig.tight_layout(); fig.savefig(FIG / f"F5_material_{qty}.png", dpi=200); plt.close(fig)
    # duyarlilik: celik fiyati / EC
    sens = []
    for m in MODELS:
        s = S[(S.dome == m) & (S.material == "steel")]; b = S[(S.dome == m) & (S.material == "bamboo")]
        if not len(s) or not len(b):
            continue
        s, b = s.iloc[0], b.iloc[0]
        for p in (1.0, 1.5, 2.0, 3.0):
            cs = p * s.cost_parts[0] / PRICES["steel_tube"] + s.cost_parts[1]
            sens.append({"Dome": m, "Parameter": f"steel tube price {p} USD/kg", "Bamboo/Steel cost": b.cost / cs})
        for ec in (1.6, 1.9, 2.51, 2.8):
            cs = ec / 2.51 * s.co2
            sens.append({"Dome": m, "Parameter": f"steel EC {ec} kgCO2e/kg", "Bamboo/Steel CO2e": b.co2 / cs})
        for ecb in (0.09, 0.30, 0.47, 1.23):
            cb = b.co2_parts[0] * ecb / 0.30 + b.co2_parts[1] + b.co2_parts[2]
            sens.append({"Dome": m, "Parameter": f"bamboo EC {ecb} kgCO2e/kg", "Bamboo/Steel CO2e": cb / s.co2})
    save_table(pd.DataFrame(sens).fillna(""), "T8_material_sensitivity", "Table 8. Sensitivity of bamboo/steel ratios to price and EC assumptions")
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", default=r"C:\BambuDome_campaign\full")
    ap.add_argument("--steel", default=r"C:\BambuDome_campaign\steel_ref_aisc37")
    ap.add_argument("--only", nargs="*", default=None, help="performance profiles convergence limits material")
    a = ap.parse_args()
    import steel_reference as _sr                      # celik referans: literatur (354MemberDome.pdf) ile ayni kesit/yonetmelik
    _sr.configure(code="asd89", catalog="aisc37", fy_mpa=248.2, e_gpa=205.0)
    FIG.mkdir(parents=True, exist_ok=True); TAB.mkdir(parents=True, exist_ok=True)
    res = load_results(Path(a.campaign))
    steel = load_results(Path(a.steel)) if (Path(a.steel) / "results").exists() else []
    do = set(a.only) if a.only else {"performance", "profiles", "convergence", "limits", "material"}
    print(len(res), "bambu isi,", len(steel), "celik isi")
    best_rows = None
    if "performance" in do:
        part_performance(res); print("performans OK")
    if "profiles" in do:
        best_rows = part_best_profiles(res); print("profiller OK")
    if "convergence" in do:
        part_convergence(res); print("yakinsama OK")
    if "limits" in do:
        part_limits(res); print("sinirlar OK")
    if "material" in do and steel:
        part_material(res, steel, best_rows); print("malzeme OK")


if __name__ == "__main__":
    main()
