# Kampanya ozeti (ham sonuclar depoda degil)
- `summary.csv`: 270 is (3 kubbe x ABC/ACO/DO x 30 tohum), NFE = 1000 x tasarim degiskeni; `global_best*.json`: en hafif tasarimlar (gen, agirlik, SAP2000 dogrulamasi).
- `steel_reference_aisc37_summary.csv`: celik referans (37 AISC boru, ASD) 120 is.
- Ham kayitlar (her isin degerlendirme basina .npz ve yakinsama gecmisi, ~135 MB) `C:\BambuDome_campaign\full\results` altinda; arsivlenip ayri paylasilmalidir (Zenodo/Release).
- Uyari: `summary.csv` ve `global_best*.json` icindeki karbon sutunlari eski (ICE tabanli) faktorlerle yazildi, guncel degildir. Guncel karbon: `../tables/T5–T8`, `../LCA_SENSITIVITY_REPORT.md` (EC_b 0.243, EC_s 1.13, EC_pipe 1.701, EC_m 0.310).
- Uyari: `steel_reference_aisc37_summary.csv` karbon sutunu da eski faktorlerle yazildi (ornek: geodesic16 3410 kg; guncel T5 degeri 2211 kg).
