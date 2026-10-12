"""
metaheuristic_optimizers.py
Tek Amacli Meta-Sezgisel Optimizasyon Motoru (16 Algoritma)
============================================================
Bambu Kubbe Yapisal Agirlik Minimizasyonu: min f = W * (1 + P)^epsilon

Desteklenen 16 Algoritma:
 1. HS   - Harmony Search (Geem et al. 2001)
 2. BBO  - Biogeography-Based Optimization (Simon 2008)
 3. WOA  - Whale Optimization Algorithm (Mirjalili & Lewis 2016)
 4. DO   - Dandelion Optimizer (Zhao et al. 2022)
 5. ABC  - Artificial Bee Colony (Karaboga 2005)
 6. ACO  - Ant Colony Optimization (Camp & Bichon 2004)
 7. BSO  - Brain Storm Optimization (Shi 2011)
 8. CSA  - Crow Search Algorithm (Askarzadeh 2016)
 9. FA   - Firefly Algorithm (Yang 2008)
10. GOA  - Grasshopper Optimization Algorithm (Saremi et al. 2017)
11. TLBO - Teaching-Learning-Based Optimization (Rao et al. 2011)
12. TSA  - Tree-Seed Algorithm (Kiran 2015)
13. GWO  - Grey Wolf Optimizer (Mirjalili et al. 2014)
14. HBA  - Honey Badger Algorithm (Hashim et al. 2022)
15. AO   - Aquila Optimizer (Abualigah et al. 2021)
16. SSO  - Social Spider Optimization (Cuevas et al. 2013)
"""

from __future__ import annotations
import math
import os
import pickle
import random
from dataclasses import dataclass, field
from typing import Callable, Any

import numpy as np


@dataclass
class Member:
    design_variables: np.ndarray          # 1-tabanli tamsayi kesit indeksleri (NVar,)
    cost_value: float = math.inf          # Yapisal agirlik W [kN]
    carbon_value: float = math.inf        # Gomulu karbon [kg CO2e]
    penalty: float = math.inf             # Toplam normalize kisit ihlali P
    penalized_cost: float = math.inf      # W * (1 + P)^epsilon
    is_feasible: bool = False

    def copy(self) -> Member:
        return Member(
            design_variables=self.design_variables.copy(),
            cost_value=self.cost_value,
            carbon_value=self.carbon_value,
            penalty=self.penalty,
            penalized_cost=self.penalized_cost,
            is_feasible=self.is_feasible,
        )


ALGORITHM_NAMES = {
    "hs": "Harmony Search (HS)",
    "bbo": "Biogeography-Based Optimization (BBO)",
    "woa": "Whale Optimization Algorithm (WOA)",
    "do": "Dandelion Optimizer (DO)",
    "abc": "Artificial Bee Colony (ABC)",
    "aco": "Ant Colony Optimization (ACO)",
    "bso": "Brain Storm Optimization (BSO)",
    "csa": "Crow Search Algorithm (CSA)",
    "fa": "Firefly Algorithm (FA)",
    "goa": "Grasshopper Optimization Algorithm (GOA)",
    "tlbo": "Teaching-Learning-Based Optimization (TLBO)",
    "tsa": "Tree-Seed Algorithm (TSA)",
    "gwo": "Grey Wolf Optimizer (GWO)",
    "hba": "Honey Badger Algorithm (HBA)",
    "ao": "Aquila Optimizer (AO)",
    "sso": "Social Spider Optimization (SSO)",
}


class OptimizationPaused(Exception):
    """stop_check() True dondu: durum iterasyon sinirinda checkpoint'e yazildi, devam edilebilir."""


class BudgetExhausted(Exception):
    """Degerlendirme (NFE) butcesi doldu; arama temiz sekilde sonlandirilir."""


# Iterasyon basina ortalama degerlendirme / pop_size (olculen). Butce esitlemesinde
# iterasyon-tabanli programlarin (WOA, GWO, AO ...) tam butceye yayilmasi icin kullanilir.
EVALS_PER_ITER_FACTOR = {"tlbo": 2.0, "abc": 2.0, "tsa": 3.5}


def iters_for_budget(method: str, pop_size: int, max_evals: int) -> int:
    f = EVALS_PER_ITER_FACTOR.get(method.lower(), 1.0)
    return max(1, int((max_evals - pop_size) // (pop_size * f)))


class MetaheuristicOptimizer:
    """16 algoritmayi barindiran tek amacli meta-sezgisel optimizasyon calistiricisi."""

    def __init__(
        self,
        eval_fn: Callable[[np.ndarray], tuple[float, float, float]],
        n_vars: int,
        lb: int = 1,
        ub: int = 24,
        pop_size: int = 40,
        max_iters: int = 100,
        penalty_exp: float = 2.0,
        seed: int | None = None,
        method: str = "abc",
        params: dict[str, Any] | None = None,
        max_evals: int | None = None,
        ckpt_path: str | None = None,
        log_prefix: str | None = None,
        ckpt_every_evals: int = 2000,
        stop_check: Callable[[], bool] | None = None,
    ):
        self.ckpt_path = ckpt_path
        self.log_prefix = log_prefix
        self.ckpt_every_evals = ckpt_every_evals
        self.stop_check = stop_check
        self._buf: list = []
        self._last_ckpt = 0
        self._it = 0
        self._done = False
        self.max_evals = max_evals
        if max_evals is not None:                 # esit NFE butcesi: iterasyon sayisi butceden turetilir
            max_iters = iters_for_budget(method, pop_size, max_evals)
        self.eval_fn = eval_fn
        self.n_vars = n_vars
        self.lb = np.full(n_vars, lb, dtype=int)
        self.ub = np.full(n_vars, ub, dtype=int)
        self.pop_size = pop_size
        self.max_iters = max_iters
        self.penalty_exp = penalty_exp
        self.method = method.lower()
        self.params = params or {}
        self.seed = seed

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.memory: list[Member] = []
        self.global_best: Member | None = None
        self.best_value: float = math.inf
        self.history: list[dict[str, Any]] = []
        self.n_evals: int = 0
        self.current_iter: int = 0

        # Algoritmaya ozel ic durumlar (AlgorithmState)
        self._init_method_state()

    def _clip(self, x: np.ndarray) -> np.ndarray:
        return np.clip(np.round(x).astype(int), self.lb, self.ub)

    def _random_variable(self, d: int) -> int:
        return random.randint(int(self.lb[d]), int(self.ub[d]))

    def _random_member(self) -> Member:
        vars_arr = np.array([self._random_variable(d) for d in range(self.n_vars)], dtype=int)
        return Member(design_variables=vars_arr)

    def evaluate_member(self, member: Member) -> None:
        """Kisit ve agirlik degerlendir, cezali maliyeti hesapla."""
        member.design_variables = self._clip(member.design_variables)
        if self.max_evals is not None and self.n_evals >= self.max_evals:
            raise BudgetExhausted()
        w, co2, p = self.eval_fn(member.design_variables)
        self.n_evals += 1
        if self.log_prefix:
            self._buf.append((member.design_variables.astype(np.int8), float(w), float(co2), float(p)))
        member.cost_value = float(w)
        member.carbon_value = float(co2)
        member.penalty = float(p)
        member.penalized_cost = float(w * ((1.0 + p) ** self.penalty_exp))
        member.is_feasible = (p <= 1e-6)

        # Global best ve history takibi
        if member.penalized_cost < self.best_value:
            self.best_value = member.penalized_cost

        if member.is_feasible:
            if self.global_best is None or member.cost_value < self.global_best.cost_value:
                self.global_best = member.copy()

    def _leader(self) -> Member:
        """En iyi bilinen cozum (varsa feasible global best, yoksa en dusuk cezali maliyet)."""
        if self.global_best is not None and self.global_best.is_feasible:
            return self.global_best
        best = self.memory[0]
        for m in self.memory[1:]:
            if m.penalized_cost < best.penalized_cost:
                best = m
        return best

    def _eval_at(self, cand: Member, target_idx: int, greedy: bool = True) -> bool:
        """Yeni adayi degerlendir; greedy ise yalniz daha iyiyse hedefin yerine koy."""
        self.evaluate_member(cand)
        replace = (not greedy) or (cand.penalized_cost < self.memory[target_idx].penalized_cost)
        if replace:
            self.memory[target_idx] = cand
        return replace

    def _roulette_wheel(self, weights: np.ndarray) -> int:
        s = float(weights.sum())
        if s <= 0:
            return random.randint(0, len(weights) - 1)
        r = random.random() * s
        acc = 0.0
        for i, w in enumerate(weights):
            acc += w
            if r <= acc:
                return i
        return len(weights) - 1

    def _random_other(self, i: int) -> int:
        if self.pop_size <= 1:
            return i
        k = random.randint(0, self.pop_size - 1)
        while k == i:
            k = random.randint(0, self.pop_size - 1)
        return k

    def _levy_step(self, beta: float = 1.5) -> float:
        """Mantegna algoritmasi ile Levy adimi."""
        num = math.gamma(1.0 + beta) * math.sin(math.pi * beta / 2.0)
        den = math.gamma((1.0 + beta) / 2.0) * beta * (2.0 ** ((beta - 1.0) / 2.0))
        sigma_u = (num / den) ** (1.0 / beta)
        u = random.gauss(0.0, sigma_u)
        v = max(abs(random.gauss(0.0, 1.0)), 1e-6)
        return u / (v ** (1.0 / beta))

    # -------------------------------------------------------------------------
    # Baslangic Populasyonu
    # -------------------------------------------------------------------------
    def initialize_population(self) -> None:
        self.memory = []
        for _ in range(self.pop_size):
            m = self._random_member()
            self.evaluate_member(m)
            self.memory.append(m)

        # Ilk lider kontrolu
        for m in self.memory:
            if m.is_feasible:
                if self.global_best is None or m.cost_value < self.global_best.cost_value:
                    self.global_best = m.copy()

    def _init_method_state(self) -> None:
        self.abc_trials = np.zeros(self.pop_size, dtype=int)
        self.aco_pheromone = [np.ones(int(self.ub[d] + 1), dtype=float) for d in range(self.n_vars)]
        self.gwo_leaders: list[Member] = []
        self.bso_clusters: list[list[int]] = []
        self.bso_centers: list[np.ndarray] = []

    # -------------------------------------------------------------------------
    # 1. HARMONY SEARCH (HS)
    # -------------------------------------------------------------------------
    def _step_hs(self, imem: int) -> None:
        hmcr = self.params.get("hmcr", 0.90)
        par = self.params.get("par", 0.60)
        pitch_bw = self.params.get("pitch_bandwidth", 0.01)

        new_vars = np.zeros(self.n_vars, dtype=int)
        for d in range(self.n_vars):
            if random.random() > hmcr:
                new_vars[d] = self._random_variable(d)
            else:
                rand_id = random.randint(0, self.pop_size - 1)
                val = self.memory[rand_id].design_variables[d]
                if random.random() <= par:
                    bw = max(1, int(round(pitch_bw * (self.ub[d] - self.lb[d]))))
                    step = random.randint(1, bw)
                    val += -step if random.random() < 0.5 else step
                new_vars[d] = val

        cand = Member(design_variables=new_vars)
        worst_idx = max(range(self.pop_size), key=lambda i: self.memory[i].penalized_cost)
        self._eval_at(cand, worst_idx, greedy=True)

    # -------------------------------------------------------------------------
    # 2. BIOGEOGRAPHY-BASED OPTIMIZATION (BBO)
    # -------------------------------------------------------------------------
    def _step_bbo(self, imem: int) -> None:
        mutation_rate = self.params.get("mutation_rate", 0.10)
        # Habitat siralamasina gore goc oranlari
        mu = np.array([(self.pop_size - i) / self.pop_size for i in range(self.pop_size)])
        lam = 1.0 - mu

        new_vars = self.memory[imem].design_variables.copy()
        for d in range(self.n_vars):
            if random.random() < lam[imem]:
                sel = self._roulette_wheel(mu)
                new_vars[d] = self.memory[sel].design_variables[d]
            if random.random() < mutation_rate:
                new_vars[d] = self._random_variable(d)

        cand = Member(design_variables=new_vars)
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 3. WHALE OPTIMIZATION ALGORITHM (WOA)
    # -------------------------------------------------------------------------
    def _step_woa(self, imem: int) -> None:
        t = self.current_iter
        max_t = self.max_iters
        a1 = 2.0 - t * (2.0 / max_t)
        a2 = -1.0 + t * (-1.0 / max_t)
        lead = self._leader().design_variables

        new_vars = np.zeros(self.n_vars, dtype=float)
        cur = self.memory[imem].design_variables
        for d in range(self.n_vars):
            A = 2.0 * a1 * random.random() - a1
            C = 2.0 * random.random()
            b = 1.0
            l1 = (a2 - 1.0) * random.random() + 1.0

            if random.random() < 0.5:
                if abs(A) >= 1.0:
                    x_rand = self.memory[random.randint(0, self.pop_size - 1)].design_variables
                    d_x = abs(C * x_rand[d] - cur[d])
                    new_vars[d] = x_rand[d] - A * d_x
                else:
                    d_lead = abs(C * lead[d] - cur[d])
                    new_vars[d] = lead[d] - A * d_lead
            else:
                dist = abs(lead[d] - cur[d])
                new_vars[d] = dist * math.exp(b * l1) * math.cos(l1 * 2.0 * math.pi) + lead[d]

        cand = Member(design_variables=self._clip(new_vars))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 4. DANDELION OPTIMIZER (DO)
    # -------------------------------------------------------------------------
    def _step_do(self, imem: int) -> None:
        T = max(self.max_iters, 2)
        it = self.current_iter
        alpha = random.random() * ((1.0 / T**2) * it**2 - 2.0 / T * it + 1.0)
        a = -1.0 / (T**2 - 2.0 * T + 1.0)
        b = -2.0 * a
        c = 1.0 - a - b
        k = 1.0 - random.random() * (c + a * it**2 + b * it)

        x = self.memory[imem].design_variables.astype(float).copy()
        # Rising stage
        for d in range(self.n_vars):
            if random.gauss(0, 1) < 1.5:
                theta = (2.0 * random.random() - 1.0) * math.pi
                row = math.exp(-theta)
                vx = row * math.cos(theta)
                vy = row * math.sin(theta)
                newv = random.uniform(self.lb[d], self.ub[d])
                x[d] += alpha * vx * vy * (newv - x[d])
            else:
                x[d] *= k

        # Decline stage
        d_mean = np.mean([m.design_variables for m in self.memory], axis=0)
        beta = random.gauss(0, 1)
        x = x - beta * alpha * (d_mean - beta * alpha * x)

        # Landing stage
        lead = self._leader().design_variables.astype(float)
        step_l = self._levy_step(1.5) * 0.1
        x = lead + step_l * alpha * (lead - x * (2.0 * it / T))

        cand = Member(design_variables=self._clip(x))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 5. ARTIFICIAL BEE COLONY (ABC)
    # -------------------------------------------------------------------------
    def _step_abc(self, imem: int) -> None:
        limit = self.params.get("limit", self.pop_size * self.n_vars)
        mr = self.params.get("mr", 0.0)

        # Employed bee
        k = self._random_other(imem)
        cand_vars = self.memory[imem].design_variables.copy()
        one_d = random.randint(0, self.n_vars - 1)
        for d in range(self.n_vars):
            if (mr > 0 and random.random() < mr) or d == one_d:
                phi = 2.0 * random.random() - 1.0
                v = int(round(cand_vars[d] + phi * (cand_vars[d] - self.memory[k].design_variables[d])))
                if v == cand_vars[d]:
                    v += -1 if random.random() < 0.5 else 1
                cand_vars[d] = v

        cand = Member(design_variables=self._clip(cand_vars))
        if self._eval_at(cand, imem, greedy=True):
            self.abc_trials[imem] = 0
        else:
            self.abc_trials[imem] += 1

        # Onlooker bee
        fits = np.array([1.0 / (1.0 + max(m.penalized_cost, 0.0)) for m in self.memory])
        onlooker_idx = self._roulette_wheel(fits)
        k2 = self._random_other(onlooker_idx)
        cand_vars2 = self.memory[onlooker_idx].design_variables.copy()
        one_d2 = random.randint(0, self.n_vars - 1)
        for d in range(self.n_vars):
            if (mr > 0 and random.random() < mr) or d == one_d2:
                phi = 2.0 * random.random() - 1.0
                v = int(round(cand_vars2[d] + phi * (cand_vars2[d] - self.memory[k2].design_variables[d])))
                if v == cand_vars2[d]:
                    v += -1 if random.random() < 0.5 else 1
                cand_vars2[d] = v

        cand2 = Member(design_variables=self._clip(cand_vars2))
        if self._eval_at(cand2, onlooker_idx, greedy=True):
            self.abc_trials[onlooker_idx] = 0
        else:
            self.abc_trials[onlooker_idx] += 1

        # Scout bee
        if self.abc_trials[imem] > limit:
            scout_cand = self._random_member()
            self._eval_at(scout_cand, imem, greedy=False)
            self.abc_trials[imem] = 0

    # -------------------------------------------------------------------------
    # 6. ANT COLONY OPTIMIZATION (ACO)
    # -------------------------------------------------------------------------
    def _step_aco(self, imem: int) -> None:
        alpha = self.params.get("alpha", 1.0)
        beta = self.params.get("beta", 0.5)
        rho = self.params.get("rho", 0.2)
        elite_frac = self.params.get("elite", 0.2)

        # Buharlasma ve feromon guncelleme (dongu basinda imem == 0)
        if imem == 0:
            for d in range(self.n_vars):
                self.aco_pheromone[d] = np.maximum((1.0 - rho) * self.aco_pheromone[d], 0.01)

            w_count = max(1, int(round(elite_frac * self.pop_size)))
            ranked = sorted(self.memory, key=lambda m: m.penalized_cost)[:w_count]
            if ranked:
                best_cost = max(ranked[0].penalized_cost, 1e-12)
                for r, m in enumerate(ranked):
                    amt = (w_count - r) / float(w_count) * (best_cost / max(m.penalized_cost, 1e-12))
                    for d in range(self.n_vars):
                        s = int(m.design_variables[d])
                        if 0 <= s < len(self.aco_pheromone[d]):
                            self.aco_pheromone[d][s] += amt

        # Karinca yeni yol secer
        cand_vars = np.zeros(self.n_vars, dtype=int)
        for d in range(self.n_vars):
            low, high = int(self.lb[d]), int(self.ub[d])
            weights = np.zeros(high - low + 1, dtype=float)
            for idx, s in enumerate(range(low, high + 1)):
                # Heuristic: kucuk kesit tercihi (1 / s)
                heuristic = 1.0 / max(s, 1)
                weights[idx] = (self.aco_pheromone[d][s] ** alpha) * (heuristic ** beta)
            chosen_offset = self._roulette_wheel(weights)
            cand_vars[d] = low + chosen_offset

        cand = Member(design_variables=cand_vars)
        worst_idx = max(range(self.pop_size), key=lambda i: self.memory[i].penalized_cost)
        self._eval_at(cand, worst_idx, greedy=True)

    # -------------------------------------------------------------------------
    # 7. BRAIN STORM OPTIMIZATION (BSO)
    # -------------------------------------------------------------------------
    def _step_bso(self, imem: int) -> None:
        p_one = self.params.get("p_one", 0.8)
        p_replace = self.params.get("p_replace", 0.2)
        step_scale = self.params.get("step_scale", 0.1)

        # K-means kumeleme (imem == 0 ise)
        if imem == 0 or not self.bso_centers:
            k = max(2, min(5, self.pop_size))
            centers = [self.memory[i].design_variables.astype(float).copy() for i in range(k)]
            for _ in range(5):
                clusters = [[] for _ in range(k)]
                for i, m in enumerate(self.memory):
                    dists = [np.linalg.norm(m.design_variables - c) for c in centers]
                    clusters[int(np.argmin(dists))].append(i)
                for ci, cl in enumerate(clusters):
                    if cl:
                        centers[ci] = np.mean([self.memory[idx].design_variables for idx in cl], axis=0)
            self.bso_centers = centers
            self.bso_clusters = clusters

        if random.random() < p_one or len(self.bso_centers) < 2:
            c_idx = random.randint(0, len(self.bso_centers) - 1)
            base = self.bso_centers[c_idx].copy()
        else:
            c1, c2 = random.sample(range(len(self.bso_centers)), 2)
            w = random.random()
            base = w * self.bso_centers[c1] + (1.0 - w) * self.bso_centers[c2]

        xi = (1.0 / (1.0 + math.exp(-(0.5 * self.max_iters - self.current_iter) / 20.0))) * random.random()
        noise = xi * np.random.randn(self.n_vars) * step_scale * (self.ub - self.lb)
        cand = Member(design_variables=self._clip(base + noise))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 8. CROW SEARCH ALGORITHM (CSA)
    # -------------------------------------------------------------------------
    def _step_csa(self, imem: int) -> None:
        ap = self.params.get("ap", 0.10)
        fl = self.params.get("fl", 2.0)
        j = self._random_other(imem)

        if random.random() >= ap:
            x = self.memory[imem].design_variables.astype(float)
            mj = self.memory[j].design_variables.astype(float)
            x_new = x + random.random() * fl * (mj - x)
            cand = Member(design_variables=self._clip(x_new))
        else:
            cand = self._random_member()

        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 9. FIREFLY ALGORITHM (FA)
    # -------------------------------------------------------------------------
    def _step_fa(self, imem: int) -> None:
        beta0 = self.params.get("beta0", 1.0)
        betamin = self.params.get("betamin", 0.2)
        gamma = self.params.get("gamma", 15.0)
        damping = self.params.get("damping", 0.97)
        alpha = self.params.get("alpha", 0.2) * (damping ** self.current_iter)

        r_max = np.linalg.norm(self.ub - self.lb)
        x = self.memory[imem].design_variables.astype(float).copy()
        own_cost = self.memory[imem].penalized_cost

        for j in range(self.pop_size):
            if j != imem and self.memory[j].penalized_cost < own_cost:
                xj = self.memory[j].design_variables.astype(float)
                dist = np.linalg.norm(x - xj)
                r_norm = (dist / r_max) if r_max > 0 else 0.0
                beta = (beta0 - betamin) * math.exp(-gamma * (r_norm**2)) + betamin
                x += beta * (xj - x)

        x += alpha * (np.random.rand(self.n_vars) - 0.5) * (self.ub - self.lb)
        cand = Member(design_variables=self._clip(x))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 10. GRASSHOPPER OPTIMIZATION ALGORITHM (GOA)
    # -------------------------------------------------------------------------
    def _step_goa(self, imem: int) -> None:
        c_max = self.params.get("c_max", 1.0)
        c_min = self.params.get("c_min", 0.00004)
        f_int = self.params.get("f", 0.5)
        l_scale = self.params.get("l", 1.5)

        progress = self.current_iter / max(self.max_iters, 1)
        c = c_max - progress * (c_max - c_min)
        xi = self.memory[imem].design_variables.astype(float)

        s_force = np.zeros(self.n_vars, dtype=float)
        for j in range(self.pop_size):
            if j == imem:
                continue
            xj = self.memory[j].design_variables.astype(float)
            dist = np.linalg.norm(xj - xi)
            r = 2.0 + (dist % 2.0)
            s_val = f_int * math.exp(-r / l_scale) - math.exp(-r)
            s_force += c * (self.ub - self.lb) / 2.0 * s_val * (xj - xi) / (dist + 1e-15)

        target = self._leader().design_variables.astype(float)
        x_new = c * s_force + target
        cand = Member(design_variables=self._clip(x_new))
        self._eval_at(cand, imem, greedy=False)

    # -------------------------------------------------------------------------
    # 11. TEACHING-LEARNING-BASED OPTIMIZATION (TLBO)
    # -------------------------------------------------------------------------
    def _step_tlbo(self, imem: int) -> None:
        # 1. Ogretmen Fazi (Teacher Phase)
        teacher = self._leader().design_variables.astype(float)
        mean_x = np.mean([m.design_variables for m in self.memory], axis=0)
        tf = round(1.0 + random.random())
        x = self.memory[imem].design_variables.astype(float).copy()
        x_new = x + random.random() * (teacher - tf * mean_x)
        cand = Member(design_variables=self._clip(x_new))
        self._eval_at(cand, imem, greedy=True)

        # 2. Ogrenci Fazi (Learner Phase)
        j = self._random_other(imem)
        x = self.memory[imem].design_variables.astype(float).copy()
        xj = self.memory[j].design_variables.astype(float)
        better = self.memory[imem].penalized_cost < self.memory[j].penalized_cost
        step = (x - xj) if better else (xj - x)
        x_new2 = x + random.random() * step
        cand2 = Member(design_variables=self._clip(x_new2))
        self._eval_at(cand2, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 12. TREE-SEED ALGORITHM (TSA)
    # -------------------------------------------------------------------------
    def _step_tsa(self, imem: int) -> None:
        st = self.params.get("st", 0.10)
        s_min = self.params.get("seeds_min", 2)
        s_max = self.params.get("seeds_max", 5)
        n_seeds = random.randint(s_min, s_max)

        tree = self.memory[imem].design_variables.astype(float)
        best_tree = self._leader().design_variables.astype(float)

        best_seed: Member | None = None
        for _ in range(n_seeds):
            r = self._random_other(imem)
            x_seed = tree.copy()
            for d in range(self.n_vars):
                alpha = 2.0 * random.random() - 1.0
                if random.random() < st:
                    x_seed[d] = tree[d] + alpha * (best_tree[d] - self.memory[r].design_variables[d])
                else:
                    x_seed[d] = tree[d] + alpha * (tree[d] - self.memory[r].design_variables[d])

            s_cand = Member(design_variables=self._clip(x_seed))
            self.evaluate_member(s_cand)
            if best_seed is None or s_cand.penalized_cost < best_seed.penalized_cost:
                best_seed = s_cand

        if best_seed is not None and best_seed.penalized_cost < self.memory[imem].penalized_cost:
            self.memory[imem] = best_seed

    # -------------------------------------------------------------------------
    # 13. GREY WOLF OPTIMIZER (GWO)
    # -------------------------------------------------------------------------
    def _step_gwo(self, imem: int) -> None:
        a_start = self.params.get("a_start", 2.0)
        progress = self.current_iter / max(self.max_iters, 1)
        a = a_start * (1.0 - progress)

        # Liderler: Alpha, Beta, Delta
        sorted_mem = sorted(self.memory, key=lambda m: m.penalized_cost)
        alpha, beta, delta = sorted_mem[0], sorted_mem[1], sorted_mem[2]

        x = self.memory[imem].design_variables.astype(float)
        x_new = np.zeros(self.n_vars, dtype=float)

        for d in range(self.n_vars):
            # Alpha
            r1, r2 = random.random(), random.random()
            A1 = 2.0 * a * r1 - a
            C1 = 2.0 * r2
            D_alpha = abs(C1 * alpha.design_variables[d] - x[d])
            X1 = alpha.design_variables[d] - A1 * D_alpha

            # Beta
            r1, r2 = random.random(), random.random()
            A2 = 2.0 * a * r1 - a
            C2 = 2.0 * r2
            D_beta = abs(C2 * beta.design_variables[d] - x[d])
            X2 = beta.design_variables[d] - A2 * D_beta

            # Delta
            r1, r2 = random.random(), random.random()
            A3 = 2.0 * a * r1 - a
            C3 = 2.0 * r2
            D_delta = abs(C3 * delta.design_variables[d] - x[d])
            X3 = delta.design_variables[d] - A3 * D_delta

            x_new[d] = (X1 + X2 + X3) / 3.0

        cand = Member(design_variables=self._clip(x_new))
        self._eval_at(cand, imem, greedy=False)

    # -------------------------------------------------------------------------
    # 14. HONEY BADGER ALGORITHM (HBA)
    # -------------------------------------------------------------------------
    def _step_hba(self, imem: int) -> None:
        beta = self.params.get("beta", 6.0)
        c_const = self.params.get("c", 2.0)
        progress = self.current_iter / max(self.max_iters, 1)
        alpha = c_const * math.exp(-progress)

        prey = self._leader().design_variables.astype(float)
        xi = self.memory[imem].design_variables.astype(float)
        xn = self.memory[(imem + 1) % self.pop_size].design_variables.astype(float)
        F = 1.0 if random.random() < 0.5 else -1.0
        digging = (random.random() < 0.5)

        x_new = np.zeros(self.n_vars, dtype=float)
        for d in range(self.n_vars):
            S = (xi[d] - xn[d]) ** 2
            di = prey[d] - xi[d]
            I = min(random.random() * S / (4.0 * math.pi * (di**2) + 1e-10), 1.0)
            if digging:
                card = abs(math.cos(2.0 * math.pi * random.random()) * (1.0 - math.cos(2.0 * math.pi * random.random())))
                x_new[d] = prey[d] + F * beta * I * prey[d] + F * random.random() * alpha * di * card
            else:
                x_new[d] = prey[d] + F * random.random() * alpha * di

        cand = Member(design_variables=self._clip(x_new))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 15. AQUILA OPTIMIZER (AO)
    # -------------------------------------------------------------------------
    def _step_ao(self, imem: int) -> None:
        T = self.max_iters
        t = max(self.current_iter, 1)
        best = self._leader().design_variables.astype(float)
        xm = np.mean([m.design_variables for m in self.memory], axis=0)
        xi = self.memory[imem].design_variables.astype(float)
        x_new = np.zeros(self.n_vars, dtype=float)

        if t <= (2.0 / 3.0) * T:
            if random.random() <= 0.5:
                # High soar with vertical stoop
                r = random.random()
                x_new = best * (1.0 - t / T) + (xm - best * r)
            else:
                # Contour flight with short glide (Levy)
                xr = self.memory[random.randint(0, self.pop_size - 1)].design_variables.astype(float)
                for d in range(self.n_vars):
                    d1 = d + 1
                    rr = 10.0 + 0.00565 * d1
                    th = -0.005 * d1 + 1.5 * math.pi
                    xs = rr * math.sin(th)
                    ys = rr * math.cos(th)
                    x_new[d] = best[d] * self._levy_step() * 0.01 + xr[d] + (ys - xs) * random.random()
        else:
            if random.random() <= 0.5:
                # Low flight with slow descent attack
                al = self.params.get("alpha", 0.1)
                de = self.params.get("delta", 0.1)
                for d in range(self.n_vars):
                    x_new[d] = (best[d] - xm[d]) * al - random.random() + ((self.ub[d] - self.lb[d]) * random.random() + self.lb[d]) * de
            else:
                # Walk and grab prey
                qf = t ** ((2.0 * random.random() - 1.0) / max((1.0 - T)**2, 1))
                g1 = 2.0 * random.random() - 1.0
                g2 = 2.0 * (1.0 - t / T)
                for d in range(self.n_vars):
                    x_new[d] = qf * best[d] - (g1 * xi[d] * random.random()) - g2 * (self._levy_step() * 0.01) + random.random() * g1

        cand = Member(design_variables=self._clip(x_new))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # 16. SOCIAL SPIDER OPTIMIZATION (SSO)
    # -------------------------------------------------------------------------
    def _step_sso(self, imem: int) -> None:
        pf = self.params.get("pf", 0.70)
        radius = self.params.get("radius", 0.50)

        # Agirliklar (fitness)
        worst_cost = max(m.penalized_cost for m in self.memory)
        best_cost = min(m.penalized_cost for m in self.memory)
        span = max(worst_cost - best_cost, 1e-12)
        weights = np.array([(worst_cost - m.penalized_cost) / span for m in self.memory])

        best_spider = self.memory[int(np.argmax(weights))]
        xi = self.memory[imem].design_variables.astype(float)

        # Titresimler: V = w_j * exp(-d_ij^2)
        v_best = weights.max() * math.exp(-np.linalg.norm(xi - best_spider.design_variables)**2 / (self.n_vars + 1e-12))
        rand_spider = self.memory[self._random_other(imem)]

        # Disi / Erkek hareketi
        x_new = np.zeros(self.n_vars, dtype=float)
        alpha = random.random()
        beta = random.random()
        if random.random() < pf:
            x_new = xi + alpha * v_best * (best_spider.design_variables - xi) + beta * (rand_spider.design_variables - xi)
        else:
            x_new = xi - alpha * v_best * (best_spider.design_variables - xi) + beta * (rand_spider.design_variables - xi)

        cand = Member(design_variables=self._clip(x_new))
        self._eval_at(cand, imem, greedy=True)

    # -------------------------------------------------------------------------
    # Tek Adim (Step) Dagiticisi
    # -------------------------------------------------------------------------
    def step_individual(self, imem: int) -> None:
        meth = self.method
        if meth == "hs":
            self._step_hs(imem)
        elif meth == "bbo":
            self._step_bbo(imem)
        elif meth == "woa":
            self._step_woa(imem)
        elif meth == "do":
            self._step_do(imem)
        elif meth == "abc":
            self._step_abc(imem)
        elif meth == "aco":
            self._step_aco(imem)
        elif meth == "bso":
            self._step_bso(imem)
        elif meth == "csa":
            self._step_csa(imem)
        elif meth == "fa":
            self._step_fa(imem)
        elif meth == "goa":
            self._step_goa(imem)
        elif meth == "tlbo":
            self._step_tlbo(imem)
        elif meth == "tsa":
            self._step_tsa(imem)
        elif meth == "gwo":
            self._step_gwo(imem)
        elif meth == "hba":
            self._step_hba(imem)
        elif meth == "ao":
            self._step_ao(imem)
        elif meth == "sso":
            self._step_sso(imem)
        else:
            raise ValueError(f"Bilinmeyen optimizasyon algoritmasi: {meth}. "
                             f"Gecerli yontemler: {list(ALGORITHM_NAMES.keys())}")

    # -------------------------------------------------------------------------
    # Ana Calistirma Dongusu (Optimize)
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Degerlendirme kaydi, checkpoint ve devam
    # -------------------------------------------------------------------------
    _NOSAVE = ("eval_fn", "stop_check", "_buf", "ckpt_path", "log_prefix", "ckpt_every_evals")

    def _flush_log(self) -> None:
        if not self.log_prefix or not self._buf:
            return
        genes = np.array([b[0] for b in self._buf], dtype=np.int8)
        obj = np.array([b[1:] for b in self._buf], dtype=np.float64)
        with open(self.log_prefix + ".genes.bin", "ab") as f:
            genes.tofile(f)
        with open(self.log_prefix + ".obj.bin", "ab") as f:
            obj.tofile(f)
        self._buf = []

    def _save_ckpt(self) -> None:
        if not self.ckpt_path:
            return
        self._flush_log()
        state = {k: v for k, v in self.__dict__.items() if k not in self._NOSAVE}
        state["_rng_py"] = random.getstate()
        state["_rng_np"] = np.random.get_state()
        tmp = self.ckpt_path + ".tmp"
        with open(tmp, "wb") as f:
            pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, self.ckpt_path)
        self._last_ckpt = self.n_evals

    def _try_resume(self) -> bool:
        if not self.ckpt_path or not os.path.exists(self.ckpt_path):
            return False
        with open(self.ckpt_path, "rb") as f:
            state = pickle.load(f)
        random.setstate(state.pop("_rng_py"))
        np.random.set_state(state.pop("_rng_np"))
        self.__dict__.update(state)
        if self.log_prefix:                       # checkpoint'ten sonra yazilmis kayitlari at
            for suffix, rec_bytes in ((".genes.bin", self.n_vars), (".obj.bin", 24)):
                fp = self.log_prefix + suffix
                if os.path.exists(fp):
                    with open(fp, "r+b") as f:
                        f.truncate(self.n_evals * rec_bytes)
        self._buf = []
        return True

    def finalize_log(self, npz_path: str) -> None:
        """Ham kayitlari tek bir sikistirilmis .npz'ye cevirir (genes, weight_kN, carbon_kg, penalty)."""
        if not self.log_prefix:
            return
        self._flush_log()
        genes = np.fromfile(self.log_prefix + ".genes.bin", dtype=np.int8).reshape(-1, self.n_vars)
        obj = np.fromfile(self.log_prefix + ".obj.bin", dtype=np.float64).reshape(-1, 3)
        tmp = npz_path + ".tmp.npz"
        np.savez_compressed(tmp, genes=genes, weight_kN=obj[:, 0], carbon_kg=obj[:, 1], penalty=obj[:, 2])
        os.replace(tmp, npz_path)
        for suffix in (".genes.bin", ".obj.bin"):
            os.remove(self.log_prefix + suffix)

    def optimize(self, callback: Callable[[int, dict], None] | None = None) -> tuple[Member, list[dict]]:
        """Populasyonu baslatir (ya da checkpoint'ten surdurur) ve butce/iterasyon bitene kadar kosturur."""
        if not self._try_resume():
            for suffix in (".genes.bin", ".obj.bin"):
                if self.log_prefix and os.path.exists(self.log_prefix + suffix):
                    os.remove(self.log_prefix + suffix)
            self.initialize_population()
            leader = self._leader()
            rec = {"iter": 0, "best_penalized": float(leader.penalized_cost),
                   "best_weight": float(leader.cost_value), "best_carbon": float(leader.carbon_value),
                   "is_feasible": bool(leader.is_feasible), "evals": self.n_evals}
            self.history.append(rec)
            if callback:
                callback(0, rec)
            self._save_ckpt()

        while not self._done:
            if self.stop_check is not None and self.stop_check():
                self._save_ckpt()
                raise OptimizationPaused()
            self._it += 1
            self.current_iter = min(self._it, self.max_iters)
            n_before = self.n_evals
            budget_hit = False
            try:
                for imem in range(self.pop_size):
                    self.step_individual(imem)
            except BudgetExhausted:
                budget_hit = True
            leader = self._leader()
            rec = {"iter": self._it, "best_penalized": float(leader.penalized_cost),
                   "best_weight": float(leader.cost_value), "best_carbon": float(leader.carbon_value),
                   "is_feasible": bool(leader.is_feasible), "evals": self.n_evals}
            self.history.append(rec)
            if callback:
                callback(self._it, rec)
            budget_left = self.max_evals is not None and self.n_evals < self.max_evals
            self._done = budget_hit or self.n_evals == n_before or (self._it >= self.max_iters and not budget_left)
            if self._done or self.n_evals - self._last_ckpt >= self.ckpt_every_evals:
                self._save_ckpt()

        final_best = self.global_best if (self.global_best and self.global_best.is_feasible) else self._leader()
        return final_best, self.history
