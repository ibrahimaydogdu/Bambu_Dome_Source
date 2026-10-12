# 🔸 TIER2_PROPOSED_METHODOLOGY.md: Önerilen Özgün Yöntem ve 3 Meta-Sezgisel Mimari (Katman 2)

Bu belge; biyo-kompozit uzay kafes ve kubbe sistemlerin tek amaçlı yapısal ağırlık optimizasyonu, ISO 22156:2021 ve IStructE (2025) ASD sınır durum kısıtlarının çarpımsal ceza fonksiyonuyla entegrasyonu, meta-sezgisel optimizasyon mimarisi ve post-optimizasyon Beşikten-Kapıya (A1–A3) LCA modelini tanımlar.

---

## 1. Tek Amaçlı Yapısal Optimizasyon Problemi ve Matematiksel Formülasyon

Problem, $N_g$ adet bağımsız eleman grubunun ayrık enkesit indekslerini arayan, ISO 22156:2021 / IStructE (2025) ASD ve ASCE 7-22 kısıtları altında tek amaçlı yapısal ağırlık minimizasyonudur:

$$\text{Denklem (10):} \quad \min_{\mathbf{X}} f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}}(\mathbf{X}) \cdot \left(1 + P(\mathbf{X})\right)^\varepsilon$$

$$\text{tasarım uzayı:} \quad \mathbf{X} = [x_1, x_2, \dots, x_{N_g}]^T \in \mathbb{Z}^{N_g}, \quad x_i \in \{1, 2, \dots, 24\}$$

- $W_{\text{bambu}}(\mathbf{X})$: Toplam yapısal bambu culm ağırlığı [kN]:
  $$W_{\text{bambu}}(\mathbf{X}) = \sum_{i=1}^{N_e} \rho_b \cdot g \cdot A_i(x_i) \cdot L_i$$
- $P(\mathbf{X})$: Toplam normalize kısıt ihlali:
  $$P(\mathbf{X}) = \sum_{g=1}^{N_g} \max_{i \in g} \max\left(0, \, DCR_i - 1.0\right) + \max\left(0, \, \frac{u_{\max}}{u_{\text{izin}}} - 1.0\right)$$
  burada her $i$ elemanı için talep/kapasite oranı:
  $$DCR_i = \max\left( \frac{N_{t,i}}{N_{t,\text{izin}}}, \, \frac{N_{c,i}}{N_{cr,\text{izin}}}, \, \frac{\lambda_i}{150}, \, \frac{|N_i|}{F_{j,Rd}} \right)$$
- $\varepsilon = 2.0$: Çarpımsal ceza üssü. Uygun çözümlerde ($P=0$) $f_{\text{pen}} = W_{\text{bambu}}$ tam yapısal ağırlığa eşittir; ihlal durumunda arama ajanı hızla uygun bölgeye itilir.
- $u_{\text{izin}} = span/150 = 40\,000 / 150 \approx 266.67\text{ mm}$ (IStructE Manual 2025 örneği).

---

## 2. Post-Optimizasyon Beşikten-Kapıya (A1–A3) LCA ve Bağlantı Karbonu Duyarlılığı

Optimizasyon sürecinde yapay çok-amaçlı Pareto kurguları yerine tek amaçlı fiziksel ağırlık minimizasyonu yürütülür; elde edilen optimum ve uygulanabilir tasarımlar üzerinde Beşikten-Kapıya (Modül A1–A3) karbon analizi optimizasyon sonrası (post-processing) aşamasında hesaplanır:

$$\text{Denklem (11):} \quad ECO_2e(\mathbf{X}) = m_{\text{bambu}}(\mathbf{X}) \cdot EC_b + m_{\text{steel}}(\mathbf{X}) \cdot EC_s + m_{\text{mortar}}(\mathbf{X}) \cdot EC_m$$

- $EC_b = 0.35\text{ kg CO}_2\text{e/kg}$ [Varsayım; Zea Escamilla & Habert 2014 Tablo 8 ile teyit edilecek]
- $EC_s = 2.10\text{ kg CO}_2\text{e/kg}$ [Varsayım; ICE v3.0 xlsx ile teyit edilecek]
- $EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ [Varsayım; ICE v3.0 xlsx ile teyit edilecek]

### Eksenel Kafeslerde Ampirik Yakın-Doğrusallık ve Çok-Amaçlı Çöküş:
Sabit düğüm kütleli basitleştirilmiş modelde $f_2 = 35.68 \cdot f_1 + \text{sabit}$ olup ilişki tam doğrusaldır ($R^2 = 1.0$). Kesite bağlı harç ve bağlantı modelinde ise uygun örneklerde kütle ile karbon arasındaki korelasyon $r = 0.91 - 0.98$ ve $R^2 = 0.81 - 0.97$ olarak ölçülmektedir. Bu durum iki amaç arasında **ampirik bir yakın-doğrusallık (quasi-collinearity)** olduğunu gösterir; analitik bir türev özdeşliği değildir. Bu yüksek korelasyon nedeniyle çok-amaçlı optimizasyon (NSGA-II, MOABC vb.) Pareto cephesini tek bir noktaya veya son derece dar bir aralığa çöktürür.

### Bağlantı Karbonunun Parametrik Duyarlılığı:
Hibrit bağlantıların (çelik manşon + harç dolgu) toplam gömülü karbondaki payı, en elverişsiz parametre kombinasyonlarında %43–52 seviyelerine düşebilmektedir (kiewitt32 kubbesinde %50'nin altına inmektedir). Bu nedenle "Dekarbonizasyon Paradoksu" kesin bir yasa değil, envanter sınırlarına ve bağlantı detaylandırmasına duyarlı parametrik bir araştırma konusudur.

---

## 3. Ayrık Tasarım Değişkeni Eşleme Operatörü (Discrete Mapping)

Sürekli meta-sezgisel arama ajanlarının ürettiği reel pozisyon vektörleri $\hat{\mathbf{X}} \in [\mathbf{X}_{min}, \mathbf{X}_{max}]^{N_g}$, 24 elemanlı Guadua enkesit kataloğundaki tamsayı indekslere haritalanır:

$$\text{Denklem (12):} \quad x_i = \text{clip}\left(\text{round}(\hat{x}_i), \, 1, \, 24\right), \quad \forall i \in \{1, \dots, N_g\}$$

---

## 4. Meta-Sezgisel Optimizasyon Motoru ve 3 Algoritmalı Kampanya Tasarımı

Kod tabanında 16 meta-sezgisel optimizasyon algoritmasından oluşan geniş bir kütüphane (`metaheuristic_optimizers.py`) yer almaktadır (HS, BBO, WOA, DO, ABC, ACO, BSO, CSA, FA, GOA, TLBO, TSA, GWO, HBA, AO, SSO).

### 3 Algoritmalı Kampanya Mimarisi:
Kullanıcı kararı uyarınca nihai deneysel kampanya, 16 algoritma yerine hiperparametre duyarlılık çalışmasından (`04_Results/TUNING_STUDY.md`) seçilecek **3 algoritma ([TUNING SONUCUNA GÖRE])** (2 bilinen yüksek performanslı yöntem + 1 görece yeni yöntem; aday havuzu: ABC, ACO, DO, GWO, WOA, TLBO; tohum 2001–2005) ile yürütülür.

### Hesaplama Bütçesi (NFE):
Hesaplama bütçesi her algoritma için tasarım değişkeni (grup) sayısı ile orantılı olarak sabitlenmiştir:
$$\text{NFE} = 1000 \times N_g$$
- **ribbed40:** 43 grup $\implies \text{NFE} = 43\,000$
- **kiewitt32:** 22 grup $\implies \text{NFE} = 22\,000$
- **geodesic16:** 23 grup $\implies \text{NFE} = 23\,000$

Her iş için checkpoint (RNG durumu dahil deterministik devam) ve değerlendirme başına `.npz` veri kaydı tutulur. 7 paralel işçide 270 işin (3 algoritma × 3 kubbe × 30 tohum) tahmini duvar saati süresi ≈ 3.5–4 saattir.

---

## 5. İstatistiksel Değerlendirme ve Hipotez Testi Protokolü

1. **30 Bağımsız Tohum (Seeds 1001–1030):** Stokastik performansı doğrulamak için her algoritma 30 bağımsız başlangıç koşusuna tabi tutulur.
2. **Wilcoxon Rank-Sum (Mann-Whitney U) Testi:** Algoritmalar arası ikili kıyaslamalarda çift taraflı non-parametrik test, çoklu karşılaştırma için **Holm düzeltmesi** ve Vargha-Delaney $A_{12}$ etki büyüklüğü hesaplanır ($p < 0.05$).
3. **Friedman Sıra Testi:** Tohum bloklu küresel sıra hiyerarşisi belirlenir.
4. **Feasibility Oranı (%):** 30 koşuda katı $P=0$ şartını sağlayan koşu yüzdesi.
