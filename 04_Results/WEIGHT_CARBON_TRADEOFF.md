# Agirlik - gomulu karbon iliskisi ve belirleyici sinir durumlar (hesaplanan)

Betik: `03_Code_Execution/weight_carbon_tradeoff.py`. Veri: kampanyada ziyaret edilen UYGUN degerlendirmeler (`penalty = 0`), her biri icin gen -> kutle -> karbon GUNCEL EC degerleriyle yeniden hesaplandi (EC_b = 0.30, EC_s = 2.38, EC_m = 0.18; hub 2.0 kg/dugum, 0.5 kg/cubuk ucu, L_inj = 2.5 D). Kayitli `carbon_kg` eski EC ile yazildigi icin yalniz karsilastirma sutununda verilmistir. Degerlendirmeler tek amacli (agirlik) aramanin ziyaret ettigi noktalardir; rastgele ornek ya da cok amacli aramanin cephesi degildir.

## 1. Korelasyon ve baskin olmayan nokta kumesi

| Dome | Uygun degerlendirme | Tekil (W, C) cifti | r (guncel EC) | R2 (guncel EC) | r (kayitli, eski EC) | R2 (kayitli, eski EC) | Baskin olmayan nokta | En dusuk W: W [kN] | C [kg CO2e] | En dusuk C: W [kN] | C [kg CO2e] | C farki (minW vs minC) [%] | W farki (minC vs minW) [%] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 1237620 | 266027 | 0.897 | 0.804 | 0.912 | 0.832 | 11 | 5.800 | 860.5 | 6.535 | 847.2 | 1.57 | 12.66 |
| Kiewitt | 975273 | 107831 | 0.724 | 0.524 | 0.782 | 0.611 | 48 | 41.058 | 4842.1 | 45.745 | 4536.2 | 6.74 | 11.41 |
| Ribbed | 1866958 | 680666 | 0.857 | 0.734 | 0.874 | 0.763 | 69 | 66.352 | 11341.1 | 72.728 | 10869.0 | 4.34 | 9.61 |

## 2. Optimum tasarimlarda belirleyici sinir durum (grup sayisi)

Her grupta en buyuk D/C degerini veren kontrol sayilir. `Ortalama`: 90 uygun kosunun ortalamasi.

| Dome | Tasarim | Cekme | Basinc | Narinlik | Baglanti | Toplam grup |
|---|---|---|---|---|---|---|
| Geodesic | en iyi | 0 | 19 | 4 | 0 | 23 |
| Geodesic | ortalama (90 kosu) [%] | 0.0 | 81.1 | 18.9 | 0.0 | 100 |
| Kiewitt | en iyi | 0 | 21 | 1 | 0 | 22 |
| Kiewitt | ortalama (90 kosu) [%] | 0.0 | 95.5 | 4.5 | 0.0 | 100 |
| Ribbed | en iyi | 0 | 41 | 2 | 0 | 43 |
| Ribbed | ortalama (90 kosu) [%] | 0.0 | 93.4 | 6.5 | 0.2 | 100 |
