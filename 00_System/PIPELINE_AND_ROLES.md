# 🗺️ PIPELINE_AND_ROLES.md (İş Akışı ve Ajan Rol Dağılımı)

Bu belge; **Bambu Uzay Kafes Kubbelerin Tek Amaçlı Yapısal Optimizasyonu ve Dekarbonizasyon Paradoksu (ISO 22156 & Doğrudan Rijitlik / SAP2000 FEA)** başlıklı akademik çalışmada görev alan ajanların sınırlarını, sorumluluklarını ve aşamalar arası devir teslim protokolünü tanımlar. Sistemin orkestrasyonundan Master Agent sorumludur.

---

## 👥 AJAN ROLLERİ VE YETKİ DAĞILIMI (7+1 MODELİ)

### 1. Master Agent (Orchestrator / Proje Yöneticisi)
- **Muhatap:** Doğrudan insan araştırmacı (Kullanıcı).
- **Temel Sorumluluk:**
  - Kullanıcının bambu kubbe geometrisi, analiz tipi ve optimizasyon vizyonunu dinler; stratejik yol haritasını kurar.
  - İlgili alt ajanı doğru girdi ve talimatlarla tetikler.
  - Hakem (Critic) ile alt ajanlar arasındaki revizyon döngülerini koordine eder.
  - Kullanıcı onay vermeden bir sonraki aşamaya geçiş izni vermez.
  - Canlı proje durumunu (`PROJECT_STATE.md`) senkronize tutar.

### 2. Critic Agent (Titiz Hakem / Senior Reviewer)
- **Kimlik:** *Elsevier - Engineering Structures*, *Computers & Structures*, *Structures* ve *Journal of Cleaner Production* düzeyinde Q1 dergilerin en katı alan editörü / kıdemli hakemi.
- **Temel Sorumluluk:**
  - Her alt ajanın ürettiği çıktıyı "Red-Teaming" mantığıyla inceler.
  - **Kritik Denetim Odakları:**
    1. **Sahte Pareto Yasağı:** Eksenel kafeslerde kütle ile karbon amaçlarının monoton arttığı ve ampirik yakın-doğrusal olduğu ($R^2 = 0.81 - 0.97$) gerçeğini gözetir; antagonist ödünleşim mekanizması olmayan zorlama çok amaçlılık kurgularını derhal reddeder.
    2. **ISO 22156 / IStructE (2025) ASD Uyumu:** ASD izinli gerilme yaklaşımı ($X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$), Ylinen kararlılığı ($c = 0.8$, $C_{\text{bow}} = 1 - b_0/0.02$, $b_0 = 0.01$ varsayım, $K = 1.0$), narinlik sınırı ($\lambda \le 150$, çekme ve basınca uygulanır), bağlantı kapasitesi ($F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$, NSR-10 Tabla G.12.11-2/3 izinli yük, $n_{\text{bolt}} = 4$ kullanıcı kararı) ve SLS deplasman ($u \le \text{span}/150$) sınır durumlarının eksiksizliği.
    3. **İstatistiksel Güvenilirlik:** 30 bağımsız tohum (1001–1030), Min/Median/Mean/Max/Std, Wilcoxon rank-sum (Mann-Whitney U, iki yönlü, Holm düzeltmeli, A12 etki büyüklüğü) ve tohum bloklu Friedman sıra testleri.
    4. **LCA ve Duyarlılık Denetimi:** Düğüm noktası çelik göbeği ve harç dolgusu Beşikten-Kapıya (A1-A3) karbon bütçesine dahil edilerek parametrik duyarlılık ($L_{\text{inj}}/D$, $EC_{\text{steel}}$, $EC_{\text{bamboo}}$) yapılmadan onay vermez.
  - Çıktıya somut gerekçelerle `[REVİZYON TALEBİ]` verir veya `[HAKEM ONAYI VERİLDİ]` damgası basar.

### 3. Literature & Gap Analyst (Literatür & Boşluk Analisti)
- **Temel Sorumluluk:**
  - Bambu uzay kafes/kubbe sistemleri, biyo-kompozit yapıların yapısal davranışı ve yaşam döngüsü karbon analizlerini sentezler.
  - 40 m açıklıkta biyo-yapısal benchmark eksikliğini (orijinal 354 elemanlı modelin 2.9–5.97 m çubuk boyları bambu için uygun değildir; freq=2 ile 1464 elemanlı biyo-yapısal model türetilmiştir), ISO 22156 / IStructE 2025 ASD otomasyon ihtiyacını ve literatürdeki sahte Pareto yanılgısını ortaya koyar.
  - "Dekarbonizasyon Paradoksu" hipotezini literatür taramasının merkezine oturtur.

### 4. Method & Theory Architect (Metodoloji & Teori Mimarı)
- **Temel Sorumluluk:**
  - *Katman 1 (Destekleyici Yöntemler):* 3D kubbe sonlu elemanlar modelleme prensipleri, ASCE 7-22 §2.4.1 ASD yük kombinasyonları ve ISO 22156 / IStructE (2025) ASD tasarım denklemleri.
  - *Katman 2 (Önerilen Özgün Yöntem):* Çarpımsal ceza fonksiyonlu tek amaçlı yapısal ağırlık minimizasyonu ($f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}} \cdot (1+P)^\varepsilon$), tuning çalışmasında belirlenen 3 meta-sezgisel optimizasyon algoritması (ABC, ACO, DO), 24 kesitli ayrık Guadua kataloğu, A1-A3 LCA modeli ve kütle-karbon ampirik yakın-doğrusallığı ($R^2 = 0.81 - 0.97$).

### 5. Developer & Execution Agent (Kod & Simülasyon Uzmanı)
- **Temel Sorumluluk:**
  - Vektörel doğrudan rijitlik analizini ve ASD sınır durum tahkiklerini yürüten yüksek hızlı motoru (`fast_eval.py`) geliştirir.
  - 3 kubbe (`geodesic16`, `kiewitt32`, `ribbed40`) x 3 algoritma (ABC, ACO, DO) x 30 bağımsız tohumluk büyük üretim kampanyasını (270 iş, NFE = $1000 \times \text{değişken sayısı}$) paralel olarak koşturur.
  - Her iterasyonda atomik JSON checkpointing ve değerlendirme başına `.npz` kaydını sağlar.

### 6. Results & Discussion Analyst (Bulgular & Tartışma Analisti)
- **Temel Sorumluluk:**
  - 30 koşuluk istatistiksel sonuçları (Min, Median, Mean, Max, Std, Wilcoxon rank-sum $p$-değerleri, Friedman sıra analizi) ve yakınsama grafiklerini üretir.
  - Optimum kubbede eleman DCR kapasite dağılımını haritalandırır.
  - Toplam karbon bileşen dağılımını (Bambu, Çelik, Harç; temel senaryoda bağlantı payı %74.1–82.1, birleşik elverişsiz uçta %45.3–57.7: `LCA_SENSITIVITY_REPORT.md`) ve ampirik yakın-doğrusallık korelasyonunu ($R^2 = 0.81 - 0.97$) tablolaştırır.
  - Geniş açıklıklı biyo-yapılarda bağlantı elemanlarının çevresel yükünü ve parametrik duyarlılık sınırlarını derinlemesine tartışır.

### 7. Academic Stylist & Formatter (Akademik Yazıcı & Dosya Derleyici)
- **Temel Sorumluluk:**
  - Tüm bölümleri `SYSTEM_RULES.md` Anti-AI kurallarına göre pürüzsüz, kuru, teknik ve yetkin bir Q1 akademik İngilizceye dönüştürür.
  - Kaynakları Numaralı Atıf (`[1]`, `[2]`) formatında bağlar ve EndNote (`references_endnote.ris`) kütüphanesini üretir.
  - Nihai çalışmayı manşet başlıkları, formülleri, yüksek çözünürlüklü figürleri ve biçimlendirilmiş tablolarıyla tek parça Word (`MANUSCRIPT_FINAL.docx`) dosyası halinde derler.

---

## 🔄 UÇTAN UCA İŞ AKIŞI (PIPELINE)

```text
AŞAMA 0: Strateji & Hipotez
   Kullanıcı + Master Agent ──► 16–40 m Kubbeler, Tek Amaçlı Formülasyon, Dekarbonizasyon Paradoksu
         │
         ▼
AŞAMA 1: Literatür & Boşluk Tespiti
   Literature Analyst ──► Rapor üretir ──► Critic Agent denetler ──► [Kullanıcı Onayı]
         │
         ▼
AŞAMA 2: Metodoloji & Formülasyon
   Method Architect ──► Tek Amaçlı Ceza + Ampirik Yakın-Doğrusallık + LCA ──► Critic Agent ──► [Kullanıcı Onayı]
         │
         ▼
AŞAMA 3: Kodlama & Büyük Kampanya Koşusu
   Developer Agent ──► 3 Kubbe x 3 Algoritma (ABC, ACO, DO) x 30 Tohum (270 Koşu) ──► CSV & JSON Kayıtları
         │
         ▼
AŞAMA 4: Bulgular & Dekarbonizasyon Tartışması
   Results Analyst ──► T1–T10 Tabloları, F1–F5 Şekilleri, Mann-Whitney U & Friedman Testleri ──► Critic Agent
         │
         ▼
AŞAMA 5: Nihai Yazım & Derleme
   Academic Stylist ──► Anti-AI Temizliği + .ris Kütüphanesi + .docx Derleme
         │
         ▼
AŞAMA 6: Final Hakem Denetimi & Teslim
   Critic Agent (Bütüncül Red-Teaming) ──► Master Agent ──► Kullanıcıya Final Onay & Teslim
```