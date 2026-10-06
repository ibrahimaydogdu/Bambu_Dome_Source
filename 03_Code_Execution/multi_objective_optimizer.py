"""
multi_objective_optimizer.py
Cok Amacli Optimizasyon Motoru: NSGA-II, MOABC, MODBO
======================================================
354-eleman Bambu Geodezik Kubbe: f1 = Yapisal Agirlik (kN), f2 = Gomulu Karbon (kg CO2e)
Kisitlar: ISO 22156 cekme/basinc/burkulma/narinlik + deplasman siniri

Algorithm 1: NSGA-II  (Deb et al. 2002)       -- evrensel Q1 baz cizgisi
Algorithm 2: MOABC    (Karaboga & Akay 2011)   -- ucak-bal-izci ABC mekanizmasi
Algorithm 3: MODBO    (Xue & Shen 2022)        -- Multi-Obj. Dung Beetle Optimizer

Ortak Pareto arsiv ve baskınlık kontrolleri paylasiliyor.
"""

from __future__ import annotations
import json
import logging
import math
import time
import random
from copy import deepcopy
from pathlib import Path
from typing import Callable

import numpy as np

from bamboo_catalog import BAMBOO_CATALOG
from carbon_calculator import compute_embodied_carbon, compute_structural_weight
from iso22156_checks import evaluate_all_members
from checkpoint_manager import CheckpointManager

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pareto Yardimci Fonksiyonlari
# ---------------------------------------------------------------------------

def dominates(obj_a: np.ndarray, obj_b: np.ndarray) -> bool:
    """obj_a, obj_b'yi baskiniyor mu? (Minimizasyon icin)"""
    return np.all(obj_a <= obj_b) and np.any(obj_a < obj_b)


def non_dominated_sort_front0(objectives: np.ndarray) -> list[int]:
    """Ilk Pareto cephesinin indekslerini dondurur (O(N^2))."""
    n = len(objectives)
    front: list[int] = []
    for i in range(n):
        dominated_by_any = False
        for j in range(n):
            if i != j and dominates(objectives[j], objectives[i]):
                dominated_by_any = True
                break
        if not dominated_by_any:
            front.append(i)
    return front


def crowding_distance(objectives: np.ndarray) -> np.ndarray:
    """Kalabalilik mesafesi hesapla (NSGA-II Ek3)."""
    n, m = objectives.shape
    dist = np.zeros(n)
    for k in range(m):
        idx = np.argsort(objectives[:, k])
        dist[idx[0]] = dist[idx[-1]] = np.inf
        rng = objectives[idx[-1], k] - objectives[idx[0], k]
        if rng < 1e-12:
            continue
        for i in range(1, n - 1):
            dist[idx[i]] += (objectives[idx[i+1], k] - objectives[idx[i-1], k]) / rng
    return dist


def update_archive(
    archive_sol: list,
    archive_obj: list,
    new_sol: np.ndarray,
    new_obj: np.ndarray,
    max_archive: int = 200,
) -> tuple[list, list]:
    """Pareto arsivini gunceller (baskinilik + kapasite siniri)."""
    # Yeni cozum mevcut arsivi baskinliyor mu?
    to_remove = []
    for i, aobj in enumerate(archive_obj):
        if dominates(new_obj, np.array(aobj)):
            to_remove.append(i)
        elif dominates(np.array(aobj), new_obj):
            return archive_sol, archive_obj  # Arsiv tarafindan baskiniyor

    for i in reversed(to_remove):
        archive_sol.pop(i)
        archive_obj.pop(i)

    archive_sol.append(new_sol.copy())
    archive_obj.append(new_obj.tolist())

    # Kapasite asildiysa kalabalilik mesafesine gore kes
    if len(archive_obj) > max_archive:
        obj_arr = np.array(archive_obj)
        cd = crowding_distance(obj_arr)
        worst = int(np.argmin(cd))
        archive_sol.pop(worst)
        archive_obj.pop(worst)

    return archive_sol, archive_obj


# ---------------------------------------------------------------------------
# Ortak Fitness Degerlendirici
# ---------------------------------------------------------------------------

class FitnessEvaluator:
    """
    SAP2000 Bridge uzerinden f1 (agirlik) ve f2 (karbon) hesaplar,
    ISO 22156 kisitlarini uygular ve ceza puani dondurur.
    """

    def __init__(
        self,
        bridge,
        member_lengths: dict,
        member_group: dict,
        n_nodes: int,
        span_m: float = 24.384,
        penalty_multiplier: float = 1000.0,
    ):
        self.bridge = bridge
        self.member_lengths = member_lengths
        self.member_group = member_group
        self.n_nodes = n_nodes
        self.span_m = span_m
        self.penalty_mul = penalty_multiplier
        self.eval_count = 0

    def evaluate(
        self, gene: np.ndarray
    ) -> tuple[float, float, float]:
        """
        gene: [sec_idx_1, ..., sec_idx_G]  -- 1-tabanli tamsayi vektoru

        Doner:
          f1          : Yapisal agirlik [kN]
          f2          : Gomulu karbon   [kg CO2e]
          penalty     : Toplam ceza (ISO 22156 ihlalleri)
        """
        gene_int = [int(round(g)) for g in gene]
        gene_int = [max(1, min(g, len(BAMBOO_CATALOG))) for g in gene_int]

        try:
            self.bridge.update_sections(gene_int, BAMBOO_CATALOG)
            axial, disp = self.bridge.run_analysis_and_read()
        except Exception as exc:
            logger.error("SAP2000 analiz hatasi: %s", exc)
            return 1e9, 1e9, 1e6

        self.eval_count += 1

        # f1: Yapisal agirlik
        f1 = compute_structural_weight(
            gene_int, BAMBOO_CATALOG, self.member_lengths, self.member_group
        )

        # f2: Gomulu karbon
        total_ec, _, _ = compute_embodied_carbon(
            gene_int, BAMBOO_CATALOG,
            self.member_lengths, self.member_group, self.n_nodes
        )
        f2 = total_ec

        # Kisit cezasi
        pen, max_dc, _ = evaluate_all_members(
            axial, self.member_lengths, self.member_group,
            gene_int, BAMBOO_CATALOG, disp,
            span_m=self.span_m,
        )
        penalty = pen * self.penalty_mul

        return f1, f2, penalty


# ---------------------------------------------------------------------------
# NSGA-II
# ---------------------------------------------------------------------------

class NSGA2:
    """
    Deb et al. (2002) NSGA-II -- Ikili Turnuva + SBX Crossover + Polinom Mutasyon.
    Ayrık kesit uzayi icin: gercek sayili olusturup yuvarlama yapilir.
    """

    def __init__(
        self,
        evaluator: FitnessEvaluator,
        n_groups: int,
        n_sections: int = 24,
        pop_size: int = 40,
        n_gen: int = 100,
        eta_c: float = 10.0,     # SBX dagılım indeksi
        eta_m: float = 20.0,     # Polinom mutasyon dagılım indeksi
        p_cross: float = 0.9,
        p_mut: float = None,
        archive_size: int = 200,
        checkpoint_path: str = "checkpoints/nsga2.json",
    ):
        self.ev = evaluator
        self.n_groups = n_groups
        self.n_sec = n_sections
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.eta_c = eta_c
        self.eta_m = eta_m
        self.p_cross = p_cross
        self.p_mut = 1.0 / n_groups if p_mut is None else p_mut
        self.archive_size = archive_size
        self.ckpt = CheckpointManager(checkpoint_path)
        self.lb = np.ones(n_groups)
        self.ub = np.full(n_groups, n_sections, dtype=float)

    # ---- Baslangic Populasyonu ----
    def _init_pop(self) -> np.ndarray:
        return np.random.uniform(self.lb, self.ub, (self.pop_size, self.n_groups))

    # ---- SBX Crossover ----
    def _sbx(self, p1: np.ndarray, p2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        c1, c2 = p1.copy(), p2.copy()
        for i in range(self.n_groups):
            if random.random() > self.p_cross:
                continue
            if abs(p1[i] - p2[i]) < 1e-9:
                continue
            u = random.random()
            if u <= 0.5:
                beta = (2 * u) ** (1.0 / (self.eta_c + 1))
            else:
                beta = (1.0 / (2 * (1 - u))) ** (1.0 / (self.eta_c + 1))
            c1[i] = 0.5 * ((1 + beta) * p1[i] + (1 - beta) * p2[i])
            c2[i] = 0.5 * ((1 - beta) * p1[i] + (1 + beta) * p2[i])
        return np.clip(c1, self.lb, self.ub), np.clip(c2, self.lb, self.ub)

    # ---- Polinom Mutasyon ----
    def _polynomial_mutation(self, x: np.ndarray) -> np.ndarray:
        x = x.copy()
        for i in range(self.n_groups):
            if random.random() > self.p_mut:
                continue
            delta = self.ub[i] - self.lb[i]
            u = random.random()
            if u < 0.5:
                delta_q = (2 * u) ** (1.0 / (self.eta_m + 1)) - 1
            else:
                delta_q = 1 - (2 * (1 - u)) ** (1.0 / (self.eta_m + 1))
            x[i] += delta * delta_q
        return np.clip(x, self.lb, self.ub)

    # ---- Ana Dongu ----
    def run(self, bridge, start_iter: int = 1) -> tuple[list, list]:
        pop = self._init_pop()
        # Checkpoint yukle
        state = self.ckpt.load()
        archive_sol, archive_obj = [], []
        if state:
            start_iter = state["iter"] + 1
            pop = np.array(state["population"])
            archive_sol = state.get("archive_sol", [])
            archive_obj = state.get("archive_obj", [])
            logger.info("NSGA-II devam ediyor: iter=%d", start_iter)

        # Ilk populasyon degerlendir
        objectives = np.full((self.pop_size, 2), np.inf)
        penalties  = np.zeros(self.pop_size)
        for i in range(self.pop_size):
            f1, f2, p = self.ev.evaluate(pop[i])
            objectives[i] = [f1 + p, f2 + p]
            penalties[i] = p
            bridge.watchdog(self.ev.eval_count)

        for gen in range(start_iter, self.n_gen + 1):
            logger.info("NSGA-II Gen %d / %d  (evals=%d)", gen, self.n_gen, self.ev.eval_count)

            # Cocuk uret
            offspring = []
            idx_list = list(range(self.pop_size))
            random.shuffle(idx_list)
            for i in range(0, self.pop_size, 2):
                a, b = idx_list[i], idx_list[min(i+1, self.pop_size-1)]
                c1, c2 = self._sbx(pop[a], pop[b])
                offspring.append(self._polynomial_mutation(c1))
                offspring.append(self._polynomial_mutation(c2))

            offspring = np.array(offspring[:self.pop_size])
            off_obj = np.full((self.pop_size, 2), np.inf)
            for i in range(self.pop_size):
                f1, f2, p = self.ev.evaluate(offspring[i])
                off_obj[i] = [f1 + p, f2 + p]
                archive_sol, archive_obj = update_archive(
                    archive_sol, archive_obj, offspring[i],
                    np.array([f1, f2]), self.archive_size
                )
                bridge.watchdog(self.ev.eval_count)

            # Birles + sirala + sec
            combined_pop = np.vstack([pop, offspring])
            combined_obj = np.vstack([objectives, off_obj])
            front0 = non_dominated_sort_front0(combined_obj)
            if len(front0) >= self.pop_size:
                cd = crowding_distance(combined_obj[front0])
                sorted_f0 = [front0[j] for j in np.argsort(-cd)[:self.pop_size]]
                pop = combined_pop[sorted_f0]
                objectives = combined_obj[sorted_f0]
            else:
                pop = combined_pop[:self.pop_size]
                objectives = combined_obj[:self.pop_size]

            # Checkpoint kaydet
            self.ckpt.save({
                "iter": gen,
                "population": pop.tolist(),
                "archive_sol": [s.tolist() for s in archive_sol],
                "archive_obj": archive_obj,
            })

        self.ckpt.delete()
        return archive_sol, archive_obj


# ---------------------------------------------------------------------------
# MOABC
# ---------------------------------------------------------------------------

class MOABC:
    """
    Karaboga & Akay (2011) -- Multi-Objective Artificial Bee Colony.
    Ucak ari → Izci ari → Izleyici ari donguleri + Pareto arsiv.
    """

    def __init__(
        self,
        evaluator: FitnessEvaluator,
        n_groups: int,
        n_sections: int = 24,
        colony_size: int = 40,   # Toplam kovan buyuklugu (ucak+izleyici)
        n_cycles: int = 100,
        limit: int = None,        # Terk siniri (n_groups * colony_size/2)
        archive_size: int = 200,
        checkpoint_path: str = "checkpoints/moabc.json",
    ):
        self.ev = evaluator
        self.n_groups = n_groups
        self.n_sec = n_sections
        self.colony = colony_size
        self.n_food = colony_size // 2      # Ucak ari sayisi
        self.n_cycles = n_cycles
        self.limit = limit if limit else n_groups * self.n_food
        self.archive_size = archive_size
        self.ckpt = CheckpointManager(checkpoint_path)
        self.lb = np.ones(n_groups)
        self.ub = np.full(n_groups, n_sections, dtype=float)

    def _rand_sol(self) -> np.ndarray:
        return np.random.uniform(self.lb, self.ub, self.n_groups)

    def _neighbor(self, xi: np.ndarray, xk: np.ndarray) -> np.ndarray:
        """Komsu cozum uret (ABC'nin standart neighbor operatoru)."""
        phi = np.random.uniform(-1, 1, self.n_groups)
        j = random.randint(0, self.n_groups - 1)
        mask = np.zeros(self.n_groups)
        mask[j] = 1.0
        v = xi + phi * (xi - xk) * mask
        return np.clip(v, self.lb, self.ub)

    def run(self, bridge) -> tuple[list, list]:
        state = self.ckpt.load()
        archive_sol, archive_obj = [], []
        start_cycle = 1

        food = np.array([self._rand_sol() for _ in range(self.n_food)])
        f_obj = np.full((self.n_food, 2), np.inf)
        trial = np.zeros(self.n_food, dtype=int)

        if state:
            start_cycle = state["iter"] + 1
            food = np.array(state["food"])
            f_obj = np.array(state["food_obj"])
            trial = np.array(state["trial"])
            archive_sol = state.get("archive_sol", [])
            archive_obj = state.get("archive_obj", [])
            logger.info("MOABC devam ediyor: cycle=%d", start_cycle)
        else:
            # Ilk yiyecek kaynagi degerlendir
            for i in range(self.n_food):
                f1, f2, p = self.ev.evaluate(food[i])
                f_obj[i] = [f1 + p, f2 + p]
                archive_sol, archive_obj = update_archive(
                    archive_sol, archive_obj, food[i], np.array([f1, f2]), self.archive_size
                )
                bridge.watchdog(self.ev.eval_count)

        for cycle in range(start_cycle, self.n_cycles + 1):
            logger.info("MOABC Cycle %d / %d  (evals=%d)", cycle, self.n_cycles, self.ev.eval_count)

            # -- Ucak Arisi Asamasi --
            for i in range(self.n_food):
                k = random.choice([j for j in range(self.n_food) if j != i])
                v = self._neighbor(food[i], food[k])
                f1, f2, p = self.ev.evaluate(v)
                v_obj = np.array([f1 + p, f2 + p])
                if dominates(v_obj, f_obj[i]):
                    food[i] = v
                    f_obj[i] = v_obj
                    trial[i] = 0
                    archive_sol, archive_obj = update_archive(
                        archive_sol, archive_obj, v, np.array([f1, f2]), self.archive_size
                    )
                else:
                    trial[i] += 1
                bridge.watchdog(self.ev.eval_count)

            # -- Izleyici Arisi Asamasi (fitness orantili secim) --
            fit = np.array([1.0 / (1.0 + max(0, np.sum(fo))) for fo in f_obj])
            fit_sum = fit.sum()
            probs = fit / fit_sum if fit_sum > 0 else np.ones(self.n_food) / self.n_food

            for _ in range(self.n_food):
                i = np.random.choice(self.n_food, p=probs)
                k = random.choice([j for j in range(self.n_food) if j != i])
                v = self._neighbor(food[i], food[k])
                f1, f2, p = self.ev.evaluate(v)
                v_obj = np.array([f1 + p, f2 + p])
                if dominates(v_obj, f_obj[i]):
                    food[i] = v
                    f_obj[i] = v_obj
                    trial[i] = 0
                    archive_sol, archive_obj = update_archive(
                        archive_sol, archive_obj, v, np.array([f1, f2]), self.archive_size
                    )
                else:
                    trial[i] += 1
                bridge.watchdog(self.ev.eval_count)

            # -- Izci Arisi Asamasi (terk siniri asanlari yenile) --
            for i in range(self.n_food):
                if trial[i] >= self.limit:
                    food[i] = self._rand_sol()
                    f1, f2, p = self.ev.evaluate(food[i])
                    f_obj[i] = [f1 + p, f2 + p]
                    trial[i] = 0
                    archive_sol, archive_obj = update_archive(
                        archive_sol, archive_obj, food[i], np.array([f1, f2]), self.archive_size
                    )
                    bridge.watchdog(self.ev.eval_count)

            # Checkpoint
            self.ckpt.save({
                "iter": cycle,
                "food": food.tolist(),
                "food_obj": f_obj.tolist(),
                "trial": trial.tolist(),
                "archive_sol": [s.tolist() for s in archive_sol],
                "archive_obj": archive_obj,
            })

        self.ckpt.delete()
        return archive_sol, archive_obj


# ---------------------------------------------------------------------------
# MODBO -- Multi-Objective Dung Beetle Optimizer (Xue & Shen 2022)
# ---------------------------------------------------------------------------

class MODBO:
    """
    Xue & Shen (2022) Dung Beetle Optimizer -- Cok Amacli Versiyonu.
    Yuvarlama bobekleri (rulo itme), bes arama yolu:
      - Boku iten bobek (Rulo itici): Levy ucusu
      - Yuvaya saplanmis bobek: iteratif optimizasyon
      - Izci bobek: global en iyi yakininda arama
      - Hirdavat (calici) bobek: yerel arama
    """

    def __init__(
        self,
        evaluator: FitnessEvaluator,
        n_groups: int,
        n_sections: int = 24,
        pop_size: int = 40,
        n_gen: int = 100,
        archive_size: int = 200,
        checkpoint_path: str = "checkpoints/modbo.json",
    ):
        self.ev = evaluator
        self.n_groups = n_groups
        self.n_sec = n_sections
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.archive_size = archive_size
        self.ckpt = CheckpointManager(checkpoint_path)
        self.lb = np.ones(n_groups)
        self.ub = np.full(n_groups, n_sections, dtype=float)

    def _levy(self, beta: float = 1.5) -> np.ndarray:
        from math import gamma
        sigma = (gamma(1+beta)*np.sin(np.pi*beta/2) /
                 (gamma((1+beta)/2)*beta*2**((beta-1)/2))) ** (1/beta)
        u = np.random.randn(self.n_groups) * sigma
        v = np.abs(np.random.randn(self.n_groups))
        return u / (v ** (1/beta))

    def _clip(self, x: np.ndarray) -> np.ndarray:
        return np.clip(x, self.lb, self.ub)

    def _global_best(self, archive_sol: list) -> np.ndarray:
        if archive_sol:
            return np.array(random.choice(archive_sol), dtype=float)
        return np.random.uniform(self.lb, self.ub, self.n_groups)

    def run(self, bridge) -> tuple[list, list]:
        state = self.ckpt.load()
        archive_sol, archive_obj = [], []
        start_gen = 1
        pop = np.random.uniform(self.lb, self.ub, (self.pop_size, self.n_groups))
        f_obj = np.full((self.pop_size, 2), np.inf)

        if state:
            start_gen = state["iter"] + 1
            pop = np.array(state["population"])
            f_obj = np.array(state["pop_obj"])
            archive_sol = state.get("archive_sol", [])
            archive_obj = state.get("archive_obj", [])
            logger.info("MODBO devam ediyor: gen=%d", start_gen)
        else:
            for i in range(self.pop_size):
                f1, f2, p = self.ev.evaluate(pop[i])
                f_obj[i] = [f1 + p, f2 + p]
                archive_sol, archive_obj = update_archive(
                    archive_sol, archive_obj, pop[i], np.array([f1, f2]), self.archive_size
                )
                bridge.watchdog(self.ev.eval_count)

        for gen in range(start_gen, self.n_gen + 1):
            logger.info("MODBO Gen %d / %d  (evals=%d)", gen, self.n_gen, self.ev.eval_count)
            t_ratio = gen / self.n_gen   # [0,1]
            x_best = self._global_best(archive_sol)

            new_pop = pop.copy()

            for i in range(self.pop_size):
                role = i % 4  # 0=roller, 1=nest, 2=scout, 3=thief
                if role == 0:
                    # Yuvarlanici: Levy ucusu
                    x_new = pop[i] + self._levy() * (pop[i] - x_best)
                elif role == 1:
                    # Yuvaya saplanmis: lokal iterasyon
                    r1 = np.random.rand(self.n_groups)
                    x_new = pop[i] + r1 * (x_best - pop[i]) * (1 - t_ratio)
                elif role == 2:
                    # Izci: global en iyi yakininda
                    r2 = np.random.randn(self.n_groups)
                    x_new = x_best + 0.1 * r2 * (pop[i] - x_best)
                else:
                    # Hirsiz: rassal yerel pertuerbasyon
                    x_r = pop[random.randint(0, self.pop_size - 1)]
                    r3 = np.random.rand(self.n_groups)
                    x_new = pop[i] + r3 * (x_r - pop[i])

                x_new = self._clip(x_new)
                f1, f2, p = self.ev.evaluate(x_new)
                v_obj = np.array([f1 + p, f2 + p])
                archive_sol, archive_obj = update_archive(
                    archive_sol, archive_obj, x_new, np.array([f1, f2]), self.archive_size
                )
                if dominates(v_obj, f_obj[i]):
                    new_pop[i] = x_new
                    f_obj[i] = v_obj
                bridge.watchdog(self.ev.eval_count)

            pop = new_pop
            self.ckpt.save({
                "iter": gen,
                "population": pop.tolist(),
                "pop_obj": f_obj.tolist(),
                "archive_sol": [s.tolist() for s in archive_sol],
                "archive_obj": archive_obj,
            })

        self.ckpt.delete()
        return archive_sol, archive_obj
