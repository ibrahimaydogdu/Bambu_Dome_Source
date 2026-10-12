"""
tuning_study.py
Algoritma secimi ve populasyon duyarliligi calismasi (nihai kampanyadan AYRI tohumlar: 2001-2005).

  python tuning_study.py run     [--models kiewitt32 geodesic16] [--algos ...] [--pops 20 40 80] [--seeds 5]
  python tuning_study.py summary [--out ../04_Results/TUNING_STUDY.md]

Her kosu: NFE = nfe_per_var x tasarim degiskeni sayisi (nihai kampanyadaki butceyle ayni).
Sonuclar C:\\BambuDome_campaign\\tuning\\<model>__<algo>__p<pop>__s<seed>.json; mevcut olanlar atlanir (devam edilebilir).
"""
from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\BambuDome_campaign\tuning")
SEED_BASE = 2000
N_GROUPS = {"ribbed40": 43, "kiewitt32": 22, "geodesic16": 23}
DEFAULT_ALGOS = ["abc", "aco", "gwo", "do", "woa", "tlbo", "hba", "ao"]


def run_one(job: dict) -> dict:
    import random
    import numpy as np
    from run_full_campaign import build_model
    from fem_bridge import FEMBridge
    from fast_eval import FastCore, CarbonModel
    from bamboo_catalog import BAMBOO_CATALOG
    from metaheuristic_optimizers import MetaheuristicOptimizer
    import logging
    logging.getLogger().setLevel(logging.WARNING)

    model = build_model(job["model"])
    bridge = FEMBridge(model); bridge.open()
    groups, _ = bridge.read_groups_and_lengths()
    core = FastCore(bridge, BAMBOO_CATALOG, model.span_m, model.disp_limit_m, CarbonModel(), "all", True)
    budget = job["nfe_per_var"] * len(groups)
    t0 = time.time()
    opt = MetaheuristicOptimizer(core.evaluate, len(groups), 1, len(BAMBOO_CATALOG), job["pop"], 10 ** 9,
                                 2.0, job["seed"], job["algo"], max_evals=budget)
    best, hist = opt.optimize()
    res = dict(job, n_groups=len(groups), nfe=opt.n_evals, elapsed_s=time.time() - t0,
               best_weight_kN=best.cost_value, penalty=best.penalty, is_feasible=best.is_feasible,
               best_penalized_kN=best.penalized_cost,
               history=[(h["evals"], h["best_penalized"]) for h in hist[:: max(1, len(hist) // 100)]])
    (ROOT / f"{job['id']}.json").write_text(json.dumps(res), encoding="utf-8")
    return dict(id=job["id"], w=best.cost_value, feas=best.is_feasible, t=res["elapsed_s"])


def cmd_run(a) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for model in a.models:                       # pahali model sona: kisa isler once biter
        for algo in a.algos:
            for pop in a.pops:
                for k in range(a.seeds):
                    seed = SEED_BASE + 1 + k
                    jid = f"{model}__{algo}__p{pop}__s{seed}"
                    if not (ROOT / f"{jid}.json").exists():
                        jobs.append(dict(id=jid, model=model, algo=algo, pop=pop, seed=seed, nfe_per_var=a.nfe_per_var))
    jobs.sort(key=lambda j: N_GROUPS[j["model"]] * {"ribbed40": 13.6, "kiewitt32": 3.8, "geodesic16": 0.8}[j["model"]],
              reverse=True)
    print(f"{datetime.now():%H:%M:%S} {len(jobs)} kosu, {a.workers} isci", flush=True)
    done = 0
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=mp.get_context("spawn")) as pool:
        futs = [pool.submit(run_one, j) for j in jobs]
        for f in as_completed(futs):
            r = f.result(); done += 1
            print(f"{datetime.now():%H:%M:%S} [{done}/{len(jobs)}] {r['id']} W={r['w']:.2f} uygun={r['feas']} {r['t']:.0f}s", flush=True)


def cmd_summary(a) -> None:
    import numpy as np
    import pandas as pd
    rows = []
    for p in ROOT.glob("*.json"):
        r = json.loads(p.read_text(encoding="utf-8"))
        rows.append(dict(model=r["model"], algo=r["algo"], pop=r["pop"], seed=r["seed"],
                         w=r["best_weight_kN"] if r["is_feasible"] else np.nan, feas=r["is_feasible"],
                         pen=r["best_penalized_kN"], penalty_P=r["penalty"], nfe=r["nfe"],
                         n_groups=r["n_groups"], elapsed_s=round(r["elapsed_s"], 1)))
    df = pd.DataFrame(rows).sort_values(["model", "algo", "pop", "seed"])
    out_csv = Path(a.out).with_name("TUNING_STUDY_runs.csv")
    df.rename(columns={"w": "weight_kN_if_feasible", "pen": "penalized_weight_kN", "feas": "is_feasible"}).to_csv(out_csv, index=False)
    print("tum kosular (CSV):", out_csv)
    if df.empty:
        print("sonuc yok"); return
    lines = ["# Algoritma secimi ve populasyon duyarliligi (tohum 2001+, nihai kampanyadan bagimsiz)", "",
             "Olcut: en iyi cezali agirlik [kN] (`best_penalized`), uygunsuz kosularda ceza dahil. Dusuk iyi.", ""]
    best_pop = {}
    for model, dm in df.groupby("model"):
        lines += [f"## {model}", "", "| Algoritma | pop | n | ortalama | std | en iyi | uygun oran |", "|---|---|---|---|---|---|---|"]
        for (algo, pop), g in dm.groupby(["algo", "pop"]):
            lines.append(f"| {algo.upper()} | {pop} | {len(g)} | {g.pen.mean():.3f} | {g.pen.std(ddof=1) if len(g) > 1 else 0:.3f} | "
                         f"{g.pen.min():.3f} | {g.feas.mean():.2f} |")
        lines.append("")
        for algo, ga in dm.groupby("algo"):
            m = ga.groupby("pop").pen.mean()
            best_pop[(model, algo)] = int(m.idxmin())
    # model basina, her algoritmanin en iyi pop'unda ortalama sira
    lines += ["## Algoritma siralamasi (her algoritma kendi en iyi pop degeriyle; model basina ortalama cezali agirlik)", "",
              "| Algoritma | " + " | ".join(sorted(df.model.unique())) + " | ortalama sira | onerilen pop |", "|---|" + "---|" * (len(df.model.unique()) + 2)]
    tab = {}
    for (model, algo), pop in best_pop.items():
        tab.setdefault(algo, {})[model] = df[(df.model == model) & (df.algo == algo) & (df["pop"] == pop)].pen.mean()
    tdf = pd.DataFrame(tab).T
    ranks = tdf.rank(axis=0).mean(axis=1)
    for algo in ranks.sort_values().index:
        pops = [best_pop[(m, algo)] for m in sorted(df.model.unique()) if (m, algo) in best_pop]
        lines.append(f"| {algo.upper()} | " + " | ".join(f"{tdf.loc[algo].get(m, float('nan')):.3f}" for m in sorted(df.model.unique()))
                     + f" | {ranks[algo]:.2f} | {pops} |")
    out = Path(a.out)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-(len(tdf) + 6):]))
    print("yazildi:", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["run", "summary"])
    ap.add_argument("--models", nargs="+", default=["kiewitt32", "geodesic16"])
    ap.add_argument("--algos", nargs="+", default=DEFAULT_ALGOS)
    ap.add_argument("--pops", nargs="+", type=int, default=[20, 40, 80])
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--nfe-per-var", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=max(1, min((os.cpu_count() or 2) - 1, 7)))
    ap.add_argument("--out", default=str(Path(__file__).parent.parent / "04_Results" / "TUNING_STUDY.md"))
    a = ap.parse_args()
    if sys.stdout.reconfigure:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd_run(a) if a.command == "run" else cmd_summary(a)
