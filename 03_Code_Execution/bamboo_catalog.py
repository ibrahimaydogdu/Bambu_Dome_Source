"""
bamboo_catalog.py
ISO 22156 Uyumlu Guadua angustifolia Ayrık Kesit Kataloğu ve Malzeme Tanımları.
"""

import numpy as np
import pandas as pd

# ==============================================================================
# MALZEME ÖZELLİKLERİ: Guadua angustifolia (ISO 22156 Parametreleri)
# ==============================================================================
MATERIAL_PROPERTIES = {
    "name": "BAMBOO_GUADUA",
    "rho": 700.0,              # kg/m^3 (Birim hacim ağırlığı)
    "E_mean": 11000.0e3,       # kPa (11,000 MPa - Ortalama Elastisite Modülü)
    "E_05": 8500.0e3,          # kPa (8,500 MPa - %5 Karakteristik Elastisite Modülü)
    "f_t_0_k": 45.0e3,         # kPa (45.0 MPa - Karakteristik lif boyuna çekme dayanımı)
    "f_c_0_k": 38.0e3,         # kPa (38.0 MPa - Karakteristik lif boyuna basınç dayanımı)
    "nu": 0.30,                # Poisson oranı
    "k_mod": 0.70,             # Yük süresi ve nem düzeltme katsayısı (Servis sınıfı 2)
    "gamma_M_t": 1.30,         # Çekme malzeme kısmi güvenlik katsayısı
    "gamma_M_c": 1.30,         # Basınç malzeme kısmi güvenlik katsayısı
    "beta_c": 0.10,            # Bambu burkulma kusur katsayısı (ISO 22156 Madde 7)
    "lambda_max": 150.0,       # Maksimum izin verilen narinlik üst sınırı
    "F_j_Rd": 120.0,           # kN (Harç dolgulu çelik mafsal düğüm eksenel kapasitesi)
    
    # Beşikten-Kapıya (A1-A3) Gömülü Karbon Katsayıları (ICE v3.0 / Ecoinvent)
    "EC_bamboo": 0.35,         # kg CO2e / kg (İşlenmiş Guadua culm)
    "EC_steel": 2.10,          # kg CO2e / kg (Bağlantı çelik flanş/cıvata)
    "EC_mortar": 0.18,         # kg CO2e / kg (Rötresiz çimento harç dolgusu)
    "node_steel_mass": 4.50,   # kg / düğüm (Ortalama çelik kütlesi)
    "node_mortar_mass": 2.80   # kg / düğüm (Ortalama harç kütlesi)
}

# Tasarım Dayanımlarının Hesabı (kPa = kN/m^2)
MATERIAL_PROPERTIES["f_t_0_d"] = (
    MATERIAL_PROPERTIES["k_mod"] * MATERIAL_PROPERTIES["f_t_0_k"] / MATERIAL_PROPERTIES["gamma_M_t"]
)  # 24,230.77 kPa (24.23 MPa)

MATERIAL_PROPERTIES["f_c_0_d"] = (
    MATERIAL_PROPERTIES["k_mod"] * MATERIAL_PROPERTIES["f_c_0_k"] / MATERIAL_PROPERTIES["gamma_M_c"]
)  # 20,461.54 kPa (20.46 MPa)

# ==============================================================================
# 24 ELEMANLI AYRIK BAMBU KESİT KATALOĞU (Discrete Catalog C)
# ==============================================================================
# D: Dış Çap (mm), t: Et Kalınlığı (mm)
RAW_CATALOG_DATA = [
    (1,  80.0,  8.0),
    (2,  80.0, 10.0),
    (3,  90.0,  9.0),
    (4,  90.0, 11.0),
    (5, 100.0,  9.0),
    (6, 100.0, 11.0),
    (7, 100.0, 13.0),
    (8, 110.0, 10.0),
    (9, 110.0, 12.0),
    (10, 110.0, 14.0),
    (11, 120.0, 10.0),
    (12, 120.0, 12.0),
    (13, 120.0, 14.0),
    (14, 120.0, 16.0),
    (15, 130.0, 11.0),
    (16, 130.0, 13.0),
    (17, 130.0, 15.0),
    (18, 140.0, 12.0),
    (19, 140.0, 14.0),
    (20, 140.0, 16.0),
    (21, 150.0, 13.0),
    (22, 150.0, 15.0),
    (23, 160.0, 14.0),
    (24, 160.0, 16.0)
]

def build_catalog_dataframe():
    """Kataloğun geometrik kesit özelliklerini SI (m, m^2, m^4) ve metrik (cm, cm^4) olarak türetir."""
    rows = []
    rho = MATERIAL_PROPERTIES["rho"]
    
    for idx, D_mm, t_mm in RAW_CATALOG_DATA:
        D_m = D_mm / 1000.0
        t_m = t_mm / 1000.0
        di_m = D_m - 2.0 * t_m
        
        # Enkesit Alanı (m^2)
        A_m2 = (np.pi / 4.0) * (D_m**2 - di_m**2)
        
        # Atalet Momenti (m^4)
        I_m4 = (np.pi / 64.0) * (D_m**4 - di_m**4)
        
        # Atalet Yarıçapı (m)
        r_m = np.sqrt(I_m4 / A_m2)
        
        # Birim Ağırlık (kg/m)
        w_kg_m = rho * A_m2
        
        # SAP2000 Kesit İsmi
        sec_name = f"BAMB_D{int(D_mm)}T{int(t_mm)}"
        
        rows.append({
            "id": idx,
            "name": sec_name,
            "D_mm": D_mm,
            "t_mm": t_mm,
            "D_m": D_m,
            "t_m": t_m,
            "di_m": di_m,
            "A_m2": A_m2,
            "I_m4": I_m4,
            "r_m": r_m,
            "w_kg_m": w_kg_m,
            # Raporlama için cm/cm^4 birimleri
            "A_cm2": A_m2 * 1e4,
            "I_cm4": I_m4 * 1e8,
            "r_cm": r_m * 100.0
        })
        
    df = pd.DataFrame(rows)
    df.set_index("id", inplace=True)
    return df

BAMBOO_CATALOG = build_catalog_dataframe()

def get_section_by_index(idx: int):
    """Verilen 1-tabanlı tamsayı indeksine karşılık gelen profil sözlüğünü döner."""
    idx = int(np.clip(idx, 1, len(BAMBOO_CATALOG)))
    return BAMBOO_CATALOG.loc[idx]

if __name__ == "__main__":
    print(f"Bambu Kataloğu Başarıyla Oluşturuldu: {len(BAMBOO_CATALOG)} kesit.")
    print(BAMBOO_CATALOG[["name", "D_mm", "t_mm", "A_cm2", "r_cm", "w_kg_m"]].head(5))
