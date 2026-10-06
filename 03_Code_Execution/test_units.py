"""
test_units.py
SAP2000 gerektirmeyen birim testleri
=====================================
Calistirilmasi: python test_units.py
"""
import sys
import math
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.WARNING)
errors = []

# ------------------------------------------------------------------
# Test 1: bamboo_catalog.py
# ------------------------------------------------------------------
try:
    from bamboo_catalog import BAMBOO_CATALOG, MATERIAL_PROPERTIES, get_section_by_index
    assert len(BAMBOO_CATALOG) == 24, f"Katalog 24 kesit olmali, bulunan: {len(BAMBOO_CATALOG)}"
    sec1 = get_section_by_index(1)
    assert abs(sec1["D_m"] - 0.080) < 1e-6
    sec24 = get_section_by_index(24)
    assert abs(sec24["D_m"] - 0.160) < 1e-6
    # Tasarim degerleri
    assert abs(MATERIAL_PROPERTIES["f_t_0_d"] - (0.70 * 45000 / 1.30)) < 1.0
    assert abs(MATERIAL_PROPERTIES["f_c_0_d"] - (0.70 * 38000 / 1.30)) < 1.0
    print("[PASS] bamboo_catalog.py")
except Exception as e:
    print(f"[FAIL] bamboo_catalog.py -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Test 2: iso22156_checks.py -- Cekme tahkiki
# ------------------------------------------------------------------
try:
    from iso22156_checks import check_member, check_displacement
    from bamboo_catalog import BAMBOO_CATALOG
    sec = BAMBOO_CATALOG.loc[5]   # D=100mm, t=9mm
    cr = check_member("test_tension", P_kN=50.0, section_row=sec, L_m=2.0)
    assert cr.mode == "tension"
    # sigma = 50 / A_m2   f_t_0_d = 24231 kPa
    sigma = 50.0 / sec["A_m2"]
    dc_expected = sigma / MATERIAL_PROPERTIES["f_t_0_d"]
    assert abs(cr.demand_capacity_ratio - max(dc_expected, 2.0/sec["r_m"]/150)) < 0.01, \
        f"DC orani: {cr.demand_capacity_ratio}"
    print("[PASS] iso22156_checks.py -- cekme")
except Exception as e:
    print(f"[FAIL] iso22156_checks.py -- cekme -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Test 3: iso22156_checks.py -- Basinc & burkulma tahkiki
# ------------------------------------------------------------------
try:
    from iso22156_checks import check_member
    from bamboo_catalog import BAMBOO_CATALOG, MATERIAL_PROPERTIES as MP

    sec = BAMBOO_CATALOG.loc[10]   # D=110mm, t=14mm
    L_m = 5.0
    cr = check_member("test_comp", P_kN=-80.0, section_row=sec, L_m=L_m)
    assert cr.mode == "compression"
    # Narinlik siniri
    lam = L_m / sec["r_m"]
    if lam > 150:
        assert cr.is_violated
    print(f"[PASS] iso22156_checks.py -- basinc  (lambda={lam:.1f}, DC={cr.demand_capacity_ratio:.3f})")
except Exception as e:
    print(f"[FAIL] iso22156_checks.py -- basinc -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Test 4: iso22156_checks.py -- Narinlik siniri
# ------------------------------------------------------------------
try:
    from iso22156_checks import check_member
    from bamboo_catalog import BAMBOO_CATALOG
    sec = BAMBOO_CATALOG.loc[1]   # En ince kesit
    L_m = 30.0  # Asiliri uzun -- lambda > 150 beklenir
    cr_comp = check_member("test_lam", P_kN=-1.0, section_row=sec, L_m=L_m)
    lam = L_m / sec["r_m"]
    assert cr_comp.is_violated and lam > 150, f"lambda={lam:.1f} > 150 olmali"
    print(f"[PASS] iso22156_checks.py -- narinlik (lambda={lam:.1f})")
except Exception as e:
    print(f"[FAIL] iso22156_checks.py -- narinlik -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Test 5: carbon_calculator.py
# ------------------------------------------------------------------
try:
    from carbon_calculator import compute_embodied_carbon, compute_structural_weight
    from bamboo_catalog import BAMBOO_CATALOG

    # Basit test kurgusu: 10 eleman, hepsi grup 1, sec_idx=1
    n_mem = 10
    member_lengths = {str(i): 2.0 for i in range(n_mem)}
    member_group   = {str(i): "1" for i in range(n_mem)}
    gene = [1]   # Tek grup

    f1 = compute_structural_weight(gene, BAMBOO_CATALOG, member_lengths, member_group)
    total_ec, bec, nec = compute_embodied_carbon(
        gene, BAMBOO_CATALOG, member_lengths, member_group, n_nodes=50
    )
    assert f1 > 0 and total_ec > 0
    # Manuel hesap
    row = BAMBOO_CATALOG.loc[1]
    A = row["A_m2"]
    mass_kg = 700 * A * 2.0 * n_mem
    expected_bec = mass_kg * 0.35
    assert abs(bec - expected_bec) < 1.0, f"Bambu karbon: {bec:.3f} != {expected_bec:.3f}"
    print(f"[PASS] carbon_calculator.py  (f1={f1:.3f} kN, EC={total_ec:.2f} kg CO2e)")
except Exception as e:
    print(f"[FAIL] carbon_calculator.py -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Test 6: checkpoint_manager.py
# ------------------------------------------------------------------
try:
    import tempfile, os
    from checkpoint_manager import CheckpointManager
    import numpy as np

    with tempfile.TemporaryDirectory() as tmpdir:
        ckpt = CheckpointManager(Path(tmpdir) / "test_ckpt.json")
        assert ckpt.load() is None  # Henuz dosya yok

        state = {
            "iter": 42,
            "population": np.random.randint(1, 25, (10, 22)).tolist(),
            "archive_obj": [[100.0, 200.0], [110.0, 190.0]],
        }
        ckpt.save(state)
        loaded = ckpt.load()
        assert loaded is not None
        assert loaded["iter"] == 42
        assert len(loaded["population"]) == 10
        ckpt.delete()
        assert ckpt.load() is None
    print("[PASS] checkpoint_manager.py")
except Exception as e:
    print(f"[FAIL] checkpoint_manager.py -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Test 7: multi_objective_optimizer.py -- Pareto yardimcilari
# ------------------------------------------------------------------
try:
    from multi_objective_optimizer import (
        dominates, non_dominated_sort_front0, crowding_distance, update_archive
    )
    import numpy as np

    obj = np.array([
        [1.0, 4.0],   # 0 -- Pareto
        [2.0, 3.0],   # 1 -- Pareto
        [3.0, 2.0],   # 2 -- Pareto
        [4.0, 1.0],   # 3 -- Pareto
        [3.0, 3.0],   # 4 -- baskiniyor
        [2.5, 3.5],   # 5 -- baskiniyor
    ])
    front = non_dominated_sort_front0(obj)
    assert set(front) == {0, 1, 2, 3}, f"Pareto front hatalı: {front}"

    cd = crowding_distance(obj[[0, 1, 2, 3]])
    assert cd[0] == float("inf") and cd[-1] == float("inf")

    # dominates
    assert dominates(np.array([1.0, 2.0]), np.array([2.0, 3.0]))
    assert not dominates(np.array([2.0, 2.0]), np.array([2.0, 2.0]))

    # Arsiv guncelle
    sols, objs = [], []
    sols, objs = update_archive(sols, objs, np.array([1.0, 2.0]), np.array([10.0, 20.0]))
    assert len(objs) == 1
    # 2. ekleme (9,19) 1.'yi (10,20) baskiliyor -> 1 kalir
    sols, objs = update_archive(sols, objs, np.array([1.5, 2.5]), np.array([9.0, 19.0]))
    assert len(objs) == 1 and objs[0] == [9.0, 19.0]
    # 3. ekleme (11,21) arsiv tarafindan baskinlaniyor -> hala 1
    sols, objs = update_archive(sols, objs, np.array([2.0, 3.0]), np.array([11.0, 21.0]))
    assert len(objs) == 1  # Baskinlaniyor, eklenmemeli
    # Gercek non-dominated ekleme: (8, 25) -> 2. cozum
    sols, objs = update_archive(sols, objs, np.array([3.0, 1.0]), np.array([8.0, 25.0]))
    assert len(objs) == 2  # Her ikisi de Pareto optimal

    print("[PASS] multi_objective_optimizer.py -- Pareto yardimcilari")
except Exception as e:
    print(f"[FAIL] multi_objective_optimizer.py -- {e}")
    errors.append(e)

# ------------------------------------------------------------------
# Sonuc
# ------------------------------------------------------------------
print()
if errors:
    print(f"TOPLAM {len(errors)} TEST HATASI. Detaylar yukarida.")
    sys.exit(1)
else:
    print("TUM TESTLER BASARILI (SAP2000 gerektirmeyen birim testleri)")
    sys.exit(0)

# Import duzeltmesi
from bamboo_catalog import MATERIAL_PROPERTIES
