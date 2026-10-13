"""
export_repro_tables_csv.py
--------------------------
Markdown raporlarındaki ve kampanya geçmişindeki verileri hakemlerin ve kamunun
doğrudan inceleyebileceği temiz, standart CSV formatlarına dönüştürür.
Üretilen CSV dosyaları:
  1. 04_Results/tables/T_stats_descriptive.csv
  2. 04_Results/tables/T_stats_friedman_ranks.csv
  3. 04_Results/tables/T_stats_wilcoxon_pairwise.csv
  4. 04_Results/tables/T_lca_base_case_breakdown.csv
  5. 04_Results/tables/T_lca_sensitivity_grout_length.csv
  6. 04_Results/tables/T_lca_sensitivity_steel_ec.csv
  7. 04_Results/tables/T_lca_sensitivity_bamboo_ec.csv
  8. 04_Results/tables/T_tuning_study_summary.csv
  9. 04_Results/tables/T_governing_limit_shares.csv
  10. 04_Results/tables/T_convergence_curves_history.csv (Şekil 3 kaynak verisi)
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR.parent / "04_Results"
TABLES_DIR = RESULTS_DIR / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)


def export_statistical_tables():
    md_path = RESULTS_DIR / "STATISTICAL_TEST_RESULTS.md"
    if not md_path.exists():
        print(f"Uyarı: {md_path} bulunamadı.")
        return

    content = md_path.read_text(encoding="utf-8")

    # 1. Descriptive stats
    # Tablo satırlarını yakala
    desc_rows = []
    lines = content.splitlines()
    in_desc = False
    for line in lines:
        if "## 1. Betimsel Istatistikler" in line:
            in_desc = True
            continue
        if in_desc and line.startswith("## 2."):
            in_desc = False
            break
        if in_desc and line.strip().startswith("|") and not "---" in line and not "Model | Algorithm" in line:
            parts = [p.strip() for p in line.strip().split("|")[1:-1]]
            if len(parts) >= 11:
                desc_rows.append({
                    "Model": parts[0],
                    "Algorithm": parts[1],
                    "Runs": int(parts[2]),
                    "Feasible": parts[3],
                    "Weight_Best_kN": float(parts[4]),
                    "Weight_Median_kN": float(parts[5]),
                    "Weight_Mean_kN": float(parts[6]),
                    "Weight_Std_kN": float(parts[7]),
                    "Carbon_Mean_kgCO2e": float(parts[8]),
                    "NFE_Mean": float(parts[9]),
                    "Time_s": float(parts[10]),
                })
    if desc_rows:
        df_desc = pd.DataFrame(desc_rows)
        out_csv = TABLES_DIR / "T_stats_descriptive.csv"
        df_desc.to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv}")

    # 2. Friedman ranks
    friedman_rows = []
    # Modelleri ve chi2/p-value'ları yakala
    models = ["geodesic16", "kiewitt32", "ribbed40"]
    for m in models:
        m_block = re.search(rf"### Model: `{m}`\s+- \*\*Friedman \$\\chi\^2_F\$:?\*\* ([\d.]+)\s+- \*\*Asymptotic \$p\$-degeri:\*\* ([^\n\r]+)", content)
        chi2 = float(m_block.group(1)) if m_block else None
        p_val_str = m_block.group(2).split()[0] if m_block else None
        p_val = float(p_val_str) if p_val_str else None

        # Ranks tablosu
        rank_sec = re.search(rf"### Model: `{m}`.*?\| Algoritma \| Ortalama Sira \|.*?\n\| [-|\s]+\|\s*\n(.*?)(?=\n\s*### Model|\n\s*## 3|\Z)", content, re.DOTALL)
        if rank_sec:
            for rline in rank_sec.group(1).strip().splitlines():
                if rline.strip().startswith("|") and not "Algoritma" in rline and not "---" in rline:
                    rparts = [p.strip() for p in rline.strip().split("|")[1:-1]]
                    if len(rparts) >= 2:
                        friedman_rows.append({
                            "Model": m,
                            "Algorithm": rparts[0],
                            "Mean_Rank": float(rparts[1]),
                            "Chi2_Friedman": chi2,
                            "p_value": p_val,
                        })
    if friedman_rows:
        df_fr = pd.DataFrame(friedman_rows)
        out_csv = TABLES_DIR / "T_stats_friedman_ranks.csv"
        df_fr.to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv}")

    # 3. Wilcoxon/Mann-Whitney pairwise
    wilcoxon_rows = []
    for m in models:
        w_sec = re.search(rf"## 3\. Wilcoxon.*?\n\s*### Model: `{m}`.*?\| Comparison \| Diff_Median \| U_Stat \| p_value \| A12_rakip_kotu \| Sig_005 \| p_Holm \|\s*\n\| [-\s|]+\|\s*\n(.*?)(?=\n\s*###|\Z)", content, re.DOTALL)
        if w_sec:
            for wline in w_sec.group(1).strip().splitlines():
                if wline.strip().startswith("|"):
                    wparts = [p.strip() for p in wline.strip().split("|")[1:-1]]
                    if len(wparts) >= 7:
                        wilcoxon_rows.append({
                            "Model": m,
                            "Comparison": wparts[0],
                            "Diff_Median_kN": float(wparts[1]),
                            "U_Statistic": float(wparts[2]),
                            "p_value": float(wparts[3]),
                            "Vargha_Delaney_A12": float(wparts[4]),
                            "Significance_005": wparts[5],
                            "p_Holm_corrected": float(wparts[6]),
                        })
    if wilcoxon_rows:
        df_wc = pd.DataFrame(wilcoxon_rows)
        out_csv = TABLES_DIR / "T_stats_wilcoxon_pairwise.csv"
        df_wc.to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv}")


def export_lca_sensitivity_tables():
    md_path = RESULTS_DIR / "LCA_SENSITIVITY_REPORT.md"
    if not md_path.exists():
        print(f"Uyarı: {md_path} bulunamadı.")
        return

    content = md_path.read_text(encoding="utf-8")

    # 1. Base case
    base_rows = []
    base_sec = re.search(r"## 1\. Temel Durum.*?\| Kubbe Modeli \| Bambu Kütlesi.*?\| [-\s|]+\|\s*\n(.*?)(?=\n\s*>|\n\s*---)", content, re.DOTALL)
    if base_sec:
        for line in base_sec.group(1).strip().splitlines():
            if line.strip().startswith("|"):
                p = [x.strip() for x in line.strip().split("|")[1:-1]]
                if len(p) >= 10:
                    base_rows.append({
                        "Dome": p[0],
                        "Bamboo_Mass_t": float(p[1]),
                        "Steel_Mass_t": float(p[2]),
                        "Grout_Mass_t": float(p[3]),
                        "Total_Mass_t": float(p[4]),
                        "Bamboo_Carbon_pct": float(p[5]),
                        "Steel_Carbon_pct": float(p[6]),
                        "Grout_Carbon_pct": float(p[7]),
                        "Total_Joint_Carbon_pct": float(p[8]),
                        "Total_Carbon_tCO2e": float(p[9]),
                    })
    if base_rows:
        df_base = pd.DataFrame(base_rows)
        out_csv = TABLES_DIR / "T_lca_base_case_breakdown.csv"
        df_base.to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv}")

    # 2. Grout length sensitivity
    grout_rows = []
    # 3. Steel EC sensitivity
    steel_rows = []
    # 4. Bamboo EC sensitivity
    bamboo_rows = []

    models = ["ribbed40", "kiewitt32", "geodesic16"]
    for m in models:
        # a) grout
        m_grout = re.search(rf"### Model: `{m}`.*?#### a\) Enjeksiyon Uzunluğunun Etkisi.*?\| L_inj / D \| Mortar Mass.*?\| [-\s|]+\|\s*\n(.*?)(?=\n\s*#### b\))", content, re.DOTALL)
        if m_grout:
            for l in m_grout.group(1).strip().splitlines():
                if l.strip().startswith("|"):
                    p = [x.strip() for x in l.strip().split("|")[1:-1]]
                    if len(p) >= 7:
                        grout_rows.append({
                            "Dome": m,
                            "L_inj_over_D": float(p[0]),
                            "Grout_Mass_t": float(p[1]),
                            "Total_Carbon_tCO2e": float(p[2]),
                            "Steel_Carbon_pct": float(p[3]),
                            "Grout_Carbon_pct": float(p[4]),
                            "Total_Joint_Carbon_pct": float(p[5]),
                            "Bamboo_Carbon_pct": float(p[6]),
                        })

        # b) steel ec
        m_steel = re.search(rf"### Model: `{m}`.*?#### b\) Çelik Gömülü Karbon.*?\| EC_steel \(kg/kg\) \| Total Carbon.*?\| [-\s|]+\|\s*\n(.*?)(?=\n\s*#### c\))", content, re.DOTALL)
        if m_steel:
            for l in m_steel.group(1).strip().splitlines():
                if l.strip().startswith("|"):
                    p = [x.strip() for x in l.strip().split("|")[1:-1]]
                    if len(p) >= 5:
                        steel_rows.append({
                            "Dome": m,
                            "EC_steel_kg_per_kg": float(p[0]),
                            "Total_Carbon_tCO2e": float(p[1]),
                            "Steel_Carbon_pct": float(p[2]),
                            "Total_Joint_Carbon_pct": float(p[3]),
                            "Bamboo_Carbon_pct": float(p[4]),
                        })

        # c) bamboo ec
        m_bamboo = re.search(rf"### Model: `{m}`.*?#### c\) Bambu Gömülü Karbon.*?\| EC_bamboo \(kg/kg\) \| Total Carbon.*?\| [-\s|]+\|\s*\n(.*?)(?=\n\s*###|\Z)", content, re.DOTALL)
        if m_bamboo:
            for l in m_bamboo.group(1).strip().splitlines():
                if l.strip().startswith("|"):
                    p = [x.strip() for x in l.strip().split("|")[1:-1]]
                    if len(p) >= 4:
                        bamboo_rows.append({
                            "Dome": m,
                            "EC_bamboo_kg_per_kg": float(p[0]),
                            "Total_Carbon_tCO2e": float(p[1]),
                            "Total_Joint_Carbon_pct": float(p[2]),
                            "Bamboo_Carbon_pct": float(p[3]),
                        })

    if grout_rows:
        pd.DataFrame(grout_rows).to_csv(TABLES_DIR / "T_lca_sensitivity_grout_length.csv", index=False)
        print(f"Kaydedildi: {TABLES_DIR / 'T_lca_sensitivity_grout_length.csv'}")
    if steel_rows:
        pd.DataFrame(steel_rows).to_csv(TABLES_DIR / "T_lca_sensitivity_steel_ec.csv", index=False)
        print(f"Kaydedildi: {TABLES_DIR / 'T_lca_sensitivity_steel_ec.csv'}")
    if bamboo_rows:
        pd.DataFrame(bamboo_rows).to_csv(TABLES_DIR / "T_lca_sensitivity_bamboo_ec.csv", index=False)
        print(f"Kaydedildi: {TABLES_DIR / 'T_lca_sensitivity_bamboo_ec.csv'}")


def export_tuning_summary_table():
    md_path = RESULTS_DIR / "TUNING_STUDY.md"
    if not md_path.exists():
        return
    content = md_path.read_text(encoding="utf-8")
    tuning_rows = []
    models = ["geodesic16", "kiewitt32", "ribbed40"]
    for m in models:
        m_sec = re.search(rf"## {m}.*?\| Algoritma \| pop \| n \| ortalama \| std \| en iyi \| uygun oran \|\s*\n\|[-\s|]+\|\s*\n(.*?)(?=\n\s*##|\Z)", content, re.DOTALL)
        if m_sec:
            for l in m_sec.group(1).strip().splitlines():
                if l.strip().startswith("|"):
                    p = [x.strip() for x in l.strip().split("|")[1:-1]]
                    if len(p) >= 7:
                        tuning_rows.append({
                            "Model": m,
                            "Algorithm": p[0],
                            "Population_Size": int(p[1]),
                            "Sample_Size_n": int(p[2]),
                            "Weight_Mean_kN": float(p[3]),
                            "Weight_Std_kN": float(p[4]),
                            "Weight_Best_kN": float(p[5]),
                            "Feasible_Ratio": float(p[6]),
                        })
    if tuning_rows:
        out_csv = TABLES_DIR / "T_tuning_study_summary.csv"
        pd.DataFrame(tuning_rows).to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv}")


def export_governing_limits_table():
    md_path = RESULTS_DIR / "GOVERNING_LIMIT_SHARES.md"
    if not md_path.exists():
        return
    content = md_path.read_text(encoding="utf-8")
    gov_rows = []
    for l in content.splitlines():
        if l.strip().startswith("|") and not "---" in l and not "Dome |" in l:
            p = [x.strip() for x in l.strip().split("|")[1:-1]]
            if len(p) >= 7:
                gov_rows.append({
                    "Dome": p[0],
                    "Design_Type": p[1],
                    "Tension_Groups": p[2],
                    "Compression_Buckling_Groups": p[3],
                    "Slenderness_Groups": p[4],
                    "Connection_Groups": p[5],
                    "Total_Groups": p[6],
                })
    if gov_rows:
        out_csv = TABLES_DIR / "T_governing_limit_shares.csv"
        pd.DataFrame(gov_rows).to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv}")


def export_convergence_curves_csv():
    """C:\\BambuDome_campaign\\full\\results içindeki 270 JSON sonucundan Şekil 3 eğrilerini CSV'ye döker."""
    results_dir = Path(r"C:\BambuDome_campaign\full\results")
    if not results_dir.exists():
        print("Uyarı: C:\\BambuDome_campaign\\full\\results dizini bulunamadı.")
        return

    # Tüm json dosyalarını yükle
    res = []
    for p in results_dir.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if "model" in d and "algo" in d and "history" in d:
                res.append(d)
        except Exception:
            pass

    if not res:
        print("Uyarı: Geçerli kampanya JSON dosyası bulunamadı.")
        return

    MODELS = ["geodesic16", "kiewitt32", "ribbed40"]
    ALGOS = ["abc", "aco", "do"]
    conv_rows = []

    for m in MODELS:
        for algo in ALGOS:
            rr = [r for r in res if r["model"] == m and r["algo"].lower() == algo]
            if not rr:
                continue
            budget = rr[0]["nfe"]
            grid = np.linspace(rr[0].get("pop", 20), budget, 300)
            curves = []
            for r in rr:
                ev = np.array([h["evals"] for h in r["history"]])
                bp = np.array([h["best_penalized"] for h in r["history"]])
                idx = np.searchsorted(ev, grid, side="right") - 1
                curves.append(bp[np.clip(idx, 0, None)])
            cur = np.array(curves)
            mean_c = cur.mean(axis=0)
            min_c = cur.min(axis=0)
            std_c = cur.std(axis=0)

            for step_i, nfe_val in enumerate(grid):
                conv_rows.append({
                    "Dome": m,
                    "Algorithm": algo.upper(),
                    "NFE": round(float(nfe_val), 1),
                    "Mean_Penalized_Weight_kN": round(float(mean_c[step_i]), 4),
                    "Best_Penalized_Weight_kN": round(float(min_c[step_i]), 4),
                    "Std_Penalized_Weight_kN": round(float(std_c[step_i]), 4),
                })

    if conv_rows:
        df_conv = pd.DataFrame(conv_rows)
        out_csv = TABLES_DIR / "T_convergence_curves_history.csv"
        df_conv.to_csv(out_csv, index=False)
        print(f"Kaydedildi: {out_csv} ({len(df_conv)} satır)")


if __name__ == "__main__":
    print("=== BAMBUDOME REPRO CSV DÖNÜŞTÜRÜCÜ BAŞLATILIYOR ===")
    export_statistical_tables()
    export_lca_sensitivity_tables()
    export_tuning_summary_table()
    export_governing_limits_table()
    export_convergence_curves_csv()
    print("=== TAMAMLANDI ===")
