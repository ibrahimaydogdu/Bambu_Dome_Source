# BambuDome — Single-Objective Structural Optimization and The Decarbonization Paradox of Large-Span Bamboo Space Domes

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![SAP2000 OAPI / Direct FEA](https://img.shields.io/badge/FEA-Direct%20Stiffness%20%2B%20SAP2000-orange)](https://www.csiamerica.com/)
[![ISO 22156:2021](https://img.shields.io/badge/Design%20Code-ISO%2022156%3A2021-green)](https://www.iso.org/standard/77013.html)
[![IStructE 2025 Manual](https://img.shields.io/badge/Manual-IStructE%202025-brightgreen)](https://www.istructe.org/)
[![LCA A1-A3](https://img.shields.io/badge/LCA-Cradle--to--Gate%20A1--A3-teal)](https://ice.org/)

---

## 🏛️ Proje Özeti ve Bilimsel Paradigma

Bu çalışma, **40 metrelik endüstriyel açıklıklı biyo-kompozit uzay kafes kubbe** sistemlerinin (*Guadua angustifolia* culmları ile) yapısal güvenliğini, kısıtlı meta-sezgisel optimizasyonunu ve yaşam döngüsü gömülü karbon dinamiklerini inceleyen kapsamlı bir hesaplamalı mekanik ve sürdürülebilirlik araştırmasıdır.

### 🚨 Stratejik Paradigma: Tek Amaçlı Formülasyon ve Post-Optimizasyon LCA
Eksenel kafes optimizasyonlarında kütle, maliyet ve gömülü karbon amaçları kesit boyutları ile monoton artmakta ve antagonist bir mekanik ödünleşim (trade-off) mekanizması barındırmamaktadır. Bu durum çok amaçlı Pareto arayışlarının tekil bir optimuma ya da çok dar bir aralığa çökmesine yol açmaktadır. Çalışmamız bu ampirik gerçeği dikkate alarak iki aşamalı bir hesaplama çerçevesi uygular:

1. **Titiz Tek Amaçlı Yapısal Ağırlık Minimizasyonu:**  
   $$\min f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}}(\mathbf{X}) \cdot (1 + P(\mathbf{X}))^\varepsilon, \quad \varepsilon = 2.0$$
   - **Tasarım Yaklaşımı (ASD):** ISO 22156:2021 ve IStructE (2025) Manual uyarınca İzin Verilen Gerilme Tasarımı (ASD): $X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$ (Manual Denk. 3.9, 6.5).
   - **Kapasite ve Kararlılık Kısıtları:** Eksenel çekme ($f_{t,k} = 40\text{ MPa}$), Ylinen elasto-plastik sütun kararlılığı ($c = 0.8$, $C_{\text{bow}} = 1 - b_0/0.02$, $b_0 = 0.01$ varsayım, $K = 1.0$), narinlik ($\lambda \le 150$, çekme ve basınca uygulanır), harç dolgulu mafsal eksenel kapasitesi ($F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$, NSR-10 Tabla G.12.11-2/3 izinli yük ve $n_{\text{bolt}} = 4$ kullanıcı kararı).
   - **Servis Edilebilirlik Sınır Durumu (SLS):** Maksimum kubbe çökmesi $u_{\max} \le \text{span}/150$ ($40\text{ m}$ için $267\text{ mm}$, IStructE 2025 Manual örneği).
   - **İstatistiksel Doğrulama:** 30 bağımsız tohum (1001–1030), Mann-Whitney U (iki yönlü, Holm düzeltmeli, A12 etki büyüklüğü) ve tohum bloklu Friedman sıra testi.
2. **Beşikten-Kapıya (A1–A3) LCA ve Bağlantı Karbonu Analizi:**  
   - Elde edilen optimum tasarımlar üzerinde prefabrik çelik düğüm göbeği, saplamalar ve harç enjeksiyonlu uç detayları modellenerek bileşen bazlı gömülü karbon dökümü ve parametrik duyarlılık yürütülür.
   - **Araştırma Sorusu:** Büyük açıklıklı biyo-yapısal uzay kafeslerde bağlantı çeliği ve harç dolgusu taban yükünün toplam gömülü karbon bilançosundaki gerçek ağırlığı ve "Dekarbonizasyon Paradoksu"nun parametrik sınırları incelenmektedir (Temel senaryoda bağlantı karbonu payı %74.1–%82.1; en elverişsiz parametre ucunda kiewitt32'de %45.3'e düşerek duyarlılık sergiler).

---

## 🔬 Dört Temel Bilimsel Katkı (Novelty & Contributions)

1. **Çelikten Biyo-Kompozite Benchmark Adaptasyonu:** Saka'nın (1991) 40 m açıklıklı 354-elemanlı çelik kubbe benchmarkının (orijinal çubuk boyları 2.9–5.97 m olup bambu narinlik sınırını aşmaktadır) $freq=2$ yoğunlaştırması ile 1464 elemanlı (çubuk boyları 0.76–3.08 m) biyo-yapısal uzay kubbeye uyarlanması.
2. **IStructE (2025) & ISO 22156 (2021) ASD Tasarım Otomasyonu:** $E_k = 10,000\text{ MPa}$, $f_{c,k} = 37.8\text{ MPa}$, $f_{t,k} = 40\text{ MPa}$, Servis Sınıfı 2 süre katsayıları ($C_{DF} = 0.55/0.65/0.85$), $FS = 2$, $C_R = 0.90$, $C_T = 1.0$ ve ASCE 7-22 §2.4.1 ASD faktörsüz yük kombinasyonları altında doğrudan rijitlik matrisi ile tam kısıt denetimi.
3. **Bağlantı Karbonu Hakimiyeti ve Duyarlılık:** Bambu culm gövdesinin hafifletilmesine karşın harç dolgulu çelik düğüm noktalarının karbon payının parametrik duyarlılıkla ($L_{\text{inj}}/D$, $EC_{\text{steel}}$, $EC_{\text{bamboo}}$) analiz edilmesi.
4. **Kütle ve Karbonun Ampirik Yakın-Doğrusallığı:** Eksenel kafes sistemlerde kütle ile karbon arasındaki ilişkinin incelenmesi; sabit düğüm modelinde $f_2$ ile $f_1$ tam doğrusal ($\text{corr} = 1.000$), kesite bağlı modelde ampirik yakın-doğrusal ($R^2 = 0.81 - 0.97$, $\text{corr} = 0.91 - 0.98$) olduğunu ve antagonist ödünleşim yokluğu nedeniyle Pareto cephesinin çöktüğünü ortaya koyması.

---

## ⚙️ Optimizasyon Algoritmaları ve Kampanya Tasarımı

Sistemde 16 tek amaçlı meta-sezgisel optimizasyon algoritması (`metaheuristic_optimizers.py`) kodlanmış ve doğrulanmıştır:
`HS, BBO, WOA, DO, ABC, ACO, BSO, CSA, FA, GOA, TLBO, TSA, GWO, HBA, AO, SSO`.

Kullanıcı kararı doğrultusunda 30 tohumluk büyük üretim kampanyası için **3 algoritma (2 bilinen iyi + 1 görece yeni yöntem)** seçilmiştir:
- **Algoritma Seçimi:** `04_Results/TUNING_STUDY.md` hiper-parametre duyarlılık çalışmasından elde edilen performansa göre seçilen 3 algoritma: **ABC (pop 20), ACO (pop 40), DO (pop 40)**.
- **Hesaplama Bütçesi:** NFE = $1000 \times \text{tasarım değişkeni sayısı}$ (her algoritma için eşit):
  - `ribbed40`: $43,000\text{ NFE}$ (43 grup)
  - `kiewitt32`: $22,000\text{ NFE}$ (22 grup)
  - `geodesic16`: $23,000\text{ NFE}$ (23 grup)
- **Kampanya Sonuçları (En İyi Ağırlıklar, 270/270 Feasible, P = 0):**
  - `geodesic16`: **5.800 kN** (ABC, s1001)
  - `kiewitt32`: **41.058 kN** (ABC, s1001; ACO da aynı değere ulaştı)
  - `ribbed40`: **66.352 kN** (ABC, s1001; ACO da aynı değere ulaştı)
- **Süre ve Paralel Yürütme:** 7 paralel işçide 270 işlik tam kampanya 3 sa 21 dk içinde tamamlanmıştır (2026-10-09).

---

## 📁 Klasör Yapısı

```
BambuDome/
├── 00_System/                  # Ajan rolleri, sistem mimarisi ve canlı proje hafızası
│   ├── system_architecture.md  # Tek amaçlı optimizasyon ve LCA veri akış mimarisi
│   ├── PIPELINE_AND_ROLES.md   # 7+1 ajan çalışma protokolü
│   ├── MASTER_AGENT.md         # Baş orkestratör direktifi
│   ├── PROJECT_STATE.md        # Canlı durum ve hafıza kaydı
│   └── SYSTEM_RULES.md         # Anti-AI yazım kuralları ve akademik anayasa
├── 01_Literature/              # Literatür matrisi ve gap analizi
│   ├── agent_01_intro_literature.md  # Giriş ve literatür ajanı talimatı
│   ├── LITERATURE_MATRIX.md          # 4 tematik literatür matrisi
│   ├── RESEARCH_GAP_AND_NOVELTY.md   # Dekarbonizasyon paradoksu & araştırma boşluğu
│   └── INTRODUCTION_SECTION_DRAFT.md # Q1 giriş bölümü akademik taslağı
├── 02_Methods/                 # Metodoloji ve matematiksel formülasyon
│   ├── agent_03_methodology.md       # Metot mimarı talimatı
│   ├── MATHEMATICAL_FORMULATION.md   # ISO 22156 & tek amaçlı ceza formülasyonu
│   ├── TIER1_BASELINE_METHODS.md     # Destekleyici FEA ve standart yöntemler
│   └── TIER2_PROPOSED_METHODOLOGY.md # Önerilen meta-sezgisel akış şeması
├── 03_Code_Execution/          # Yüksek performanslı Python optimizasyon motoru
│   ├── bamboo_catalog.py             # 24 Guadua kesit kataloğu (Tablo 2); fiyat: price_scenarios.py (T9)
│   ├── fast_eval.py                  # Vektörel doğrudan rijitlik & ASD kısıt tahkikleri
│   ├── metaheuristic_optimizers.py   # 16 tek amaçlı meta-sezgisel optimizasyon algoritması
│   ├── run_full_campaign.py          # Durdurulup sürdürülebilir kampanya otomasyonu
│   ├── statistical_analysis.py       # Wilcoxon rank-sum (Mann-Whitney U) & Friedman testleri
│   ├── lca_sensitivity_analysis.py   # Beşikten-kapıya (A1-A3) parametrik duyarlılık taraması
│   ├── CAMPAIGN_EXECUTION_PLAN.md    # 3 kubbe x 3 algoritma x 30 seed planı
│   └── test_units.py                 # Birim testleri
├── 04_Results/                 # Sonuçlar ve istatistiksel analiz
│   ├── agent_04_results.md           # Sonuç analisti talimatı
│   ├── TUNING_STUDY.md               # Algoritma hiper-parametre duyarlılık çalışması
│   └── LCA_SENSITIVITY_REPORT.md     # Parametrik LCA duyarlılık dökümü
├── 05_Drafts/                  # Makale taslağı ve yayın hazırlığı
│   ├── agent_06_writer.md            # Makale sentez ve yazıcı ajanı talimatı
│   ├── STYLIST_AGENT_PROMPT.md       # Anti-AI akademik üslup kılavuzu
│   └── MANUSCRIPT_FINAL.md           # Tam metin makale taslağı
└── 06_Review_Audit/            # Kıdemli hakem denetim havuzu
    ├── agent_02_reviewer.md          # Titiz değerlendirme hakemi talimatı
    ├── CRITIC_PROMPT.md              # Hakem denetim filtreleri ve kırmızı çizgiler
    ├── AUDIT_CHECKLIST.md            # Resmi hakem denetim cetveli
    └── REVIEW_LOG/                   # Hakem denetim raporları (Round 1-6)
```

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.10+
- NumPy, SciPy, Pandas, Matplotlib

```bash
# Bağımlılıkları yükleyin
pip install numpy scipy pandas matplotlib

# Doğrulama testlerini çalıştırın
cd 03_Code_Execution
python test_units.py
python test_fast_eval.py
```

### 30 Tohumluk Üretim Kampanyasını Başlatma
```bash
# Ön kontrol (preflight)
python run_full_campaign.py preflight --profile full

# Tam kampanya başlatma (3 kubbe x 3 algoritma x 30 tohum = 270 iş)
python run_full_campaign.py start --profile full --background

# Durum izleme
python run_full_campaign.py status --profile full
```
