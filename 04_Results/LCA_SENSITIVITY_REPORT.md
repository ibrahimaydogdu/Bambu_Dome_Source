# 🌿 BambuDome Beşikten-Kapıya (A1–A3) LCA Duyarlılık ve Karbon Ayrıştırma Raporu

Bu rapor; 16, 32 ve 40 m açıklıklı Guadua bambu uzay kafes kubbelerde bağlantı detaylarının (çelik mafsal flanşları + enjeksiyon harcı)
yapısal gömülü karbon bilançosundaki ağırlığını ve parametrik duyarlılık sınırlarını belgeler.

**Tasarım kaynağı:** `C:\BambuDome_campaign\full\results` içindeki her kubbe için en hafif uygun çözüm (kampanya sonucu, el ile girilmiş gen yok). Tasarımlar:

- `ribbed40`: 66.35 kN, algoritma ABC, tohum 1001
- `kiewitt32`: 41.06 kN, algoritma ABC, tohum 1001
- `geodesic16`: 5.80 kN, algoritma ABC, tohum 1001

---

## 1. Temel Durum (Base-Case) Karbon ve Kütle Dökümü

Varsayılan Parametreler: $L_{\text{inj}} = 2.5 D$, $EC_{\text{bamboo}} = 0.243$ (türetilmiş), $EC_{\text{steel}} = 1.13$ (bauforumstahl EPD), $EC_{\text{mortar}} = 0.310\text{ kg CO}_2\text{e/kg}$ (SikaGrout-312 HP EPD).

| Kubbe Modeli | Bambu Kütlesi (t) | Çelik Kütlesi (t) | Harç Kütlesi (t) | Toplam Kütle (t) | Bambu Karbonu % | Çelik Karbonu % | Harç Karbonu % | Toplam Bağlantı Karbonu % | Toplam Karbon (t CO2e) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ribbed40 | 6.76 | 2.47 | 19.02 | 28.26 | 15.90 | 27.05 | 57.05 | 84.10 | 10.34 |
| kiewitt32 | 4.19 | 0.79 | 9.43 | 14.41 | 21.03 | 18.55 | 60.42 | 78.97 | 4.84 |
| geodesic16 | 0.59 | 0.21 | 1.06 | 1.86 | 20.36 | 33.15 | 46.49 | 79.64 | 0.71 |

> Temel senaryoda bağlantı bileşenleri (çelik + harç) toplam gömülü karbonun %79.0–%84.1'ini, yalnızca çelik %18.6–%33.1'ini oluşturur (bu tasarımlar için; $EC_s$ ve $EC_m$ değerleri beyan edilmiş EPD değerleridir (bauforumstahl, SikaGrout-312 HP), $EC_b$ INBAR TR35 ve Zea & Habert 2014'ten türetilmiş baz değerdir).

---

## 2. Parametrik Duyarlılık Analizi (Sensitivity Analysis)

### Model: `ribbed40`

#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\text{inj}} / D \in [1.5, 3.5]$)
| L_inj / D | Mortar Mass (t) | Total Carbon (t CO2e) | Steel Carbon % | Mortar Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- | --- | --- |
| 1.50 | 11.41 | 7.98 | 35.05 | 44.35 | 79.40 | 20.60 |
| 2.00 | 15.22 | 9.16 | 30.53 | 51.52 | 82.05 | 17.95 |
| 2.50 | 19.02 | 10.34 | 27.05 | 57.05 | 84.10 | 15.90 |
| 3.00 | 22.83 | 11.52 | 24.28 | 61.45 | 85.73 | 14.27 |
| 3.50 | 26.63 | 12.69 | 22.02 | 65.03 | 87.05 | 12.95 |

#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\text{steel}} \in [0.565, 2.26]\text{ kg CO}_2\text{e/kg}$)
| EC_steel (kg/kg) | Total Carbon (t CO2e) | Steel Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- |
| 0.56 | 8.94 | 15.64 | 81.61 | 18.39 |
| 0.85 | 9.64 | 21.81 | 82.96 | 17.04 |
| 1.13 | 10.34 | 27.05 | 84.10 | 15.90 |
| 1.70 | 11.75 | 35.81 | 86.01 | 13.99 |
| 2.26 | 13.13 | 42.58 | 87.48 | 12.52 |

#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\text{bamboo}} \in [0.0324, 1.23]\text{ kg CO}_2\text{e/kg}$)
| EC_bamboo (kg/kg) | Total Carbon (t CO2e) | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- |
| 0.03 | 8.91 | 97.54 | 2.46 |
| 0.10 | 9.37 | 92.78 | 7.22 |
| 0.24 | 10.34 | 84.10 | 15.90 |
| 0.50 | 12.07 | 71.99 | 28.01 |
| 1.23 | 17.01 | 51.10 | 48.90 |

### Model: `kiewitt32`

#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\text{inj}} / D \in [1.5, 3.5]$)
| L_inj / D | Mortar Mass (t) | Total Carbon (t CO2e) | Steel Carbon % | Mortar Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- | --- | --- |
| 1.50 | 5.66 | 3.67 | 24.46 | 47.81 | 72.27 | 27.73 |
| 2.00 | 7.54 | 4.25 | 21.10 | 54.98 | 76.08 | 23.92 |
| 2.50 | 9.43 | 4.84 | 18.55 | 60.42 | 78.97 | 21.03 |
| 3.00 | 11.31 | 5.42 | 16.55 | 64.69 | 81.24 | 18.76 |
| 3.50 | 13.20 | 6.01 | 14.94 | 68.12 | 83.06 | 16.94 |

#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\text{steel}} \in [0.565, 2.26]\text{ kg CO}_2\text{e/kg}$)
| EC_steel (kg/kg) | Total Carbon (t CO2e) | Steel Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- |
| 0.56 | 4.39 | 10.22 | 76.82 | 23.18 |
| 0.85 | 4.61 | 14.63 | 77.96 | 22.04 |
| 1.13 | 4.84 | 18.55 | 78.97 | 21.03 |
| 1.70 | 5.29 | 25.52 | 80.77 | 19.23 |
| 2.26 | 5.73 | 31.30 | 82.26 | 17.74 |

#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\text{bamboo}} \in [0.0324, 1.23]\text{ kg CO}_2\text{e/kg}$)
| EC_bamboo (kg/kg) | Total Carbon (t CO2e) | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- |
| 0.03 | 3.96 | 96.57 | 3.43 |
| 0.10 | 4.24 | 90.12 | 9.88 |
| 0.24 | 4.84 | 78.97 | 21.03 |
| 0.50 | 5.91 | 64.60 | 35.40 |
| 1.23 | 8.97 | 42.59 | 57.41 |

### Model: `geodesic16`

#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\text{inj}} / D \in [1.5, 3.5]$)
| L_inj / D | Mortar Mass (t) | Total Carbon (t CO2e) | Steel Carbon % | Mortar Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- | --- | --- |
| 1.50 | 0.63 | 0.57 | 40.72 | 34.26 | 74.99 | 25.01 |
| 2.00 | 0.85 | 0.64 | 36.55 | 41.00 | 77.55 | 22.45 |
| 2.50 | 1.06 | 0.71 | 33.15 | 46.49 | 79.64 | 20.36 |
| 3.00 | 1.27 | 0.77 | 30.33 | 51.04 | 81.37 | 18.63 |
| 3.50 | 1.48 | 0.84 | 27.95 | 54.88 | 82.83 | 17.17 |

#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\text{steel}} \in [0.565, 2.26]\text{ kg CO}_2\text{e/kg}$)
| EC_steel (kg/kg) | Total Carbon (t CO2e) | Steel Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- |
| 0.56 | 0.59 | 19.87 | 75.59 | 24.41 |
| 0.85 | 0.65 | 27.17 | 77.82 | 22.18 |
| 1.13 | 0.71 | 33.15 | 79.64 | 20.36 |
| 1.70 | 0.82 | 42.73 | 82.55 | 17.45 |
| 2.26 | 0.94 | 49.79 | 84.71 | 15.29 |

#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\text{bamboo}} \in [0.0324, 1.23]\text{ kg CO}_2\text{e/kg}$)
| EC_bamboo (kg/kg) | Total Carbon (t CO2e) | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- |
| 0.03 | 0.58 | 96.70 | 3.30 |
| 0.10 | 0.62 | 90.48 | 9.52 |
| 0.24 | 0.71 | 79.64 | 20.36 |
| 0.50 | 0.86 | 65.53 | 34.47 |
| 1.23 | 1.29 | 43.59 | 56.41 |

---

## 3. Senaryo Sınırları (hesaplanan)

Birleşik senaryo: parametreler bağlantı payını azaltan yönde birlikte uygulandı (L_inj=1.5D, EC_steel=0.565, EC_bamboo=0.50, EC_mortar=0.155). Bu, tek parametreli taramaların en düşük değeri değildir:

- `ribbed40`: bağlantı payı %48.4 (bambu %51.6)
- `kiewitt32`: bağlantı payı %38.8 (bambu %61.2)
- `geodesic16`: bağlantı payı %42.1 (bambu %57.9)

Tek parametreli taramalarda (a–c) görülen en düşük bağlantı payı: `ribbed40` %51.1, `kiewitt32` %42.6, `geodesic16` %43.6.

Tekil taramalar a–c tablolarındadır. Bu rapordaki sayılar varsayılan EC değerlerine bağlıdır ve literatürle doğrulanana kadar nihai bulgu sayılmamalıdır.
