# Kampanya Özeti (Nihai Senkronize Veriler)
- `summary.csv`: 270 iş (3 kubbe x ABC/ACO/DO x 30 tohum), NFE = 1000 x tasarım değişkeni; `global_best*.json`: en hafif tasarımlar (gen, ağırlık, SAP2000 doğrulaması).
- `steel_reference_aisc37_summary.csv`: çelik referans (37 AISC boru, ASD) 120 iş.
- Ham kayıtlar (her işin değerlendirme başına .npz ve yakınsama geçmişi, ~135 MB) `C:\BambuDome_campaign\full\results` altında; gerektiğinde Zenodo/Release ile paylaşılabilir.
- Karbon sütunları: Tüm `best_embodied_carbon_kgCO2e` ve `carbon_kgCO2e` sütunları, EPD faktörleri (EC_bamboo 0.243, EC_steel 1.13, EC_pipe 1.701, EC_mortar 0.310 kg CO2e/kg) ile yeniden hesaplanarak `../tables/T5–T8` ve `../LCA_SENSITIVITY_REPORT.md` ile tam senkronize edilmiştir.
