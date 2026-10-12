"""
run_campaign.py
Gozetimsiz (unattended) optimizasyon kampanyasi yoneticisi
==========================================================
Duman testi -> 16 Meta-Sezgisel Algoritma x N bagimsiz kosu.

Her (algoritma, kosu) cifti ayri bir main.py sureci olarak calistirilir:
  - Tamamlanan isler campaign_state.json'a islenir; betik yeniden
    baslatildiginda bitenler atlanir.
  - Surec cokerse yetim surecler oldurulur ve is ayni
    checkpoint'ten devam ettirilir (en fazla --max-retries deneme).
  - Her is icin zaman asimi (--timeout-h) vardir; asilirsa surec oldurulup
    yeniden baslatilir.

Kullanim (03_Code_Execution klasorunde):
  python run_campaign.py                      # varsayilan: 6 temel algo x 15 kosu, pop=40, gen=100
  python run_campaign.py --runs 2 --gen 5     # kisa deneme kampanyasi
  python run_campaign.py --algos all --runs 30
  python run_campaign.py --skip-smoke         # duman testini atla
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / "campaign_state.json"
CAMPAIGN_LOG = BASE_DIR / "logs" / "campaign.log"
SEED_BASE = 1000


def log(msg: str) -> None:
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    CAMPAIGN_LOG.parent.mkdir(exist_ok=True)
    with open(CAMPAIGN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            log("UYARI: campaign_state.json bozuk, sifirdan olusturuluyor.")
    return {"smoke_ok": False, "done": {}}


def save_state(state: dict) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, STATE_FILE)


def kill_orphan_sap() -> None:
    """Arkada kalmis SAP2000 sureclerini sonlandirir."""
    subprocess.run(
        ["taskkill", "/F", "/IM", "SAP2000.exe", "/T"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(3)


def run_job(cmd: list[str], timeout_s: float) -> int:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    log("CALISTIR: " + " ".join(cmd[1:]))
    proc = subprocess.Popen(cmd, cwd=str(BASE_DIR), env=env)
    try:
        return proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        log(f"ZAMAN ASIMI ({timeout_s/3600:.1f} sa) -- surec sonlandiriliyor.")
        proc.kill()
        return -999
    except KeyboardInterrupt:
        log("Kullanici tarafindan durduruldu (Ctrl+C). Checkpoint korunuyor.")
        proc.kill()
        kill_orphan_sap()
        sys.exit(130)


    from metaheuristic_optimizers import ALGORITHM_NAMES
    ap = argparse.ArgumentParser(description="BambuDome optimizasyon kampanyasi (16 Meta-Sezgisel Algoritma)")
    ap.add_argument("--algos", nargs="+", default=["abc", "hs", "gwo", "woa", "tlbo", "bbo"],
                    choices=list(ALGORITHM_NAMES.keys()) + ["all"])
    ap.add_argument("--model", default="geodesic16", choices=["geodesic16", "kiewitt32", "ribbed40"])
    ap.add_argument("--runs", type=int, default=15, help="Algoritma basina bagimsiz kosu")
    ap.add_argument("--pop", type=int, default=40)
    ap.add_argument("--gen", type=int, default=100)
    ap.add_argument("--max-retries", type=int, default=5)
    ap.add_argument("--timeout-h", type=float, default=24.0, help="Is basina zaman asimi [saat]")
    ap.add_argument("--skip-smoke", action="store_true")
    args = ap.parse_args()

    if "all" in args.algos:
        args.algos = list(ALGORITHM_NAMES.keys())

    py = sys.executable
    state = load_state()
    log("=" * 70)
    log(f"KAMPANYA: model={args.model} algos={args.algos} runs={args.runs} pop={args.pop} gen={args.gen}")

    # 1) Duman testi
    if not args.skip_smoke and not state.get("smoke_ok"):
        kill_orphan_sap()
        rc = run_job([py, "test_units.py"], timeout_s=300)
        kill_orphan_sap()
        if rc != 0:
            log(f"DUMAN TESTI BASARISIZ (rc={rc}). logs/ klasorunu inceleyin. Kampanya durdu.")
            sys.exit(1)
        state["smoke_ok"] = True
        save_state(state)
        log("Duman testi BASARILI.")

    # 2) Uretim kosulari (kosu-ici algoritma sirasi: her kosu numarasi icin tum algoritmalar,
    #    boylece kampanya yarida kalsa bile algoritmalar dengeli sayida kosuya sahip olur)
    jobs = [(r, a) for r in range(1, args.runs + 1) for a in args.algos]
    total = len(jobs)
    for n, (run_id, algo) in enumerate(jobs, 1):
        key = f"{algo}_r{run_id:02d}_p{args.pop}_g{args.gen}"
        if key in state["done"]:
            continue
        seed = SEED_BASE + run_id  # Ayni kosu no -> tum algoritmalar ayni tohum
        log(f"--- Is {n}/{total}: {key} (seed={seed}) ---")

        for attempt in range(1, args.max_retries + 1):
            kill_orphan_sap()
            t0 = time.time()
            rc = run_job(
                [py, "main.py", "--algo", algo, "--model", args.model, "--pop", str(args.pop),
                 "--gen", str(args.gen), "--run-id", str(run_id), "--seed", str(seed)],
                timeout_s=args.timeout_h * 3600,
            )
            dt = time.time() - t0
            if rc == 0:
                state["done"][key] = {
                    "finished": datetime.now().isoformat(timespec="seconds"),
                    "elapsed_s": round(dt, 1), "seed": seed, "attempts": attempt,
                }
                save_state(state)
                log(f"TAMAM: {key}  ({dt/60:.1f} dk, deneme {attempt})")
                break
            log(f"HATA: {key} rc={rc}, deneme {attempt}/{args.max_retries} -- "
                f"60 sn sonra checkpoint'ten devam edilecek.")
            time.sleep(60)
        else:
            log(f"VAZGECILDI: {key} {args.max_retries} denemede tamamlanamadi. Sonraki ise geciliyor.")

    kill_orphan_sap()
    done = sum(1 for r, a in jobs if f"{a}_r{r:02d}_p{args.pop}_g{args.gen}" in state["done"])
    log(f"KAMPANYA BITTI: {done}/{total} is tamamlandi. Sonuclar: results/")


if __name__ == "__main__":
    main()
