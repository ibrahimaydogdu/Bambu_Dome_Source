"""
bamboo_catalog.py
ISO 22156 Uyumlu Guadua angustifolia Ayrık Kesit Kataloğu ve Malzeme Tanımları.
"""

import numpy as np
import pandas as pd

# ==============================================================================
# MALZEME ÖZELLİKLERİ: Guadua angustifolia (ISO 22156 Parametreleri)
# ==============================================================================
# Kaynak: IStructE, "Manual for the design of bamboo structures to ISO 22156:2021", v1.0 (2025) [Manual].
# ISO 22156 izinli gerilme (ASD) esaslidir: X_allow = X_k * C_R * C_DF * C_T / FS  (Manual Denk. 3.9, 6.5).
MATERIAL_PROPERTIES = {
    "name": "BAMBOO_GUADUA",
    "rho": 700.0,              # kg/m^3  (Manual Tablo 4.4 sema tasarim degeri; Guadua ort. 680, Tablo A3.9)
    "E_k": 10000.0e3,          # kPa (10 GPa) tasarim modulu E_k: Manual Tablo 4.4 sema alt siniri (her D/t icin gecerli;
                               #      D/t>=10 tropik bambu icin 15 GPa). FEM rijitligi ve Ylinen P_e'de kullanilir.
    "f_t_0_k": 40.0e3,         # kPa (40 MPa) boyuna cekme karakteristik (Manual Tablo 4.4 sema; Guadua'ya ozel veri yok)
    "f_c_0_k": 37.8e3,         # kPa (37.8 MPa) boyuna basinc karakteristik (Manual Tablo A3.4, Guadua, n=922)
    "nu": 0.30,                # Poisson orani (varsayim)
    # --- ASD katsayilari (Manual Denk. 3.9 / 6.5; Servis Sinifi 2) ---
    "C_R": 0.90,               # tekil culm eleman (Manual: 0.90 tekil, 1.1 >=4 paralel culm / tekrarli yapi)
    "C_T": 1.0,                # servis sicakligi < 38 C
    "FS": 2.0,                 # boyuna davranis (cekme, basinc): FS=2 (kayma icin 4)
    "C_DF": {"permanent": 0.55, "transient": 0.65, "instantaneous": 0.85},   # Servis Sinifi 2 (Manual ornek, s.~140)
    # --- Basinc (Ylinen, Manual Denk. 6.1-6.4) ---
    "ylinen_c": 0.8,           # Manual Ek. A6.2
    "b0": 0.01,                # baslangic egriligi (varsayim: L/100; Manual b0<=0.02) -> C_bow = 1 - b0/0.02
    "K_eff": 1.0,              # kafes elemani etkin boy katsayisi (Manual Tablo 6.1)
    "lambda_max": 150.0,       # narinlik siniri -- KAYNAK DOGRULANAMADI (varsayim)
    # --- Baglanti ---
    "F_bolt_adm": 13.25,       # kN: NSR-10 Tabla G.12.11-2 (PDF s.138): #5 (5/8") civata, cift kesme, lif dogrultusu, D=100 mm, IZINLI yuk
    "n_bolt": 4,               # culm ucu basina civata sayisi (kullanici karari); aralik >= 150 mm (NSR-10 G.12.11.3.13)
    "C_g": 0.93,               # NSR-10 Tabla G.12.11-3: 4 civata, Guadua elemani grup azaltma katsayisi (s.139)
    # --- Servis siniri ---
    "disp_limit_ratio": 150.0, # yer degistirme siniri = aciklik/150 (Manual ornegi; ISO 22156 sehim siniri vermez)

    # Beşikten-Kapıya (A1-A3) Gömülü Karbon Katsayıları -- celik/harc: ICE Educational V5.0 (Haz 2026); bambu: turetilmis (varsayim)
    "EC_bamboo": 0.30,         # kg CO2e / kg culm (A1-A3, biyojenik karbon HARIC): turetilmis; bkz. 04_Results/EC_BAMBOO_METHOD.md (aralik 0.09-1.23)
    "EC_steel": 2.38,          # kg CO2e / kg baglanti celigi: ICE Educational V5.0 (Haz 2026) "Steel, Plate" 2.38 (worldsteel 2023); galvanizli 2.62
    "EC_steel_tube": 2.51,     # kg CO2e / kg celik boru (CHS): ICE V5.0 "Steel, welded pipe" 2.51 (seamless tube 1.90)
    "EC_mortar": 0.18,         # kg CO2e / kg: ICE V5.0 harc 1:3; rotresiz grout satiri yok -> proxy (varsayim)
    "node_steel_mass": 4.50,   # kg / düğüm ("fixed" modu)
    "node_mortar_mass": 2.80   # kg / düğüm ("fixed" modu)
}
MATERIAL_PROPERTIES["F_j_Rd"] = (MATERIAL_PROPERTIES["n_bolt"] * MATERIAL_PROPERTIES["F_bolt_adm"]
                                 * MATERIAL_PROPERTIES["C_g"])   # kN = 49.3, baglanti siniri (NSR-10 izinli yuk)
MATERIAL_PROPERTIES["E_mean"] = MATERIAL_PROPERTIES["E_k"]      # FEM/SAP uyumu (ad korunur)

# ASD kapasite carpani: C_R * C_DF * C_T / FS  (yuk suresine gore)
ASD_K = {d: MATERIAL_PROPERTIES["C_R"] * v * MATERIAL_PROPERTIES["C_T"] / MATERIAL_PROPERTIES["FS"]
         for d, v in MATERIAL_PROPERTIES["C_DF"].items()}

# ==============================================================================
# 24 ELEMANLI AYRIK BAMBU KESİT KATALOĞU (Tablo 2: Morfolojik Çeşitlendirilmiş)
# ==============================================================================
# Kaynak: Kolombiya NSR-10 Título G & IStructE Manual (Trujillo et al., 2025)
# D: Dış Çap (mm), t: Et Kalınlığı (mm), t/D varyasyonu: 0.06 - 0.16
RAW_CATALOG_DATA = [
    (1,   80.0,  6.0),   # t/D = 0.075 (Tepe culm, ultra hafif)
    (2,   80.0,  9.0),   # t/D = 0.113 (Orta culm standart)
    (3,   80.0, 12.0),   # t/D = 0.150 (Dip culm, yüksek çekme)
    (4,   90.0,  7.0),   # t/D = 0.078
    (5,   90.0, 10.0),   # t/D = 0.111
    (6,   90.0, 14.0),   # t/D = 0.156
    (7,  100.0,  7.0),   # t/D = 0.070 (Yüksek r, minimum kütle)
    (8,  100.0, 10.0),   # t/D = 0.100
    (9,  100.0, 14.0),   # t/D = 0.140
    (10, 110.0,  8.0),   # t/D = 0.073
    (11, 110.0, 11.0),   # t/D = 0.100
    (12, 110.0, 15.0),   # t/D = 0.136
    (13, 120.0,  8.0),   # t/D = 0.067 (Geniş çap, hafif kütle)
    (14, 120.0, 12.0),   # t/D = 0.100
    (15, 120.0, 16.0),   # t/D = 0.133
    (16, 130.0,  9.0),   # t/D = 0.069
    (17, 130.0, 13.0),   # t/D = 0.100
    (18, 130.0, 18.0),   # t/D = 0.138
    (19, 140.0, 10.0),   # t/D = 0.071
    (20, 140.0, 15.0),   # t/D = 0.107
    (21, 140.0, 20.0),   # t/D = 0.143
    (22, 160.0, 10.0),   # t/D = 0.063 (Maksimum narinlik direnci)
    (23, 160.0, 15.0),   # t/D = 0.094
    (24, 160.0, 22.0),   # t/D = 0.138 (Maksimum basma kapasitesi)
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
