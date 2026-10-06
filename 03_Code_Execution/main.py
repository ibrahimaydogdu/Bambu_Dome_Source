"""
main.py
Bambu Geodezik Kubbe -- Cok Amacli Optimizasyon Ana Sureci
==========================================================
Calisma Akisi:
  1. SAP2000 Bridge ac, malzeme + kesit tanimla
  2. Grup ve uzunlukları oku
  3. Yuk kombinasyonlarini oku
  4. NSGA-II / MOABC / MODBO algoritmalarini sirayla calistir
  5. Her algoritmanin Pareto arsivini kaydet
  6. Karsilastirmali Pareto cephesi ve metrik raporunu yaz

Kullanim:
  python main.py [--algo nsga2|moabc|modbo|all] [--pop 40] [--gen 100]
                 [--hidden] [--smoke-test]
"""

from __future__ import annotations
import argparse
import csv
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Proje modulleri ----
sys.path.insert(0, str(Path(__file__).parent))
from bamboo_catalog import BAMBOO_CATALOG
from sap2000_bridge import SAP2000Bridge
from iso22156_checks import evaluate_all_members
from carbon_calculator import compute_embodied_carbon, compute_structural_weight
from checkpoint_manager import CheckpointManager
from multi_objective_optimizer import (
    FitnessEvaluator, NSGA2, MOABC, MODBO,
    non_dominated_sort_front0, crowding_distance,
    dominates,
)

# ---------------------------------------------------------------------------
# Konfigurasyon
# ---------------------------------------------------------------------------
BASE_DIR   = Path(__file__).parent
SDB_PATH   = BASE_DIR / "BBO_API" / "354Memberdome" / "alara3v16.sdb"
OUTPUT_DIR = BASE_DIR / "results"
CKPT_DIR   = BASE_DIR / "checkpoints"

SPAN_M     = 24.384   # Referans aciklik [m] -- literatur 354-eleman kubbesi
N_NODES    = 127      # 354-eleman geodezik kubbe dugum sayisi (yaklasik)


# ---------------------------------------------------------------------------
# Loglama
# ---------------------------------------------------------------------------
def setup_logging(level: str = "INFO") -> None:
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"run_{ts}.log"

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(str(log_file), encoding="utf-8"),
        ],
    )
    logging.info("Log dosyasi: %s", log_file)


# ---------------------------------------------------------------------------
# Sonuc kayit
# ---------------------------------------------------------------------------
def save_pareto(
    archive_sol: list,
    archive_obj: list,
    algo_name: str,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV
    csv_path = output_dir / f"pareto_{algo_name}_{ts}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["f1_weight_kN", "f2_carbon_kgCO2e"] +
                   [f"g{i+1}" for i in range(len(archive_sol[0]) if archive_sol else 1)])
        for sol, obj in zip(archive_sol, archive_obj):
            w.writerow([obj[0], obj[1]] + [int(round(g)) for g in sol])
    logging.info("Pareto CSV kaydedildi: %s", csv_path)

    # JSON
    json_path = output_dir / f"pareto_{algo_name}_{ts}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {"algorithm": algo_name, "timestamp": ts,
             "objectives": archive_obj,
             "solutions": [list(map(float, s)) for s in archive_sol]},
            f, indent=2, ensure_ascii=False
        )
    logging.info("Pareto JSON kaydedildi: %s", json_path)


def compute_hypervolume_approx(
    obj_list: list,
    ref_point: tuple = (1e7, 1e7),
) -> float:
    """Monte Carlo hipervolum tahmini (2B, ~5000 orneklem)."""
    if not obj_list:
        return 0.0
    n_samples = 5000
    obj_arr = np.array(obj_list)
    lo = obj_arr.min(axis=0)
    hi = np.array(ref_point)
    pts = np.random.uniform(lo, hi, (n_samples, 2))
    dominated = np.zeros(n_samples, dtype=bool)
    for o in obj_arr:
        dominated |= np.all(pts >= o, axis=1)
    vol = np.prod(hi - lo) * dominated.mean()
    return float(vol)


def plot_pareto(results: dict, output_dir: Path) -> None:
    """Tum algoritmalarin Pareto cephelerini tek grafikte cizer."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = {"nsga2": "#1f77b4", "moabc": "#ff7f0e", "modbo": "#2ca02c"}
    markers = {"nsga2": "o", "moabc": "s", "modbo": "^"}

    for algo, (sols, objs) in results.items():
        if not objs:
            continue
        obj_arr = np.array(objs)
        front_idx = non_dominated_sort_front0(obj_arr)
        front_obj = obj_arr[front_idx]
        sorted_idx = np.argsort(front_obj[:, 0])
        ax.plot(
            front_obj[sorted_idx, 0], front_obj[sorted_idx, 1],
            marker=markers.get(algo, "o"),
            color=colors.get(algo, "gray"),
            label=algo.upper(),
            linewidth=1.5,
            markersize=6,
        )

    ax.set_xlabel("f₁: Yapisal Agirlik [kN]", fontsize=13)
    ax.set_ylabel("f₂: Gomulu Karbon [kg CO₂e]", fontsize=13)
    ax.set_title("354-Eleman Bambu Geodezik Kubbe -- Pareto Cephesi Karsilastirmasi", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = output_dir / f"pareto_comparison_{ts}.png"
    plt.savefig(str(fig_path), dpi=200)
    plt.close()
    logging.info("Pareto grafigi kaydedildi: %s", fig_path)


# ---------------------------------------------------------------------------
# Smoke Test (Duman Testi)
# ---------------------------------------------------------------------------

def smoke_test(bridge: SAP2000Bridge) -> None:
    """
    1 birey, 1 analiz. SAP2000 baglantisini ve temel okuma fonksiyonlarini test eder.
    """
    logging.info("=" * 60)
    logging.info("DUMAN TESTI BASLADI")

    bridge.define_bamboo_material()
    bridge.define_bamboo_sections(BAMBOO_CATALOG)
    groups, lengths = bridge.read_groups_and_lengths()
    combos = bridge.read_load_combos()

    logging.info("Grup sayisi  : %d", len(groups))
    logging.info("Eleman sayisi: %d", len(lengths))
    logging.info("Yuk durumu   : %d", len(combos))

    # Minimum kesitli birey
    n_groups = len(groups)
    test_gene = [1] * n_groups  # En kucuk kesit (ID=1)
    bridge.update_sections(test_gene, BAMBOO_CATALOG)
    axial, disp = bridge.run_analysis_and_read()

    logging.info("Eksenel kuvvet ornegi (ilk 3 eleman):")
    for k, (mem, P) in enumerate(list(axial.items())[:3]):
        logging.info("  Eleman %-6s  P = %+.3f kN", mem, P)

    max_disp = max(
        (abs(u1**2 + u2**2 + u3**2)**0.5 for u1, u2, u3 in disp.values()),
        default=0.0
    )
    logging.info("Maks. yer degistirme: %.6f m", max_disp)

    pen, max_dc, check_results = evaluate_all_members(
        axial, lengths,
        {m: g for m, g in zip(lengths.keys(), ["1"] * len(lengths))},
        test_gene, BAMBOO_CATALOG, disp, span_m=SPAN_M
    )
    logging.info("ISO 22156 Ceza  : %.4f", pen)
    logging.info("Maks. D/C orani : %.4f", max_dc)

    f1 = compute_structural_weight(
        test_gene, BAMBOO_CATALOG, lengths,
        {m: g for m, g in zip(lengths.keys(), ["1"] * len(lengths))}
    )
    total_ec, _, _ = compute_embodied_carbon(
        test_gene, BAMBOO_CATALOG, lengths,
        {m: g for m, g in zip(lengths.keys(), ["1"] * len(lengths))},
        N_NODES
    )
    logging.info("f1 = %.3f kN   f2 = %.3f kg CO2e", f1, total_ec)
    logging.info("DUMAN TESTI TAMAMLANDI -- Baglanti ve okuma fonksiyonlari calisıyor.")
    logging.info("=" * 60)


# ---------------------------------------------------------------------------
# Ana Giris Noktasi
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bambu Geodezik Kubbe -- Cok Amacli Optimizasyon"
    )
    parser.add_argument(
        "--algo", default="all",
        choices=["nsga2", "moabc", "modbo", "all"],
        help="Calistirilacak algoritma"
    )
    parser.add_argument("--pop",  type=int, default=40,  help="Populasyon / Kovan buyuklugu")
    parser.add_argument("--gen",  type=int, default=100, help="Nesil / Dongu sayisi")
    parser.add_argument("--hidden", action="store_true", default=True,
                        help="SAP2000'i gizli calistir")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Sadece duman testi yap")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING"])
    args = parser.parse_args()

    setup_logging(args.log_level)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CKPT_DIR.mkdir(parents=True, exist_ok=True)

    logging.info("SAP2000 model dosyasi: %s", SDB_PATH)
    if not SDB_PATH.exists():
        logging.error("Model dosyasi bulunamadi: %s", SDB_PATH)
        sys.exit(1)

    # SAP2000 Bridge baslatma
    bridge = SAP2000Bridge(
        sdb_path=SDB_PATH,
        hidden=args.hidden,
        restart_every=100,
    )
    bridge.open()

    try:
        if args.smoke_test:
            smoke_test(bridge)
            return

        bridge.define_bamboo_material()
        bridge.define_bamboo_sections(BAMBOO_CATALOG)
        groups, lengths = bridge.read_groups_and_lengths()
        combos = bridge.read_load_combos()

        n_groups  = len(groups)
        n_sections = len(BAMBOO_CATALOG)
        logging.info("n_groups=%d  n_sections=%d  n_combos=%d",
                     n_groups, n_sections, len(combos))

        evaluator = FitnessEvaluator(
            bridge=bridge,
            member_lengths=lengths,
            member_group=bridge._member_group,
            n_nodes=N_NODES,
            span_m=SPAN_M,
        )

        algos_to_run = (
            ["nsga2", "moabc", "modbo"] if args.algo == "all" else [args.algo]
        )
        results: dict[str, tuple[list, list]] = {}

        for algo in algos_to_run:
            logging.info("=" * 60)
            logging.info("Algoritma basliyor: %s", algo.upper())
            t0 = time.time()

            if algo == "nsga2":
                opt = NSGA2(
                    evaluator=evaluator,
                    n_groups=n_groups,
                    n_sections=n_sections,
                    pop_size=args.pop,
                    n_gen=args.gen,
                    checkpoint_path=str(CKPT_DIR / "nsga2.json"),
                )
                sols, objs = opt.run(bridge)
            elif algo == "moabc":
                opt = MOABC(
                    evaluator=evaluator,
                    n_groups=n_groups,
                    n_sections=n_sections,
                    colony_size=args.pop,
                    n_cycles=args.gen,
                    checkpoint_path=str(CKPT_DIR / "moabc.json"),
                )
                sols, objs = opt.run(bridge)
            elif algo == "modbo":
                opt = MODBO(
                    evaluator=evaluator,
                    n_groups=n_groups,
                    n_sections=n_sections,
                    pop_size=args.pop,
                    n_gen=args.gen,
                    checkpoint_path=str(CKPT_DIR / "modbo.json"),
                )
                sols, objs = opt.run(bridge)
            else:
                continue

            elapsed = time.time() - t0
            hv = compute_hypervolume_approx(objs)
            logging.info(
                "%s tamamlandi: Pareto=%d cozum  HV~=%.4e  Sure=%.1f s",
                algo.upper(), len(objs), hv, elapsed,
            )
            results[algo] = (sols, objs)
            save_pareto(sols, objs, algo, OUTPUT_DIR)

        if results:
            plot_pareto(results, OUTPUT_DIR)

            # Ozet metrikleri EXECUTION_LOG.md'ye ekle
            log_md = BASE_DIR / "EXECUTION_LOG.md"
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_md, "a", encoding="utf-8") as f:
                f.write(f"\n## Run @ {ts}\n")
                f.write(f"| Algoritma | Pareto N | HV (approx) |\n")
                f.write(f"|-----------|----------|-------------|\n")
                for algo, (sols, objs) in results.items():
                    hv = compute_hypervolume_approx(objs)
                    f.write(f"| {algo.upper()} | {len(objs)} | {hv:.4e} |\n")
            logging.info("EXECUTION_LOG.md guncellendi.")

    finally:
        bridge.close()


if __name__ == "__main__":
    main()
