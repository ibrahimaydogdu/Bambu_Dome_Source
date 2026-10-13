"""En iyi bambu tasarimlarinin 3B, plan ve yan gorunumleri.
Cikti: 15 cm genislik, alt alta 3 gorunus, yazi 9 pt; renk ve kalinlik = en iyi cozumdeki dis cap."""
import json, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from run_full_campaign import build_model
from bamboo_catalog import BAMBOO_CATALOG

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(ROOT, "../04_Results/figures/domes"))
os.makedirs(OUT, exist_ok=True)
DATA_DIR = os.path.abspath(os.path.join(ROOT, "../04_Results/campaign_final"))
CM = 1 / 2.54
plt.rcParams.update({"font.family": "serif", "font.size": 9})
TITLE = {"geodesic16": "(a) Geodesic (span 16 m)", "kiewitt32": "(b) Kiewitt (span 32 m)", "ribbed40": "(c) Ribbed (span 40 m)"}
for n in TITLE:
    d = json.load(open(os.path.join(DATA_DIR, f"global_best_{n}.json")))
    m = build_model(n)
    Dmm = np.zeros(len(m.fi))
    for gi, mem in enumerate(m.group_members):
        Dmm[mem] = BAMBOO_CATALOG.iloc[d["gene"][gi]]["D_m"] * 1000
    P = m.xyz; seg = np.stack([P[m.fi], P[m.fj]], axis=1)
    norm = plt.Normalize(Dmm.min(), Dmm.max()); cmap = LinearSegmentedColormap.from_list("br", ["#1f3fbf", "#7a3fa0", "#d7191c"])
    col = cmap(norm(Dmm)); lw = 0.4 + 1.0 * (Dmm - Dmm.min()) / max(Dmm.max() - Dmm.min(), 1)
    R = np.abs(P[:, :2]).max(); zm = P[:, 2].max()
    fig = plt.figure(figsize=(15 * CM, 20 * CM))
    gs = fig.add_gridspec(4, 1, height_ratios=[5.6, 6.2, 2.8, 0.5], hspace=0.5, left=0.13, right=0.97, top=0.96, bottom=0.075)
    ax = fig.add_subplot(gs[0], projection="3d")
    ax.add_collection3d(Line3DCollection(seg, colors=col, linewidths=lw))
    ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_zlim(0, zm)
    ax.set_box_aspect((2 * R, 2 * R, zm), zoom=1.3); ax.view_init(28, -55)
    ax.set_xlabel("x [m]", labelpad=-4); ax.set_ylabel("y [m]", labelpad=-4); ax.set_zticks([])
    ax.tick_params(pad=-3)
    ax.set_title(f"{TITLE[n]}: (i) 3D view", fontsize=9, pad=-8)
    for k, (a, b, t) in enumerate([(0, 1, "(ii) Plan view"), (0, 2, "(iii) Side view")], start=1):
        ax2 = fig.add_subplot(gs[k])
        ax2.add_collection(LineCollection(seg[:, :, [a, b]], colors=col, linewidths=lw))
        ax2.set_xlim(P[:, a].min() - 1, P[:, a].max() + 1); ax2.set_ylim(P[:, b].min() - 1, P[:, b].max() + 1)
        ax2.set_aspect("equal"); ax2.set_title(t, fontsize=9)
        ax2.set_xlabel("xyz"[a] + " [m]"); ax2.set_ylabel("xyz"[b] + " [m]")
    cax = fig.add_subplot(gs[3])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal")
    cb.set_label("Culm outer diameter of the best design, D [mm]")
    fig.savefig(f"{OUT}/{n}_views.png", dpi=300); plt.close(fig)
    print(n, len(m.fi), "members", Dmm.min(), Dmm.max())
