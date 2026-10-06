"""
iso22156_checks.py
ISO 22156 Bambu Yapisal Tasarim Tahkikleri
==========================================
Cekme, basincl (Euler burkulma + ISO narinlik siniri),
narinlik (lambda <= 150) ve deplasman kisitlarini uygular.

Tum formul kaynaklari:
  - ISO 22156:2021  Bamboo structures - Structural design
  - bamboo_catalog.py::MATERIAL_PROPERTIES (k_mod, gamma_M, beta_c)
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from bamboo_catalog import MATERIAL_PROPERTIES as MP


# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
K_MOD       = MP["k_mod"]          # 0.70
GAM_M_T     = MP["gamma_M_t"]      # 1.30 (cekme)
GAM_M_C     = MP["gamma_M_c"]      # 1.30 (basinc)
F_T_0_K     = MP["f_t_0_k"]        # 45,000 kPa
F_C_0_K     = MP["f_c_0_k"]        # 38,000 kPa
F_T_0_D     = MP["f_t_0_d"]        # 24,231 kPa (tasarim degeri)
F_C_0_D     = MP["f_c_0_d"]        # 20,462 kPa
BETA_C      = MP["beta_c"]         # 0.10
E_05        = MP["E_05"]            # 8,500,000 kPa
LAMBDA_MAX  = MP["lambda_max"]      # 150.0


@dataclass
class CheckResult:
    """Tek bir eleman icin tahkik ciktisi."""
    member_id: str
    P_kN: float              # Pozitif = cekme, Negatif = basinc
    A_m2: float
    r_m: float
    L_m: float
    lambda_val: float        # Narinlik orani
    mode: str                # "tension" | "compression" | "zero"
    demand_capacity_ratio: float   # >= 0; > 1.0 ise ihlal var
    is_violated: bool

    @property
    def penalty(self) -> float:
        """Ceza degeri: max(0, DC_ratio - 1). Ihlal yok => 0."""
        return max(0.0, self.demand_capacity_ratio - 1.0)


def check_member(
    member_id: str,
    P_kN: float,
    section_row,
    L_m: float,
) -> CheckResult:
    """
    Tek eleman icin ISO 22156 Madde 7/8 tahkiki.

    Parametreler
    ------------
    member_id  : Eleman adi ('1', '23', vb.)
    P_kN       : Eksenel kuvvet kN (+ cekme, - basinc)
    section_row: catalog_df.loc[sec_idx] satirindaki Series
    L_m        : Eleman uzunlugu [m]

    Doner
    -----
    CheckResult (narinlik + cekme veya basinc + burkulma)
    """
    A  = float(section_row["A_m2"])
    r  = float(section_row["r_m"])

    # --- Narinlik ---
    lam = L_m / r if r > 0 else 9999.0

    if abs(P_kN) < 1e-9:
        return CheckResult(
            member_id=member_id,
            P_kN=P_kN,
            A_m2=A,
            r_m=r,
            L_m=L_m,
            lambda_val=lam,
            mode="zero",
            demand_capacity_ratio=lam / LAMBDA_MAX,
            is_violated=(lam > LAMBDA_MAX),
        )

    # --- Narinlik kisiti ---
    lam_violation = max(0.0, lam - LAMBDA_MAX) / LAMBDA_MAX

    if P_kN > 0:
        # CEKME  (ISO 22156 Md. 7.2)
        # sigma_t = P / A  <=  f_t_0_d
        sigma = P_kN / A
        dc = sigma / F_T_0_D
        dc = max(dc, lam / LAMBDA_MAX)   # narinlik de DC'ye dahil
        return CheckResult(
            member_id=member_id,
            P_kN=P_kN,
            A_m2=A,
            r_m=r,
            L_m=L_m,
            lambda_val=lam,
            mode="tension",
            demand_capacity_ratio=dc,
            is_violated=(dc > 1.0),
        )
    else:
        # BASINC + BURKULMA  (ISO 22156 Md. 7.3 / Ylinen formulu)
        P_abs = abs(P_kN)

        # Kismi cekme / basinc karsilikli etki katsayisi (Ylinen stab.)
        # f_c_cr = Euler kritik gerilmesi
        if lam <= 0:
            lam_safe = 1.0
        else:
            lam_safe = lam

        # Euler kritik gerilmesi: f_c_cr = pi^2 * E_05 / lambda^2
        f_c_cr = (math.pi ** 2 * E_05) / (lam_safe ** 2)

        # Ylinen sutun kararlilik katsayisi
        ratio = f_c_cr / F_C_0_D
        cp_num = (1.0 + ratio) / (2.0 * BETA_C)
        cp = cp_num - math.sqrt(cp_num ** 2 - ratio / BETA_C)
        cp = max(0.0, min(1.0, cp))

        # Tasarim basinc kapasitesi
        f_c_d_eff = F_C_0_D * cp

        # Talebin kapasiteye orani
        sigma_c = P_abs / A
        dc_c = sigma_c / f_c_d_eff if f_c_d_eff > 0 else 9999.0
        dc = max(dc_c, lam / LAMBDA_MAX)

        return CheckResult(
            member_id=member_id,
            P_kN=P_kN,
            A_m2=A,
            r_m=r,
            L_m=L_m,
            lambda_val=lam,
            mode="compression",
            demand_capacity_ratio=dc,
            is_violated=(dc > 1.0),
        )


def check_displacement(
    displacements: dict[str, tuple[float, float, float]],
    span_m: float = 24.384,   # 354-eleman geodezik kubbe referans acikligi
    disp_limit_ratio: float = 1.0 / 200.0,
) -> tuple[float, float]:
    """
    Yer degistirme kisitini degerlendirir.

    disp_limit = span / 200  (ASCE 7 / literatur degeri)

    Doner:
      max_disp_m : Modeldeki maksimum mutlak yer degistirme [m]
      dc_disp    : Talebin kapasiteye orani (> 1.0 ise ihlal)
    """
    limit = span_m * disp_limit_ratio
    max_d = 0.0
    for u1, u2, u3 in displacements.values():
        total = math.sqrt(u1**2 + u2**2 + u3**2)
        if total > max_d:
            max_d = total
    dc = max_d / limit if limit > 0 else 9999.0
    return max_d, dc


def evaluate_all_members(
    axial_forces: dict[str, float],
    member_lengths: dict[str, float],
    member_group: dict[str, str],
    group_section_indices: list[int],
    catalog_df,
    displacements: dict[str, tuple[float, float, float]],
    span_m: float = 24.384,
    disp_limit_ratio: float = 1.0 / 200.0,
) -> tuple[float, float, list[CheckResult]]:
    """
    Tum elemanlar icin ISO 22156 tahkikini yapar.

    Doner:
      penalty_structural : Toplam yapisal ceza degeri (NSGA-II kisit degeri)
      max_dc             : En kritik D/C orani
      results            : Her eleman icin CheckResult listesi
    """
    results: list[CheckResult] = []
    total_penalty = 0.0

    for mem_id, P_kN in axial_forces.items():
        grp = member_group.get(mem_id, "1")
        try:
            grp_idx = int(grp) - 1
            sec_idx = group_section_indices[grp_idx]
        except (IndexError, ValueError):
            sec_idx = 1

        sec_row = catalog_df.loc[int(sec_idx)]
        L_m = member_lengths.get(mem_id, 1.0)

        cr = check_member(mem_id, P_kN, sec_row, L_m)
        results.append(cr)
        total_penalty += cr.penalty

    # Yer degistirme kisiti
    _max_disp, dc_disp = check_displacement(
        displacements, span_m=span_m, disp_limit_ratio=disp_limit_ratio
    )
    if dc_disp > 1.0:
        total_penalty += (dc_disp - 1.0)

    max_dc = max((r.demand_capacity_ratio for r in results), default=0.0)
    max_dc = max(max_dc, dc_disp)

    return total_penalty, max_dc, results
