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
    from bamboo_catalog import ASD_K
    assert abs(ASD_K["permanent"] - 0.90 * 0.55 / 2.0) < 1e-12
    assert abs(ASD_K["instantaneous"] - 0.90 * 0.85 / 2.0) < 1e-12
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
    from bamboo_catalog import ASD_K
    # ASD: sigma = (P/k) / A  <=  f_t_0_k   (k = surekli yuk carpani)
    sigma = 50.0 / ASD_K["permanent"] / sec["A_m2"]
    dc_expected = sigma / MATERIAL_PROPERTIES["f_t_0_k"]
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
# Test 7: metaheuristic_optimizers.py -- 16 Algoritma Entegrasyonu
# ------------------------------------------------------------------
try:
    from metaheuristic_optimizers import MetaheuristicOptimizer, ALGORITHM_NAMES
    import numpy as np

    def dummy_eval(gene):
        # Basit hedef ve ceza fonksiyonu
        w = float(np.sum((gene - 10)**2))
        p = 0.0 if np.sum(gene) > 5 else 0.5
        return w, w * 0.35, p

    assert len(ALGORITHM_NAMES) == 16, f"16 algoritma bekleniyordu, {len(ALGORITHM_NAMES)} bulundu"
    for code in ALGORITHM_NAMES.keys():
        opt = MetaheuristicOptimizer(dummy_eval, n_vars=4, pop_size=6, max_iters=2, seed=123, method=code)
        best, hist = opt.optimize()
        assert best is not None
        assert len(hist) == 3  # iter 0, 1, 2

    print("[PASS] metaheuristic_optimizers.py -- 16 Optimizasyon Yontemi Dogrulandi")
except Exception as e:
    print(f"[FAIL] metaheuristic_optimizers.py -- {e}")
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
