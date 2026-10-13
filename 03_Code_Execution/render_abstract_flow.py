"""
render_abstract_flow.py
Yüksek çözünürlüklü ve Q1 dergi standartlarında Graphical Abstract ve Metodoloji Akış Şeması üretir.
"""
import os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "04_Results" / "figures"
DOMES_DIR = OUT / "domes"
CM = 1 / 2.54

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 8,
    "mathtext.fontset": "cm",
})

BLUE = "#1a365d"
ACCENT_BLUE = "#2b6cb0"
RED = "#c53030"
GREEN = "#276749"
GREY = "#4a5568"
LIGHT_BG = "#f7fafc"
CARD_BG = "#edf2f7"

def box(ax, x, y, w, h, text, fc="#ebf8ff", ec="#3182ce", fs=8, bold=False, text_col="#1a202c"):
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.02",
        fc=fc, ec=ec, lw=1.2, zorder=2
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=text_col, linespacing=1.25, zorder=3)

def arrow(ax, p, q, col="#4a5568"):
    ax.add_patch(FancyArrowPatch(
        p, q, arrowstyle="-|>", mutation_scale=10, lw=1.2, color=col, shrinkA=0, shrinkB=0, zorder=4
    ))

# -----------------------------------------------------------------------------------------
# 1. GRAPHICAL ABSTRACT (ENHANCED PUBLICATION-READY VERSION)
# -----------------------------------------------------------------------------------------
bw = {
    "Geodesic (16 m)": (18.211, 13.434, 5.800, 11.404, 0.319, 0.639),
    "Kiewitt (32 m)":  (141.320, 68.456, 41.058, 60.666, 0.424, 0.926),
    "Ribbed (40 m)":   (277.222, 128.955, 66.352, 104.685, 0.493, 1.021)
}

fig = plt.figure(figsize=(19 * CM, 10.5 * CM), dpi=300)

# Banner Başlık
ax_title = fig.add_axes([0.02, 0.88, 0.96, 0.10])
ax_title.set_axis_off()
ax_title.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01,rounding_size=0.03", fc="#2a4365", ec="none"))
ax_title.text(0.5, 0.52, "Sizing Optimization of Guadua Bamboo Space Domes & Connection Decarbonization Paradox",
              ha="center", va="center", fontsize=8.5, fontweight="bold", color="white")

# Üst Aşama Kartları
ax_flow = fig.add_axes([0.02, 0.64, 0.96, 0.22])
ax_flow.set_axis_off(); ax_flow.set_xlim(0, 1); ax_flow.set_ylim(0, 1)

box(ax_flow, 0.16, 0.5, 0.28, 0.85,
    "STRUCTURAL SYSTEMS\n• Guadua Bamboo vs Steel Pipes\n• 3 Domes: 16 m, 32 m, 40 m Spans\n• 8 ASD Combinations (ASCE 7-22)",
    fc="#ebf8ff", ec="#3182ce", fs=7, text_col="#2b6cb0")

box(ax_flow, 0.50, 0.5, 0.28, 0.85,
    "DISCRETE OPTIMIZATION\n• Min Structural Mass (ASD Codes)\n• 3 Optimizers: ABC, ACO, DO\n• 30 Seeds (270 Bamboo + 120 Steel)",
    fc="#feebc8", ec="#dd6b20", fs=7, text_col="#c05621")

box(ax_flow, 0.84, 0.5, 0.28, 0.85,
    "POST-OPTIMIZATION LCA & COST\n• Cradle-to-Gate (A1–A3) Embodied CO₂\n• Hardware (Steel Hubs & Grout Infill)\n• 4 International Price Markets",
    fc="#e6fffa", ec="#319795", fs=7, text_col="#234e52")

arrow(ax_flow, (0.305, 0.5), (0.355, 0.5), col="#3182ce")
arrow(ax_flow, (0.645, 0.5), (0.695, 0.5), col="#dd6b20")

# Sol Alt: Karşılaştırmalı Çubuk Grafik
ax_bar = fig.add_axes([0.08, 0.12, 0.57, 0.46])
metrics = ["Member\nWeight", "System\nWeight", "Embodied\nCO₂", "Material\nCost"]
x = np.arange(4); w = 0.24
cols = ["#63b3ed", "#4c51bf", "#e53e3e"]

for k, (n, (sb, ss, mb, ms, co, cost)) in enumerate(bw.items()):
    vals = [mb / ms, sb / ss, co, cost]
    bars = ax_bar.bar(x + (k - 1) * w, vals, w, color=cols[k], edgecolor="#2d3748", lw=0.6, label=n)
    for xi, v in zip(x + (k - 1) * w, vals):
        offset = 0.05
        ax_bar.text(xi, v + offset, f"{v:.2f}", ha="center", va="bottom", fontsize=6.2, fontweight="bold", color="#1a202c")

ax_bar.axhline(1.0, color="#718096", lw=1.0, ls="--", zorder=1)
ax_bar.text(-0.35, 1.05, "Steel Parity (1.0)", fontsize=6.0, color="#4a5568", ha="left", fontweight="bold")
ax_bar.set_xticks(x)
ax_bar.set_xticklabels(metrics, fontsize=7.2, fontweight="bold")
ax_bar.set_ylim(0, 2.65)
ax_bar.set_ylabel("Bamboo / Steel Ratio [–]", fontsize=7.8, fontweight="bold")
ax_bar.legend(fontsize=6.5, frameon=True, facecolor="white", edgecolor="#cbd5e0", loc="upper left", ncol=3)
ax_bar.spines[["top", "right"]].set_visible(False)
ax_bar.grid(axis="y", ls=":", alpha=0.5)

# Sağ Alt: Temel Çıkarımlar Kartı (Key Highlights Card)
ax_info = fig.add_axes([0.68, 0.09, 0.30, 0.50])
ax_info.set_axis_off(); ax_info.set_xlim(0, 1); ax_info.set_ylim(0, 1)

info_patch = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03", fc="#f7fafc", ec="#cbd5e0", lw=1.2)
ax_info.add_patch(info_patch)

ax_info.text(0.08, 0.92, "Key Decarbonization Insights", fontsize=7.6, fontweight="bold", color="#2b6cb0")

bullet_text = (
    "• Member Efficiency:\n"
    "  Bamboo culms are 32–49% lighter\n"
    "  than equivalent structural steel pipes.\n\n"
    "• Connection Weight Penalty:\n"
    "  Injected grout infill makes bamboo\n"
    "  systems 1.36–2.15x heavier than steel.\n\n"
    "• Connection Carbon Paradox:\n"
    "  Steel hardware & grout carry 79–84%\n"
    "  of the bamboo domes' embodied CO2.\n\n"
    "• Net Decarbonization:\n"
    "  Bamboo domes achieve 51–68% lower\n"
    "  cradle-to-gate CO2 than steel domes."
)
ax_info.text(0.08, 0.78, bullet_text, fontsize=6.1, va="top", color="#2d3748", linespacing=1.18)

fig.text(0.08, 0.015, "Note: Ratios below the dashed 1.0 line favor bamboo. Cost evaluated under baseline Indonesian schedule (α = 2.0).",
         fontsize=5.8, color="#718096", style="italic")

fig.savefig(OUT / "graphical_abstract.png", dpi=300)
plt.close(fig)
print("Updated: graphical_abstract.png successfully generated with publication aesthetics.")
