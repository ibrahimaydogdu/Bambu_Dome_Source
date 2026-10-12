"""
fast_eval.py
Vektorlestirilmis degerlendirme cekirdegi (NumPy): f1, f2 ve normalize ceza P.

Tanimlar (CAMPAIGN_EXECUTION_PLAN.md):
  f1 = yapisal bambu agirligi [kN]      = g/1000 * sum(rho_b * A_i * L_i)
  f2 = gomulu karbon [kg CO2e]          = EC_b*M_bambu + EC_s*M_celik + EC_m*M_harc
       "section" modu (varsayilan): her cubugun iki ucuna harc enjeksiyonu ve celik sapla
           M_harc  = sum_i 2 * rho_m * pi/4 * (D_i - 2 t_i)^2 * L_inj,  L_inj = k * D_i
           M_celik = N_dugum*m_hub + sum_i 2 * (c_s0 + c_s1 * D_i)
       "fixed" modu: eski sabit dugum modeli (f2, f1'in dogrusal kopyasi -> Pareto tek nokta)
  P  = sum_g max_{i in g} max(DC_i - 1, 0)  +  max(u_max/u_izin - 1, 0)
       DC_i: cekme / basinc(Ylinen) / narinlik (ISO 22156), her yuk durumu zarfinda
       (en buyuk cekme ve en buyuk basinc ayri kontrol edilir)

Esdegerlik: tek bir kuvvet icin dc_force(), iso22156_checks.check_member() ile ayni sayiyi verir
(bkz. test_fast_eval.py).
"""

from __future__ import annotations
import math
from dataclasses import dataclass

import numpy as np

from bamboo_catalog import MATERIAL_PROPERTIES as MP, ASD_K
from truss_model import CASE_DURATION

F_T_K = MP["f_t_0_k"]
F_C_K = MP["f_c_0_k"]
E_K = MP["E_k"]
YLINEN_C = MP["ylinen_c"]
C_BOW = 1.0 - MP["b0"] / 0.02
K_EFF = MP["K_eff"]
LAMBDA_MAX = MP["lambda_max"]
RHO_B = MP["rho"]
F_J_RD = MP["F_j_Rd"]


@dataclass
class CarbonModel:
    mode: str = "section"            # "section" | "fixed"
    rho_mortar: float = 2100.0       # kg/m3  (non-shrink grout)
    m_hub: float = 2.0               # kg / dugum (merkezi celik gobek)
    c_s0: float = 0.5                # kg / cubuk ucu (sapla, somun, pul)
    c_s1: float = 0.0                # kg / m cubuk dis capi (0 = prefabrik standart baglanti)
    l_inject_factor: float = 2.5     # L_inject = faktor * D
    ec_bamboo: float = MP["EC_bamboo"]
    ec_steel: float = MP["EC_steel"]
    ec_mortar: float = MP["EC_mortar"]
    node_steel_kg: float = MP["node_steel_mass"]     # yalniz "fixed" modu
    node_mortar_kg: float = MP["node_mortar_mass"]   # yalniz "fixed" modu

    def as_dict(self) -> dict:
        return dict(self.__dict__)


def ylinen_fcr(lam):
    """Karakteristik basinc kapasitesi / A [kPa]: Ylinen (Manual Denk. 6.1-6.4), P_c,k/A = f_c,k, P_e,k/A = pi^2 E_k C_bow/(K L/r)^2."""
    lam_s = np.maximum(np.asarray(lam, float) * K_EFF, 1.0)
    pe = math.pi ** 2 * E_K * C_BOW / lam_s ** 2
    x = (F_C_K + pe) / (2.0 * YLINEN_C)
    return x - np.sqrt(x ** 2 - F_C_K * pe / YLINEN_C)


def dc_force(Ns, A, r, L, slender: str = "all", Nj=None):
    """Eleman basina talep/kapasite (ISO 22156 ASD, Manual Denk. 3.9/6.5; iso22156_checks.check_member ile ayni).
    Ns: eksenel kuvvet / (C_R C_DF C_T / FS) [kN] (cekme +) -> karakteristik kapasiteyle karsilastirilir.
    Nj: baglanti kontrolu icin ham (olceksiz) kuvvet; None -> baglanti kontrolu yok. slender='all' -> lambda/150 her elemana."""
    lam = L / r
    dc_slender = lam / LAMBDA_MAX
    tension = Ns > 1e-9
    comp = Ns < -1e-9
    dct = np.where(tension, Ns / A / F_T_K, 0.0)
    dcc = np.where(comp, np.abs(Ns) / A / ylinen_fcr(lam), 0.0)
    sl = dc_slender if slender == "all" else np.where(comp, dc_slender, 0.0)
    dc = np.maximum(np.maximum(dct, dcc), sl)
    if Nj is not None:
        dc = np.maximum(dc, np.abs(Nj) / F_J_RD)
    return dc


class FastCore:
    """Bir FEMBridge (analyze_arrays/set_member_areas) uzerinde vektorel degerlendirme."""

    def __init__(self, bridge, catalog, span_m: float, disp_limit_m: float | None,
                 carbon: CarbonModel | None = None, slenderness: str = "all",
                 envelope: bool = True):
        self.bridge = bridge
        self.carbon = carbon or CarbonModel()
        self.slender = slenderness
        self.envelope = envelope
        self.gidx = bridge.group_index
        self.L = bridge.member_lengths_arr
        self.G = int(self.gidx.max()) + 1
        self.order = np.argsort(self.gidx, kind="stable")
        counts = np.bincount(self.gidx, minlength=self.G)
        self.starts = np.concatenate(([0], np.cumsum(counts)[:-1]))
        self.n_nodes = bridge.n_nodes
        self.kcase = np.array([ASD_K[CASE_DURATION.get(n, "permanent")] for n in bridge._load_combos])
        self.limit = disp_limit_m if disp_limit_m is not None else span_m / MP['disp_limit_ratio']
        # kesit tablolari (katalog indeksi 1..24 -> dizi indeksi 0..23)
        self.A_sec = catalog["A_m2"].to_numpy(float)
        self.r_sec = catalog["r_m"].to_numpy(float)
        D = catalog["D_m"].to_numpy(float)
        t = catalog["t_m"].to_numpy(float)
        c = self.carbon
        self.steel_end = c.c_s0 + c.c_s1 * D                                         # kg / cubuk ucu
        self.mortar_end = c.rho_mortar * math.pi / 4.0 * (D - 2 * t) ** 2 * (c.l_inject_factor * D)  # kg / uc
        self.fixed_const = c.ec_steel * self.n_nodes * c.node_steel_kg + c.ec_mortar * self.n_nodes * c.node_mortar_kg
        self.last: dict = {}

    def objectives(self, sec: np.ndarray, A: np.ndarray):
        mass_b = float((RHO_B * A * self.L).sum())
        f1 = mass_b * 9.81 / 1000.0
        c = self.carbon
        if c.mode == "fixed":
            f2 = c.ec_bamboo * mass_b + self.fixed_const
        else:
            m_steel = self.n_nodes * c.m_hub + 2.0 * float(self.steel_end[sec].sum())
            m_mortar = 2.0 * float(self.mortar_end[sec].sum())
            f2 = c.ec_bamboo * mass_b + c.ec_steel * m_steel + c.ec_mortar * m_mortar
        return f1, f2

    def evaluate(self, gene: np.ndarray):
        """gene: 1-tabanli tamsayi kesit indeksleri (grup basina). Doner: f1, f2, P (normalize ceza)."""
        sec = np.asarray(np.round(gene[self.gidx] - 1), dtype=int)
        A = self.A_sec[sec]
        r = self.r_sec[sec]
        self.bridge.set_member_areas(A)
        N, umax = self.bridge.analyze_arrays()
        Ns = N / self.kcase[None, :]                       # ASD: yuk suresi sinifina gore olcekli kuvvet
        if self.envelope:
            Nj = np.abs(N).max(axis=1)
            dc = np.maximum(dc_force(Ns.max(axis=1), A, r, self.L, self.slender, Nj),
                            dc_force(Ns.min(axis=1), A, r, self.L, self.slender, Nj))
        else:                                    # eski davranis: olcekli kuvveti en buyuk tek durum
            pick = np.argmax(np.abs(Ns), axis=1)
            idx = np.arange(N.shape[0])
            dc = dc_force(Ns[idx, pick], A, r, self.L, self.slender, N[idx, pick])
        dcg = np.maximum.reduceat(dc[self.order], self.starts)           # grup basina en kritik eleman
        p_strength = float(np.maximum(dcg - 1.0, 0.0).sum())
        p_disp = max(umax / self.limit - 1.0, 0.0)
        f1, f2 = self.objectives(sec, A)
        self.last = dict(max_dc=float(dc.max()), umax=umax, p_strength=p_strength, p_disp=p_disp, dc=dc)
        return f1, f2, p_strength + p_disp
