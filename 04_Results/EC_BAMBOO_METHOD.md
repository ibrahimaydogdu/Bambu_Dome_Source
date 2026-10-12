# Bambu culm gömülü karbonu (A1–A3) için türetme yöntemi

**Amaç:** Doğrudan kaynağı olmayan EC_bambu (kg CO₂e/kg yuvarlak culm, A1–A3, **biyojenik karbon hariç**) değerini, elimizdeki yayınlardan izlenebilir bir yöntemle türetmek. Kod değeri: **0,30** (aralık 0,09–1,23).

## Yöntem
EC_bambu(d) = **EC_üretim + EC_nakliye(d)**
- **EC_üretim** (hasat, kürleme/emprenye, kurutma): iki bağımsız sınırdan geometrik ortalama.
  - Alt sınır (**varsayım**; culm için doğrudan kaynak yok): INBAR TR35 Tablo 1 (p.20), laminat bambu panelinin kg başına **hasat 0,0156 + plantasyon→şerit tesisi nakliyesi 0,0168 = 0,0324 kg CO₂e/kg** (üretim sonrası işlem yok).
  - Üst sınır: ICE V5.0 (Haz. 2026) "Timber, Softwood – No Carbon Storage" **0,2626 kg CO₂e/kg** (A1–A3, fırın kurutmalı biçilmiş ahşap; ICE Summary satır 945). Aynı tabloda Hardwood 0,3056, Glulam 0,28, CLT 0,25 kg/kg.
  - Temel: √(0,0324 × 0,2626) = **0,092 kg CO₂e/kg**.
- **EC_nakliye(d) = 0,185·10⁻³ × d[km] × f_yük** kg CO₂e/kg.
  - Yoğunluk: INBAR TR35 Tablo 1: 28 t kamyon (EURO3), 12,51 t·km → 2,314 kg CO₂e ⇒ **0,185 kg CO₂e/(t·km)**.
  - Yük faktörü: Zea Escamilla & Habert 2014 (s. 3–4): içi boş culmların yığın yoğunluğu **100 kg/m³**; kamyon hacimle dolduğu için taşınan kütle EcoInvent'in modellediği ağırlık kapasitesinden **3,8 kat düşük** ⇒ f_yük = 3,8 (hacim sınırlı), 1,0 (kütle sınırlı alt sınır).
- **Üst bağımsız doğrulama:** Zea Escamilla & Habert 2014 Tablo 8: 1 m³ bambu direk iklim değişikliği **12,37 mPt**; normalizasyon 9950 kg CO₂ ⇒ 123 kg CO₂e/m³; yığın yoğunluğu 100 kg/m³ ⇒ **1,23 kg CO₂e/kg** (uzun mesafe/ithalat senaryosu; nakliye payı baskın). Katı et yoğunluğu 700 kg/m³ alınırsa 0,176 (yanlış birim; kullanılmaz).

## Senaryolar (kg CO₂e/kg culm)
| Tedarik | d | Alt (üretim 0,032; f=1) | **Temel (üretim 0,092; f=3,8)** | Üst (üretim 0,263; f=3,8) |
|---|---|---|---|---|
| Yerel | 50 km | 0,041 | **0,127** | 0,298 |
| Bölgesel | 300 km | 0,088 | **0,303** | 0,474 |
| İthal (Zea 2014) | uzun | — | **1,23** | — |

**Seçim:** bölgesel tedarik (300 km) için temel değer **0,30** kg CO₂e/kg; duyarlılık aralığı **0,09 – 1,23**. Önceki 0,35 değeri bu aralıkta; türetilmiş değerin ~%14 üstündeydi.

## Sınırlamalar (makalede yazılmalı)
1. TR35 verisi laminat panel içindir (hasat/nakliye adımları culm'a benzer, ama kg başına verim farkı düzeltilmedi; alt sınır iyimser).
2. Emprenye (boraks) ve açık havada kurutma için doğrudan veri yok; ICE softwood üst sınır olarak kullanıldı.
3. Biyojenik karbon (depolama) hariç: Vogtländer 2010 / TR35 culm için **5,69 kg CO₂/kg** depolama bildirir (Zea 2018, s.3 aktarımı). Yaşam sonu (yakma) kredisi ve depolama A1–A3 dışıdır.
4. 1,23 kg/kg Avrupa'ya ithalat senaryosudur; Kolombiya/yerel kullanım için uygun değil.
5. Kaynak doğrulaması: Restrepo 2016 (bambu levha) ve Zea 2018 (bina m² başına) culm kg/kg vermez; yalnızca bağlam (Zea 2018, Tablo 2: Kolombiya bambu çerçeveli evde CO₂e: bambu %6,4, çelik %34,7, nakliye %49,0).
