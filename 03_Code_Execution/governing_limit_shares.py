"""
governing_limit_shares.py
Optimum tasarimlarda her tasarim grubunda en buyuk D/C degerini hangi kontrolun (cekme, basinc, narinlik, baglanti) verdigini sayar.
Girdi: kampanya sonuclari (results/*.json). Cikti: 04_Results/GOVERNING_LIMIT_SHARES.md
Kullanim: python governing_limit_shares.py [--campaign C:\\BambuDome_campaign\\full]
"""
from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse
from pathlib import Path
import results_report as rr

NAME = {"geodesic16": "Geodesic", "kiewitt32": "Kiewitt", "ribbed40": "Ribbed"}


def governing(model, res):
    _, _, core, _ = rr.bamboo_context(model)
    feas = [r for r in res if r["model"] == model and r["is_feasible"]]
    best = min(feas, key=lambda r: r["best_structural_weight_kN"])
    lb = rr.limit_breakdown(core, best["solution"])
    agg = {k: 0.0 for k in lb["gov_groups"]}
    for r in feas:
        x = rr.limit_breakdown(core, r["solution"])
        for k in agg:
            agg[k] += x["gov_groups"][k] / x["n_groups"] / len(feas)
    return lb, agg, len(feas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", default=r"C:\BambuDome_campaign\full")
    a = ap.parse_args()
    res = rr.load_results(Path(a.campaign))
    L = ["# Optimum tasarimlarda belirleyici sinir durum (grup sayisi)", "",
         "Betik: `03_Code_Execution/governing_limit_shares.py`. Her grupta en buyuk D/C degerini veren kontrol sayilir. "
         "`Ortalama`: dome basina 90 uygun kosunun ortalamasi.", "",
         "| Dome | Tasarim | Cekme | Basinc | Narinlik | Baglanti | Toplam grup |", "|---|---|---|---|---|---|---|"]
    for m in rr.MODELS:
        lb, agg, n = governing(m, res)
        g = lb["gov_groups"]
        L.append(f"| {NAME[m]} | en iyi | {g['tension']} | {g['compression']} | {g['slenderness']} | {g['joint']} | {lb['n_groups']} |")
        L.append(f"| {NAME[m]} | ortalama ({n} kosu) [%] | {100*agg['tension']:.1f} | {100*agg['compression']:.1f} | {100*agg['slenderness']:.1f} | {100*agg['joint']:.1f} | 100 |")
    out = Path(__file__).parent.parent / "04_Results" / "GOVERNING_LIMIT_SHARES.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("yazildi:", out)


if __name__ == "__main__":
    main()
