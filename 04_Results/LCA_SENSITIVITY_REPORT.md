# 🌿 BambuDome Beşikten-Kapıya (A1–A3) LCA Duyarlılık ve Karbon Ayrıştırma Raporu

Bu rapor; 40 m açıklıklı Guadua bambu uzay kafes kubbelerde bağlantı detaylarının (çelik mafsal flanşları + enjeksiyon harcı)
yapısal gömülü karbon bilançosundaki ağırlığını ve parametrik duyarlılık sınırlarını belgeler.

**Tasarım kaynağı:** `C:\BambuDome_campaign\full\results` içindeki her kubbe için en hafif uygun çözüm (kampanya sonucu, el ile girilmiş gen yok). Tasarımlar:

- `ribbed40`: 66.35 kN, algoritma ABC, tohum 1001
- `kiewitt32`: 41.06 kN, algoritma ABC, tohum 1001
- `geodesic16`: 5.80 kN, algoritma ABC, tohum 1001

---

## 1. Temel Durum (Base-Case) Karbon ve Kütle Dökümü

Varsayılan Parametreler: $L_{\text{inj}} = 2.5 D$, $EC_{\text{bamboo}} = 0.30$ (türetilmiş), $EC_{\text{steel}} = 2.38$ (ICE V5.0 plate), $EC_{\text{mortar}} = 0.18\text{ kg CO}_2\text{e/kg}$.

| Kubbe Modeli | Bambu Kütlesi (t) | Çelik Kütlesi (t) | Harç Kütlesi (t) | Toplam Kütle (t) | Bambu Karbonu % | Çelik Karbonu % | Harç Karbonu % | Toplam Bağlantı Karbonu % | Toplam Karbon (t CO2e) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ribbed40 | 6.76 | 2.47 | 19.02 | 28.26 | 17.89 | 51.92 | 30.19 | 82.11 | 11.34 |
| kiewitt32 | 4.19 | 0.79 | 9.43 | 14.41 | 25.93 | 39.03 | 35.04 | 74.07 | 4.84 |
| geodesic16 | 0.59 | 0.21 | 1.06 | 1.86 | 20.61 | 57.25 | 22.13 | 79.39 | 0.86 |

> Temel senaryoda bağlantı bileşenleri (çelik + harç) toplam gömülü karbonun %74.1–%82.1'ini, yalnızca çelik %39.0–%57.3'ini oluşturur (bu tasarımlar ve bu varsayımlar için; EC değerleri doğrulanmamış varsayımdır).

---

## 2. Parametrik Duyarlılık Analizi (Sensitivity Analysis)

### Model: `ribbed40`

#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\text{inj}} / D \in [1.5, 3.5]$)
| L_inj / D | Mortar Mass (t) | Total Carbon (t CO2e) | Steel Carbon % | Mortar Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- | --- | --- |
| 1.50 | 11.41 | 9.97 | 59.05 | 20.60 | 79.65 | 20.35 |
| 2.00 | 15.22 | 10.66 | 55.25 | 25.70 | 80.96 | 19.04 |
| 2.50 | 19.02 | 11.34 | 51.92 | 30.19 | 82.11 | 17.89 |
| 3.00 | 22.83 | 12.03 | 48.96 | 34.16 | 83.13 | 16.87 |
| 3.50 | 26.63 | 12.71 | 46.32 | 37.71 | 84.04 | 15.96 |

#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\text{steel}} \in [1.2, 3.0]\text{ kg CO}_2\text{e/kg}$)
| EC_steel (kg/kg) | Total Carbon (t CO2e) | Steel Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- |
| 1.20 | 8.42 | 35.25 | 75.91 | 24.09 |
| 1.90 | 10.15 | 46.30 | 80.02 | 19.98 |
| 2.38 | 11.34 | 51.92 | 82.11 | 17.89 |
| 2.62 | 11.93 | 54.31 | 83.00 | 17.00 |
| 3.00 | 12.87 | 57.65 | 84.24 | 15.76 |

#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\text{bamboo}} \in [0.09, 1.23]\text{ kg CO}_2\text{e/kg}$)
| EC_bamboo (kg/kg) | Total Carbon (t CO2e) | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- |
| 0.09 | 9.92 | 93.86 | 6.14 |
| 0.20 | 10.66 | 87.32 | 12.68 |
| 0.30 | 11.34 | 82.11 | 17.89 |
| 0.47 | 12.49 | 74.55 | 25.45 |
| 1.23 | 17.63 | 52.82 | 47.18 |

### Model: `kiewitt32`

#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\text{inj}} / D \in [1.5, 3.5]$)
| L_inj / D | Mortar Mass (t) | Total Carbon (t CO2e) | Steel Carbon % | Mortar Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- | --- | --- |
| 1.50 | 5.66 | 4.16 | 45.39 | 24.45 | 69.84 | 30.16 |
| 2.00 | 7.54 | 4.50 | 41.97 | 30.15 | 72.11 | 27.89 |
| 2.50 | 9.43 | 4.84 | 39.03 | 35.04 | 74.07 | 25.93 |
| 3.00 | 11.31 | 5.18 | 36.47 | 39.30 | 75.77 | 24.23 |
| 3.50 | 13.20 | 5.52 | 34.23 | 43.03 | 77.26 | 22.74 |

#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\text{steel}} \in [1.2, 3.0]\text{ kg CO}_2\text{e/kg}$)
| EC_steel (kg/kg) | Total Carbon (t CO2e) | Steel Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- |
| 1.20 | 3.91 | 24.40 | 67.85 | 32.15 |
| 1.90 | 4.46 | 33.82 | 71.85 | 28.15 |
| 2.38 | 4.84 | 39.03 | 74.07 | 25.93 |
| 2.62 | 5.03 | 41.34 | 75.05 | 24.95 |
| 3.00 | 5.33 | 44.65 | 76.46 | 23.54 |

#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\text{bamboo}} \in [0.09, 1.23]\text{ kg CO}_2\text{e/kg}$)
| EC_bamboo (kg/kg) | Total Carbon (t CO2e) | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- |
| 0.09 | 3.96 | 90.50 | 9.50 |
| 0.20 | 4.42 | 81.08 | 18.92 |
| 0.30 | 4.84 | 74.07 | 25.93 |
| 0.47 | 5.55 | 64.58 | 35.42 |
| 1.23 | 8.73 | 41.06 | 58.94 |

### Model: `geodesic16`

#### a) Enjeksiyon Uzunluğunun Etkisi ($L_{\text{inj}} / D \in [1.5, 3.5]$)
| L_inj / D | Mortar Mass (t) | Total Carbon (t CO2e) | Steel Carbon % | Mortar Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- | --- | --- |
| 1.50 | 0.63 | 0.78 | 62.81 | 14.57 | 77.38 | 22.62 |
| 2.00 | 0.85 | 0.82 | 59.90 | 18.53 | 78.43 | 21.57 |
| 2.50 | 1.06 | 0.86 | 57.25 | 22.13 | 79.39 | 20.61 |
| 3.00 | 1.27 | 0.90 | 54.83 | 25.43 | 80.26 | 19.74 |
| 3.50 | 1.48 | 0.94 | 52.60 | 28.47 | 81.06 | 18.94 |

#### b) Çelik Gömülü Karbon Katsayısının Etkisi ($EC_{\text{steel}} \in [1.2, 3.0]\text{ kg CO}_2\text{e/kg}$)
| EC_steel (kg/kg) | Total Carbon (t CO2e) | Steel Carbon % | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- | --- |
| 1.20 | 0.62 | 40.31 | 71.22 | 28.78 |
| 1.90 | 0.76 | 51.67 | 76.70 | 23.30 |
| 2.38 | 0.86 | 57.25 | 79.39 | 20.61 |
| 2.62 | 0.91 | 59.59 | 80.51 | 19.49 |
| 3.00 | 0.99 | 62.80 | 82.06 | 17.94 |

#### c) Bambu Gömülü Karbon Katsayısının Etkisi ($EC_{\text{bamboo}} \in [0.09, 1.23]\text{ kg CO}_2\text{e/kg}$)
| EC_bamboo (kg/kg) | Total Carbon (t CO2e) | Total Joint Carbon % | Bamboo Carbon % |
| --- | --- | --- | --- |
| 0.09 | 0.74 | 92.77 | 7.23 |
| 0.20 | 0.80 | 85.24 | 14.76 |
| 0.30 | 0.86 | 79.39 | 20.61 |
| 0.47 | 0.96 | 71.08 | 28.92 |
| 1.23 | 1.41 | 48.43 | 51.57 |

---

## 3. Senaryo Sınırları (hesaplanan)

Parametreler bağlantı payı açısından en elverişsiz uçta (L_inj=1.5D, EC_steel=1.2, EC_bamboo=0.47, EC_mortar=0.12 birlikte):

- `ribbed40`: bağlantı payı %57.7 (bambu %42.3)
- `kiewitt32`: bağlantı payı %45.3 (bambu %54.7)
- `geodesic16`: bağlantı payı %53.9 (bambu %46.1)

Tekil taramalar a–c tablolarındadır. Bu rapordaki sayılar varsayılan EC değerlerine bağlıdır ve literatürle doğrulanana kadar nihai bulgu sayılmamalıdır.
