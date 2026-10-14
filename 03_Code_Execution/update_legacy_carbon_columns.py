"""
update_legacy_carbon_columns.py
Recalculates best_embodied_carbon_kgCO2e across summary.csv, global_best_*.json,
and steel_reference_aisc37_summary.csv using current declared EPD factors:
  EC_bamboo     = 0.243 kg CO2e/kg (TR35 + DEFRA 2023 transport)
  EC_steel      = 1.130 kg CO2e/kg (Bauforumstahl plate EPD)
  EC_steel_tube = 1.701 kg CO2e/kg (Welded Tube of Canada HSS EPD)
  EC_mortar     = 0.310 kg CO2e/kg (SikaGrout-312 HP EPD)
"""

import sys, json, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from results_report import bamboo_context, bamboo_breakdown, steel_breakdown
from steel_reference import configure, make_core as steel_core

def update_all():
    base_dir = Path(__file__).resolve().parent.parent
    res_dir = Path(r"C:\BambuDome_campaign\full\results")
    campaign_final_dir = base_dir / "04_Results" / "campaign_final"

    # 1. Update summary.csv (bamboo 270 runs)
    models = {}
    for m in ["geodesic16", "kiewitt32", "ribbed40"]:
        _, _, core, cat = bamboo_context(m)
        models[m] = (core, cat)

    csv_path = campaign_final_dir / "summary.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fieldnames = list(rows[0].keys())

    updated = 0
    for r in rows:
        m = r["model"]
        algo = r["algo"]
        seed = r["seed"]
        jf = res_dir / f"{m}__{algo}__s{seed}.json"
        if jf.exists():
            jd = json.loads(jf.read_text(encoding="utf-8"))
            gene = jd["solution"]
            core, cat = models[m]
            bd = bamboo_breakdown(core, cat, gene)
            tot_co2 = bd["co2_bamboo"] + bd["co2_steel"] + bd["co2_mortar"]
            r["best_embodied_carbon_kgCO2e"] = f"{tot_co2:.4f}"
            updated += 1

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Updated summary.csv: {updated} / {len(rows)} rows.")

    # 2. Update global_best_*.json
    bests = {
        "geodesic16": campaign_final_dir / "global_best_geodesic16.json",
        "kiewitt32": campaign_final_dir / "global_best_kiewitt32.json",
        "ribbed40": campaign_final_dir / "global_best_ribbed40.json",
    }
    for m, p in bests.items():
        d = json.loads(p.read_text(encoding="utf-8"))
        core, cat = models[m]
        bd = bamboo_breakdown(core, cat, d["gene"])
        tot_co2 = bd["co2_bamboo"] + bd["co2_steel"] + bd["co2_mortar"]
        d["carbon"] = tot_co2
        p.write_text(json.dumps(d, indent=1), encoding="utf-8")
        print(f"Updated {p.name}: carbon = {tot_co2:.2f} kg CO2e")

    # 3. Update steel_reference_aisc37_summary.csv (120 runs)
    configure(catalog="aisc37")
    steel_cores = {}
    for m in ["ribbed354", "ribbed40", "kiewitt32", "geodesic16"]:
        _, _, sc, _ = steel_core(m)
        steel_cores[m] = sc

    steel_csv = campaign_final_dir / "steel_reference_aisc37_summary.csv"
    with open(steel_csv, "r", encoding="utf-8") as f:
        s_rows = list(csv.DictReader(f))
    s_fields = list(s_rows[0].keys())

    s_updated = 0
    for r in s_rows:
        m = r["model"]
        sol = [int(x) for x in r["solution"].split()]
        sc = steel_cores[m]
        bd = steel_breakdown(sc, sol)
        tot_co2 = bd["co2_tube"] + bd["co2_conn"]
        r["carbon_kgCO2e"] = f"{tot_co2:.4f}"
        s_updated += 1

    with open(steel_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=s_fields)
        writer.writeheader()
        writer.writerows(s_rows)
    print(f"Updated steel_reference_aisc37_summary.csv: {s_updated} / {len(s_rows)} rows.")

    # 4. Update campaign_final/README.md
    readme_path = campaign_final_dir / "README.md"
    readme_content = """# Kampanya Özeti (Nihai Senkronize Veriler)
- `summary.csv`: 270 iş (3 kubbe x ABC/ACO/DO x 30 tohum), NFE = 1000 x tasarım değişkeni; `global_best*.json`: en hafif tasarımlar (gen, ağırlık, SAP2000 doğrulaması).
- `steel_reference_aisc37_summary.csv`: çelik referans (37 AISC boru, ASD) 120 iş.
- Ham kayıtlar (her işin değerlendirme başına .npz ve yakınsama geçmişi, ~135 MB) `C:\\BambuDome_campaign\\full\\results` altında; gerektiğinde Zenodo/Release ile paylaşılabilir.
- Karbon sütunları: Tüm `best_embodied_carbon_kgCO2e` ve `carbon_kgCO2e` sütunları, EPD faktörleri (EC_bamboo 0.243, EC_steel 1.13, EC_pipe 1.701, EC_mortar 0.310 kg CO2e/kg) ile yeniden hesaplanarak `../tables/T5–T8` ve `../LCA_SENSITIVITY_REPORT.md` ile tam senkronize edilmiştir.
"""
    readme_path.write_text(readme_content, encoding="utf-8")
    print("Updated campaign_final/README.md.")

if __name__ == "__main__":
    update_all()
