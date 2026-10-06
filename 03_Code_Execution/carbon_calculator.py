"""
carbon_calculator.py
Besikten-Kapiya (A1-A3) Gomulu Karbon Hesaplayicisi
====================================================
Bambu govde (culm) + celik flansh/civata dugum + rotresiz cimento harc dolgusu
bilesenlerini kapsayan Life Cycle Assessment (A1-A3 kapsamlari).

Kaynak katsayilari: ICE v3.0 (Hammond & Jones) / Ecoinvent 3.9
"""

from __future__ import annotations
import math
from bamboo_catalog import MATERIAL_PROPERTIES as MP


# ---------------------------------------------------------------------------
# Karbon Emisiyon Katsayilari (kg CO2e / kg)
# ---------------------------------------------------------------------------
EC_BAMBOO  = MP["EC_bamboo"]       # 0.35 kg CO2e/kg  -- Islenmis Guadua culm
EC_STEEL   = MP["EC_steel"]        # 2.10 kg CO2e/kg  -- Celik flansh / civata
EC_MORTAR  = MP["EC_mortar"]       # 0.18 kg CO2e/kg  -- Rotresiz cimento harc

# Ortalama dugum malzeme kutleleri (kg/dugum)
NODE_STEEL_KG  = MP["node_steel_mass"]    # 4.50 kg/dugum
NODE_MORTAR_KG = MP["node_mortar_mass"]   # 2.80 kg/dugum

# Bambu yogunlugu
RHO_BAMBOO = MP["rho"]  # 700 kg/m3


def bamboo_member_mass(
    A_m2: float,
    L_m: float,
) -> float:
    """Tek bambu cubugu kutlesini hesaplar. [kg]"""
    return RHO_BAMBOO * A_m2 * L_m


def node_embodied_carbon(
    n_nodes: int,
    node_steel_kg: float = NODE_STEEL_KG,
    node_mortar_kg: float = NODE_MORTAR_KG,
) -> float:
    """
    Tum celik dugum birlesleri icin A1-A3 gomulu karbon hesaplar.
    [kg CO2e]

    n_nodes       : Modeldeki toplam dugum sayisi
    node_steel_kg : Her dugumde kullanilan celik kutlesi [kg]
    node_mortar_kg: Her dugumde kullanilan harc kutlesi  [kg]
    """
    co2_steel  = n_nodes * node_steel_kg  * EC_STEEL
    co2_mortar = n_nodes * node_mortar_kg * EC_MORTAR
    return co2_steel + co2_mortar


def compute_embodied_carbon(
    group_section_indices: list[int],
    catalog_df,
    member_lengths: dict[str, float],
    member_group: dict[str, str],
    n_nodes: int,
    node_steel_kg: float = NODE_STEEL_KG,
    node_mortar_kg: float = NODE_MORTAR_KG,
) -> tuple[float, float, float]:
    """
    Kubbenin toplam A1-A3 gomulu karbonunu hesaplar.

    Parametreler
    ------------
    group_section_indices : Her simetri grubunun katalog indeksi (1-tabanli)
    catalog_df            : BAMBOO_CATALOG DataFrame
    member_lengths        : {eleman_adi: uzunluk_m}
    member_group          : {eleman_adi: grup_adi}
    n_nodes               : Toplam dugum sayisi
    node_steel_kg         : Dugum basi celik kutlesi [kg]
    node_mortar_kg        : Dugum basi harc kutlesi  [kg]

    Doner
    -----
    total_EC_kg_co2e  : Toplam gomulu karbon [kg CO2e]
    bamboo_EC         : Bambu govde karbonu  [kg CO2e]
    node_EC           : Dugum karbonu        [kg CO2e]
    """
    bamboo_ec = 0.0

    for mem_id, L_m in member_lengths.items():
        grp = member_group.get(mem_id, "1")
        try:
            grp_idx = int(grp) - 1
            sec_idx = group_section_indices[grp_idx]
        except (IndexError, ValueError):
            sec_idx = 1

        row = catalog_df.loc[int(sec_idx)]
        A_m2 = float(row["A_m2"])

        mass_kg = bamboo_member_mass(A_m2, L_m)
        bamboo_ec += mass_kg * EC_BAMBOO

    node_ec = node_embodied_carbon(n_nodes, node_steel_kg, node_mortar_kg)
    total_ec = bamboo_ec + node_ec
    return total_ec, bamboo_ec, node_ec


def compute_structural_weight(
    group_section_indices: list[int],
    catalog_df,
    member_lengths: dict[str, float],
    member_group: dict[str, str],
) -> float:
    """
    Kubbenin toplam yapisal agirligini (bambu govde) hesaplar. [kN]
    kN = kg * 9.81 / 1000
    """
    total_mass_kg = 0.0
    for mem_id, L_m in member_lengths.items():
        grp = member_group.get(mem_id, "1")
        try:
            grp_idx = int(grp) - 1
            sec_idx = group_section_indices[grp_idx]
        except (IndexError, ValueError):
            sec_idx = 1
        row = catalog_df.loc[int(sec_idx)]
        A_m2 = float(row["A_m2"])
        total_mass_kg += bamboo_member_mass(A_m2, L_m)

    return total_mass_kg * 9.81 / 1000.0  # kN
