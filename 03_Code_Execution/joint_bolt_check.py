"""
joint_bolt_check.py
En iyi bambu tasarimlarinda her eleman icin NSR-10 (Tabla G.12.11-2/3, G.12.11.3.13) ile gereken civata sayisi ve
bu civatalarin sigmasi icin gereken minimum eleman boyu. Kisa elemanlar icin baglanti detayi sinirlamasini belirler.

Kurallar (NSR-10, Titulo G, Cap. G.12): #5 (5/8") civata, cift kesme, lif dogrultusu izinli yuk P(D) (Tabla G.12.11-2, s.138);
grup katsayisi C_g (Tabla G.12.11-3, s.139); civata araligi >= 150 mm, uc mesafe >= 150 mm (cekme) / 100 mm (basinc) (G.12.11.3.13, s.139).
Gereken boy: L >= 2*(e + (n-1)*150) + 150 mm (iki ucun civata bolgeleri ust uste binmez, ic civatalar arasi >= 150 mm).
Kullanim: python joint_bolt_check.py
"""
import json, glob
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).parent.parent / "04_Results" / "tables"
DTAB = np.array([80, 90, 100, 110, 115, 120, 125, 130, 135, 140, 150.])
PTAB = np.array([11.540, 12.806, 13.250, 14.515, 15.185, 15.855, 16.525, 17.195, 17.865, 18.535, 19.800])   # kN, #5 civata
CG = {1: 1.0, 2: 1.0, 3: 0.97, 4: 0.93, 5: 0.89, 6: 0.82}


def main():
    from run_full_campaign import build_model
    from fem_bridge import FEMBridge
    from fast_eval import FastCore
    from bamboo_catalog import BAMBOO_CATALOG as C
    rows = []
    for m in ("geodesic16", "kiewitt32", "ribbed40"):
        mod = build_model(m); b = FEMBridge(mod); b.open(); b.read_groups_and_lengths()
        core = FastCore(b, C, mod.span_m, mod.disp_limit_m)
        best = min([json.load(open(f)) for f in glob.glob(f"C:/BambuDome_campaign/full/results/{m}__*.json")],
                   key=lambda r: (not r["is_feasible"], r["best_structural_weight_kN"]))
        gene = np.array(best["solution"]); core.evaluate(gene)
        N, _ = b.analyze_arrays(); Nmax = np.abs(N).max(axis=1)
        sec = gene[core.gidx] - 1
        D = C["D_m"].to_numpy(float)[sec] * 1000
        P = np.interp(D, DTAB, PTAB)
        tens = N.max(axis=1) >= -N.min(axis=1)
        L = core.L * 1000
        nreq = np.full(len(L), 7)
        for i in range(len(L)):
            for n in range(1, 7):
                if n * P[i] * CG[n] >= Nmax[i]:
                    nreq[i] = n; break
        edge = np.where(tens, 150, 100)
        need = np.array([2 * (edge[i] + (min(nreq[i], 6) - 1) * 150) + 150 for i in range(len(L))])
        short = (L < need) | (nreq == 7)
        rows.append({"Dome": m, "Members": len(L), **{f"n_req={k}": int((nreq == k).sum()) for k in range(1, 5)},
                     "n_req>4": int((nreq > 4).sum()), "Members too short for required bolts": int(short.sum()),
                     "Share [%]": 100 * short.mean(), "Shortest member [m]": L.min() / 1000,
                     "Max force in too-short members [kN]": float(Nmax[short].max()) if short.any() else 0.0,
                     "Members < 1.35 m (4 bolts both ends)": int((L < 1350).sum())})
    t = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    t.to_csv(OUT / "T10_joint_bolt_requirement.csv", index=False)
    import results_report as rr
    (OUT / "T10_joint_bolt_requirement.md").write_text(
        "### Table 10. Bolts required per member end (NSR-10 allowable load, #5 bolt) and members too short to host them\n\n"
        + rr.md_table(t, "{:.2f}") + "\n", encoding="utf-8")
    print(t.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
