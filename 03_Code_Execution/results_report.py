"""
results_report.py
Kampanya sonuclarindan makale tablo ve sekilleri (04_Results/figures, 04_Results/tables).
  1.1 en iyi cozumler ve kesit profilleri      1.2 yakinsama (en iyi / ortalama)
  1.3 kararlilik (box-plot; istatistik testleri statistical_analysis.py)
  1.4 sinirlayici dominasyonu (max D/C, hangi kontrol belirleyici)
  2.1-2.3 malzeme etkisi: celik referans (steel_reference.py) ile agirlik / CO2 ve bambu bilesen dagilimi
  Maliyet burada hesaplanmaz: belgelenmis fiyatlarla malzeme maliyeti price_scenarios.py (T9, T9a).

Kullanim: python results_report.py [--campaign C:\\BambuDome_campaign\\full] [--steel C:\\BambuDome_campaign\\steel_ref]
EC degerleri bamboo_catalog.py'den (beyan edilmis EPD degerleri; EC_bamboo turetilmis); duyarlilik tablolari ayrica uretilir.
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
ALGO_MARK = {"abc": "o", "aco": "s", "do": "^"}
G = 9.81

# --- Sekil bicimi: A4, 2.5 cm kenar boslugu -> metin genisligi 16 cm; yazilar bu boyutta 11 pt --------
CM = 1 / 2.54
FIG_W = 16.0 * CM
FONT_PT = 11
NAME = {"geodesic16": "Geodesic", "kiewitt32": "Kiewitt", "ribbed40": "Ribbed", "ribbed354": "Reference"}
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": FONT_PT, "axes.titlesize": FONT_PT, "axes.labelsize": FONT_PT,
    "xtick.labelsize": FONT_PT, "ytick.labelsize": FONT_PT, "legend.fontsize": FONT_PT - 1,
    "hatch.linewidth": 0.6, "savefig.dpi": 600,
})


def _visible_texts(fig):
    """Cizilen (gorunur, bos olmayan) tum yazilar: baslik, eksen etiketi, gorunur aralikta tick etiketi, lejant, notlar."""
    out = []
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            eps = 1e-9 * max(abs(lo), abs(hi), 1.0)
            for locs, labs in ((axis.get_majorticklocs(), axis.get_majorticklabels()),
                               (axis.get_minorticklocs(), axis.get_minorticklabels())):
                out += [t for loc, t in zip(locs, labs) if lo - eps <= loc <= hi + eps]
            out.append(axis.label)
        out += [ax.title, ax._left_title, ax._right_title] + list(ax.texts)
        if ax.get_legend():
            out += list(ax.get_legend().get_texts())
    for lg in fig.legends:
        out += list(lg.get_texts())
    out += list(fig.texts)
    return [t for t in out if t.get_visible() and t.get_text().strip()]


def check_text_layout(fig, name):
    """Yazilarin birbirine binip binmedigini ve sekil disina tasip tasmadigini denetler; sorunlari dondurur."""
    r = fig.canvas.get_renderer()
    fig.canvas.draw()
    items, seen = [], set()
    for t in _visible_texts(fig):
        b = t.get_window_extent(r)
        key = (t.get_text(), round(b.x0), round(b.y0), round(b.x1), round(b.y1))
        if key not in seen:                          # twinx eksenlerinin ortak x etiketleri ayni yere iki kez sayilmasin
            seen.add(key); items.append((t, b))
    fb = fig.bbox
    issues = []
    for t, b in items:
        if b.x0 < fb.x0 - 1 or b.y0 < fb.y0 - 1 or b.x1 > fb.x1 + 1 or b.y1 > fb.y1 + 1:
            issues.append(f"sekil disina tasiyor: '{t.get_text()}'")
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            (ti, bi), (tj, bj) = items[i], items[j]
            if bi.overlaps(bj):
                issues.append(f"cakisiyor: '{ti.get_text()}' <-> '{tj.get_text()}'")
    print(f"  {name}: {len(items)} yazi, {'cakisma yok' if not issues else str(len(issues)) + ' SORUN'}")
    for s in issues:
        print("    -", s)
    return issues


def save_fig(fig, name):
    check_text_layout(fig, name)
    fig.savefig(FIG / name, dpi=600)
    plt.close(fig)

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
    """Kutle ve karbon bilesenleri (bambu culm / baglanti celigi / harc). Maliyet: price_scenarios.py."""
    c = core.carbon
    sec = np.asarray(gene)[core.gidx] - 1
    A = core.A_sec[sec]; L = core.L
    mass_b = float((700.0 * A * L).sum())
    m_steel = core.n_nodes * c.m_hub + 2.0 * float(core.steel_end[sec].sum())
    m_mortar = 2.0 * float(core.mortar_end[sec].sum())
    return dict(mass_bamboo=mass_b, mass_steel=m_steel, mass_mortar=m_mortar,
                co2_bamboo=c.ec_bamboo * mass_b, co2_steel=c.ec_steel * m_steel, co2_mortar=c.ec_mortar * m_mortar)


def steel_breakdown(core, gene):
    sec = np.asarray(gene)[core.gidx] - 1
    A = core.A_sec[sec]
    mass = float((7850.0 * A * core.L).sum())
    conn = core.conn_kg
    return dict(mass_tube=mass, mass_conn=conn, co2_tube=core.ec_tube * mass, co2_conn=core.ec_conn * conn)


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
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    fig, ax = plt.subplots(1, 3, figsize=(FIG_W, 8.0 * CM))
    for a_, m in zip(ax, MODELS):
        dm = df[df.model == m]
        algos = sorted(dm.algo.unique())
        data = [dm[dm.algo == a].w.to_numpy() for a in algos]
        bp = a_.boxplot(data, tick_labels=[x.upper() for x in algos], patch_artist=True, showmeans=True)
        for patch, a in zip(bp["boxes"], algos):
            patch.set_facecolor(ALGO_COL.get(a, "gray")); patch.set_alpha(0.5)
        for i, d in enumerate(data, 1):
            a_.scatter(np.random.default_rng(0).normal(i, 0.05, len(d)), d, s=6, c="k", alpha=0.5, zorder=3)
        a_.set_title(NAME[m]); a_.grid(alpha=0.3)
    ax[0].set_ylabel("Structural weight [kN]")
    # sembol aciklamalari: matplotlib boxplot varsayilanlari (medyan turuncu cizgi, ortalama yesil ucgen, ayrik deger bos daire)
    handles = [Line2D([], [], ls="none", marker="o", ms=3, color="k", alpha=0.5, label="Individual runs (30 seeds)"),
               Line2D([], [], color="C1", lw=1.5, label="Median"),
               Line2D([], [], ls="none", marker="^", color="green", label="Mean"),
               Line2D([], [], ls="none", marker="o", mfc="none", mec="k", label="Outliers (>1.5 IQR)"),
               Patch(facecolor="0.7", edgecolor="k", label="Interquartile range (box)")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.15, 1, 1))
    save_fig(fig, "F3_boxplots.png")
    return dict(df=df, table=t)


def part_best_profiles(res):
    from bamboo_catalog import BAMBOO_CATALOG as C
    best_rows = []
    fig, ax = plt.subplots(3, 1, figsize=(FIG_W, 19.0 * CM))
    for a_, m in zip(ax, MODELS):
        rr = [r for r in res if r["model"] == m and r["is_feasible"]]
        b = min(rr, key=lambda r: r["best_structural_weight_kN"])
        gene = np.array(b["solution"])
        D = C["D_m"].to_numpy(float)[gene - 1] * 1000; t = C["t_m"].to_numpy(float)[gene - 1] * 1000
        best_rows.append({"Dome": m, "Best [kN]": b["best_structural_weight_kN"], "Algorithm": b["algo"].upper(),
                          "Seed": b["seed"], "Groups": len(gene), "Carbon [kgCO2e]": b["best_embodied_carbon_kgCO2e"]})
        pd.DataFrame(dict(group=np.arange(1, len(gene) + 1), section=gene, D_mm=D, t_mm=t, tD=t / D)).to_csv(
            TAB / f"T2_best_profile_{m}.csv", index=False)
        hb = a_.bar(np.arange(1, len(gene) + 1), D, color="#a9c4e0", edgecolor="#4f6f8f", lw=0.4, label="Outer diameter D")
        a_.set_ylabel("D [mm]"); a_.set_xlabel("Design group")
        a_.set_title(f"{NAME[m]} ({len(gene)} design groups): {b['algo'].upper()}, W = {b['best_structural_weight_kN']:.2f} kN")
        a2 = a_.twinx()
        hl, = a2.plot(np.arange(1, len(gene) + 1), t, "o-", color="#08306b", ms=3, lw=1.2, label="Wall thickness t")
        a2.set_ylabel("t [mm]")
        a_.grid(alpha=0.3)
        if m == MODELS[0]:
            a_.legend(handles=[hb, hl], loc="lower center", bbox_to_anchor=(0.5, 1.18), ncol=2, frameon=False)
    fig.tight_layout()
    save_fig(fig, "F1_best_profiles.png")
    save_table(pd.DataFrame(best_rows), "T2_best_solutions", "Table 2. Best solution per dome")
    return best_rows


def part_convergence(res):
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter, NullLocator
    fig, ax = plt.subplots(3, 1, figsize=(FIG_W, 21.0 * CM))
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
            mk = dict(marker=ALGO_MARK.get(algo), ms=3.5, markevery=(10, 30))
            a_.plot(grid, cur.mean(axis=0), color=ALGO_COL.get(algo), lw=1.6, label=f"{algo.upper()} mean of 30 runs", **mk)
            a_.plot(grid, cur.min(axis=0), color=ALGO_COL.get(algo), lw=1.0, ls="--", label=f"{algo.upper()} best of 30 runs",
                    mfc="none", **mk)
        a_.set_yscale("log"); a_.set_title(NAME[m]); a_.grid(alpha=0.3, which="both")
        lo = min(min(c) for c in [[h["best_penalized"] for h in r["history"]][-1:] for r in res if r["model"] == m])
        a_.set_ylim(lo * 0.9, lo * 4)
        # log eksende okunur sade sayilar (6, 8, 10, 20 ... yerine 6x10^0 gosterimi yok)
        ticks = [v * 10 ** e for e in range(-1, 4) for v in (1, 2, 4, 6, 8) if lo * 0.9 <= v * 10 ** e <= lo * 4]
        a_.yaxis.set_major_locator(FixedLocator(ticks)); a_.yaxis.set_minor_locator(NullLocator())
        a_.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}")); a_.yaxis.set_minor_formatter(NullFormatter())
        a_.set_ylabel("Best penalized weight [kN]")
    ax[-1].set_xlabel("Number of function evaluations (NFE)")
    h, l = ax[0].get_legend_handles_labels()
    order = [0, 2, 4, 1, 3, 5]                       # ust satir: ortalamalar, alt satir: en iyiler
    fig.legend([h[i] for i in order], [l[i] for i in order], loc="upper center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save_fig(fig, "F2_convergence.png")


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
    fig, ax = plt.subplots(1, 2, figsize=(FIG_W, 8.0 * CM), sharey=True)
    # renk + desen: siyah-beyaz baskida da ayirt edilebilir
    cols = {"tension": ("#1f77b4", "////"), "compression": ("#d62728", "\\\\\\\\"),
            "slenderness": ("#2ca02c", "..."), "joint": ("#ff7f0e", "xxx")}
    for j, (title, pick) in enumerate((("Best design", 1), ("Mean of all runs", 2))):
        bottom = np.zeros(len(shares))
        for k, (col, hatch) in cols.items():
            v = np.array([s[pick][k] for s in shares]) * 100
            ax[j].bar([NAME[s[0]] for s in shares], v, bottom=bottom, width=0.6, color=col, alpha=0.75,
                      hatch=hatch, edgecolor="k", lw=0.5, label=k.capitalize())
            bottom += v
        ax[j].set_title(title)
    ax[0].set_ylabel("Groups governed by check [%]")
    h, l = ax[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, frameon=False, handlelength=2.2, handleheight=1.2)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    save_fig(fig, "F4_governing_limit_states.png")


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
                         co2=bd["co2_tube"] + bd["co2_conn"], co2_parts=(bd["co2_tube"], bd["co2_conn"], 0.0),
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
                         co2_parts=(bd["co2_bamboo"], bd["co2_steel"], bd["co2_mortar"]),
                         n=len(rr), maxlen=float(core.L.max()), nmem=len(core.L)))
    S = pd.DataFrame(rows)
    ref = S[S.structure == "Steel ribbed354"].iloc[0] if (S.structure == "Steel ribbed354").any() else None
    tab = S[["structure", "nmem", "maxlen", "w_member", "w_total", "co2"]].copy()
    tab.columns = ["Structure", "Members", "Max member length [m]", "Member weight [kN]", "Total system weight [kN]",
                   "Embodied carbon [kgCO2e]"]
    if ref is not None:
        for col, rc in (("Member weight [kN]", "w_member"), ("Embodied carbon [kgCO2e]", "co2")):
            tab[f"{col.split(' [')[0]} / steel354"] = S[rc] / ref[rc]
    save_table(tab, "T5_material_comparison",
               "Table 5. Steel vs bamboo (same span and load patterns; best design of 30 runs; material cost: Table 9)")
    # ayni geometri: bambu / celik orani
    pair = []
    for m in MODELS:
        s = S[(S.dome == m) & (S.material == "steel")]; b = S[(S.dome == m) & (S.material == "bamboo")]
        if len(s) and len(b):
            s, b = s.iloc[0], b.iloc[0]
            pair.append({"Dome": m, "Steel member weight [kN]": s.w_member, "Bamboo member weight [kN]": b.w_member,
                         "Bamboo/Steel weight": b.w_member / s.w_member,
                         "Steel CO2e [t]": s.co2 / 1000, "Bamboo CO2e [t]": b.co2 / 1000, "Bamboo/Steel CO2e": b.co2 / s.co2})
    save_table(pd.DataFrame(pair), "T6_same_geometry_ratio", "Table 6. Same-geometry comparison (material effect only)")
    # bilesen dagilimi (bambu)
    br = []
    for _, r in S[S.material == "bamboo"].iterrows():
        for key, labels in (("co2_parts", ("culm", "steel connectors", "mortar")),):
            tot = sum(r[key])
            br.append({"Dome": r.dome, "Quantity": "CO2e",
                       **{f"{lab} [%]": 100 * v / tot for lab, v in zip(labels, r[key])}, "Total": tot})
    save_table(pd.DataFrame(br), "T7_bamboo_component_breakdown", "Table 7. Bamboo structure: component shares of CO2e (cost shares: Table 9)")
    # sekiller
    for qty, key, ylab, scale in (("weight", None, "Member weight [kN]", 1.0), ("co2", "co2_parts", "Embodied carbon [t CO$_2$e]", 1e-3)):
        fig, ax = plt.subplots(figsize=(FIG_W, 8.5 * CM))
        names = [f"{NAME[d]}\n{mt}" for d, mt in zip(S.dome, S.material)]; x = np.arange(len(names))
        bw = 0.5
        if key is None:
            from matplotlib.patches import Patch
            ax.bar(x, S.w_member, width=bw, edgecolor="k", lw=0.5,
                   color=["#7f7f7f" if mt == "steel" else "#c8a96e" for mt in S.material],
                   hatch=["////" if mt == "steel" else "" for mt in S.material])
            top = S.w_member.to_numpy()
            ax.legend(handles=[Patch(facecolor="#7f7f7f", hatch="////", edgecolor="k", label="Steel tubes"),
                               Patch(facecolor="#c8a96e", edgecolor="k", label="Bamboo culms")],
                      loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
        else:
            bottom = np.zeros(len(S))
            labs = [("Tube (steel) / culm (bamboo)", "#c8a96e", ""), ("Steel connectors", "#555555", "////"),
                    ("Mortar", "#e8d5b0", "...")]
            for j, (lab, col, hatch) in enumerate(labs):
                v = np.array([p[j] for p in S[key]]) * scale
                ax.bar(x, v, width=bw, bottom=bottom, color=col, hatch=hatch, edgecolor="k", lw=0.5, label=lab)
                bottom += v
            top = bottom
            ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False, handlelength=2.0)
        for i, v in enumerate(top):
            ax.text(i, v + 0.015 * top.max(), f"{v:.1f}", ha="center", va="bottom", fontsize=FONT_PT - 1)
        ax.set_ylim(0, 1.12 * top.max())
        ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel(ylab); ax.grid(alpha=0.3, axis="y")
        ax.set_xlim(-0.6, len(names) - 0.4)
        fig.tight_layout()
        save_fig(fig, f"F5_material_{qty}.png")
    # duyarlilik: EC (fiyat duyarliligi price_scenarios.py, T9)
    sens = []
    for m in MODELS:
        s = S[(S.dome == m) & (S.material == "steel")]; b = S[(S.dome == m) & (S.material == "bamboo")]
        if not len(s) or not len(b):
            continue
        s, b = s.iloc[0], b.iloc[0]
        for ec in (0.851, 1.701, 2.552, 3.402):
            cs = ec / 1.701 * s.co2
            sens.append({"Dome": m, "Parameter": f"steel EC {ec} kgCO2e/kg", "Bamboo/Steel CO2e": b.co2 / cs})
        for ecb in (0.0324, 0.243, 0.50, 1.23):
            cb = b.co2_parts[0] * ecb / 0.243 + b.co2_parts[1] + b.co2_parts[2]
            sens.append({"Dome": m, "Parameter": f"bamboo EC {ecb} kgCO2e/kg", "Bamboo/Steel CO2e": cb / s.co2})
    save_table(pd.DataFrame(sens).fillna(""), "T8_material_sensitivity", "Table 8. Sensitivity of bamboo/steel CO2e ratio to EC assumptions")
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
