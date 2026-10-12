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
from bamboo_catalog import MATERIAL_PROPERTIES as MP, ASD_K


# ---------------------------------------------------------------------------
# Sabitler (kaynaklar: bamboo_catalog.py)
# ---------------------------------------------------------------------------
F_T_K       = MP["f_t_0_k"]       # kPa
F_C_K       = MP["f_c_0_k"]       # kPa
E_K         = MP["E_k"]           # kPa
YLINEN_C    = MP["ylinen_c"]
C_BOW       = 1.0 - MP["b0"] / 0.02
K_EFF       = MP["K_eff"]
LAMBDA_MAX  = MP["lambda_max"]
F_J_RD      = MP["F_j_Rd"]        # kN


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
    k_asd: float | None = None,
) -> CheckResult:
    """
    Tek eleman icin ISO 22156 ASD tahkiki (Manual Denk. 3.9, 6.1-6.5).

    k_asd: C_R*C_DF*C_T/FS kapasite carpani (yuk suresi sinifina gore, bamboo_catalog.ASD_K);
           None -> surekli yuk (en kati). Talep P/k_asd karakteristik kapasiteyle karsilastirilir.
    Baglanti kontrolu |P| / F_j_Rd (olceksiz) ve narinlik lambda/lambda_max ayrica dahil edilir.
    """
    k = ASD_K["permanent"] if k_asd is None else k_asd
    A = float(section_row["A_m2"])
    r = float(section_row["r_m"])
    lam = L_m / r if r > 0 else 9999.0
    dc_sl = lam / LAMBDA_MAX
    if abs(P_kN) < 1e-9:
        return CheckResult(member_id, P_kN, A, r, L_m, lam, "zero", dc_sl, dc_sl > 1.0)

    dc_joint = abs(P_kN) / F_J_RD
    Ps = P_kN / k
    if P_kN > 0:
        mode = "tension"
        dc_m = (Ps / A) / F_T_K
    else:
        mode = "compression"
        lam_s = max(lam * K_EFF, 1.0)
        pe = math.pi ** 2 * E_K * C_BOW / lam_s ** 2
        x = (F_C_K + pe) / (2.0 * YLINEN_C)
        fcr = x - math.sqrt(x * x - F_C_K * pe / YLINEN_C)
        dc_m = (abs(Ps) / A) / fcr if fcr > 0 else 9999.0
    dc = max(dc_m, dc_sl, dc_joint)
    return CheckResult(member_id, P_kN, A, r, L_m, lam, mode, dc, dc > 1.0)


def check_displacement(
    displacements: dict[str, tuple[float, float, float]],
    span_m: float = 40.0,   # 40 m kubbe referans acikligi
    disp_limit_ratio: float = 1.0 / MP['disp_limit_ratio'],
    disp_limit_m: float | None = None,
) -> tuple[float, float]:
    """
    Yer degistirme kisitini degerlendirir.

    disp_limit_m verilirse (SLS limit: orn. S/360, tum dugumler): her dugumun
    her yondeki (U1,U2,U3) bilesenleri bu mutlak sinirla karsilastirilir.
    Verilmezse: bileske / (span * disp_limit_ratio).

    Doner:
      max_disp_m : Modeldeki maksimum mutlak yer degistirme [m]
      dc_disp    : Talebin kapasiteye orani (> 1.0 ise ihlal)
    """
    limit = disp_limit_m if disp_limit_m is not None else span_m * disp_limit_ratio
    max_d = 0.0
    for u1, u2, u3 in displacements.values():
        if disp_limit_m is not None:
            total = max(abs(u1), abs(u2), abs(u3))
        else:
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
    disp_limit_ratio: float = 1.0 / MP['disp_limit_ratio'],
    disp_limit_m: float | None = None,
) -> tuple[float, float, list[CheckResult]]:
    """
    Tum elemanlar icin ISO 22156 tahkikini yapar.

    Doner:
      penalty_structural : Toplam yapisal ceza degeri (normalize kisit ihlali P)
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
        displacements, span_m=span_m, disp_limit_ratio=disp_limit_ratio,
        disp_limit_m=disp_limit_m,
    )
    if dc_disp > 1.0:
        total_penalty += (dc_disp - 1.0)

    max_dc = max((r.demand_capacity_ratio for r in results), default=0.0)
    max_dc = max(max_dc, dc_disp)

    return total_penalty, max_dc, results
