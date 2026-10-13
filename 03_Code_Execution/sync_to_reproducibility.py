"""
sync_to_reproducibility.py
--------------------------
BambuDome projesindeki güncel kod, figür, tablo (CSV) ve modelleri
BambuDome-reproducibility deposuna senkronize eder.
"""
import shutil
from pathlib import Path

SRC_ROOT = Path(r"G:\Drive'ım\MyProjects\Makale Çalışmaları\2027\BambuDome")
DST_ROOT = Path(r"G:\Drive'ım\MyProjects\Makale Çalışmaları\2027\BambuDome-reproducibility")

if not DST_ROOT.exists():
    raise FileNotFoundError(f"Hedef repo bulunamadı: {DST_ROOT}")

# 1. Tables kopyala
src_tables = SRC_ROOT / "04_Results" / "tables"
dst_tables = DST_ROOT / "04_Results" / "tables"
dst_tables.mkdir(parents=True, exist_ok=True)

for p in src_tables.glob("T_*.csv"):
    shutil.copy2(p, dst_tables / p.name)
    print(f"Kopyalandı: {p.name}")

if (src_tables / "README.md").exists():
    shutil.copy2(src_tables / "README.md", dst_tables / "README.md")
    print("Kopyalandı: tables/README.md")

# 2. Code execution
src_code = SRC_ROOT / "03_Code_Execution"
dst_code = DST_ROOT / "03_Code_Execution"
for py_name in ["export_repro_tables_csv.py", "joint_capacity_by_diameter.py", "bamboo_catalog.py", 
                "carbon_calculator.py", "lca_sensitivity_analysis.py", "results_report.py"]:
    if (src_code / py_name).exists():
        shutil.copy2(src_code / py_name, dst_code / py_name)
        print(f"Kopyalandı: {py_name}")

# 3. SAP2000 models
src_sap = SRC_ROOT / "04_Results" / "SAP2000_models"
dst_sap = DST_ROOT / "04_Results" / "SAP2000_models"
if src_sap.exists():
    dst_sap.mkdir(parents=True, exist_ok=True)
    for p in src_sap.glob("*"):
        if p.is_file():
            shutil.copy2(p, dst_sap / p.name)
    print("SAP2000 modelleri kopyalandı.")

# 4. Figures
src_fig = SRC_ROOT / "04_Results" / "figures"
dst_fig = DST_ROOT / "04_Results" / "figures"
for f_name in ["method_flowchart.png", "F5_material_co2.png", "graphical_abstract.png"]:
    if (src_fig / f_name).exists():
        shutil.copy2(src_fig / f_name, dst_fig / f_name)
        print(f"Kopyalandı: figures/{f_name}")

# 5. Domes figures
src_domes = src_fig / "domes"
dst_domes = dst_fig / "domes"
if src_domes.exists():
    dst_domes.mkdir(parents=True, exist_ok=True)
    for p in src_domes.glob("*.png"):
        shutil.copy2(p, dst_domes / p.name)
    print("Kubbe şekilleri kopyalandı.")

print("=== SENKRONİZASYON TAMAMLANDI ===")
