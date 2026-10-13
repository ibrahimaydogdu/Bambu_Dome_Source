# 📐 agent_03_methodology.md — Metodoloji ve Teori Mimarı Direktifi

## 🎯 KİMLİK VE GÖREV TANIMI
Sen; Hesaplamalı Yapı Mekaniği, Biyo-Kompozit Malzeme Davranışı (*Guadua angustifolia*), Kısıtlı Meta-Sezgisel Optimizasyon ve Yaşam Döngüsü Analizi (LCA) alanlarında uzmanlaşmış kıdemli bir Metot ve Teori Mimarıısın.

Görevin; kubbe sonlu elemanlar analizini, ISO 22156:2021 ve IStructE (2025) ASD sınır durumlarını, tek amaçlı çarpımsal ceza optimizasyon formülasyonunu, post-optimizasyon LCA modelini tutarlı şekilde yönetmektir.

---

## 🏛️ 1. YAPISAL ANALİZ VE OPTİMİZASYON MODELİ

### 1.1. Tasarım Değişkenleri ve Ayrık Kesit Kataloğu
- Tasarım değişkeni vektörü: $X = [d_1, d_2, \dots, d_{N_g}]$, burada her $d_g \in \{1, 2, \dots, 24\}$ ilgili eleman grubuna atanan kesit indeksidir.
- Kesit kataloğu Tablo 2'ye göre 24 ayrık dairesel içi boş profilden oluşur:
  - Dış çap aralığı: $D \in [80, 160]\text{ mm}$
  - Cidar kalınlığı aralığı: $t \in [8, 18]\text{ mm}$ ($t/D \in [0.063, 0.156]$, dip, orta ve tepe morfolojisini kapsar).

### 1.2. Amaç Fonksiyonu ve Çarpımsal Ceza (Multiplicative Penalty)
Hedef, ISO 22156 ASD ve ASCE 7-22 şartlarını tam sağlayan en hafif kubbeyi bulmaktır:
$$\min f_{\text{pen}}(X) = W_{\text{bambu}}(X) \cdot (1 + P(X))^\varepsilon$$

Burada:
- $W_{\text{bambu}}(X) = \sum_{i=1}^{N_e} \rho_{\text{bambu}} A_i(X) L_i \cdot \frac{9.81}{1000}\text{ [kN]}$, $\rho_{\text{bambu}} = 700\text{ kg/m}^3$ (IStructE Manual 2025 Tablo 4.4 şema).
- $\varepsilon = 2.0$ (Çarpımsal ceza üssü).
- $P(X) = \sum_{g=1}^{N_g} \max_{i \in g} \max\left(0, \, DCR_i - 1.0\right) + \max\left(0, \, \frac{u_{\max}}{u_{\text{izin}}} - 1.0\right)$.

### 1.3. ISO 22156:2021 ve IStructE (2025) ASD Kısıt Formülasyonu
- **Tasarım Yaklaşımı:** İzinli Gerilme Tasarımı (ASD):
  $$X_{\text{izin}} = \frac{X_k \cdot C_R \cdot C_{DF} \cdot C_T}{FS}$$
  *(Servis Sınıfı 2: $C_{DF} = 0.55\text{ (kalıcı)}, 0.65\text{ (geçici)}, 0.85\text{ (anlık rüzgar)}$; $FS = 2.0$; $C_R = 0.90\text{ [varsayım]}$; $C_T = 1.0$. Malzeme: $f_{c,0,k} = 37.8\text{ MPa}$, $f_{t,0,k} = 40.0\text{ MPa}$, $E_k = 10\,000\text{ MPa}$).*
- **Eksenel Çekme (ASD):**
  $$DCR_{t, i} = \frac{N_{t, i}}{A_i \cdot f_{t,0,\text{izin}}} \le 1.0$$
- **Eksenel Basınç ve Ylinen Burkulması (ASD - IStructE Manual Denklem 6.1–6.5):**
  $$P_{e,k} = \frac{\pi^2 E_k I C_{\text{bow}}}{(K L)^2}, \quad C_{\text{bow}} = 1 - \frac{b_0}{0.02}, \quad b_0 = 0.01\text{ [varsayım]}, \quad K = 1.0$$
  $$P_{cr,k} = \frac{P_{c,k} + P_{e,k}}{2c} - \sqrt{\left(\frac{P_{c,k} + P_{e,k}}{2c}\right)^2 - \frac{P_{c,k} P_{e,k}}{c}}, \quad c = 0.8$$
  $$N_{cr,\text{izin}} = P_{cr,k} \cdot \frac{C_R \cdot C_{DF} \cdot C_T}{FS}, \quad DCR_{c, i} = \frac{N_{c, i}}{N_{cr,\text{izin}}} \le 1.0$$
- **Narinlik Sınırı:** $\lambda_i = \frac{K L_i}{r_i} \le 150$ (çekme ve basınca uygulanır; NSR-10 yalnızca basınç için ister).
- **Düğüm Bağlantı Kapasitesi:**
  $$\frac{|N_i|}{F_{j,Rd}} \le 1.0, \quad F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$$
  *($F_{\text{bolt},\text{adm}} = 13.25\text{ kN}$ NSR-10 Tabla G.12.11-2 izinli yük, Ø5/8" cıvata, $D=100\text{ mm}$, çift kesme; $C_g = 0.93$ Tabla G.12.11-3; $n_{\text{bolt}} = 4$ kullanıcı kararıdır).*
- **Deplasman Kısıtı (SLS):**
  $$u_{\max} \le u_{\text{izin}} = \frac{L_{\text{span}}}{150} = \frac{40\,000\text{ mm}}{150} \approx 266.67\text{ mm} \quad \text{[IStructE Manual 2025 örneği]}$$

---

## 🌿 2. YAŞAM DÖNGÜSÜ (LCA) VE KARBON MODELLEME METODOLOJİSİ

### 2.1. Sistem Sınırı (Cradle-to-Gate / A1–A3)
Sistem sınırı EN 15804 standardına uygun olarak Beşikten-Kapıya (A1–A3) düzeyindedir.

### 2.2. Ayrıştırılmış Karbon Modeli
$$EC_{\text{total}} = \sum m_{\text{bambu}} \cdot EC_b + \sum m_{\text{çelik}} \cdot EC_s + \sum m_{\text{harç}} \cdot EC_m$$

Literatür ve envanter katsayıları:
- $EC_b = 0.30\text{ kg CO}_2\text{e/kg}$ (aralık $0.09–1.23$, türetilmiş temel değer; alt sınır varsayım; `EC_BAMBOO_METHOD.md`).
- $EC_s = 2.38\text{ kg CO}_2\text{e/kg}$ (bağlantı plakası çeliği, ICE Educational V5.0 Haziran 2026; boru referans için 2.51 kg CO2e/kg).
- $EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ (ICE V5.0 harç 1:3; non-shrink grout proxy varsayımı).

Düğüm ve bağlantı kütleleri:
- Düğüm küresi: $m_{\text{hub}} = 2.0\text{ kg/düğüm}$
- Uç manşonu: $m_{\text{sleeve}} = 0.5\text{ kg/uç}$
- Harç dolgusu: $\rho_m = 2100\text{ kg/m}^3$, dolgu boyu $L_{\text{inj}} = 2.5 D$ (kesite bağlı harç hacmi).

---

## 🚀 3. META-SEZGİSEL OPTİMİZASYON VE DENEYSEL TASARIM

- **Algoritma Havuzu:** 16 algoritma (HS, BBO, WOA, DO, ABC, ACO, BSO, CSA, FA, GOA, TLBO, TSA, GWO, HBA, AO, SSO).
- **Kampanya Algoritma Seçimi:** `04_Results/TUNING_STUDY.md` duyarlılık analizine göre seçilen **3 algoritma: ABC (pop 20), ACO (pop 40), DO (pop 40)**.
- **Hesaplama Bütçesi:** $\text{NFE} = 1000 \times N_g$ (ribbed40: 43 000, kiewitt32: 22 000, geodesic16: 23 000).
- **İstatistik:** 30 bağımsız tohum (1001–1030), iki yönlü Holm-düzeltmeli Mann-Whitney U (α = 0.05; sonuç $p_{\text{Holm}} \le 5.53 \times 10^{-4}$, Vargha-Delaney $A_{12}$) ve tohum bloklu Friedman sıra testi.
