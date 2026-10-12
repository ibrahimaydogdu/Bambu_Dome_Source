"""
statistical_analysis.py
BambuDome Kampanya Sonuclari Istatiksel Hipotez Testi ve Siralama Motoru
==========================================================================
30 bagimsiz tohum (1001-1030) sonuclari uzerinde:
  1. Betimsel Istatistikler (Min, Medyan, Ortalama, Maks, Std. Sapma, Basari Orani)
  2. Friedman Siralama Testi (16 algoritma karsilastirmasi)
  3. Wilcoxon Rank-Sum / Mann-Whitney U Testi (p < 0.05, Holm duzeltmeli)
  4. Markdown ve LaTeX tablo uretimi

Kullanim:
  python statistical_analysis.py [--results-dir C:\\BambuDome_campaign\\full\\results] [--output-dir ../04_Results]
"""

from __future__ import annotations
import os
import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
from scipy import stats

BASE_DIR = Path(__file__).parent


def load_campaign_results(results_dir: Path) -> pd.DataFrame:
    """Belirtilen dizindeki tum JSON sonuc dosyalarini okur."""
    rows = []
    json_files = list(results_dir.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"Sonuc dosyasi bulunamadi: {results_dir}")

    for p in json_files:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if "model" in data and "algo" in data:
                rows.append({
                    "job": data.get("job", p.stem),
                    "model": data["model"],
                    "algo": data["algo"].lower(),
                    "algo_name": data.get("algo_name", data["algo"].upper()),
                    "seed": data.get("seed", 0),
                    "is_feasible": data.get("is_feasible", False),
                    "penalty": data.get("penalty", 0.0),
                    "penalized_weight_kN": data.get("best_penalized_weight_kN", 1e9),
                    "structural_weight_kN": data.get("best_structural_weight_kN", 1e9),
                    "embodied_carbon_kg": data.get("best_embodied_carbon_kgCO2e", 1e9),
                    "nfe": data.get("nfe", 0),
                    "elapsed_s": data.get("elapsed_s", 0.0),
                })
        except Exception as e:
            print(f"Uyari: {p.name} okunamadi: {e}", file=sys.stderr)

    return pd.DataFrame(rows)


def compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Her model ve algoritma icin betimsel istatistik tablosu olusturur."""
    summary = []
    models = sorted(df["model"].unique())
    algos = sorted(df["algo"].unique())

    for model in models:
        df_m = df[df["model"] == model]
        for algo in algos:
            sub = df_m[df_m["algo"] == algo]
            if sub.empty:
                continue
            n_runs = len(sub)
            n_feas = int(sub["is_feasible"].sum())
            weights = sub["penalized_weight_kN"].to_numpy()
            carbon = sub["embodied_carbon_kg"].to_numpy()

            summary.append({
                "Model": model,
                "Algorithm": algo.upper(),
                "Runs": n_runs,
                "Feasible": f"{n_feas}/{n_runs}",
                "Weight_Best": float(np.min(weights)),
                "Weight_Median": float(np.median(weights)),
                "Weight_Mean": float(np.mean(weights)),
                "Weight_Std": float(np.std(weights, ddof=1)) if n_runs > 1 else 0.0,
                "Carbon_Mean": float(np.mean(carbon)),
                "NFE_Mean": float(np.mean(sub["nfe"])),
                "Time_s": float(np.mean(sub["elapsed_s"])),
            })

    return pd.DataFrame(summary)


def compute_friedman_test(df: pd.DataFrame, model_name: str, metric: str = "penalized_weight_kN") -> tuple[float, float, pd.Series]:
    """Algoritmalar uzerinde Friedman siralama testi uygular."""
    df_m = df[df["model"] == model_name]
    piv = df_m.pivot(index="seed", columns="algo", values=metric)
    piv = piv.dropna()

    if len(piv) < 5 or piv.shape[1] < 2:
        return np.nan, np.nan, pd.Series()

    # Friedman testi
    data_matrix = [piv[col].to_numpy() for col in piv.columns]
    res = stats.friedmanchisquare(*data_matrix)

    # Ortalama siralama (Mean Rank)
    ranks = piv.rank(axis=1, ascending=True)
    mean_ranks = ranks.mean(axis=0).sort_values()

    return float(res.statistic), float(res.pvalue), mean_ranks


def compute_wilcoxon_tests(df: pd.DataFrame, model_name: str, control_algo: str,
                           metric: str = "penalized_weight_kN") -> pd.DataFrame:
    """Kontrol algoritmasina karsi Wilcoxon rank-sum (= Mann-Whitney U) testi, iki yonlu.
    Her algoritmanin 30 kosusu bagimsiz orneklem sayilir. Etki buyuklugu: A12 = P(rakip daha kotu)."""
    df_m = df[df["model"] == model_name]
    groups = {a: g[metric].to_numpy(float) for a, g in df_m.groupby("algo")}
    if control_algo not in groups:
        return pd.DataFrame()
    ctrl_vals = groups[control_algo]
    results = []
    for algo, comp_vals in groups.items():
        if algo == control_algo:
            continue
        if np.array_equal(np.sort(comp_vals), np.sort(ctrl_vals)):
            stat, p_val = float(len(comp_vals) * len(ctrl_vals) / 2), 1.0
        else:
            res = stats.mannwhitneyu(comp_vals, ctrl_vals, alternative="two-sided", method="auto")
            stat, p_val = float(res.statistic), float(res.pvalue)
        a12 = stat / (len(comp_vals) * len(ctrl_vals))       # U/(n1 n2) = P(rakip > kontrol) + 0.5 P(=)
        results.append({
            "Comparison": f"{control_algo.upper()} vs {algo.upper()}",
            "Diff_Median": float(np.median(comp_vals) - np.median(ctrl_vals)),
            "U_Stat": stat,
            "p_value": p_val,
            "A12_rakip_kotu": a12,
            "Sig_005": "~",
        })

    out = pd.DataFrame(results)
    if not out.empty:                                   # Holm-Bonferroni (ailelik hata orani)
        p = out["p_value"].to_numpy(float)
        order = np.argsort(p)
        adj = np.empty_like(p)
        run = 0.0
        for k, idx in enumerate(order):
            run = max(run, (len(p) - k) * p[idx])
            adj[idx] = min(run, 1.0)
        out["p_Holm"] = adj
        sig = out["p_Holm"] < 0.05
        out["Sig_005"] = np.where(sig, np.where(out["Diff_Median"] > 0, "+", "-"), "~")
    return out


def df_to_markdown(df: pd.DataFrame) -> str:
    """tabulate paketine bagimli olmadan DataFrame'i Markdown tablosuna cevirir."""
    if df.empty:
        return ""
    headers = [str(c) for c in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]
    for _, row in df.iterrows():
        row_str = []
        for val in row:
            if isinstance(val, float):
                row_str.append(f"{val:.2e}" if (val != 0 and abs(val) < 1e-3) else (f"{val:.4f}" if abs(val) < 1e3 else f"{val:.1f}"))
            else:
                row_str.append(str(val))
        lines.append("| " + " | ".join(row_str) + " |")
    return "\n".join(lines)


def export_markdown_report(summary_df: pd.DataFrame, friedman_dict: dict,
                           wilcoxon_dict: dict, out_file: Path):
    """Bulgular ve istatistik raporunu Markdown formatinda kaydeder."""
    lines = [
        "# 📊 BambuDome Meta-Sezgisel Kampanya Istatistiksel Degerlendirme Raporu",
        "",
        "Bu rapor; Secilen meta-sezgisel optimizasyon algoritmalarinin (ABC, ACO, DO) 3 kubbe topolojisi ve 30 bagimsiz tohum",
        "(1001–1030) uzerindeki stokastik performansini, Friedman sira testini ve Wilcoxon rank-sum (Mann-Whitney U, Holm duzeltmeli) ikili karsilastirmalarini icerir.",
        "",
        "---",
        "",
        "## 1. Betimsel Istatistikler (Descriptive Statistics)",
        "",
        df_to_markdown(summary_df),
        "",
        "---",
        "",
        "## 2. Friedman Siralama Testi (Friedman Rank Test)",
        "",
    ]

    for model, (f_stat, p_val, ranks) in friedman_dict.items():
        lines.append(f"### Model: `{model}`")
        lines.append(f"- **Friedman $\\chi^2_F$:** {f_stat:.3f}")
        lines.append(f"- **Asymptotic $p$-degeri:** {p_val:.4e} {'(p < 0.001, Guclu Anlamlilik)' if p_val < 0.001 else ''}")
        lines.append("")
        lines.append("**Algoritmalarin Ortalama Siralamalari (Mean Ranks - Dusuk sira daha basarilidir):**")
        lines.append("")
        if not ranks.empty:
            rank_df = ranks.reset_index()
            rank_df.columns = ["Algoritma", "Ortalama Sira"]
            rank_df["Algoritma"] = rank_df["Algoritma"].str.upper()
            lines.append(df_to_markdown(rank_df))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. Wilcoxon Rank-Sum (Mann-Whitney U) Karsilastirmalari")
    lines.append("")
    lines.append("Isaret Notasyonu (Holm-duzeltmeli $p < 0.05$): `+` Kontrol algoritmasi istatistiksel olarak ustun, `-` Rakip ustun, `~` Anlamli fark yok.")
    lines.append("")

    for model, w_df in wilcoxon_dict.items():
        lines.append(f"### Model: `{model}`")
        if not w_df.empty:
            lines.append(df_to_markdown(w_df))
        lines.append("")

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Istatistik raporu kaydedildi: {out_file}")


def main():
    parser = argparse.ArgumentParser(description="BambuDome Istatistiksel Analiz Motoru")
    parser.add_argument("--results-dir", type=str, default=r"C:\BambuDome_campaign\full\results",
                        help="Kampanya sonuclarinin bulundugu dizin")
    parser.add_argument("--output-dir", type=str, default=str(BASE_DIR.parent / "04_Results"),
                        help="Rapor cikti dizini")
    args = parser.parse_args()

    results_path = Path(args.results_dir)
    if not results_path.exists() or not list(results_path.glob("*.json")):
        # Sentetik/ornek veri URETILMEZ: rapor yalnizca gercek kampanya sonuclarindan olusur.
        print(f"HATA: gercek sonuc dosyasi yok: {results_path}. Once kampanyayi kosturun.", file=sys.stderr)
        return 2
    df = load_campaign_results(results_path)
    n_exp = df.groupby(["model", "algo"]).size()
    if (n_exp < 30).any():
        print(f"Uyari: {int((n_exp < 30).sum())} (model, algoritma) hucresinde 30'dan az tohum var; "
              f"rapor TAMAMLANMAMIS kampanyayi yansitir.", file=sys.stderr)

    summary_df = compute_descriptive_stats(df)
    friedman_dict = {}
    wilcoxon_dict = {}

    for model in df["model"].unique():
        f_stat, p_val, ranks = compute_friedman_test(df, model)
        friedman_dict[model] = (f_stat, p_val, ranks)

        best_algo = ranks.index[0] if not ranks.empty else "abc"
        w_df = compute_wilcoxon_tests(df, model, control_algo=best_algo)
        wilcoxon_dict[model] = w_df

    out_file = Path(args.output_dir) / "STATISTICAL_TEST_RESULTS.md"
    export_markdown_report(summary_df, friedman_dict, wilcoxon_dict, out_file)


if __name__ == "__main__":
    sys.exit(main() or 0)
