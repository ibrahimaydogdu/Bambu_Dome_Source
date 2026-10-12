"""
validate_sap.py -- parametrik kubbe modelini SAP2000'e yazar, SAP2000'de analiz eder
ve FEM cozucusu + ISO 22156 tahkikleriyle karsilastirir.
Kullanim: python validate_sap.py [model|freq] [rastgele_birey=2] [seed=0]
  model: ribbed40 | geodesic16 | kiewitt32 ; sayi verilirse ribbed kubbe freq'i (1 = 354 eleman)
"""
from fem_bridge import FEMBridge  # numpy'dan once BLAS ipligini sabitler
import sys, time, logging
import numpy as np
from pathlib import Path
from bamboo_catalog import BAMBOO_CATALOG
from truss_model import build_dome_model
from sap_export import verify_with_sap
from dome_types import build_preset, geometry_report

WORK = Path(r"C:\BambuDome_work\verify")


def main(which="2", n_rand=2, seed=0):
    logging.basicConfig(level=logging.WARNING)
    model = build_dome_model(int(which)) if str(which).isdigit() else build_preset(which)
    freq = which
    G = len(model.group_names)
    rng = np.random.default_rng(seed)
    genes = {"hepsi-1": [1] * G, "hepsi-24": [24] * G}
    for i in range(n_rand):
        genes[f"rastgele-{i + 1}"] = rng.integers(1, 25, G).tolist()
    print(f"{freq}: {len(model.joint_names)} dugum, {len(model.frame_names)} cubuk, {G} grup, "
          f"aciklik {model.span_m} m, yer degistirme siniri {model.disp_limit_m * 100:.1f} cm")
    worst = [0.0, 0.0, 0.0]
    for name, g in genes.items():
        t = time.time()
        r = verify_with_sap(model, g, BAMBOO_CATALOG, WORK, tag=f"v_{name}",
                            span_m=model.span_m, disp_limit_m=model.disp_limit_m)
        dd = abs(r["dc_fem"] - r["dc_sap"]) / max(r["dc_sap"], 1e-12)
        worst = [max(worst[0], r["err_axial"]), max(worst[1], r["err_disp"]), max(worst[2], dd)]
        print(f"  {name:11s} maxN={r['max_axial_kN']:8.2f} kN | hata: eksenel {r['err_axial']:.1e}  "
              f"yer degistirme {r['err_disp']:.1e} | maxD/C FEM {r['dc_fem']:.4f} SAP {r['dc_sap']:.4f} "
              f"| ceza FEM {r['pen_fem']:.4f} SAP {r['pen_sap']:.4f} | {time.time() - t:.0f} s")
    print(f"EN KOTU: eksenel {worst[0]:.2e}  yer degistirme {worst[1]:.2e}  D/C bagil {worst[2]:.2e}")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else "2", int(a[1]) if len(a) > 1 else 2, int(a[2]) if len(a) > 2 else 0)
