# 🏗️ system_architecture.md — Genel Sistem ve Hesaplama Mimarisi

Bu belge; **Bambu Uzay Kafes Kubbelerin Tek Amaçlı Yapısal Optimizasyonu ve Dekarbonizasyon Paradoksu** çerçevesinde çalışan çok ajanlı sistemin hesaplama mimarisini, veri akışını, amaç fonksiyonu formülasyonunu ve istatistiksel değerlendirme protokolünü tanımlar.

---

## 1. STRATEJİK PARADİGMA DÖNÜŞÜMÜ VE MATEMATİKSEL TEMEL

### 1.1. Çok Amaçlı Modelin Terk Edilme Gerekçesi (Ampirik Yakın-Doğrusallık)
Eksenel kafes sistemlerde yapısal eleman hacmi $V = \sum A_i L_i$ minimize edildiğinde:
- Yapısal Bambu Kütlesi: $M_{\text{bambu}} = \rho_{\text{bambu}} \cdot V$
- Bambu Gömülü Karbonu: $EC_{\text{bambu}} = EF_{\text{bambu}} \cdot M_{\text{bambu}}$
- Bambu Maliyeti: $C_{\text{bambu}} = c_m \cdot M_{\text{bambu}}$ (veya boya/çapa bağlı monotonik maliyet)

Sabit düğüm modelinde kütle ile karbon tam doğrusal bir ilişki ($f_2$, $f_1$'in tam doğrusal fonksiyonudur; corr = 1.000, `test_fast_eval.py`) sergiler. Kesite bağlı bağlantı modelinde ise ziyaret edilen uygun tasarımlarda $r = 0.72 - 0.90$ ($R^2 = 0.52 - 0.80$) ölçülür; en hafif tasarımın karbonu bulunan en düşüğün %1.6–6.7 üstündedir (`04_Results/WEIGHT_CARBON_TRADEOFF.md`). Amaçlar yakındır ancak özdeş değildir. Çok amaçlı arama bu çalışmada yapılmamıştır.

### 1.2. İki Aşamalı Mimari
1. **Aşama 1: Titiz Tek Amaçlı Yapısal Ağırlık Minimizasyonu:** Kısıtları tam sağlayan en hafif ve güvenli yapısal tasarımı bulmak ($\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$).
2. **Aşama 2: Beşikten-Kapıya (A1–A3) LCA Ayrıştırması & Parametrik Duyarlılık:** Optimum tasarımın bağlantı bileşenlerini (çelik göbek, saplamalar, harç enjeksiyonu) modelleyerek karbon ayak izini ayrıştırmak ve parametre aralıklarında ($L_{\text{inj}}/D$, $EC_{\text{steel}}$, $EC_{\text{bamboo}}$) duyarlılığı test etmek.

---

## 2. AMAÇ VE CEZA FONKSİYONU MİMARİSİ (ASD ESASLI)

Optimizasyon problemi, ayrık kesit uzayında ISO 22156:2021 ve IStructE (2025) Manual uyarınca İzin Verilen Gerilme Tasarımı (ASD) ve ASCE 7-22 §2.4.1 yük kombinasyonları altında formüle edilir:

$$\min f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}}(\mathbf{X}) \cdot (1 + P(\mathbf{X}))^\varepsilon$$

Burada:
- $W_{\text{bambu}}(\mathbf{X}) = \sum_{i=1}^{N_e} \rho_{\text{bambu}} \cdot A_i(\mathbf{X}) \cdot L_i \cdot \frac{9.81}{1000}$ [kN] (Yapısal bambu kütlesi ağırlığı, $\rho = 700\text{ kg/m}^3$, Manual Tablo 4.4)
- $\varepsilon = 2.0$: Çarpımsal ceza üssü
- $P(\mathbf{X})$: Boyutsuz normalize toplam kısıt ihlali:
  $$P(\mathbf{X}) = \sum_{g=1}^{N_g} P_{\text{strength}, g}(\mathbf{X}) + P_{\text{disp}}(\mathbf{X})$$

### 2.1. Grup Bazlı Mukavemet, Kararlılık ve Bağlantı Kısıtı ($P_{\text{strength}, g}$)
IStructE (2025) Manual Denk. 3.9 ve 6.5 uyarınca izin verilen gerilmeler: $X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$.
- Servis Sınıfı 2: $C_{DF} = 0.55$ (kalıcı $D$), $0.65$ (geçici $D+S$), $0.85$ (anlık rüzgarlı kombinasyonlar)
- Güvenlik katsayısı: $FS = 2.0$ (lif boyuna); $C_R = 0.90$ (tekil culm, muhafazakâr varsayım); $C_T = 1.0$
- Karakteristik dayanımlar: Eksenel çekme $f_{t,k} = 40.0\text{ MPa}$ (Manual Tablo 4.4 şema), eksenel basınç $f_{c,k} = 37.8\text{ MPa}$ (Manual Tablo A3.4, Guadua, $n=922$)
- Elastisite modülü: $E_k = 10,000\text{ MPa}$ (Manual Tablo 4.4)

Eleman talep/kapasite oranı:
$$D/C_{\text{strength}, i} = \max\left( D/C_{\text{tens}, i}, \, D/C_{\text{buck}, i}, \, \frac{\lambda_i}{150}, \, \frac{|N_i|}{F_{j,Rd}} \right)$$

Burada:
- Eksenel çekme: $D/C_{\text{tens}, i} = \dfrac{N_{t, i}}{A_i \cdot f_{t,\text{izin}}}$
- Ylinen sütun kararlılığı (Manual Denk. 6.1, Ek A6.2): $c = 0.8$, $P_{e,k} = \pi^2 \cdot E_k \cdot I_i \cdot C_{\text{bow}} / (K L_i)^2$, $C_{\text{bow}} = 1 - b_0/0.02$, $b_0 = 0.01$ (varsayım), $K = 1.0$. İzin verilen $N_{cr} = N_{cr,k} \cdot C_R \cdot C_{DF} \cdot C_T / FS$. $D/C_{\text{buck}, i} = |N_{c, i}| / N_{cr,\text{izin}}$.
- Narinlik kısıtı: $\lambda_i = L_i / r_i \le 150$ (NSR-10 yalnızca basınç için ister; çekme ve basınca uygulanması bilinçli muhafazakârdır).
- Bağlantı kapasitesi: $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$ ($F_{\text{bolt},\text{adm}}$: NSR-10 Tabla G.12.11-2 izinli yük, Ø5/8" cıvata, $D=100\text{ mm}$, çift kesme; $C_g = 0.93$: Tabla G.12.11-3; $n_{\text{bolt}} = 4$ kullanıcı kararı).
- Grup cezası: $P_{\text{strength}, g} = \max_{i \in g} \max\left(D/C_{\text{strength}, i} - 1.0, \, 0.0\right)$.

### 2.2. Deplasman Servis Kısıtı ($P_{\text{disp}}$)
Kubbe tepe noktası ve düğüm düşey yer değiştirmeleri (SLS - IStructE 2025 Manual örneği):
$$u_{\text{izin}} = \frac{\text{span}}{150} = \frac{40000\text{ mm}}{150} \approx 266.67\text{ mm}$$
$$P_{\text{disp}} = \max\left(\frac{u_{\max}}{u_{\text{izin}}} - 1.0, \, 0.0\right)$$

---

## 3. UÇTAN UCA VERİ AKIŞI (DATA PIPELINE)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. MODEL VE GEOMETRİ HAZIRLIĞI                              │
│    - 3 Topoloji: geodesic16, kiewitt32, ribbed40 (S = 16/32/40 m) │
│    - Tablo 2: 24 Ayrık Guadua Kesit Kataloğu (D: 80-160 mm) │
│    - ASCE 7-22 §2.4.1 ASD Faktörsüz Yük Kombinasyonları    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. TEK AMAÇLI OPTİMİZASYON MOTORU                           │
│    - 3 Algoritma: ABC, ACO, DO (2 bilinen + 1 yeni)         │
│    - 30 Bağımsız Tohum (1001–1030) x NFE = 1000 * N_grup    │
│    - Vektörel Hızlı Doğrudan Rijitlik Çözücüsü (fast_eval)  │
│    - Çarpımsal Ceza Fonksiyonu, P = 0 Feasible Arşivi       │
│    - İterasyon Checkpointing & Değerlendirme Başına .npz    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. İSTATİSTİKSEL VE ALGORİTMİK DEĞERLENDİRME                │
│    - Min, Medyan, Ortalama, Maks, Std Sapma                 │
│    - Yakınsama Eğrileri (Convergence curves) ve NFE         │
│    - Wilcoxon Rank-Sum (Mann-Whitney U, Holm, A12)         │
│    - Tohum Bloklu Friedman Sıra Testi                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. POST-OPTIMİZASYON BAĞLANTI GEOMETRİSİ & DETAYLANDIRMA    │
│    - Eleman Başına Prefabrik Çelik Saplama/Manşon Boyutları │
│    - Çelik Düğüm Göbeği Kütlesi (m_hub = 2.0 kg)            │
│    - Uç Bölge Harç Enjeksiyon Hacmi (L_inj = 2.5 D varsayım)│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. BEŞİKTEN-KAPIYA (A1-A3) LCA VE PARAMETRİK DUYARLILIK     │
│    - Bambu Karbonu: m_bambu * 0.30 kg CO2e/kg (türetilmiş)  │
│    - Çelik Bağlantı: m_steel * 2.38 kg CO2e/kg (ICE V5.0)   │
│    - Harç Enjeksiyonu: m_mortar * 0.18 kg CO2e/kg (proxy)   │
│    - Parametrik Duyarlılık: L_inj / D, EC_steel, EC_bamboo  │
│    - Kütle-Karbon İlişkisi (R^2=0.52-0.80)│
└─────────────────────────────────────────────────────────────┘
```

---

## 4. ALGORİTMA DEĞERLENDİRME VE İSTATİSTİKSEL PROTOKOL

Çok amaçlı metrikler yerine, tek amaçlı stokastik optimizasyon literatürünün katı Q1 standartları uygulanır:

1. **Bağımsız Koşu Sayısı:** Her kubbe topolojisi ve algoritma kombinasyonu için **30 bağımsız rastgele tohum (1001–1030)** çalıştırılır (Toplam 270 iş).
2. **Tanımlayıcı İstatistikler:**
   - **En İyi (Best / Min Fitness):** Küresel optimuma yakınlık derecesi.
   - **Medyan (Median Fitness):** Dağılımın merkezsel eğilimi.
   - **Ortalama (Mean Fitness):** Algoritmanın beklenen performansı.
   - **En Kötü (Worst / Max Fitness):** Yerel minimuma saplanma riski.
   - **Standart Sapma (Std Dev):** Çözüm uzayındaki saçılma.
   - **Uygulanabilirlik Oranı (Feasibility Rate %):** 30 çalıştırmada kısıtları sıfır ihlalle ($P=0$) sağlayan koşuların yüzdesi.
   - **Hesaplama Yükü (NFE & Wall-Clock Time):** Hedef bütçe (NFE = $1000 \times N_{\text{grup}}$).
3. **Hipotez Testleri ve İstatistiksel Anlamlılık:**
   - **Wilcoxon Rank-Sum Testi (Mann-Whitney U):** İki yönlü, Holm düzeltmeli ve Vargha-Delaney A12 etki büyüklüğü ile çiftli algoritma karşılaştırmaları ($p < 0.05$ istatistiksel üstünlük eşiği).
   - **Friedman İki Yönlü Sıra Testi:** Tohum bloklu algoritma genel performans sıralaması (Mean Rank).
4. **Görselleştirme Şablonları:**
   - Ortalama ve en iyi yakınsama geçmişi eğrileri.
   - 30 tohumluk nihai ağırlık dağılımı box-plot grafikleri.
