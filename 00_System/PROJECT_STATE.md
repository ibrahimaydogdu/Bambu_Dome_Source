# 🧠 PROJECT_STATE.md (Canlı Proje Hafızası ve Durum Paneli)

*Son Güncelleme: 2026-10-09 | Büyük Dokümantasyon Revizyonu: ASD Mekaniği, 3 Algoritmalı Kampanya Tasarımı ve Teyitli Bilimsel Temeller*  
*Aktif Tur (Iteration / Round): Round #7 (Tam Belge Senkronizasyonu ve Hakem/Yazar Standardizasyonu)*  
*Mevcut Aşama: Aşama 3 (Büyük Kampanya Hazırlığı ve Kod Entegrasyonu)*  
*Aktif Profil: Profil A - Yapısal Optimizasyon, Biyo-Esaslı Malzemeler ve Sürdürülebilirlik*  

---

## 📌 1. PROJE KİMLİĞİ VE HEDEFLER

- **Çalışmanın Başlığı:** *Is Bamboo Truly Zero-Carbon? Single-Objective Structural Optimization and the Decarbonization Paradox of Large-Span Spatial Domes*
- **Hedef Q1 Dergileri:** 
  - *Journal of Cleaner Production* (Elsevier, IF: 9.7+)
  - *Engineering Structures* (Elsevier, IF: 5.5+)
  - *Computers & Structures* (Elsevier, IF: 4.8+)
  - *Structures* (Elsevier / IStructE, IF: 4.1+)
- **Ana Problem & Kapsam:** 
  - 40 m açıklıklı biyo-yapısal uzay kafes kubbe benchmarkının (*Guadua angustifolia* culmları ile) **ISO 22156:2021** ve **IStructE (2025)** İzinli Gerilme Tasarımı (**ASD**) ile ASCE 7-22 kısıtları altında tek amaçlı yapısal ağırlık minimizasyonu.
  - Kesite bağlı bağlantı modelinde kütle ile gömülü karbon arasındaki ampirik yakın-doğrusallık ($R^2 = 0.81 - 0.97$) sebebiyle çok-amaçlı Pareto cephesinin tek noktaya / dar aralığa çökmesi gerekçesiyle tek amaçlı optimizasyon ($\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$, $\varepsilon=2.0$) yürütülmesi ve post-optimizasyon Beşikten-Kapıya (A1–A3) LCA ayrıştırması modeli.
  - **Araştırma Konusu:** Biyo-yapısal kubbelerde hibrit bağlantı bileşenlerinin (çelik manşon/düğüm ve enjeksiyon harcı) toplam gömülü karbondaki payı ve bu payın envanter parametrelerine duyarlılığı ("Dekarbonizasyon Paradoksu").

---

## 🚦 2. AŞAMA ONAY VE İLERLEME TABLOSU

| Aşama No | Aşama Adı | Görevli Ajan | Durum | Hakem (Critic) Kararı | Kullanıcı Onayı |
| :--- :---: | :--- | :--- | :--- : | :--- : | :--- : |
| **0** | Strateji, Kapsam & Problem Tanımı | Master Agent | 🟢 Tamamlandı | [HAKEM ONAYI VERİLDİ] | Onaylandı |
| **1** | Literatür & Boşluk Tespiti (Dekarbonizasyon Paradoksu) | Literature Analyst | 🟢 Tamamlandı | [HAKEM ONAYI VERİLDİ] | Onaylandı |
| **2** | Metodoloji, Formülasyon & ASD Tasarımı | Method Architect | 🟢 Tamamlandı | [HAKEM ONAYI VERİLDİ] | Onaylandı |
| **3** | Kod Geliştirme, Hızlı Değerlendirici & Kampanya Motoru | Developer Agent | 🟡 Aktif | [HAKEM ONAYI VERİLDİ] | Kullanıcı Onayı Bekleniyor |
| **4** | Bulgular, 3 Algoritma 30 Seed İstatistikleri & LCA | Results Analyst | ⚪ Beklemede | - | - |
| **5** | Anti-AI Nihai Metin & Referanslar | Academic Stylist | ⚪ Beklemede | - | - |
| **6** | Final Hakem Denetimi & Word (.docx) | Master + Stylist | ⚪ Beklemede | - | - |

*(Durum İfadeleri: ⚪ Beklemede | 🟡 Aktif | 🔴 Revizyonda | 🟢 Tamamlandı)*

---

## 🔄 3. DİNAMİK TUR GÜNLÜĞÜ (ITERATION HISTORY)

### 📍 [Round 7] - [2026-10-09] - Master Agent & Tüm Sistem Ajanları (Büyük Belge ve Standart Revizyonu)
Kullanıcının `00_System/DOCS_UPDATE_PROMPT.md` talimatı doğrultusunda tüm proje belgeleri (`README.md`, `AGENTS.md`, `00_System/*`, `01_Literature/*`, `02_Methods/*`, `03_Code_Execution/*`, `04_Results/*`, `05_Drafts/*`, `06_Review_Audit/*`) baştan aşağı revize edildi ve kesin tutarlılık sağlandı:

1. **Mekanik Model: LRFD → ASD (ISO 22156 / IStructE Manual 2025):**
   - LRFD ve $\gamma_M$ ifadeleri tamamen kaldırıldı; İzinli Gerilme Tasarımı (ASD: $X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$, Manual Denklem 3.9, 6.5) formüle edildi.
   - Servis Sınıfı 2 katsayıları: $C_{DF} = 0.55$ (kalıcı), $0.65$ (geçici), $0.85$ (anlık rüzgar); $FS = 2.0$; $C_R = 0.90$ [varsayım]; $C_T = 1.0$. Kapasite çarpanları $k_{\text{ASD}} = 0.2475 / 0.2925 / 0.3825$.
   - Yük kombinasyonları: ASCE 7-22 §2.4.1 ASD faktörsüz kombinasyonlar ($D$; $D+S$; $D+0.6W$; $D+0.75S+0.45W$; $0.6D+0.6W$).
   - Basınç ve Burkulma: Ylinen parametresi $c = 0.8$ (Manual Denklem 6.1, Ek A6.2); Euler elastik burkulma yükü $P_{e,k} = \pi^2 E_k I C_{\text{bow}} / (KL)^2$; $C_{\text{bow}} = 1 - b_0/0.02$, $b_0 = 0.01$ [varsayım]; $K = 1.0$; izin verilen kapasite $N_{cr,\text{izin}} = P_{cr,k} \cdot k_{\text{ASD}}$. Hatalı "$\beta_c = 0.10$ ISO 22156 Madde 7'den" ifadesi tüm belgelerden temizlendi.
   - Malzeme: $E_k = 10\,000\text{ MPa}$ (Manual Tablo 4.4 şema alt sınırı, tüm $D/t$ için; $E_{05}$ kavramı kaldırıldı); $f_{t,0,k} = 40.0\text{ MPa}$; $f_{c,0,k} = 37.8\text{ MPa}$ ($n=922$); $\rho = 700\text{ kg/m}^3$.
   - Narinlik sınırı: $\lambda \le 150$ [kaynağı doğrulanamadı, varsayım].
   - SLS Deplasman sınırı: $u_{\max} \le span/150 = 266.67\text{ mm}$ (IStructE Manual örneği; ISO 22156 sınır vermez). Eski $L/360$ ve "ASCE 7 sehim" ifadeleri kaldırıldı.
   - Bağlantı Kapasitesi: $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\max} = 2 \times 26.6 = 53.2\text{ kN}$. $F_{\text{bolt},\max} = 26.6\text{ kN}$ Correal vd. 2021 Tablo 4 Ø15.9 mm tek cıvata deney tepe yüküdür. $n_{\text{bolt}} = 2$ çapraz cıvata varsayımdır (gerekçe: tek cıvatada ribbed40'ta 231 eleman, kiewitt32'de 8 eleman kesitten bağımsız sınırı aşmaktadır).
   - Doğrulanmış referans ağırlıklar: Kesit 24'te tüm kubbeler uygun ($DCR \le 0.75$); ağırlıklar `geodesic16` $20.9\text{ kN}$, `kiewitt32` $84.5\text{ kN}$, `ribbed40` $190.0\text{ kN}$. Eski geçersiz optimum ağırlıklar ("~4 kN", "~28 kN", "~58 kN") silindi.

2. **Optimizasyon Tasarımı ve 3 Algoritmalı Kampanya:**
   - Değerlendirme bütçesi: $\text{NFE} = 1000 \times \text{tasarım grubu sayısı}$ (ribbed40: 43 000, kiewitt32: 22 000, geodesic16: 23 000). Eski 4040 NFE ifadeleri kaldırıldı.
   - Algoritma sayısı: 16 algoritmalık havuzdan `04_Results/TUNING_STUDY.md` duyarlılık analiziyle seçilen **3 algoritma ([TUNING SONUCUNA GÖRE])** ile kampanya yürütülecek (adaylar: ABC, ACO, DO, GWO, WOA, TLBO; tohum 2001–2005). AGENTS.md ve tüm ilgili kurallar buna göre uyarlandı.
   - İstatistik: İki yönlü Holm-düzeltmeli Wilcoxon rank-sum (Mann-Whitney U, Vargha-Delaney $A_{12}$) ve tohum bloklu Friedman sıra testi; 30 bağımsız tohum (1001–1030). "Wilcoxon signed-rank" ifadeleri kaldırıldı.
   - Deterministik kayıt: Her iş için atomik JSON checkpoint (RNG durumu dahil) ve değerlendirme başına `.npz` veri kaydı.
   - Süre bütçesi: 7 paralel işçide ribbed40 koşusu ~16 dk; 270 işlik tam kampanya (3 algoritma × 3 kubbe × 30 tohum) tahmini duvar saati ≈ 3.5–4 saat.

3. **Tek Amaçlı Formülasyon ve Topoloji Netleştirmesi:**
   - $\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$, $\varepsilon=2.0$.
   - "$\nabla EC \parallel \nabla W$ analitik ispatı" ve "$R^2 \approx 0.99$" iddiaları kaldırıldı. Kesite bağlı bağlantı modelinde ampirik olarak $R^2 = 0.81 - 0.97$ ($r = 0.91 - 0.98$) seviyesinde yakın-doğrusallık (quasi-collinearity) bulunduğu ve Pareto cephesinin tek noktaya / dar aralığa çöktüğü açıklandı.
   - Topoloji: Saka (1991) 40 m çelik benchmark'ı 354 elemanlıdır ($L \in [2.9, 5.97]\text{ m}$, bambu için uygulanamaz). Bu çalışmadaki `ribbed40` modeli Saka geometrisinden uyarlanan $freq=2$ yoğunlaştırmasıdır (1464 eleman, $L \in [0.76, 3.08]\text{ m}$).

4. **Gömülü Karbon (LCA) ve Duyarlılık:**
   - $EC_b = 0.35, EC_s = 2.10, EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ katsayıları unverified literature assumption (varsayım; ICE v3.0 ve Zea Escamilla & Habert 2014 Tablo 8 teyit bekliyor) olarak etiketlendi.
   - Önceden yazılmış sabit manşet yüzdeler ("%50–65", "%67–75") kaldırıldı. Bağlantı payının en elverişsiz parametre kombinasyonunda %43–52'ye düştüğü (kiewitt32'de %50'nin altına indiği) ve nihai yüzdelerin gerçek kampanya optimumlarından hesaplanacağı belirtildi.

5. **Literatür Atıfları:**
   - Papers klasöründeki birincil kaynaklarla doğrulandı: Trujillo et al. (2025 IStructE Manual), Zea Escamilla & Habert (2014), Correal et al. (2021), Paraskeva et al. (2019, Kao Jue M6 cıvata), Jones & Hammond (2019 ICE v3.0), ISO 22156:2021.
   - Doğrulanamayan atıflar ("Trujillo 2021", "Paraskeva 2017", "MOABC" atıfları) tamamen kaldırıldı.

---

## 🧩 4. AJANLARA ÖZEL AKTİF HAFIZA NOTLARI

### 🏗️ Developer Agent:
- Yalnızca **Tek Amaçlı Yapısal Optimizasyon** koşturulur: $\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$ ($\varepsilon = 2.0$).
- ASD sınır durumları: $X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$ ($FS=2.0, C_R=0.90, C_T=1.0$). Ylinen $c=0.8, C_{\text{bow}}, b_0=0.01$, bağlantı $F_{j,Rd}=53.2\text{ kN}$ ($n_{\text{bolt}}=2$), sehim $span/150 = 267\text{ mm}$.
- `tuning_study.py` çıktısına göre seçilecek **3 algoritma ([TUNING SONUCUNA GÖRE])** 30 tohum (1001–1030) ve 3 kubbe üzerinde koşturulacak (270 iş).
- NFE bütçesi: $1000 \times N_g$ (ribbed40: 43 000, kiewitt32: 22 000, geodesic16: 23 000). Checkpoint ve `.npz` kayıtları tutulur.

### ⚖️ Critic Agent:
- Sahte Pareto veya yapay çok-amaçlılık tespit edildiği an derhal reddedilir.
- LRFD veya $\gamma_M$ katsayıları içeren modeller reddedilir; ISO 22156 / IStructE 2025 ASD kuralları denetlenir.
- 3 algoritma kıyaslamasında iki yönlü Holm-düzeltmeli Wilcoxon rank-sum (Mann-Whitney U) ve Friedman sıra testleri aranır.
- LCA katsayılarının literatür varsayımı olduğu ve bağlantı payının parametrik duyarlılıkla incelendiği kontrol edilir.