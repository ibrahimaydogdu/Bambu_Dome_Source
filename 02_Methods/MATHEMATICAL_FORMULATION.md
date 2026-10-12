# 📐 MATHEMATICAL_FORMULATION.md: Tek Amaçlı Yapısal Optimizasyon ve ISO 22156 Kısıt Formülasyonu

Bu belge; tek amaçlı yapısal ağırlık minimizasyonu probleminin matematiksel modelini, **ISO 22156:2021** standart sınır durum kısıtlarını, çarpımsal ceza fonksiyonunu ve post-optimizasyon Beşikten-Kapıya (A1–A3) LCA ayrıştırma formülasyonunu tanımlar.

---

## 1. Problem Tanımı ve Tasarım Değişkenleri

Optimizasyon problemi, $N_g$ adet bağımsız eleman grubuna atanacak ayrık enkesit profil indekslerinin belirlenmesidir:

$$\text{Denklem (1):} \quad \mathbf{X} = [x_1, x_2, \dots, x_{N_g}]^T \in \mathbb{Z}^{N_g}, \quad x_i \in \{1, 2, \dots, 24\}$$

Burada $x_i$, 24 elemanlı Guadua angustifolia culm kataloğundaki dış çap $D$ ve et kalınlığı $t$ ikilisini temsil eden ayrık tamsayı indekstir.

---

## 2. Amaç Fonksiyonu ve Çarpımsal Ceza Modeli

Eksenel kafes sistemlerde hem bambu karkas kütlesi hem de düğüm bağlantı hacimleri (çelik mafsal ve uç harç tıkacı) kesit boyutlarının ($D, t$) monoton artan fonksiyonlarıdır. Yapısal tasarım uzayında kütleyi azaltırken gömülü karbonu artıran antagonist bir mekanik mekanizma bulunmadığından ve değişkenler arasında ampirik yakın-doğrusallık ($R^2 \in [0.81, 0.97]$) gözlendiğinden, çok amaçlı Pareto cephesi daralarak tekil bir optimuma ya da çok dar bir aralığa çökmektedir. Bu doğrultuda problem, katı tek amaçlı yapısal ağırlık minimizasyonu olarak formüle edilmiştir:

$$\text{Denklem (2):} \quad \min_{\mathbf{X}} f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}}(\mathbf{X}) \cdot \left(1 + P(\mathbf{X})\right)^\varepsilon$$

### 2.1. Yapısal Bambu Ağırlığı ($W_{\text{bambu}}$)
$$\text{Denklem (3):} \quad W_{\text{bambu}}(\mathbf{X}) = \sum_{i=1}^{N_e} \rho_b \cdot g \cdot A_i(x_i) \cdot L_i \quad [\text{kN}]$$

- $N_e$: Toplam çubuk eleman adedi.
- $\rho_b = 700\text{ kg/m}^3$: Guadua culm karakteristik birim hacim kütlesi (IStructE 2025 Manual Tablo 4.4 şema).
- $g = 9.80665\text{ m/s}^2$: Yerçekimi ivmesi.
- $A_i(x_i)$: $i$. elemanın seçilen profile karşılık gelen net enkesit alanı ($\text{m}^2$).
- $L_i$: $i$. elemanın uzunluğu ($\text{m}$).

### 2.2. Toplam Normalize Kısıt İhlali ($P(\mathbf{X})$) ve Çarpımsal Ceza
$$\text{Denklem (4):} \quad P(\mathbf{X}) = \sum_{g=1}^{N_g} P_{\text{strength}, g}(\mathbf{X}) + P_{\text{disp}}(\mathbf{X})$$

- $P_{\text{strength}, g} = \max\left(0, \, DCR_{\max, g} - 1.0\right)$ (Her gruptaki en kritik çubuğun ASD kapasite aşımı; çekme, Ylinen basınç, narinlik ve mafsal kapasitesi dahil)
- $P_{\text{disp}} = \max\left(0, \, \frac{u_{\max}}{u_{\text{allow}}} - 1.0\right)$ (Maksimum kubbe çökmesi SLS aşımı)
- $\varepsilon = 2.0$: Çarpımsal ceza üssü. Uygun çözümlerde ($P=0$) ceza çarpanı $(1+0)^2 = 1.0$ olup $f_{\text{pen}} = W_{\text{bambu}}$ değerini verir.

---

## 3. Tasarım Kısıtları (ASD - ISO 22156:2021 & IStructE 2025 Manual)

Tasarım felsefesi İzin Verilen Gerilme Tasarımıdır (ASD). IStructE Manual Denk. 3.9 ve 6.5 uyarınca izin verilen gerilmeler:
$$\text{Denklem (5):} \quad X_{\text{izin}} = \frac{X_k \cdot C_R \cdot C_{DF} \cdot C_T}{FS}$$

- **Süre Katsayısı ($C_{DF}$):** Servis Sınıfı 2; $C_{DF} = 0.55$ (kalıcı yük $D$), $0.65$ (geçici yük $D+S$), $0.85$ (anlık rüzgarlı yükler).
- **Güvenlik Katsayısı ($FS$):** $FS = 2.0$ (lif boyuna gerilmeler için).
- **Diğer Düzeltmeler:** $C_R = 0.90$ (tekil culm için muhafazakâr varsayım; Manual $\ge 4$ paralel culm için 1.1 önermektedir), $C_T = 1.0$.
- **Kapasite Çarpanı:** $k = \frac{C_R \cdot C_{DF} \cdot C_T}{FS} \in \{0.2475, \, 0.2925, \, 0.3825\}$.
- **Yük Kombinasyonları:** ASCE 7-22 §2.4.1 ASD faktörsüz kombinasyonları: $D$; $D+S$; $D+0.6W$; $D+0.75S+0.45W$; $0.6D+0.6W$.

### 3.1. Eksenel Çekme Gerilmesi Kısıtı (Manual Denk. 6.5)
Her $i = 1, \dots, N_e$ elemanı için hesap eksenel çekme gerilmesi $\sigma_{t, i} = N_{t, i} / A_i(x_i)$:

$$\text{Denklem (6):} \quad DCR_{tens, i} = \frac{N_{t, i}}{A_i(x_i) \cdot f_{t,\text{izin}}} \le 1.0$$

- $f_{t,k} = 40.0\text{ MPa}$ (IStructE 2025 Manual Tablo 4.4 şema değeri).

### 3.2. Eksenel Basınç ve Ylinen Sütun Kararlılığı Kısıtı (Manual Denk. 6.1–6.4)
Her $i = 1, \dots, N_e$ elemanı için hesap eksenel basınç kuvveti $N_{c, i}$:

$$\text{Denklem (7):} \quad DCR_{buck, i} = \frac{N_{c, i}}{N_{cr,\text{izin}, i}} \le 1.0$$

Burada Ylinen karakteristik kritik yükü $N_{cr,k, i}$:

$$\text{Denklem (8):} \quad P_{e,k, i} = \frac{\pi^2 \cdot E_k \cdot I_i(x_i) \cdot C_{\text{bow}}}{(K \cdot L_i)^2}$$

- $E_k = 10,000\text{ MPa}$ (IStructE 2025 Manual Tablo 4.4 şema alt sınırı; FEM rijitliği ve burkulma hesabı aynı $E_k$'yi kullanır).
- $K = 1.0$ (Mafsallı uzay kafes elemanı).
- $C_{\text{bow}} = 1 - \frac{b_0}{0.02}$, $b_0 = 0.01$ (eğrilik kusuru varsayımı).
- Ylinen denklem katsayısı: $c = 0.8$ (Manual Denk. 6.1, Ek A6.2).
- $N_{c,k} = A_i(x_i) \cdot f_{c,k}$, $f_{c,k} = 37.8\text{ MPa}$ (Manual Tablo A3.4, Guadua angustifolia, $n = 922$).
- İzin verilen kritik kuvvet: $N_{cr,\text{izin}, i} = \frac{N_{cr,k, i} \cdot C_R \cdot C_{DF} \cdot C_T}{FS}$.

### 3.3. Geometrik Narinlik Üst Sınırı
$$\text{Denklem (9):} \quad DCR_{slend, i} = \frac{\lambda_i}{\lambda_{max}} \le 1.0, \quad \lambda_i = \frac{L_i}{r_i(x_i)}, \quad \lambda_{max} = 150.0 \quad \text{(varsayım)}$$

### 3.4. Harç Dolgulu Çelik Mafsal Bağlantı Kapasitesi
$$\text{Denklem (10):} \quad DCR_{joint, i} = \frac{|N_i|}{F_{j,Rd}} \le 1.0$$

- $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\max} = 2 \times 26.6\text{ kN} = 53.2\text{ kN}$.
- $F_{\text{bolt},\max} = 26.6\text{ kN}$: Correal vd. 2021 (CBM 305, Tablo 4) Ø15.9 mm cıvata tek bağlantı deney maksimum yüküdür (tasarım değeri değildir).
- $n_{\text{bolt}} = 2$ (çapraz cıvata) varsayımdır; $n_{\text{bolt}} = 1$ durumunda en büyük servis kuvveti (39.8 kN) nedeniyle kesitten bağımsız kapasite aşımı oluşacağından 2 cıvata zorunlu varsayılmıştır.

### 3.5. Servis Edilebilirlik Deplasman Kısıtı (SLS)
$$\text{Denklem (11):} \quad \frac{|u_{\max}|}{u_{\text{allow}}} \le 1.0, \quad u_{\text{allow}} = \frac{\text{span}}{150} = \frac{40\text{ m}}{150} \approx 0.267\text{ m} \quad \text{(IStructE 2025 Manual örneği)}$$

---

## 4. Post-Optimizasyon Beşikten-Kapıya LCA ($ECO_2e$) ve Duyarlılık

Optimizasyon tamamlandıktan sonra optimum tasarımlar üzerinde Beşikten-Kapıya (Modül A1–A3) gömülü karbon analizi yürütülür:

$$\text{Denklem (12):} \quad ECO_2e(\mathbf{X}) = m_{\text{bambu}} \cdot EC_b + m_{\text{steel}} \cdot EC_s + m_{\text{mortar}} \cdot EC_m \quad [\text{kg CO}_2\text{e}]$$

- $m_{\text{steel}} = N_n \cdot m_{\text{hub}} + 2 \sum_{i=1}^{N_e} (c_{s0} + c_{s1} D_i(x_i))$
- $m_{\text{mortar}} = 2 \sum_{i=1}^{N_e} \rho_m \frac{\pi}{4} (D_i - 2 t_i)^2 (L_{\text{inj}}), \quad L_{\text{inj}} = 2.5 D_i$
- Emisyon katsayıları: $EC_b = 0.35\text{ kg CO}_2\text{e/kg}$, $EC_s = 2.10\text{ kg CO}_2\text{e/kg}$, $EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ (varsayım; ICE v3.0 ve Zea Escamilla & Habert 2014 Tablo 8 ile teyit edilecektir).
- Düğüm parametreleri: $m_{\text{hub}} = 2.0\text{ kg/düğüm}$, $c_{s0} = 0.5\text{ kg/uç}$, $\rho_m = 2100\text{ kg/m}^3$ (varsayım).
- Bağlantı karbonunun payı ve Dekarbonizasyon Paradoksu, parametrik duyarlılık analizi ($L_{\text{inj}}/D \in [1.5, 3.5]$, $EC_s$, $EC_b$) ile incelenir.

---

## 5. Değişken ve Katsayı İsimlendirme Tablosu (Nomenclature)

| Sembol | Tanım | Değer / Birim |
| :--- | :--- | :---: |
| $\mathbf{X}$ | Ayrık kesit tasarım vektörü ($N_g$ grup) | $\{1, \dots, 24\}^{N_g}$ |
| $W_{\text{bambu}}$ | Yapısal bambu karkas ağırlığı | kN |
| $f_{\text{pen}}$ | Cezalı amaç fonksiyonu | kN |
| $P$ | Toplam normalize kısıt ihlali | - (Uygun: $P=0$) |
| $\varepsilon$ | Çarpımsal ceza üssü | $2.0$ |
| $D, t$ | Guadua culm dış çapı ve et kalınlığı | mm |
| $A, I, r$ | Enkesit alanı, atalet momenti, atalet yarıçapı | $\text{m}^2, \text{m}^4, \text{m}$ |
| $f_{c,k}, f_{c,\text{izin}}$ | Karakteristik ve izin verilen eksenel basınç dayanımı | $37.8\text{ MPa} / \text{ASD katsayılı}$ |
| $f_{t,k}, f_{t,\text{izin}}$ | Karakteristik ve izin verilen eksenel çekme dayanımı | $40.0\text{ MPa} / \text{ASD katsayılı}$ |
| $E_k$ | Karakteristik elastisite modülü | $10,000\text{ MPa}$ |
| $c$ | Ylinen kararlılık formülü katsayısı | $0.80$ |
| $C_{\text{bow}}, b_0$ | Eğrilik kusuru katsayısı ve başlangıç eğriliği | $1 - b_0/0.02, \quad b_0 = 0.01\text{ (varsayım)}$ |
| $\lambda_{max}$ | Narinlik üst sınırı | $150\text{ (varsayım)}$ |
| $F_{j,Rd}$ | Harç dolgulu mafsal eksenel kapasite sınırı | $53.2\text{ kN (2 cıvata varsayımı)}$ |
| $u_{\text{allow}}$ | SLS deplasman sınırı ($\text{span}/150$) | $266.7\text{ mm}$ |
| $EC_b, EC_s, EC_m$ | Bambu, çelik ve harç karbon katsayıları | $0.35, 2.10, 0.18\text{ kg CO}_2\text{e/kg (varsayım)}$ |
