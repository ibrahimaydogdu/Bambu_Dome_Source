"""
weight_carbon_tradeoff.py
Kampanyada ziyaret edilen UYGUN tasarimlar (penalty = 0) uzerinde agirlik - gomulu karbon iliskisi ve
optimum tasarimlarda belirleyici sinir durum dagilimi. Karbon, her degerlendirmenin geninden GUNCEL EC degerleriyle
(bamboo_catalog.py) yeniden hesaplanir; kayitli carbon_kg alani eski EC ile yazildigi icin kullanilmaz (ayrica
karsilastirma icin raporlanir).

Cikti: 04_Results/WEIGHT_CARBON_TRADEOFF.md
Kullanim: python weight_carbon_tradeoff.py [--campaign C:\\BambuDome_campaign\\full]

Yontem notu: degerlendirmeler tek amacli (agirlik) aramanin ziyaret ettigi noktalardir; rastgele ornek veya gercek
cok amacli Pareto cephesi DEGILDIR. "Cephe" burada yalniz ziyaret edilen uygun tasarimlarin baskin olmayan alt kumesidir.
"""
from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse
import glob
from pathlib import Path
import numpy as np
import results_report as rr
from bamboo_catalog import MATERIAL_PROPERTIES as MP

G = 9.81
NAME = {"geodesic16": "Geodesic", "kiewitt32": "Kiewitt", "ribbed40": "Ribbed"}


def group_tables(core):
    """Grup x kesit tablolari: culm kutlesi, baglanti celigi kutlesi, harc kutlesi [kg]."""
    ng, ns = core.G, len(core.A_sec)
    Wg, Sg, Mg = (np.zeros((ng, ns)) for _ in range(3))
    for g in range(ng):
        idx = np.flatnonzero(core.gidx == g)
        Lg = core.L[idx]
        for s in range(ns):
            Wg[g, s] = (MP["rho"] * core.A_sec[s] * Lg).sum()
            Sg[g, s] = 2.0 * core.steel_end[s] * len(idx)
            Mg[g, s] = 2.0 * core.mortar_end[s] * len(idx)
    return Wg, Sg, Mg


def analyse(model, campaign):
    _, _, core, _ = rr.bamboo_context(model)
    c = core.carbon
    Wg, Sg, Mg = group_tables(core)
    ar, base = np.arange(core.G), core.n_nodes * c.m_hub
    W, C, Cold = [], [], []
    for f in sorted(glob.glob(str(Path(campaign) / "results" / f"{model}__*.npz"))):
        z = np.load(f)
        ok = z["penalty"] == 0
        ge = z["genes"][ok].astype(int) - 1
        mb, ms, mm = Wg[ar, ge].sum(1), base + Sg[ar, ge].sum(1), Mg[ar, ge].sum(1)
        w = mb * G / 1000.0
        assert np.allclose(w, z["weight_kN"][ok], rtol=1e-9), f          # kayitli agirlikla tutarlilik
        W.append(w)
        C.append(c.ec_bamboo * mb + c.ec_steel * ms + c.ec_mortar * mm)
        Cold.append(z["carbon_kg"][ok])
    W, C, Cold = map(np.concatenate, (W, C, Cold))
    r, ro = np.corrcoef(W, C)[0, 1], np.corrcoef(W, Cold)[0, 1]
    key = np.unique(np.round(np.stack([W, C], 1), 9), axis=0)
    k = key[np.lexsort((key[:, 1], key[:, 0]))]
    cm = np.minimum.accumulate(k[:, 1])
    nd = np.r_[True, k[1:, 1] < cm[:-1] - 1e-9]
    iw, ic = k[:, 0].argmin(), k[:, 1].argmin()
    return dict(n_eval=len(W), n_unique=len(k), n_front=int(nd.sum()), r=r, R2=r * r, r_old=ro, R2_old=ro * ro,
                W_minW=k[iw, 0], C_minW=k[iw, 1], W_minC=k[ic, 0], C_minC=k[ic, 1],
                dC=100 * (k[iw, 1] - k[ic, 1]) / k[ic, 1], dW=100 * (k[ic, 0] - k[iw, 0]) / k[iw, 0])


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
    L = ["# Agirlik - gomulu karbon iliskisi ve belirleyici sinir durumlar (hesaplanan)", "",
         "Betik: `03_Code_Execution/weight_carbon_tradeoff.py`. Veri: kampanyada ziyaret edilen UYGUN degerlendirmeler (`penalty = 0`), her biri icin gen -> kutle -> karbon "
         "GUNCEL EC degerleriyle yeniden hesaplandi (EC_b = 0.30, EC_s = 2.38, EC_m = 0.18; hub 2.0 kg/dugum, 0.5 kg/cubuk ucu, L_inj = 2.5 D). "
         "Kayitli `carbon_kg` eski EC ile yazildigi icin yalniz karsilastirma sutununda verilmistir. Degerlendirmeler tek amacli (agirlik) aramanin ziyaret ettigi noktalardir; "
         "rastgele ornek ya da cok amacli aramanin cephesi degildir.", "",
         "## 1. Korelasyon ve baskin olmayan nokta kumesi", "",
         "| Dome | Uygun degerlendirme | Tekil (W, C) cifti | r (guncel EC) | R2 (guncel EC) | r (kayitli, eski EC) | R2 (kayitli, eski EC) | Baskin olmayan nokta | "
         "En dusuk W: W [kN] | C [kg CO2e] | En dusuk C: W [kN] | C [kg CO2e] | C farki (minW vs minC) [%] | W farki (minC vs minW) [%] |", "|" + "---|" * 14]
    for m in rr.MODELS:
        d = analyse(m, a.campaign)
        L.append(f"| {NAME[m]} | {d['n_eval']} | {d['n_unique']} | {d['r']:.3f} | {d['R2']:.3f} | {d['r_old']:.3f} | {d['R2_old']:.3f} | {d['n_front']} | "
                 f"{d['W_minW']:.3f} | {d['C_minW']:.1f} | {d['W_minC']:.3f} | {d['C_minC']:.1f} | {d['dC']:.2f} | {d['dW']:.2f} |")
    L += ["", "## 2. Optimum tasarimlarda belirleyici sinir durum (grup sayisi)", "",
          "Her grupta en buyuk D/C degerini veren kontrol sayilir. `Ortalama`: 90 uygun kosunun ortalamasi.", "",
          "| Dome | Tasarim | Cekme | Basinc | Narinlik | Baglanti | Toplam grup |", "|---|---|---|---|---|---|---|"]
    for m in rr.MODELS:
        lb, agg, n = governing(m, res)
        g = lb["gov_groups"]
        L.append(f"| {NAME[m]} | en iyi | {g['tension']} | {g['compression']} | {g['slenderness']} | {g['joint']} | {lb['n_groups']} |")
        L.append(f"| {NAME[m]} | ortalama ({n} kosu) [%] | {100*agg['tension']:.1f} | {100*agg['compression']:.1f} | {100*agg['slenderness']:.1f} | {100*agg['joint']:.1f} | 100 |")
    out = Path(__file__).parent.parent / "04_Results" / "WEIGHT_CARBON_TRADEOFF.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("yazildi:", out)


if __name__ == "__main__":
    main()
