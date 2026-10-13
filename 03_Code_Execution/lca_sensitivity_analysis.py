"""
lca_sensitivity_analysis.py
Besikten-Kapiya (A1-A3) Gomulu Karbon Duyarlilik Analizi ve Parametrik Tarama
=============================================================================
Guadua uzay kafes kubbelerde baglanti karbonunun (celik flans + harc dolgusu)
bambu culm govde karbonuna gore oranini ve "Dekarbonizasyon Paradoksu"nun
parametre degisimlerine karsi direncini test eder.

Degistirilen parametreler:
  - L_inj_factor: 1.5 - 3.5 (varsayilan 2.5)
  - EC_steel    : 0.565 - 2.26 kg CO2e/kg (varsayilan 1.13; bauforumstahl EPD, tesis araligi 0.5-2 kat)
  - EC_bamboo   : 0.0324 - 1.23 kg CO2e/kg (varsayilan 0.243; turetilmis)
  - EC_mortar   : 0.155 - 0.62 kg CO2e/kg (varsayilan 0.310; 0.5-2 kat, varsayim)

Kullanim:
  python lca_sensitivity_analysis.py [--output-dir ../04_Results]
"""

from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd

from bamboo_catalog import BAMBOO_CATALOG as C, MATERIAL_PROPERTIES as MP
from dome_types import build_preset
from truss_model import build_dome_model
from fem_bridge import FEMBridge
from fast_eval import FastCore, CarbonModel


BASE_DIR = Path(__file__).parent


def get_representative_designs(results_dir: Path) -> dict[str, dict]:
    """Kampanya sonuclarindan her kubbe icin en hafif UYGUN cozumu (gercek optimum) okur."""
    best: dict[str, dict] = {}
    for p in sorted(results_dir.glob("*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        if not r.get("is_feasible") or "solution" not in r:
            continue
        m = r["model"]
        if m not in best or r["best_structural_weight_kN"] < best[m]["weight"]:
            best[m] = dict(weight=r["best_structural_weight_kN"], algo=r["algo"], seed=r["seed"],
                           gene=np.array(r["solution"], dtype=int))
    if not best:
        raise FileNotFoundError(f"Uygun cozum iceren sonuc yok: {results_dir}")
    builders = {"ribbed40": lambda: build_dome_model(2, 40.0),
                "kiewitt32": lambda: build_preset("kiewitt32"),
                "geodesic16": lambda: build_preset("geodesic16")}
    designs = {}
    for m in ("ribbed40", "kiewitt32", "geodesic16"):
        if m in best:
            designs[m] = dict(model_builder=builders[m], **best[m])
    return designs


def compute_lca_breakdown(model, gene: np.ndarray, carbon: CarbonModel) -> dict:
    """Belirli bir model, gen ve karbon parametre seti icin detayli LCA dökümü."""
    bridge = FEMBridge(model)
    bridge.open()
    groups, lengths = bridge.read_groups_and_lengths()
    G = len(groups)
    if len(gene) != G:
        raise ValueError(f"gen uzunlugu {len(gene)} != grup sayisi {G}")

    sec_idx = np.asarray(np.round(gene[bridge.group_index] - 1), dtype=int)
    A = C["A_m2"].to_numpy(float)[sec_idx]
    D = C["D_m"].to_numpy(float)[sec_idx]
    t = C["t_m"].to_numpy(float)[sec_idx]
    L = bridge.member_lengths_arr
    N_nodes = bridge.n_nodes

    # Bambu kütlesi [kg]
    mass_b = float((MP["rho"] * A * L).sum())

    # Çelik kütlesi [kg]
    steel_ends = carbon.c_s0 + carbon.c_s1 * D
    mass_s = float(N_nodes * carbon.m_hub + 2.0 * steel_ends.sum())

    # Harç kütlesi [kg]
    mortar_ends = carbon.rho_mortar * math.pi / 4.0 * (D - 2.0 * t) ** 2 * (carbon.l_inject_factor * D)
    mass_m = float(2.0 * mortar_ends.sum())

    # Karbon bilesenleri [kg CO2e]
    co2_b = mass_b * carbon.ec_bamboo
    co2_s = mass_s * carbon.ec_steel
    co2_m = mass_m * carbon.ec_mortar
    co2_total = co2_b + co2_s + co2_m
    co2_joint = co2_s + co2_m

    return {
        "mass_bamboo_kg": mass_b,
        "mass_steel_kg": mass_s,
        "mass_mortar_kg": mass_m,
        "mass_total_kg": mass_b + mass_s + mass_m,
        "co2_bamboo_kg": co2_b,
        "co2_steel_kg": co2_s,
        "co2_mortar_kg": co2_m,
        "co2_joint_kg": co2_joint,
        "co2_total_kg": co2_total,
        "pct_bamboo_co2": (co2_b / co2_total) * 100.0,
        "pct_steel_co2": (co2_s / co2_total) * 100.0,
        "pct_mortar_co2": (co2_m / co2_total) * 100.0,
        "pct_joint_co2": (co2_joint / co2_total) * 100.0,
    }


def run_parametric_sensitivity(designs: dict):
    base_results = {}
    
    # 1. Temel Durum Analizi (Base Case)
    base_cm = CarbonModel(
        l_inject_factor=2.5,
        ec_bamboo=0.243,
        ec_steel=1.13,
        ec_mortar=0.310,
    )

    for m_name, d_info in designs.items():
        m = d_info["model_builder"]()
        res = compute_lca_breakdown(m, d_info["gene"], base_cm)
        base_results[m_name] = res

    # 2. Parametrik Taramalar (Tekil Parametre Degisimi)
    param_ranges = {
        "L_inj_factor": [1.5, 2.0, 2.5, 3.0, 3.5],
        "EC_steel": [0.565, 0.85, 1.13, 1.70, 2.26],
        "EC_bamboo": [0.0324, 0.10, 0.243, 0.50, 1.23],
        "EC_mortar": [0.155, 0.23, 0.310, 0.47, 0.62],
    }

    sensitivity_tables = {}

    for m_name, d_info in designs.items():
        m = d_info["model_builder"]()
        m_tables = {}

        # L_inj_factor taraması
        rows_linj = []
        for val in param_ranges["L_inj_factor"]:
            cm = CarbonModel(l_inject_factor=val, ec_bamboo=0.243, ec_steel=1.13, ec_mortar=0.310)
            r = compute_lca_breakdown(m, d_info["gene"], cm)
            rows_linj.append({
                "L_inj / D": val,
                "Mortar Mass (t)": r["mass_mortar_kg"] / 1000.0,
                "Total Carbon (t CO2e)": r["co2_total_kg"] / 1000.0,
                "Steel Carbon %": r["pct_steel_co2"],
                "Mortar Carbon %": r["pct_mortar_co2"],
                "Total Joint Carbon %": r["pct_joint_co2"],
                "Bamboo Carbon %": r["pct_bamboo_co2"],
            })
        m_tables["L_inj"] = pd.DataFrame(rows_linj)

        # EC_steel taraması
        rows_steel = []
        for val in param_ranges["EC_steel"]:
            cm = CarbonModel(l_inject_factor=2.5, ec_bamboo=0.243, ec_steel=val, ec_mortar=0.310)
            r = compute_lca_breakdown(m, d_info["gene"], cm)
            rows_steel.append({
                "EC_steel (kg/kg)": val,
                "Total Carbon (t CO2e)": r["co2_total_kg"] / 1000.0,
                "Steel Carbon %": r["pct_steel_co2"],
                "Total Joint Carbon %": r["pct_joint_co2"],
                "Bamboo Carbon %": r["pct_bamboo_co2"],
            })
        m_tables["EC_steel"] = pd.DataFrame(rows_steel)

        # EC_bamboo taraması
        rows_bam = []
        for val in param_ranges["EC_bamboo"]:
            cm = CarbonModel(l_inject_factor=2.5, ec_bamboo=val, ec_steel=1.13, ec_mortar=0.310)
            r = compute_lca_breakdown(m, d_info["gene"], cm)
            rows_bam.append({
                "EC_bamboo (kg/kg)": val,
                "Total Carbon (t CO2e)": r["co2_total_kg"] / 1000.0,
                "Total Joint Carbon %": r["pct_joint_co2"],
                "Bamboo Carbon %": r["pct_bamboo_co2"],
            })
        m_tables["EC_bamboo"] = pd.DataFrame(rows_bam)

        worst = compute_lca_breakdown(m, d_info["gene"], CarbonModel(
            l_inject_factor=1.5, ec_bamboo=0.50, ec_steel=0.565, ec_mortar=0.155))
        m_tables["worst"] = worst
        sensitivity_tables[m_name] = m_tables

    return base_results, sensitivity_tables


def df_to_md(df: pd.DataFrame) -> str:
    headers = [str(c) for c in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]
    for _, row in df.iterrows():
        row_str = []
        for val in row:
            if isinstance(val, float):
                row_str.append(f"{val:.2f}" if abs(val) < 1000 else f"{val:.1f}")
            else:
                row_str.append(str(val))
        lines.append("| " + " | ".join(row_str) + " |")
    return "\n".join(lines)


def export_lca_report(base_results: dict, sensitivity_tables: dict, designs: dict, src: Path, out_file: Path):
    lines = [
        "# 🌿 BambuDome Beşikten-Kapıya (A1–A3) LCA Duyarlılık ve Karbon Ayrıştırma Raporu",
        "",
        "Bu rapor; 16, 32 ve 40 m açıklıklı Guadua bambu uzay kafes kubbelerde bağlantı detaylarının (çelik mafsal flanşları + enjeksiyon harcı)",
        "yapısal gömülü karbon bilançosundaki ağırlığını ve parametrik duyarlılık sınırlarını belgeler.",
        "",
        f"**Tasarım kaynağı:** `{src}` içindeki her kubbe için en hafif uygun çözüm "
        "(kampanya sonucu, el ile girilmiş gen yok). Tasarımlar:",
        "",
        *[f"- `{k}`: {v['weight']:.2f} kN, algoritma {v['algo'].upper()}, tohum {v['seed']}" for k, v in designs.items()],
        "",
        "---",
        "",
        "## 1. Temel Durum (Base-Case) Karbon ve Kütle Dökümü",
        "",
        "Varsayılan Parametreler: $L_{\\text{inj}} = 2.5 D$, $EC_{\\text{bamboo}} = 0.243$ (türetilmiş), $EC_{\\text{steel}} = 1.13$ (bauforumstahl EPD), $EC_{\\text{mortar}} = 0.310\\text{ kg CO}_2\\text{e/kg}$ (SikaGrout-312 HP EPD).",
        "",
    ]

    base_summary = []
    for m_name, r in base_results.items():
        base_summary.append({
            "Kubbe Modeli": m_name,
            "Bambu Kütlesi (t)": r["mass_bamboo_kg"] / 1000.0,
            "Çelik Kütlesi (t)": r["mass_steel_kg"] / 1000.0,
            "Harç Kütlesi (t)": r["mass_mortar_kg"] / 1000.0,
            "Toplam Kütle (t)": r["mass_total_kg"] / 1000.0,
            "Bambu Karbonu %": r["pct_bamboo_co2"],
            "Çelik Karbonu %": r["pct_steel_co2"],
            "Harç Karbonu %": r["pct_mortar_co2"],
            "Toplam Bağlantı Karbonu %": r["pct_joint_co2"],
            "Toplam Karbon (t CO2e)": r["co2_total_kg"] / 1000.0,
        })
    lines.append(df_to_md(pd.DataFrame(base_summary)))
    lines.append("")
    jp = [r["pct_joint_co2"] for r in base_results.values()]
    sp = [r["pct_steel_co2"] for r in base_results.values()]
    lines.append(f"> Temel senaryoda bağlantı bileşenleri (çelik + harç) toplam gömülü karbonun %{min(jp):.1f}–%{max(jp):.1f}'ini, "
                 f"yalnızca çelik %{min(sp):.1f}–%{max(sp):.1f}'ini oluşturur (bu tasarımlar için; $EC_s$ ve $EC_m$ değerleri beyan edilmiş EPD değerleridir (bauforumstahl, SikaGrout-312 HP), $EC_b$ INBAR TR35 ve Zea & Habert 2014'ten türetilmiş baz değerdir).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Parametrik Duyarlılık Analizi (Sensitivity Analysis)")
    lines.append("")

    for m_name, tables in sensitivity_tables.items():
        lines.append(f"### Model: `{m_name}`")
        lines.append("")
        lines.append("#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\\text{inj}} / D \\in [1.5, 3.5]$)")
        lines.append(df_to_md(tables["L_inj"]))
        lines.append("")
        lines.append("#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\\text{steel}} \\in [0.565, 2.26]\\text{ kg CO}_2\\text{e/kg}$)")
        lines.append(df_to_md(tables["EC_steel"]))
        lines.append("")
        lines.append("#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\\text{bamboo}} \\in [0.0324, 1.23]\\text{ kg CO}_2\\text{e/kg}$)")
        lines.append(df_to_md(tables["EC_bamboo"]))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines += ["## 3. Senaryo Sınırları (hesaplanan)", "",
              "Birleşik senaryo: parametreler bağlantı payını azaltan yönde birlikte uygulandı (L_inj=1.5D, EC_steel=0.565, EC_bamboo=0.50, EC_mortar=0.155). Bu, tek parametreli taramaların en düşük değeri değildir:", ""]
    for m, t in sensitivity_tables.items():
        lines.append(f"- `{m}`: bağlantı payı %{t['worst']['pct_joint_co2']:.1f} (bambu %{t['worst']['pct_bamboo_co2']:.1f})")
    lines.append("")
    lines.append("Tek parametreli taramalarda (a–c) görülen en düşük bağlantı payı: " + ", ".join(
        f"`{m}` %{min(t[k]['Total Joint Carbon %'].min() for k in ('L_inj', 'EC_steel', 'EC_bamboo')):.1f}"
        for m, t in sensitivity_tables.items()) + ".")
    lines.append("")
    lines.append("Tekil taramalar a–c tablolarındadır. Bu rapordaki sayılar varsayılan EC değerlerine bağlıdır ve literatürle doğrulanana kadar nihai bulgu sayılmamalıdır.")
    lines.append("")

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"LCA duyarlilik raporu kaydedildi: {out_file}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", default="C:/BambuDome_campaign/full/results")
    args = ap.parse_args()
    src = Path(args.results_dir)
    designs = get_representative_designs(src)
    base_res, sens_tables = run_parametric_sensitivity(designs)
    out_file = BASE_DIR.parent / "04_Results" / "LCA_SENSITIVITY_REPORT.md"
    export_lca_report(base_res, sens_tables, designs, src, out_file)


if __name__ == "__main__":
    main()
