"""
price_scenarios.py
Ulke bazli fiyat senaryolari (gercek belgelerden) ve maliyet karsilastirmasi.

Belgeler (Evidence/): Jawa Tengah HSD/HSPK 2024 (Endonezya), CPWD DSR 2023 Vol.I (Hindistan), CSB 2026 Agustos (Turkiye).
Kurlar (Evidence/FX/): Dunya Bankasi PA.NUS.FCRF (IMF-IFS yillik ort.): Hindistan 2023, Endonezya 2024; TCMB 03.08.2026 gunluk kuru.
Eksik kalemler ORANLA doldurulur (asagida): yapisal capli bambu, Turkiye/Hindistan bambu fiyati, Turkiye grout/celik malzeme.
OCR ile okunan degerler (Jateng, DSR) sayfada gozle dogrulanmalidir (bkz. 04_Results/PARAMETER_EVIDENCE_REVIEW.md, 6. bolum).

Kullanim: python price_scenarios.py
"""
from __future__ import annotations
import sys
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE.parent / "04_Results" / "tables"

FX = {"IND2023": 82.5992764460784, "IDN2024": 15855.448286671, "TUR2026": (47.4497 + 47.5352) / 2, "COL2025": 4053.13583333333}

# --- ham veriler (yerel para) -------------------------------------------------------------------
IDN = dict(steel_mat=np.mean([18000, 16053, 20300, 18000]),          # Rp/kg Baja Profil (Jateng, 4 bolge)
           grout=np.mean([7173, 8380, 9705, 8911]),                  # Rp/kg Semen Grout
           bamboo7_per_m=np.mean([21546, 22409, 22009, 21712]) / 6)   # OCRBambu.md (kullanici transkripsiyonu) ile teyitli  # Rp/m, Bambu D 6-8 cm, 6 m
IND = dict(steel_mat=59.65, tube_erected=194.40, bolts=159.35, grout=28.00)   # Rs/kg (DSR 2023: 1007, 10.16.1, 10.20, 1251)
TUR = dict(tube_erected=106.70, fabricated=190.01)                              # TL/kg (CSB Agustos 2026: 15.165.1002, 15.550.1201)

D_REF_MM = 70.0
# Kolombiya 2026 (guaduabambucolombia.co, 27.06.2026): 6 m birim 38.500 COP (=6.417 COP/m); "metro lineal" 7.500 COP. Cap BELIRTILMEMIS (varsayim: D_ref = 120 mm).
COL = dict(unit6m=38500.0, lineal=7500.0)
COL_D_REF_MM = 120.0


def derive(alpha: float = 2.0) -> pd.DataFrame:
    """Her ulke icin USD fiyat seti. Eksikler oranla (Endonezya/Hindistan gozlemlerinden)."""
    idn = {k: v / FX["IDN2024"] for k, v in IDN.items()}
    ind = {k: v / FX["IND2023"] for k, v in IND.items()}
    tur = {k: v / FX["TUR2026"] for k, v in TUR.items()}
    r_b = idn["bamboo7_per_m"] / idn["steel_mat"]                      # [m/kg-esdeger]: bambu(D70) USD/m / celik malzeme USD/kg
    r_g = np.mean([idn["grout"] / idn["steel_mat"], ind["grout"] / ind["steel_mat"]])
    k_tube = ind["tube_erected"] / ind["steel_mat"]                    # yerine konmus boru kafes / celik malzeme (Hindistan)
    k_bolt = ind["bolts"] / ind["steel_mat"]                           # cıvata (tam) / celik malzeme
    rows = []
    # Endonezya 2024
    rows.append(dict(country="Indonesia 2024 (Jateng HSD)", steel_mat=idn["steel_mat"], steel_erected=idn["steel_mat"] * k_tube,
                     conn=idn["steel_mat"] * k_bolt, grout=idn["grout"], bamboo_ref=idn["bamboo7_per_m"], d_ref=70.0,
                     note="bambu, celik malzeme, grout: belgeden; erected/baglanti: Hindistan oranlari"))
    # Hindistan 2023
    rows.append(dict(country="India 2023 (CPWD DSR)", steel_mat=ind["steel_mat"], steel_erected=ind["tube_erected"],
                     conn=ind["bolts"], grout=ind["grout"], bamboo_ref=r_b * ind["steel_mat"], d_ref=70.0,
                     note="celik, baglanti, grout: belgeden; bambu: Endonezya oranindan (r_b)"))
    # Turkiye 2026
    mat = tur["tube_erected"] / k_tube
    rows.append(dict(country="Turkiye 2026 (CSB Agustos)", steel_mat=mat, steel_erected=tur["tube_erected"],
                     conn=tur["fabricated"], grout=r_g * mat, bamboo_ref=r_b * mat, d_ref=70.0,
                     note="erected ve imalat: belgeden; celik malzeme=erected/k_tube (Hindistan); grout, bambu: oranla"))
    # Kolombiya 2026: yalniz bambu (Guadua) fiyati belgeli; celik/grout Endonezya-Hindistan ortalamasi (USD) proxy
    sm = np.mean([idn["steel_mat"], ind["steel_mat"]]); gr = np.mean([idn["grout"], ind["grout"]])
    rows.append(dict(country="Colombia 2026 (Guadua, D_ref=120 mm varsayim)", steel_mat=sm, steel_erected=sm * k_tube, conn=sm * k_bolt,
                     grout=gr, bamboo_ref=COL["unit6m"] / 6.0 / FX["COL2025"], d_ref=COL_D_REF_MM,
                     note="bambu: Guadua 6 m birim fiyat (2026, kur=2025 ort.); celik/grout: Endonezya-Hindistan ortalamasi (proxy)"))
    df = pd.DataFrame(rows)
    df.attrs.update(r_b=r_b, r_g=r_g, k_tube=k_tube, k_bolt=k_bolt, alpha=alpha)
    return df


def culm_price_per_m(D_m, bamboo_ref, alpha, d_ref=D_REF_MM):
    return bamboo_ref * (np.asarray(D_m) * 1000.0 / d_ref) ** alpha


def main() -> None:
    sys.path.insert(0, str(BASE))
    import results_report as rr
    import steel_reference as sr
    from results_report import MODELS
    sr.configure(code="asd89", catalog="aisc37", fy_mpa=248.2, e_gpa=205.0)
    res = rr.load_results(Path(r"C:\BambuDome_campaign\full"))
    steel = rr.load_results(Path(r"C:\BambuDome_campaign\steel_ref_aisc37"))
    OUT.mkdir(parents=True, exist_ok=True)

    inputs = []
    designs = {}
    for m in MODELS:
        _, _, core, cat = rr.bamboo_context(m)
        best = min([r for r in res if r["model"] == m and r["is_feasible"]], key=lambda r: r["best_structural_weight_kN"])
        gene = np.array(best["solution"])
        sec = gene[core.gidx] - 1
        D = cat["D_m"].to_numpy(float)[sec]
        bd = rr.bamboo_breakdown(core, cat, gene)
        _, _, sc, _ = sr.make_core(m)
        sbest = min([r for r in steel if r["model"] == m and r["is_feasible"]], key=lambda r: r["best_structural_weight_kN"])
        sb = rr.steel_breakdown(sc, sbest["solution"])
        designs[m] = dict(L=core.L, D=D, bd=bd, steel_mass=sb["mass_tube"] + sb["mass_conn"])

    rows = []
    for alpha in (1.5, 2.0, 2.5, 3.0):
        P = derive(alpha)
        if alpha == 2.0:
            inputs = P.copy()
            inputs.to_csv(OUT / "T9a_price_scenario_inputs_USD.csv", index=False)
            (OUT / "T9a_price_scenario_inputs_USD.md").write_text(
                "### Table 9a. Price scenario inputs (nominal USD at document-year FX; derived items from ratios)\n\n"
                + rr.md_table(inputs, "{:.4g}") + f"\n\nRatios: r_b (bamboo D=70 mm USD/m per steel-material USD/kg) = {P.attrs['r_b']:.3f}; "
                f"r_grout = {P.attrs['r_g']:.3f}; k_tube (erected/material) = {P.attrs['k_tube']:.2f}; k_bolt = {P.attrs['k_bolt']:.2f}. "
                f"FX: INR 2023 = {FX['IND2023']:.2f}, IDR 2024 = {FX['IDN2024']:.0f}, TRY (TCMB 03.08.2026) = {FX['TUR2026']:.4f} per USD.\n", encoding="utf-8")
        for _, p in P.iterrows():
            for m in MODELS:
                d = designs[m]
                culm = float((culm_price_per_m(d["D"], p.bamboo_ref, alpha, p.d_ref) * d["L"]).sum())
                conn = d["bd"]["mass_steel"] * p.steel_mat          # baglanti celigi: celik MALZEME fiyati (kapsam: yalniz malzeme)
                mort = d["bd"]["mass_mortar"] * p.grout
                bamboo = culm + conn + mort
                steel_mat = d["steel_mass"] * p.steel_mat            # celik yapi: yalniz malzeme
                rows.append({"Scenario": p.country, "alpha": alpha, "Dome": m, "Bamboo material cost [USD]": bamboo,
                             "culm [%]": 100 * culm / bamboo, "connector steel [%]": 100 * conn / bamboo, "mortar/grout [%]": 100 * mort / bamboo,
                             "Steel material cost [USD]": steel_mat, "Bamboo/Steel (material only)": bamboo / steel_mat})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "T9_price_scenarios_cost.csv", index=False)
    (OUT / "T9_price_scenarios_cost.md").write_text(
        "### Table 9. Cost of optimum designs under country price scenarios (material-only scope for both structures)\n\n"
        + rr.md_table(t, "{:.3f}") + "\n", encoding="utf-8")
    print(t.round(3).to_string())


if __name__ == "__main__":
    main()
