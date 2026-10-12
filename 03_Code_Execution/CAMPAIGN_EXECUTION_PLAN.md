# 🚀 ULUSLARARASI AKADEMİK (Q1/SCI) BÜYÜK KAMPANYA PLANI (FULL RUN SCENARIO)
## Bambu Uzay Kubbe Sistemlerinin Tek Amaçlı Yapısal Optimizasyonu ve Dekarbonizasyon Paradoksu (ISO 22156 / IStructE 2025 ASD)

**Doküman:** `03_Code_Execution/CAMPAIGN_EXECUTION_PLAN.md`  
**Rol:** Computational Structural Engineering & AI Optimization Reviewer  

---

## 🎯 1. STRATEJİK PARADİGMA VE AMAÇ FONKSİYONU FORMÜLASYONU

Eksenel kafeslerde kesite bağlı bağlantı modelinde kütle ile gömülü karbon arasındaki korelasyon $r = 0.91 - 0.98$ ($R^2 = 0.81 - 0.97$) olarak ampirik bir yakın-doğrusallık (quasi-collinearity) gösterdiğinden, çok-amaçlı Pareto cephesi tek bir noktaya veya son derece dar bir aralığa çökmektedir. Bu nedenle çok-amaçlı sözde Pareto kurgusu terk edilmiş ve **Tek Amaçlı Yapısal Ağırlık Optimizasyonu + Post-Optimizasyon Beşikten-Kapıya LCA Ayrıştırması** modeline geçilmiştir.

### 1.1. Tek Amaçlı Yapısal Ağırlık Minimizasyonu ($f_{\text{pen}}$ - Minimize)
ISO 22156:2021, IStructE (2025) ASD ve ASCE 7-22 şartlarını tam sağlayan en hafif bambu kubbe tasarımı aranır:

$$f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}}(\mathbf{X}) \cdot (1 + P(\mathbf{X}))^\varepsilon \quad [\text{kN}]$$

Burada:
- $W_{\text{bambu}}(\mathbf{X}) = \frac{g}{1000} \sum_{i=1}^{N_m} \rho_b \cdot A_i(x_i) \cdot L_i \quad [\text{kN}]$
- $\rho_b = 700\text{ kg/m}^3$ (*Guadua angustifolia* yoğunluğu; IStructE Manual 2025 Tablo 4.4 şema)
- $A_i(x_i)$: $i$. çubuğun 24 kesitli katalogdan seçilen kesit alanı ($\text{m}^2$)
- $L_i$: Çubuk boyu ($\text{m}$)
- $g = 9.81\text{ m/s}^2$
- $\varepsilon = 2.0$ (Çarpımsal ceza üssü)
- $P(\mathbf{X})$: Boyutsuz normalize toplam kısıt ihlali:
  $$P(\mathbf{X}) = \sum_{g=1}^{N_g} \max_{i \in g} \max\left(DCR_i - 1.0, \, 0.0\right) + \max\left(\frac{u_{\max}}{u_{\text{izin}}} - 1.0, \, 0.0\right)$$

### 1.2. İzinli Gerilme Tasarımı (ASD) Kısıtları (IStructE Manual 2025 / ISO 22156)
- **Kapasite Çarpanı ve Güvenlik:** $X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$ (Manual Denklem 3.9, 6.5).
  - $FS = 2.0$, $C_R = 0.90$ [varsayım], $C_T = 1.0$.
  - $C_{DF} = 0.55$ ($D$, kalıcı), $0.65$ ($D+S$, geçici), $0.85$ ($W$ içeren kombinasyonlar, anlık).
  - Malzeme: $f_{c,0,k} = 37.8\text{ MPa}$, $f_{t,0,k} = 40.0\text{ MPa}$, $E_k = 10\,000\text{ MPa}$.
- **Eksenel Çekme:** $DCR_{t,i} = N_{t,i} / (A_i \cdot f_{t,0,\text{izin}}) \le 1.0$.
- **Eksenel Basınç ve Ylinen Burkulması (IStructE Manual 2025 Denklem 6.1–6.5):**
  - $P_{e,k} = \pi^2 E_k I C_{\text{bow}} / (K L)^2$, $C_{\text{bow}} = 1 - b_0 / 0.02$, $b_0 = 0.01$ [varsayım], $K = 1.0$.
  - Ylinen parametresi $c = 0.8$ (Manual Denklem 6.1, Ek A6.2).
  - $N_{cr,\text{izin}} = P_{cr,k} \cdot C_R \cdot C_{DF} \cdot C_T / FS$, $DCR_{c,i} = N_{c,i} / N_{cr,\text{izin}} \le 1.0$.
- **Narinlik Sınırı:** $\lambda_i = K L_i / r_i \le 150$ [kaynağı doğrulanamadı, varsayım].
- **Bağlantı Sınırı:** $|N_i| / F_{j,Rd} \le 1.0$, $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\max} = 2 \times 26.6 = 53.2\text{ kN}$.
  - $F_{\text{bolt},\max} = 26.6\text{ kN}$ (Correal vd. 2021 Tablo 4 deney maksimum yükü).
  - $n_{\text{bolt}} = 2$ (çapraz çift cıvata) varsayımdır. Tek cıvatada 231 eleman (ribbed40) ve 8 eleman (kiewitt32) kesitten bağımsız olarak sınırı aştığından zorunlu bir kabuldür; duyarlılık konusu olarak incelenir.
- **Servis Deplasmanı (SLS):**
  $$u_{\max} \le u_{\text{izin}} = \frac{L_{\text{span}}}{150} = \frac{40\,000\text{ mm}}{150} \approx 266.67\text{ mm} \quad \text{[IStructE Manual 2025 örneği]}$$

Doğrulanmış temel sonuç: Tüm elemanlar katalogdaki en büyük kesitteyken (Kesit 24, $D=160\text{ mm}, t=16\text{ mm}$) üç kubbe de tüm ASD sınırlarını tam sağlamaktadır (en gayrimüsait $DCR = 0.75$). Bu referans tasarımda yapısal ağırlıklar: `geodesic16` $20.9\text{ kN}$, `kiewitt32` $84.5\text{ kN}$, `ribbed40` $190.0\text{ kN}$'dur (eski geçersiz optimum ağırlıklar belgelerden çıkarılmıştır).

---

## 🌿 2. BEŞİKTEN-KAPIYA (A1–A3) LCA VE DEKARBONİZASYON PARADOKSU

Optimizasyon tamamlandıktan sonra elde edilen en hafif, uygulanabilir ($P=0$) kubbe geometrisi üzerinde yaşam döngüsü karbon analizi yürütülür:

$$EC_{\text{total}} = M_{\text{bambu}} \cdot EC_b + M_{\text{steel}} \cdot EC_s + M_{\text{mortar}} \cdot EC_m \quad [\text{kg CO}_2\text{e}]$$

### Literatür Parametreleri ve Varsayımlar:
1. **$EC_b = 0.35\text{ kg CO}_2\text{e/kg}$:** [Varsayım; Zea Escamilla & Habert 2014 Tablo 8 ile teyit edilecek].
2. **$EC_s = 2.10\text{ kg CO}_2\text{e/kg}$:** [Varsayım; ICE v3.0 xlsx ile teyit edilecek].
3. **$EC_m = 0.18\text{ kg CO}_2\text{e/kg}$:** [Varsayım; ICE v3.0 xlsx ile teyit edilecek].
4. **Bağlantı Geometrisi:**
   - Düğüm gövdesi kütlesi: $m_{\text{hub}} = 2.0\text{ kg/düğüm}$
   - Çubuk ucu çelik manşon/saplama: $0.50\text{ kg/uç}$
   - Uç bölge harç dolgusu: $\rho = 2100\text{ kg/m}^3$, dolgu boyu $L_{\text{inj}} = 2.5 D$ (kesite bağlı harç kütlesi).

*LCA Duyarlılık Notu:* Hibrit bağlantı karbon payı, en elverişsiz parametre setinde %43–52 seviyelerine düşebilmektedir. Dolayısıyla nihai karbon dökümü ve manşet bulgu, tam kampanya sonuçları alındıktan sonra hesaplanacak olup ön-yazılı sabit bir yüzde verilmez.

---

## 🪵 3. 24 ELEMANLI GERÇEKÇİ GUADUA KESİT KATALOĞU (TABLO 2)

| İndeks | Dış Çap $D$ [mm] | Et Kalınlığı $t$ [mm] | $t/D$ Oranı | $A$ [$\text{cm}^2$] | $r$ [$\text{cm}$] | Morfolojik Konum |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | 80 | 8.0 | 0.100 | 18.10 | 2.57 | Sobrebasa (Üst) |
| **1** | 80 | 10.0 | 0.125 | 21.99 | 2.52 | Sobrebasa |
| **2** | 90 | 8.0 | 0.089 | 20.61 | 2.92 | Sobrebasa |
| **3** | 90 | 10.0 | 0.111 | 25.13 | 2.86 | Sobrebasa |
| **4** | 90 | 12.0 | 0.133 | 29.41 | 2.81 | Sobrebasa |
| **5** | 100 | 8.0 | 0.080 | 23.12 | 3.27 | Sobrebasa Standart |
| **6** | 100 | 10.0 | 0.100 | 28.27 | 3.21 | Sobrebasa Standart |
| **7** | 100 | 12.0 | 0.120 | 33.18 | 3.16 | Sobrebasa Standart |
| **8** | 110 | 9.0 | 0.082 | 28.56 | 3.59 | Basa Estructural |
| **9** | 110 | 11.0 | 0.100 | 34.21 | 3.53 | Basa Estructural |
| **10** | 110 | 13.0 | 0.118 | 39.62 | 3.48 | Basa Estructural |
| **11** | 120 | 10.0 | 0.083 | 34.56 | 3.91 | Basa Estructural |
| **12** | 120 | 12.0 | 0.100 | 40.72 | 3.85 | Basa Estructural |
| **13** | 120 | 14.0 | 0.117 | 46.62 | 3.80 | Basa Estructural |
| **14** | 130 | 10.0 | 0.077 | 37.70 | 4.26 | Basa Pesada |
| **15** | 130 | 12.0 | 0.092 | 44.49 | 4.20 | Basa Pesada |
| **16** | 130 | 15.0 | 0.115 | 54.19 | 4.12 | Basa Pesada |
| **17** | 140 | 11.0 | 0.079 | 44.58 | 4.58 | Basa Pesada |
| **18** | 140 | 13.0 | 0.093 | 51.87 | 4.52 | Basa Pesada |
| **19** | 140 | 16.0 | 0.114 | 62.33 | 4.44 | Basa Pesada |
| **20** | 150 | 12.0 | 0.080 | 52.02 | 4.90 | Cepa Seleccionada (Dip) |
| **21** | 150 | 15.0 | 0.100 | 63.62 | 4.82 | Cepa Seleccionada |
| **22** | 160 | 13.0 | 0.081 | 60.04 | 5.23 | Cepa Seleccionada |
| **23** | 160 | 16.0 | 0.100 | 72.38 | 5.14 | Cepa Seleccionada |

---

## ⚙️ 4. BÜYÜK KAMPANYA MATRİSİ VE ÇALIŞTIRMA PARAMETRELERİ

### 4.1. İncelenen 3 Kubbe Topolojisi ($Span = 40.0\text{ m}$)
1. **`geodesic16`:** 115 çubuk, 46 düğüm, 23 tasarım grubu ($\text{NFE} = 23\,000$).
2. **`kiewitt32`:** 456 çubuk, 161 düğüm, 20 tasarım grubu ($\text{NFE} = 22\,000$, 22 değişken).
3. **`ribbed40` ($freq=2$):** 1464 çubuk, 321 düğüm, 43 tasarım grubu ($\text{NFE} = 43\,000$).
   - *Topoloji Notu:* Orijinal Saka (1991) 40 m çelik benchmark'ı 354 eleman içermekte olup çubuk boyları 2.9–5.97 m arasındadır ve bambu culm sınırlarına uymaz. Bu çalışmadaki model Saka geometrisinden uyarlanan $freq=2$ yoğunlaştırmasıdır ($L \in [0.76, 3.08]\text{ m}$).

### 4.2. Algoritma Seçimi ve 3 Algoritmalı Kampanya Tasarımı
Kod tabanında 16 algoritma (`metaheuristic_optimizers.py`) yer almaktadır. Ancak nihai kampanya, `04_Results/TUNING_STUDY.md` duyarlılık analizinden (aday havuzu: ABC, ACO, DO, GWO, WOA, TLBO; tohum 2001–2005) belirlenen **3 algoritma ([TUNING SONUCUNA GÖRE])** (2 bilinen yüksek performanslı yöntem + 1 görece yeni yöntem) ile yürütülür.

### 4.3. Koşu Parametreleri ve Hesaplama Bütçesi
- **Hesaplama Bütçesi:** $\text{NFE} = 1000 \times \text{tasarım grubu sayısı}$ (ribbed40: 43 000, kiewitt32: 22 000, geodesic16: 23 000).
- **Bağımsız Tohum Sayısı:** **$R = 30$ bağımsız tohum** (`seed = [1001, ..., 1030]`).
- **Toplam İş Sayısı:** $3 \text{ Kubbe} \times 3 \text{ Algoritma} \times 30 \text{ Tohum} = \mathbf{270\text{ optimizasyon koşusu}}$.
- **Paralel Süre (7 İşçi):** Ribbed40 koşusu 7 paralel işçide yaklaşık 16 dk sürmektedir. 270 işlik tam kampanyanın tahmini duvar saati süresi ≈ **3.5–4 saattir**.
- **Kayıt ve Devam:** Her iş için RNG durumunu içeren atomik JSON checkpoint ve değerlendirme başına `.npz` kayıt dosyaları tutulur (kesintiye uğrayan koşu bit düzeyinde özdeş sonuçla devam eder).

---

## 📊 5. İSTATİSTİKSEL VE AKADEMİK DEĞERLENDİRME PROTOKOLÜ

1. **Tanımlayıcı İstatistikler:** Min, Mean, Median, Max, Std Dev, Feasibility Rate (%).
2. **Hipotez Testleri:**
   - **Wilcoxon Rank-Sum Testi (Mann-Whitney U):** Algoritmalar arası ikili kıyaslamalarda çift taraflı test, çoklu karşılaştırma için **Holm düzeltmesi** ve Vargha-Delaney $A_{12}$ etki büyüklüğü ($p < 0.05$).
   - **Friedman Testi:** Tohum bloklu küresel sıra hiyerarşisi.
3. **Grafiksel Çıktılar:**
   - Yakınsama profilleri ($\pm 1$ Std gölgeli).
   - DCR kapasite kullanım dağılımı (çekme, Ylinen basınç, narinlik, bağlantı).
   - Post-optimizasyon gömülü karbon bileşen dağılımı (bambu, çelik, harç).

---

## 📚 6. DOĞRULANMIŞ LİTERATÜR ATIFLARI

1. **Paraskeva, T. S., Pradhan, N. P., Stoura, C. D., & Dimitrakopoulos, E. G. (2019).** *"Monotonic loading testing and characterization of new multi-full-culm bamboo to steel connections."* Construction and Building Materials, 201, 473–483. DOI: 10.1016/j.conbuildmat.2018.12.198. *(Kao Jue, M6 cıvata).*
2. **Trujillo, D., Harries, K., Kaminski, S., & Lopez, L. F. (2025).** *"Manual for the design of bamboo structures to ISO 22156:2021."* The Institution of Structural Engineers (IStructE), London. ISBN: 978-1-906335-97-7.
3. **Zea Escamilla, E., & Habert, G. (2014).** *"Environmental impacts of bamboo-based construction materials representing global production diversity."* Journal of Cleaner Production, 69, 117–127. DOI: 10.1016/j.jclepro.2014.01.067.
4. **Correal, J. F., Prada, M., Suárez, F., & Moreno, M. (2021).** *"Bearing capacity of bolted-mortar infill connections in bamboo and yield model formulation."* Construction and Building Materials, 305, 124597. DOI: 10.1016/j.conbuildmat.2021.124597. *(Guadua, F_bolt,max deney yükü).*
5. **Jones, C., & Hammond, G. (2019).** *"Inventory of Carbon and Energy (ICE) Version 3.0."* Circular Ecology.
6. **ISO 22156:2021.** *"Bamboo structures — Structural design."* International Organization for Standardization, Geneva.
