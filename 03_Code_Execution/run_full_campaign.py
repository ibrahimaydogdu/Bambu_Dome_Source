"""
run_full_campaign.py
Kampanya otomasyonu: 3 model x 3 algoritma x N tohum, cok cekirdekli, duraklatilip
surdurulebilir, arka planda calisabilir.  Iki profil:
  pilot : 1 tohum   -> C:\\BambuDome_campaign\\pilot
  full  : 30 tohum (270 is) -> C:\\BambuDome_campaign\\full

Komutlar (03_Code_Execution klasorunde; --profile pilot|full verin):
  python run_full_campaign.py dry-run   --profile full      # is listesi + sure tahmini
  python run_full_campaign.py preflight --profile full      # model/amac/sure kontrolleri
  python run_full_campaign.py start     --profile full [--background]
  python run_full_campaign.py status    --profile full
  python run_full_campaign.py pause     --profile full
  python run_full_campaign.py verify    --profile full      # eksik / basarisiz / supheli isler
  python run_full_campaign.py redo      --profile full --jobs ribbed40__abc__s1003 ...
  python run_full_campaign.py finalize  --profile full      # ozet CSV + en iyi cozumler -> SAP2000 .sdb

Kayit ve devam:
  * Her is bittiginde results/<is>.json (en iyi agirlik, karbon, ceza, NFE, sure) yazilir;
    yakinsama ve istatistik analizleri yeniden kosu gerektirmeden bu dosyalardan yapilir.
  * Optimizer checkpoint'i her iterasyonda yazilir (RNG durumu dahil); degerlendirme kaydi
    checkpoint ile ayni anda diske yazilir. Devamda kosu, kesintisiz kosuyla ayni sonucu verir.
  * `start` tamamlanmis isleri atlar, yarim isleri checkpoint'ten surdurur, basarisizlari yeniden dener.
  * Kod dosyalari degisirse (parmak izi) eski checkpoint'lerle devam reddedilir (--force-config ile gecilir).
"""

from __future__ import annotations
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import csv
import hashlib
import json
import multiprocessing as mp
import random
import subprocess
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CAMPAIGN_ROOT = Path(r"C:\BambuDome_campaign")
from metaheuristic_optimizers import ALGORITHM_NAMES
MODELS = ["ribbed40", "kiewitt32", "geodesic16"]        # maliyet sirasina gore
ALGOS = list(ALGORITHM_NAMES.keys())                    # 16 meta-sezgisel yontem
SEED_BASE = 1000                                         # tohumlar 1001 ... 1030
PROFILES = {"pilot": 1, "full": 30}
PARALLEL_FACTOR = 1.17                                   # 7 surec paralelken olculen yavaslama (verim 0.86-0.92)
JOB_OVERHEAD_S = 5.0                                     # is basina surec baslatma + model kurma + yazma
# Seri tam degerlendirme suresi [s] (olculen, seyrek cozucu; preflight yeniden olcer)
EVAL_S = {"ribbed40": 0.0136, "kiewitt32": 0.0038, "geodesic16": 0.00078}
CODE_FILES = ["fast_eval.py", "metaheuristic_optimizers.py", "checkpoint_manager.py", "truss_model.py",
              "dome_types.py", "fem_bridge.py", "iso22156_checks.py", "bamboo_catalog.py"]
N_GROUPS = {"ribbed40": 43, "kiewitt32": 22, "geodesic16": 23}   # tasarim degiskeni sayisi (preflight dogrular)
CFG_KEYS = ("pop", "pop_map", "nfe_per_var", "seeds", "models", "algos", "penalty_mode", "penalty_exp", "carbon", "slenderness")


class CampaignStop(Exception):
    """STOP dosyasi goruldu: is, son checkpoint ile temiz durur."""


# ---------------------------------------------------------------------------
# Yollar / dosya yardimcilari
# ---------------------------------------------------------------------------
class Paths:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.results = self.root / "results"
        self.ckpt = self.root / "checkpoints"
        self.progress = self.root / "progress"
        self.failed = self.root / "failed"
        self.final = self.root / "final"
        self.stop = self.root / "STOP"
        self.status = self.root / "status.json"
        self.pid = self.root / "campaign.pid"
        self.log = self.root / "campaign.log"
        self.config = self.root / "config.json"

    def make(self):
        for d in (self.root, self.results, self.ckpt, self.progress, self.failed):
            d.mkdir(parents=True, exist_ok=True)


def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def log(msg: str) -> None:
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}", flush=True)


def code_hash() -> dict:
    out = {}
    for f in CODE_FILES:
        p = BASE_DIR / f
        out[f] = hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "yok"
    return out


def job_id(model: str, algo: str, seed: int) -> str:
    return f"{model}__{algo}__s{seed}"


def build_jobs(cfg: dict) -> list[dict]:
    jobs = []
    for k in range(cfg["seeds"]):
        seed = SEED_BASE + 1 + k
        for model in cfg["models"]:
            for algo in cfg["algos"]:
                jobs.append(dict(id=job_id(model, algo, seed), model=model, algo=algo,
                                 seed=seed, run_id=k + 1))
    return jobs


def budget(cfg: dict, model: str) -> int:
    """Esit NFE butcesi: tasarim degiskeni sayisi x nfe_per_var (model basina, algoritmadan bagimsiz)."""
    return int(cfg["nfe_per_var"]) * N_GROUPS[model]


def pop_of(cfg: dict, algo: str) -> int:
    return int(cfg.get("pop_map", {}).get(algo, cfg["pop"]))


def est_seconds(model: str, algo: str, cfg: dict) -> float:
    return budget(cfg, model) * EVAL_S[model] * PARALLEL_FACTOR + JOB_OVERHEAD_S


def build_model(name: str):
    if name == "ribbed40":
        from truss_model import build_dome_model
        return build_dome_model(2, 40.0)
    from dome_types import build_preset
    return build_preset(name)


def make_evaluator(model, bridge, groups_lengths, cfg):
    from fast_eval import FastCore, CarbonModel
    from bamboo_catalog import BAMBOO_CATALOG
    return FastCore(bridge=bridge, catalog=BAMBOO_CATALOG, span_m=model.span_m,
                    disp_limit_m=model.disp_limit_m, carbon=CarbonModel(**cfg["carbon"]),
                    slenderness=cfg["slenderness"], envelope=True)


# ---------------------------------------------------------------------------
# Calisan surec: tek is
# ---------------------------------------------------------------------------
def run_job(job: dict, cfg: dict, root: str) -> dict:
    """Bir (model, algoritma, tohum) isini kosar. Ayri surecte calisir."""
    import numpy as np
    from fem_bridge import FEMBridge
    from bamboo_catalog import BAMBOO_CATALOG
    from metaheuristic_optimizers import MetaheuristicOptimizer, ALGORITHM_NAMES, OptimizationPaused

    P = Paths(Path(root))
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    prog_path = P.progress / f"{job['id']}.json"
    ckpt_path = P.ckpt / f"{job['id']}.pkl"
    log_prefix = P.ckpt / f"{job['id']}.evlog"
    prog = json.loads(prog_path.read_text(encoding="utf-8")) if prog_path.exists() else \
        dict(evals=0, elapsed_s=0.0, resumes=0, attempts=0)
    resumed = ckpt_path.exists()
    if resumed:
        prog["resumes"] += 1
    prog["attempts"] += 1

    if P.stop.exists():
        return dict(id=job["id"], status="stopped")

    random.seed(job["seed"])
    np.random.seed(job["seed"] % (2 ** 32))

    model = build_model(job["model"])
    bridge = FEMBridge(model); bridge.open()
    groups, lengths = bridge.read_groups_and_lengths()
    core = make_evaluator(model, bridge, lengths, cfg)

    t0 = time.time()
    base_elapsed = prog["elapsed_s"]

    nfe_budget = budget(cfg, job["model"])
    pop = pop_of(cfg, job["algo"])
    opt = MetaheuristicOptimizer(
        eval_fn=core.evaluate,
        n_vars=len(groups),
        lb=1,
        ub=len(BAMBOO_CATALOG),
        pop_size=pop,
        max_iters=10 ** 9,
        max_evals=nfe_budget,                         # tum algoritmalar icin esit NFE butcesi
        penalty_exp=cfg["penalty_exp"],
        seed=job["seed"],
        method=job["algo"],
        ckpt_path=str(ckpt_path),
        log_prefix=str(log_prefix),
        stop_check=P.stop.exists,
    )

    try:
        best_member, history = opt.optimize()
    except OptimizationPaused:
        prog["elapsed_s"] = base_elapsed + (time.time() - t0)
        prog["evals"] = opt.n_evals
        _atomic_write(prog_path, json.dumps(prog))
        return dict(id=job["id"], status="stopped")

    elapsed = base_elapsed + (time.time() - t0)
    prog["elapsed_s"] = elapsed
    prog["evals"] = opt.n_evals
    _atomic_write(prog_path, json.dumps(prog))

    result = dict(
        job=job["id"], model=job["model"], algo=job["algo"],
        algo_name=ALGORITHM_NAMES.get(job["algo"], job["algo"].upper()),
        seed=job["seed"], run_id=job["run_id"],
        pop=pop, penalty_mode=cfg["penalty_mode"], penalty_exp=cfg["penalty_exp"],
        carbon=cfg["carbon"], slenderness=cfg["slenderness"], n_groups=len(groups),
        nfe=opt.n_evals, nfe_budget=nfe_budget, elapsed_s=elapsed, resumes=prog["resumes"],
        best_penalized_weight_kN=best_member.penalized_cost,
        best_structural_weight_kN=best_member.cost_value,
        best_embodied_carbon_kgCO2e=best_member.carbon_value,
        penalty=best_member.penalty,
        is_feasible=best_member.is_feasible,
        solution=best_member.design_variables.tolist(),
        history=history,
        finished=datetime.now().isoformat(timespec="seconds"),
    )
    opt.finalize_log(str(P.results / f"{job['id']}.npz"))     # degerlendirme basina kayit (gen, W, CO2e, P)
    _atomic_write(P.results / f"{job['id']}.json", json.dumps(result))     # .json = is tamam isareti
    if ckpt_path.exists():
        ckpt_path.unlink()
    return dict(id=job["id"], status="done", elapsed_s=result["elapsed_s"], nfe=opt.n_evals,
                best_weight=best_member.cost_value, is_feasible=best_member.is_feasible)


# ---------------------------------------------------------------------------
# On kontrol
# ---------------------------------------------------------------------------
def preflight(cfg: dict, allow_collinear: bool, n_samples: int = 12) -> bool:
    import numpy as np
    from fem_bridge import FEMBridge

    ok = True
    log("ON KONTROL basladi")
    for name in cfg["models"]:
        model = build_model(name)
        b = FEMBridge(model); b.open()
        groups, lengths = b.read_groups_and_lengths(); G = len(groups)
        ev = make_evaluator(model, b, lengths, cfg)
        Lmax = max(lengths.values())
        if G != N_GROUPS[name]:
            log(f"  !! {name}: grup sayisi {G} != beklenen {N_GROUPS[name]}"); ok = False
        rng = np.random.default_rng(0)
        ev.evaluate(rng.integers(1, 25, G))                         # isinma
        t = time.time()
        F = np.array([ev.evaluate(rng.integers(1, 25, G))[:2] for _ in range(n_samples)])
        dt = (time.time() - t) / n_samples
        EVAL_S[name] = dt
        _, _, p24 = ev.evaluate(np.full(G, 24, dtype=int))
        corr = float(np.corrcoef(F[:, 0], F[:, 1])[0, 1])
        log(f"  {name}: {len(model.joint_names)} dugum, {len(lengths)} cubuk, {G} grup, Lmax={Lmax:.2f} m | "
            f"tum-24 ceza={p24:.3f} | {dt * 1000:.1f} ms/degerlendirme (seri) | corr(W,ECO2e)={corr:.6f}")
        if Lmax > 4.0 + 1e-9:
            log(f"  !! {name}: cubuk boyu 4 m ustu"); ok = False
        if p24 > 0:
            log(f"  !! {name}: en buyuk kesitlerle bile uygun cozum yok"); ok = False
    log("ON KONTROL basarili" if ok else "ON KONTROL BASARISIZ.")
    return ok


def print_estimate(cfg: dict, workers: int) -> None:
    jobs = build_jobs(cfg)
    tot = {m: 0.0 for m in cfg["models"]}
    for j in jobs:
        tot[j["model"]] += est_seconds(j["model"], j["algo"], cfg)
    cpu_h = sum(tot.values()) / 3600
    log(f"{len(jobs)} is = {len(cfg['models'])} model x {len(cfg['algos'])} algoritma x {cfg['seeds']} tohum | "
        f"NFE = {cfg['nfe_per_var']} x tasarim degiskeni; pop={cfg['pop']} {cfg.get('pop_map') or ''}")
    for m, sec in tot.items():
        log(f"  {m}: NFE/is={budget(cfg, m)}  {sec / 3600:.2f} isci-saat  ({EVAL_S[m] * 1000:.1f} ms seri, x{PARALLEL_FACTOR} paralel)")
    longest = max((est_seconds(m, a, cfg) for m in cfg["models"] for a in cfg["algos"]), default=0)
    log(f"  TOPLAM: {cpu_h:.2f} isci-saat; {workers} isciyle ~ {max(cpu_h / workers, longest / 3600):.2f} saat duvar saati "
        f"(en uzun is {longest / 60:.1f} dk; is basina {JOB_OVERHEAD_S:.0f} sn sabit yuk dahil)")


# ---------------------------------------------------------------------------
# Orkestrator
# ---------------------------------------------------------------------------
def done_ids(P: Paths) -> set[str]:
    return {p.stem for p in P.results.glob("*.json")}


def write_status(P: Paths, cfg: dict, total: int, running: dict, failed: set, t_start: float) -> None:
    done = len(done_ids(P))
    _atomic_write(P.status, json.dumps(dict(
        updated=datetime.now().isoformat(timespec="seconds"), total=total, done=done,
        running=sorted(running), failed=sorted(failed), pending=total - done - len(running) - len(failed),
        elapsed_s=time.time() - t_start, workers=cfg.get("workers"),
        stop_requested=P.stop.exists()), indent=1))


def cmd_start(args, cfg: dict, P: Paths) -> int:
    P.make()
    now_hash = code_hash()
    if P.config.exists():
        old = json.loads(P.config.read_text(encoding="utf-8"))
        diff_cfg = any(old.get(k) != cfg.get(k) for k in CFG_KEYS)
        diff_code = old.get("code_hash") != now_hash
        if (diff_cfg or diff_code) and not args.force_config:
            what = "parametreler" if diff_cfg else "kod dosyalari (parmak izi)"
            log(f"HATA: mevcut kampanyadan farkli {what}. Eski sonuc/checkpoint'ler yeni kodla karisabilir. "
                f"Yeni bir klasor kullanin ya da --force-config verin.")
            return 2
    _atomic_write(P.config, json.dumps({**{k: cfg[k] for k in CFG_KEYS}, "code_hash": now_hash,
                                        "created": datetime.now().isoformat(timespec="seconds")}, indent=1))

    if args.background:                              # kendini ayrik surec olarak yeniden baslat
        argv = [a for a in sys.argv[1:] if a != "--background"]
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
        with open(P.log, "a", encoding="utf-8") as lf:
            proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve())] + argv, cwd=str(BASE_DIR),
                                    stdout=lf, stderr=lf, stdin=subprocess.DEVNULL, creationflags=flags,
                                    close_fds=True)
        sel = f"--profile {args.profile}" if args.profile else f"--campaign-dir {P.root}"
        log(f"Arka planda baslatildi (PID {proc.pid}). Log: {P.log}\n"
            f"  ilerleme: python run_full_campaign.py status {sel}\n"
            f"  duraklat: python run_full_campaign.py pause {sel}")
        return 0

    if not args.skip_preflight and not preflight(cfg, args.allow_collinear):
        return 3
    print_estimate(cfg, cfg["workers"])

    if P.stop.exists():
        P.stop.unlink()
    _atomic_write(P.pid, str(os.getpid()))
    jobs = build_jobs(cfg)
    attempts: dict[str, int] = {}
    failed: set[str] = set()
    pending = [j for j in jobs if j["id"] not in done_ids(P)]
    log(f"{len(jobs) - len(pending)} is zaten tamam; {len(pending)} is calistirilacak, {cfg['workers']} isci.")
    t_start = time.time()
    running: dict = {}                               # future -> job
    ctx = mp.get_context("spawn")
    interrupted = False
    try:
        with ProcessPoolExecutor(max_workers=cfg["workers"], mp_context=ctx) as pool:
            while pending or running:
                while pending and len(running) < cfg["workers"] and not P.stop.exists() and not interrupted:
                    j = pending.pop(0)
                    running[pool.submit(run_job, j, cfg, str(P.root))] = j
                if not running:
                    break
                write_status(P, cfg, len(jobs), {j["id"]: 1 for j in running.values()}, failed, t_start)
                try:
                    finished, _ = wait(list(running), timeout=5, return_when=FIRST_COMPLETED)
                except KeyboardInterrupt:
                    log("Ctrl+C: duraklatiliyor (isler son iterasyonda kaydedilecek)...")
                    P.stop.touch(); interrupted = True
                    continue
                for f in finished:
                    j = running.pop(f)
                    try:
                        r = f.result()
                    except Exception:
                        attempts[j["id"]] = attempts.get(j["id"], 0) + 1
                        err = traceback.format_exc()
                        log(f"HATA {j['id']} (deneme {attempts[j['id']]}): {err.splitlines()[-1]}")
                        if attempts[j["id"]] <= args.max_retries:
                            pending.insert(0, j)       # checkpoint'ten devam
                        else:
                            failed.add(j["id"])
                            _atomic_write(P.failed / f"{j['id']}.txt", err)
                        continue
                    if r["status"] == "done":
                        d = len(done_ids(P))
                        log(f"TAMAM {r['id']}  NFE={r['nfe']} sure={r['elapsed_s'] / 60:.1f} dk "
                            f"agirlik={r['best_weight']:.2f} kN uygun={r['is_feasible']}  [{d}/{len(jobs)}]")
                    else:
                        pending.insert(0, j)
                if P.stop.exists() and not running:
                    break
    finally:
        write_status(P, cfg, len(jobs), {}, failed, t_start)
        if P.pid.exists():
            P.pid.unlink()
    d = len(done_ids(P))
    if P.stop.exists():
        log(f"DURAKLATILDI: {d}/{len(jobs)} is tamam. Devam icin ayni 'start' komutunu tekrar calistirin.")
    elif failed:
        log(f"Bitti, {len(failed)} is basarisiz (bkz. {P.failed}). {d}/{len(jobs)} tamam. "
            f"Yeniden denemek icin 'start' komutunu tekrar calistirin.")
    else:
        log(f"KAMPANYA TAMAMLANDI: {d}/{len(jobs)} is. Sonraki adim: verify, sonra finalize")
    return 0


# ---------------------------------------------------------------------------
# status / pause / verify / redo / finalize
# ---------------------------------------------------------------------------
def _pid_alive(pid: int) -> bool:
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
    return str(pid) in out


def cmd_status(args, cfg: dict, P: Paths) -> int:
    jobs = build_jobs(cfg)
    done = done_ids(P)
    pid = int(P.pid.read_text()) if P.pid.exists() else None
    alive = bool(pid) and _pid_alive(pid)
    log(f"Kampanya: {len(done)}/{len(jobs)} is tamam | orkestrator: "
        f"{'CALISIYOR (PID %d)' % pid if alive else 'calismiyor'} | STOP: {'var' if P.stop.exists() else 'yok'}")
    for m in cfg["models"]:
        row = []
        for a in cfg["algos"]:
            n = sum(1 for j in jobs if j["model"] == m and j["algo"] == a and j["id"] in done)
            row.append(f"{a} {n}/{cfg['seeds']}")
        log(f"  {m}: " + " | ".join(row))
    if P.status.exists():
        s = json.loads(P.status.read_text())
        log(f"  calisan: {len(s['running'])} | basarisiz: {len(s['failed'])} | son guncelleme: {s['updated']}")
        for r in s["running"][:cfg.get("workers") or 8]:
            pp = P.progress / f"{r}.json"
            ev = json.loads(pp.read_text())["evals"] if pp.exists() else 0
            log(f"    {r}: ~{ev} degerlendirme")
    return 0


def cmd_pause(args, cfg: dict, P: Paths) -> int:
    P.root.mkdir(parents=True, exist_ok=True)
    P.stop.touch()
    log("STOP dosyasi olusturuldu: isler son iterasyonun checkpoint'iyle duracak (birkac saniye-dakika). "
        "Devam icin 'start' komutunu tekrar calistirin.")
    return 0


def cmd_verify(args, cfg: dict, P: Paths) -> int:
    jobs = build_jobs(cfg)
    missing, partial, failed, suspicious, empty = [], [], [], [], []
    for j in jobs:
        rp = P.results / f"{j['id']}.json"
        if not rp.exists():
            if (P.failed / f"{j['id']}.txt").exists():
                failed.append(j["id"])
            elif (P.ckpt / f"{j['id']}.pkl").exists():
                partial.append(j["id"])
            else:
                missing.append(j["id"])
            continue
        try:
            r = json.loads(rp.read_text(encoding="utf-8"))
            problems = []
            if r["seed"] != j["seed"] or r["model"] != j["model"] or r["algo"] != j["algo"]:
                problems.append("kimlik uyusmuyor")
            if not r.get("is_feasible", False):
                empty.append(j["id"])
            if problems:
                suspicious.append((j["id"], "; ".join(problems)))
        except Exception as exc:
            suspicious.append((j["id"], f"okunamadi: {exc}"))
    log(f"DOGRULAMA: {len(jobs)} is | tamam {len(jobs) - len(missing) - len(partial) - len(failed)} | "
        f"hic baslamamis {len(missing)} | yarim (checkpoint var) {len(partial)} | basarisiz {len(failed)} | "
        f"supheli {len(suspicious)} | uygun cozum bulunamayan {len(empty)}")
    for name, lst in (("EKSIK", missing), ("YARIM", partial), ("BASARISIZ", failed), ("UYGUN COZUMSUZ", empty)):
        if lst:
            log(f"  {name}: " + ", ".join(lst[:12]) + (f" ... (+{len(lst) - 12})" if len(lst) > 12 else ""))
    for jid, why in suspicious:
        log(f"  SUPHELI {jid}: {why}")
    if missing or partial or failed:
        log("  -> Eksik/yarim/basarisiz isleri tamamlamak icin 'start' komutunu tekrar calistirin.")
    if suspicious or empty:
        log("  -> Belirli isleri bastan yaptirmak icin: redo --jobs <is_adi ...>")
    return 0 if not (missing or partial or failed or suspicious) else 1


def cmd_redo(args, cfg: dict, P: Paths) -> int:
    if not args.jobs:
        log("HATA: --jobs <is_adi veya parca ...> verin (or. ribbed40__abc__s1003 veya geodesic16)")
        return 2
    n = 0
    for j in build_jobs(cfg):
        if any(sub in j["id"] for sub in args.jobs):
            for p in (P.results / f"{j['id']}.json", P.ckpt / f"{j['id']}.pkl", P.results / f"{j['id']}.npz",
                      P.ckpt / f"{j['id']}.evlog.genes.bin", P.ckpt / f"{j['id']}.evlog.obj.bin",
                      P.progress / f"{j['id']}.json", P.failed / f"{j['id']}.txt"):
                if p.exists():
                    p.unlink()
            n += 1
    log(f"{n} is sifirlandi. Calistirmak icin 'start' komutunu verin.")
    return 0


def cmd_finalize(args, cfg: dict, P: Paths) -> int:
    P.final.mkdir(parents=True, exist_ok=True)
    rows, best = [], {}
    for p in sorted(P.results.glob("*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        rows.append(dict(
            model=r["model"], algo=r["algo"], algo_name=r.get("algo_name", r["algo"]),
            seed=r["seed"], nfe=r["nfe"], elapsed_s=round(r["elapsed_s"], 1),
            resumes=r.get("resumes", 0), is_feasible=r.get("is_feasible", False),
            penalty=r.get("penalty", 0.0),
            best_penalized_weight_kN=r.get("best_penalized_weight_kN", 0.0),
            best_structural_weight_kN=r.get("best_structural_weight_kN", 0.0),
            best_embodied_carbon_kgCO2e=r.get("best_embodied_carbon_kgCO2e", 0.0),
        ))
        m = r["model"]
        w = r.get("best_structural_weight_kN", 1e9)
        if r.get("is_feasible", False):
            if m not in best or w < best[m]["weight"]:
                best[m] = dict(
                    model=m, algo=r["algo"], seed=r["seed"],
                    weight=w,
                    penalized_weight=r.get("best_penalized_weight_kN", w),
                    carbon=r.get("best_embodied_carbon_kgCO2e", 0.0),
                    is_feasible=True,
                    gene=r.get("solution", []),
                )
    with open(P.final / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["model"])
        w.writeheader(); w.writerows(rows)
    log(f"Ozet: {P.final / 'summary.csv'} ({len(rows)} is)")
    _atomic_write(P.final / "global_best.json", json.dumps({f"{m}__min_weight": v for m, v in best.items()}, indent=1))
    for m, b in sorted(best.items()):
        log(f"  genel en iyi {m}: agirlik={b['weight']:.3f} kN, karbon={b['carbon']:.1f} kgCO2e ({b['algo']}, tohum {b['seed']})")
    if args.no_sap or not best:
        return 0
    from bamboo_catalog import BAMBOO_CATALOG
    from sap_export import verify_with_sap
    for m, b in sorted(best.items()):
        model = build_model(m)
        log(f"SAP2000'e yaziliyor: {m} (en hafif cozum) ...")
        r = verify_with_sap(model, b["gene"], BAMBOO_CATALOG, P.final / "sap_work", tag=f"best_{m}",
                            span_m=model.span_m, disp_limit_m=model.disp_limit_m,
                            deliver_path=P.final / f"global_best_{m}.sdb")
        r.pop("sdb_path", None)
        r.update(b); r["model"] = m
        _atomic_write(P.final / f"global_best_{m}.json", json.dumps(r, indent=1))
        log(f"  {m}: hata eksenel {r['err_axial']:.1e}, yer degistirme {r['err_disp']:.1e}; "
            f"D/C FEM {r['dc_fem']:.4f} / SAP {r['dc_sap']:.4f}")
    return 0


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Kampanya otomasyonu (cok cekirdekli, surdurulebilir)")
    ap.add_argument("command", choices=["dry-run", "preflight", "start", "status", "pause", "verify",
                                        "redo", "finalize"])
    ap.add_argument("--profile", choices=list(PROFILES), default=None,
                    help="pilot: 1 tohum -> C:\\BambuDome_campaign\\pilot ; full: 30 tohum -> ...\\full")
    ap.add_argument("--campaign-dir", default=None, help="Kampanya klasoru (profil yoksa varsayilan ./campaign)")
    ap.add_argument("--models", nargs="+", default=MODELS, choices=MODELS)
    ap.add_argument("--algos", nargs="+", default=ALGOS, choices=ALGOS)
    ap.add_argument("--seeds", type=int, default=None, help="Bagimsiz tohum sayisi (1001 ...); profil belirler")
    ap.add_argument("--pop", type=int, default=40)
    ap.add_argument("--pop-map", default="", help="algoritma basina populasyon, or. abc=40,gwo=60,do=80")
    ap.add_argument("--nfe-per-var", type=int, default=1000, help="NFE butcesi = bu deger x tasarim degiskeni sayisi")
    ap.add_argument("--penalty-mode", default="multiplicative", choices=["multiplicative", "additive"])
    ap.add_argument("--penalty-exp", type=float, default=2.0, help="Carpimsal ceza ussu eps")
    ap.add_argument("--carbon-model", default="section", choices=["section", "fixed"])
    ap.add_argument("--c-s1", type=float, default=0.0, help="Celik bag. kg/m cubuk capi (0 = prefabrik, 4.5 = alternatif)")
    ap.add_argument("--slenderness", default="all", choices=["all", "compression"])
    ap.add_argument("--workers", type=int, default=max(1, min((os.cpu_count() or 2) - 1, 7)))
    ap.add_argument("--background", action="store_true", help="start: ayrik arka plan sureci olarak calistir")
    ap.add_argument("--max-retries", type=int, default=2)
    ap.add_argument("--skip-preflight", action="store_true")
    ap.add_argument("--allow-collinear", action="store_true", help="f1/f2 dogrusal olsa da on kontrolu gec")
    ap.add_argument("--force-config", action="store_true", help="parametre/kod farkina ragmen devam et")
    ap.add_argument("--no-sap", action="store_true", help="finalize: SAP2000 dosyalarini yazma")
    ap.add_argument("--best-by", nargs="+", default=["f1", "f2"], choices=["f1", "f2"],
                    help="finalize: hangi uc nokta icin SAP2000 dosyasi yazilsin")
    ap.add_argument("--jobs", nargs="+", default=None, help="redo: sifirlanacak is adlari (alt dize)")
    args = ap.parse_args()

    if args.profile:
        root = Path(args.campaign_dir) if args.campaign_dir else CAMPAIGN_ROOT / args.profile
        seeds = args.seeds if args.seeds is not None else PROFILES[args.profile]
    else:
        root = Path(args.campaign_dir) if args.campaign_dir else BASE_DIR / "campaign"
        seeds = args.seeds if args.seeds is not None else 30
    P = Paths(root)
    carbon = dict(mode=args.carbon_model, c_s1=args.c_s1)
    from fast_eval import CarbonModel                      # tam parametre kumesini kaydet
    carbon = CarbonModel(**carbon).as_dict()
    pop_map = {k: int(v) for k, v in (kv.split("=") for kv in args.pop_map.split(",") if kv)}
    cfg = dict(pop=args.pop, pop_map=pop_map, nfe_per_var=args.nfe_per_var, seeds=seeds, models=list(args.models), algos=list(args.algos),
               penalty_mode=args.penalty_mode, penalty_exp=args.penalty_exp, carbon=carbon,
               slenderness=args.slenderness, workers=args.workers)
    cmd = args.command
    if cmd == "dry-run":
        print_estimate(cfg, cfg["workers"]); return 0
    if cmd == "preflight":
        return 0 if preflight(cfg, args.allow_collinear) else 3
    if cmd == "start":
        return cmd_start(args, cfg, P)
    return {"status": cmd_status, "pause": cmd_pause, "verify": cmd_verify,
            "redo": cmd_redo, "finalize": cmd_finalize}[cmd](args, cfg, P)


if __name__ == "__main__":
    sys.exit(main())
