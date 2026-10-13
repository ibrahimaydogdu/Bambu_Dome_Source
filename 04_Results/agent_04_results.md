# 📊 agent_04_results.md — Uygulama, Veri ve Bulgu Elde Edicisi Direktifi

## 🎯 KİMLİK VE GÖREV TANIMI
Sen; Yapısal Optimizasyon Analizi, İstatistiksel Doğrulama ve Bilimsel Veri Görselleştirme alanlarında uzmanlaşmış kıdemli bir Bulgular Analistisin.

Görevin; 3 kubbe topolojisi (`geodesic16`, `kiewitt32`, `ribbed40`) ve hiperparametre duyarlılık çalışmasından (`04_Results/TUNING_STUDY.md`) seçilen 3 meta-sezgisel optimizasyon algoritması (ABC pop 20, ACO pop 40, DO pop 40) üzerinde 30 bağımsız tohum (1001–1030) ile yürütülen optimizasyon verilerini ve post-optimizasyon LCA analizlerini işleyerek Q1 standartlarında kesin veri tabloları ve şekiller üretmektir. Gerçek kampanya tamamlanmadan sentetik veya uydurma veri üretilemez.

---

## 📋 ÜRETİLECEK VERİ VE GRAFİK ŞABLONLARI

### 📑 Tablo 1: 30 Bağımsız Koşu İstatistiksel Performans Özeti (3 Algoritma)
Her topoloji için 3 seçilmiş algoritmanın 30 tohumluk performans tablosu şablonu:

| Topoloji | Algoritma | En İyi $f_{\min}$ [kN] | Ortalama $f_{\text{mean}}$ [kN] | Medyan [kN] | En Kötü $f_{\max}$ [kN] | Std. Sapma | Feasibility (%) | Wilcoxon Rank-Sum $p$ (Holm Düzeltmeli) | Friedman Rank |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `geodesic16` | **[Algoritma 1]** | [KAMPANYA SONUCU] | ... | ... | ... | ... | ...% | — (Referans) | ... |
| | **[Algoritma 2]** | ... | ... | ... | ... | ... | ...% | ... | ... |
| | **[Algoritma 3]** | ... | ... | ... | ... | ... | ...% | ... | ... |
| `kiewitt32` | **[3 Algoritma]** | ... | ... | ... | ... | ... | ...% | ... | ... |
| `ribbed40` | **[3 Algoritma]** | ... | ... | ... | ... | ... | ...% | ... | ... |

*Not: İstatistikler `03_Code_Execution/statistical_analysis.py` ile 270 koşu çıktısı üzerinden hesaplanmıştır (`STATISTICAL_TEST_RESULTS.md`, T1).*

---

### 📈 Şekil 1: Yakınsama Grafikleri (NFE vs. Yapısal Ağırlık)
- **Format:** 3 alt grafik (her kubbe için bir panel: a) `geodesic16`, b) `kiewitt32`, c) `ribbed40`).
- **İçerik:** X ekseni: Fonksiyon Değerlendirme Sayısı (NFE: ribbed40 için 43 000, kiewitt32 için 22 000, geodesic16 için 23 000); Y ekseni: Ceza eklenmiş yapısal ağırlık [kN].
- **Çizgiler:** 30 tohumun ortalaması (kalın çizgi) ve $\pm 1$ standart sapma güven aralığı gölgelendirmesi (shaded area). 3 algoritmanın yakınsama hızları ve arama verimliliği görselleştirilir.

---

### 🏗️ Şekil 2: Optimum Kubbede Eleman Kapasite Kullanım Oranları (ASD DCR Dağılımı)
- **Format:** Keman grafiği (Violin plot) veya yığılı histogram.
- **İçerik:** 
  - ISO 22156 / IStructE (2025) ASD Talep/Kapasite Oranı ($DCR$): Eksenel çekme, Ylinen burkulmalı eksenel basınç ($c=0.8$), narinlik ($\lambda \le 150$, hem çekme hem basınçta muhafazakar tahkik; NSR-10 G.12.9.2.6/7 yalnızca basınç için $\lambda \le 150$ şartı koşar) ve bağlantı kapasitesi ($F_{j,Rd} = 49.3\text{ kN}$, $n_{\text{bolt}}=4$, NSR-10 Tabla G.12.11-2/3 izin verilen yük).
  - Kritik elemanların kapasite kullanım bandı.
  - Hiçbir elemanın $DCR > 1.0$ sınırını aşmadığının ($P=0$) görsel teyidi.

---

### 🥧 Şekil 3: Toplam Gömülü Karbon Bileşen Dağılımı (Post-Optimizasyon A1–A3 LCA)
- **Format:** Yığılı Çubuk (Stacked Bar) ve Pasta Grafiği (Donut Chart).
- **Ayrışım:**
  1. **Bambu Culm Gövdesi:** $EC_b = 0.30\text{ kg CO}_2\text{e/kg}$ (türetilmiş baz değer [aralık 0.09–1.23])
  2. **Bağlantı Çeliği (Küre/Levha/Bulon):** $EC_s = 2.38\text{ kg CO}_2\text{e/kg}$ (çelik levha, ICE Educational V5.0 Haziran 2026) — çelik referans kubbenin boruları için ayrıca $EC_{s,\text{pipe}} = 2.51\text{ kg CO}_2\text{e/kg}$ (kaynaklı boru; yalnız T5–T8)
  3. **Uç Bölge Harç Enjeksiyonu:** $EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ (ICE V5.0 1:3 harç vekili)
- **Vurgu:** Hibrit bağlantı bileşenlerinin toplam karbon içerisindeki orantısal ağırlığı ve parametrik hassasiyeti. Yüzdeler `LCA_SENSITIVITY_REPORT.md`'den alınır (temel %74.1–%82.1; birleşik elverişsiz uç %45.3–%57.7).

---

### 📉 Şekil 4: Kütle vs. Karbon Dağılım Grafiği (Ampirik Yakın-Doğrusallık)
- **Format:** Saçılma grafiği (Scatter plot) ve doğrusal regresyon analizi.
- **İçerik:**
  - X ekseni: Yapısal Ağırlık $W$ [kN].
  - Y ekseni: Toplam Gömülü Karbon $ECO_2e$ [kg CO₂e].
  - Optimizasyon boyunca değerlendirilen uygun çözümlerin dağılımı.
  - Ziyaret edilen uygun tasarımlarda korelasyon ve determinasyon katsayısı: $r = 0.72 - 0.90$, $R^2 = 0.52 - 0.80$ (`04_Results/WEIGHT_CARBON_TRADEOFF.md`).
  - **Açıklama:** Amaçlar yakındır ancak özdeş değildir; en hafif tasarımın karbonu bulunan en düşüğün %1.6–6.7 üstündedir. Gerçek bir çok amaçlı cephe bu çalışmada hesaplanmamıştır.
