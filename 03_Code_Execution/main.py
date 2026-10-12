"""
main.py
Bambu Geodezik Kubbe -- Tek Amacli Meta-Sezgisel Optimizasyon Ana Sureci (16 Yontem)
===================================================================================
Calisma Akisi:
  1. Kubbe modelini yukle (geodesic16, kiewitt32, ribbed40)
  2. FastCore dogrudan rijitlik ve ISO 22156 tahkik cekirdegi kur
  3. Secilen algoritma(lar)i calistir (16 meta-sezgisel yontem)
  4. En iyi cozum, agirlik [kN], gomulu karbon [kg CO2e] ve yakinsama gecmisini kaydet

Kullanim:
  python main.py [--algo hs|bbo|woa|do|abc|aco|bso|csa|fa|goa|tlbo|tsa|gwo|hba|ao|sso|all]
                 [--model geodesic16|kiewitt32|ribbed40]
                 [--pop 40] [--gen 100] [--seed 1001]
"""

from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import csv
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

# ---- Proje modulleri ----
sys.path.insert(0, str(Path(__file__).parent))
from bamboo_catalog import BAMBOO_CATALOG
from fem_bridge import FEMBridge
from fast_eval import FastCore, CarbonModel
from metaheuristic_optimizers import MetaheuristicOptimizer, ALGORITHM_NAMES

BASE_DIR   = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "results"
SPAN_M     = 40.0


def setup_logging(level: str = "INFO") -> None:
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"run_{ts}.log"

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(str(log_file), encoding="utf-8"),
        ],
    )


def build_dome_bridge(model_name: str, freq: int = 2):
    if model_name in ("dome", "ribbed40"):
        from truss_model import build_dome_model
        model = build_dome_model(freq, SPAN_M)
    elif model_name in ("geodesic16", "kiewitt32"):
        from dome_types import build_preset
        model = build_preset(model_name)
    else:
        raise ValueError(f"Bilinmeyen model: {model_name}")
    bridge = FEMBridge(model)
    bridge.open()
    return bridge, model


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bambu Geodezik Kubbe -- Tek Amacli Meta-Sezgisel Optimizasyon (16 Algoritma)"
    )
    parser.add_argument(
        "--algo", default="abc",
        choices=list(ALGORITHM_NAMES.keys()) + ["all"],
        help="Calistirilacak optimizasyon algoritmasi (varsayilan: abc)"
    )
    parser.add_argument("--model", default="geodesic16",
                        choices=["geodesic16", "kiewitt32", "ribbed40", "dome"],
                        help="Kubbe modeli (varsayilan: geodesic16)")
    parser.add_argument("--pop",  type=int, default=40,  help="Populasyon / Hafiza boyutu")
    parser.add_argument("--gen",  type=int, default=100, help="Iterasyon sayisi")
    parser.add_argument("--freq", type=int, default=2,   help="ribbed40/dome halka sikligi")
    parser.add_argument("--penalty-exp", type=float, default=2.0, help="Carpimsal ceza ussu (default: 2.0)")
    parser.add_argument("--carbon-model", default="section", choices=["section", "fixed"],
                        help="Karbon modeli (default: section)")
    parser.add_argument("--run-id", type=int, default=0, help="Kosu ID")
    parser.add_argument("--seed", type=int, default=1001, help="Rastgele tohum")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING"])
    args = parser.parse_args()

    setup_logging(args.log_level)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    bridge, model = build_dome_bridge(args.model, args.freq)
    groups, lengths = bridge.read_groups_and_lengths()
    n_groups = len(groups)
    logging.info("Model: %s | Eleman sayisi: %d | Grup sayisi: %d | Aciklik: %.1f m",
                 args.model, len(lengths), n_groups, model.span_m)

    core = FastCore(
        bridge=bridge,
        catalog=BAMBOO_CATALOG,
        span_m=model.span_m,
        disp_limit_m=model.disp_limit_m,
        carbon=CarbonModel(mode=args.carbon_model),
        slenderness="all",
        envelope=True,
    )

    algos_to_run = list(ALGORITHM_NAMES.keys()) if args.algo == "all" else [args.algo]
    results_summary = []

    for algo in algos_to_run:
        logging.info("=" * 60)
        logging.info("Algoritma basliyor: %s (%s)", algo.upper(), ALGORITHM_NAMES[algo])
        t0 = time.time()

        opt = MetaheuristicOptimizer(
            eval_fn=core.evaluate,
            n_vars=n_groups,
            lb=1,
            ub=len(BAMBOO_CATALOG),
            pop_size=args.pop,
            max_iters=args.gen,
            penalty_exp=args.penalty_exp,
            seed=args.seed,
            method=algo,
        )

        best_member, history = opt.optimize()
        elapsed = time.time() - t0

        logging.info("%s Tamamlandi! Sure: %.2f s | Evals: %d",
                     algo.upper(), elapsed, opt.n_evals)
        logging.info("  En Iyi Cezali Agirlik: %.3f kN", best_member.penalized_cost)
        logging.info("  Yapisal Bambu Agirligi: %.3f kN", best_member.cost_value)
        logging.info("  Gomulu Karbon: %.3f kg CO2e", best_member.carbon_value)
        logging.info("  Kisit Ihlali P: %.4f (Feasible=%s)",
                     best_member.penalty, best_member.is_feasible)

        # Sonuc kayit
        out_rec = {
            "model": args.model,
            "algorithm": algo,
            "algorithm_name": ALGORITHM_NAMES[algo],
            "seed": args.seed,
            "pop_size": args.pop,
            "max_iters": args.gen,
            "elapsed_s": elapsed,
            "evals": opt.n_evals,
            "best_penalized_weight_kN": best_member.penalized_cost,
            "best_structural_weight_kN": best_member.cost_value,
            "best_embodied_carbon_kgCO2e": best_member.carbon_value,
            "penalty": best_member.penalty,
            "is_feasible": best_member.is_feasible,
            "best_sections": best_member.design_variables.tolist(),
            "history": history,
        }
        results_summary.append(out_rec)

        out_path = OUTPUT_DIR / f"{args.model}_{algo}_s{args.seed}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out_rec, f, indent=2, ensure_ascii=False)
        logging.info("Sonuc kaydedildi: %s", out_path)

    bridge.close()
    logging.info("Tum calismalar tamamlandi.")


if __name__ == "__main__":
    main()
