# 🏛️ TIER1_BASELINE_METHODS.md: Destekleyici ve İlgili Yöntemler (Katman 1)

Bu belge; çalışmada kullanılan sonlu elemanlar kabullerini, **ISO 22156:2021** ve **IStructE (2025)** kılavuzu izinli gerilme tasarımı (ASD) teorisini, beşikten-kapıya gömülü karbon ($ECO_2e$) hesaplama altyapısını ve meta-sezgisel optimizasyon referans yöntemlerini tanımlar. *(Spesifik kubbe geometrileri ve sayısal yük değerleri yöntem değil, Bölüm 3/4'teki "Sayısal Uygulama ve Tasarım Örnekleri" konusudur).*

---

## 1. 3D Uzay Kafes/Kubbe Sonlu Elemanlar Modelleme ve OAPI Prensipleri

### 1.1. Sonlu Elemanlar İdealleştirmesi
- **Eleman Tipi:** 3D çubuk elemanlar (Frame element).
- **Uç Serbestlikleri (Moment Releases):** Uzay kafes/kubbe sistemlerde çubukların uç bağlantıları mafsallı olarak idealleştirilir ($M_{22} = 0, M_{33} = 0$). Elemanlar salt eksenel çekme ve eksenel basınç kuvveti taşır.
- **Düğüm Noktası Kinematiği:** Mafsallı düğüm noktalarında serbest dönmeler ($R_x, R_y, R_z$) mevcut olup, yük aktarımı düğüm ötelemeleri ($U_x, U_y, U_z$) üzerinden gerçekleşir.
- **OAPI COM Yönetimi:** SAP2000 OAPI oturumu `eUnits.kN_m_C` (Kilonewton, Metre, Santigrat) birim kilidi altında yönetilir.

### 1.2. Genel Yükleme ve Sınır Durum Felsefesi (ASCE 7-22 ASD)
Sistem; zati yük ($D$), kar yükü ($S$) ve rüzgar yükü ($W$) kombinasyonları altında **ASCE 7-22 §2.4.1 ASD** (faktörsüz) kombinasyonlarına göre analiz edilir:
1. $D$ (Kalıcı yük, $C_{DF} = 0.55$)
2. $D + S$ (Geçici/orta süreli kar, $C_{DF} = 0.65$)
3. $D + 0.6W$ (Anlık rüzgar, $C_{DF} = 0.85$)
4. $D + 0.75S + 0.45W$ (Anlık rüzgar kombinasyonu, $C_{DF} = 0.85$)
5. $0.6D + 0.6W$ (Anlık rüzgar emme/kaldırma, $C_{DF} = 0.85$)

---

## 2. ISO 22156:2021 ve IStructE (2025) İzinli Gerilme Tasarımı (ASD) Tahkikleri

Yapısal bambu elemanların dayanım ve stabilite kontrolleri **ISO 22156:2021** ve **IStructE (2025)** *Manual for the design of bamboo structures to ISO 22156:2021* (Denklem 3.9, 6.5) uyarınca İzinli Gerilme Tasarımı (Allowable Stress Design - ASD) ilkelerine göre yürütülür. ISO 22156 izinli gerilme esaslı bir standart olup, yük faktörü veya malzeme kısmi katsayısı ($\gamma_M$) içermez.

### 2.1. İzin Verilen Dayanımlar ve Düzeltme Katsayıları
İzin verilen dayanım ($X_{\text{izin}}$), karakteristik dayanımın ($X_k$) servis ve güvenlik katsayılarıyla ölçeklenmesiyle hesaplanır:

$$\text{Denklem (1):} \quad X_{\text{izin}} = \frac{X_k \cdot C_R \cdot C_{DF} \cdot C_T}{FS}$$

Kapasite çarpanı $k_{\text{ASD}} = \frac{C_R \cdot C_{DF} \cdot C_T}{FS}$ olarak tanımlanır:
- $FS = 2.0$: Boyuna gerilmeler için güvenlik katsayısı (IStructE Manual Denklem 3.9).
- $C_R = 0.90$: Güvenilirlik/grup etkisi katsayısı (Tekil culm elemanlar için muhafazakâr varsayım; Manual $\ge 4$ paralel culm için $1.1$ öngörür).
- $C_{DF}$: Yük süresi katsayısı (Servis Sınıfı 2):
  - Kalıcı yük ($D$): $C_{DF} = 0.55 \implies k_{\text{ASD}} = 0.2475$
  - Geçici/orta süreli yük ($D+S$): $C_{DF} = 0.65 \implies k_{\text{ASD}} = 0.2925$
  - Anlık yük ($W$ içeren kombinasyonlar): $C_{DF} = 0.85 \implies k_{\text{ASD}} = 0.3825$
- $C_T = 1.0$: Sıcaklık katsayısı ($T \le 40^\circ\text{C}$).

*Malzeme Özellikleri (*Guadua angustifolia*, IStructE Manual 2025 Tablo 4.4 şema ve Tablo A3.4):*
- Karakteristik boyuna basınç dayanımı: $f_{c,0,k} = 37.8\text{ MPa}$ ($n = 922$)
- Karakteristik boyuna çekme dayanımı: $f_{t,0,k} = 40.0\text{ MPa}$ (Manual Tablo 4.4 şema alt sınırı)
- Karakteristik elastisite modülü: $E_k = 10\,000\text{ MPa}$ (Tüm $D/t$ oranları için şema alt sınırı; FEM rijitliği ve burkulma analizi aynı $E_k$ değerini kullanır; $E_{05}$ kavramı kullanılmaz).
- Birim hacim kütlesi: $\rho = 700\text{ kg/m}^3$ (Guadua ortalaması $\approx 680\text{ kg/m}^3$, Tablo A3.9).

### 2.2. Eksenel Çekme Tahkiki
Eksenel servis çekme kuvveti ($N_t$), net enkesit alanı ($A$) ve izin verilen çekme gerilmesi ($f_{t,0,\text{izin}}$) sınırını aşamaz:

$$\text{Denklem (2):} \quad \frac{N_t}{N_{t,\text{izin}}} \le 1.0, \quad \text{burada } N_{t,\text{izin}} = A \cdot \frac{f_{t,0,k} \cdot C_R \cdot C_{DF} \cdot C_T}{FS}$$

### 2.3. Eksenel Basınç ve Ylinen Burkulma Tahkiki
Dış çap $D$ ve et kalınlığı $t$ olan dairesel içi boş bambu enkesitte ($d_i = D - 2t$):
Enkesit alanı $A = \frac{\pi}{4}(D^2 - d_i^2)$, atalet momenti $I = \frac{\pi}{64}(D^4 - d_i^4)$ ve atalet yarıçapı $r = \frac{\sqrt{D^2 + d_i^2}}{4}$'tür.

1. **Narinlik Sınırı:**
   $$\text{Denklem (3):} \quad \lambda = \frac{K \cdot L}{r} \le \lambda_{\max} = 150 \quad \text{[kaynağı doğrulanamadı, muhafazakâr mühendislik varsayımı]}$$
   Kafes elemanları için burkulma boyu katsayısı $K = 1.0$'dir.

2. **Ylinen Formülasyonu ve Euler Kararsızlığı (IStructE Manual 2025 Denklem 6.1–6.5, Ek A6.2):**
   Karakteristik elastik Euler burkulma yükü:
   $$\text{Denklem (4):} \quad P_{e,k} = \frac{\pi^2 E_k I C_{\text{bow}}}{(K L)^2}$$
   Burada eğrilik düzeltme çarpanı $C_{\text{bow}} = 1 - b_0 / 0.02$'dir; culm başlangıç eğrilik oranı $b_0 = 0.01$ olarak alınmıştır ($C_{\text{bow}} = 0.50$, varsayım).
   
   Ylinen formülasyonu ($c = 0.8$ plastikleşme parametresi, Manual Denklem 6.1):
   $$\text{Denklem (5):} \quad P_{cr,k} = \frac{P_{c,k} + P_{e,k}}{2c} - \sqrt{\left(\frac{P_{c,k} + P_{e,k}}{2c}\right)^2 - \frac{P_{c,k} P_{e,k}}{c}}$$
   burada $P_{c,k} = A \cdot f_{c,0,k}$ karakteristik ezilme yüküdür.
   
   İzin verilen eksenel basınç kapasitesi ($N_{cr,\text{izin}}$):
   $$\text{Denklem (6):} \quad N_{cr,\text{izin}} = P_{cr,k} \cdot \frac{C_R \cdot C_{DF} \cdot C_T}{FS}$$
   
   Basınç tahkik şartı:
   $$\text{Denklem (7):} \quad \frac{N_c}{N_{cr,\text{izin}}} \le 1.0$$

### 2.4. Düğüm Noktası Bağlantı Kapasitesi
Bambu kafes elemanlarının uç bağlantılarında eksenel yük aktarım sınır durumu:

$$\text{Denklem (8):} \quad \frac{|N|}{F_{j,Rd}} \le 1.0$$

Burada $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\max} = 2 \times 26.6 = 53.2\text{ kN}$'dur.
- $F_{\text{bolt},\max} = 26.6\text{ kN}$: Correal vd. 2021 (*Constr. Build. Mater.* 305: 124597) Tablo 4'ten alınan Ø15.9 mm tekil cıvatalı, harç enjeksiyonlu *Guadua* bağlantısının **deneysel maksimum tepe yüküdür** (izin verilen tasarım değeri değildir).
- $n_{\text{bolt}} = 2$ (çapraz çift cıvata) **kaynaksız bir varsayımdır**.
- *Gerekçe ve kısıtlayıcı duyarlılık:* Tek cıvata ($n_{\text{bolt}} = 1, 26.6\text{ kN}$) kabulünde, ribbed40 kubbesinde 1464 elemanın 231'i, kiewitt32 kubbesinde 8 eleman en büyük kesit (kesit 24) seçilse dahi sınırı aşmaktadır (maksimum servis kuvveti $39.8\text{ kN}$). Dolayısıyla $n_{\text{bolt}} = 2$ kabulü yapısal uygulanabilirlik için zorunlu bir varsayım olup çalışmada duyarlılık konusu olarak tartışılır.

### 2.5. Servis Edilebilirlik Sınır Durumu (SLS - Deplasman)
Maksimum düğüm düşey yer değiştirmesi açıklık ($S$) cinsinden sınırlandırılır (IStructE Manual 2025 örneği; ISO 22156 doğrudan sehim sınırı vermez):

$$\text{Denklem (9):} \quad \frac{|u_{\max}|}{u_{\text{izin}}} \le 1.0, \quad u_{\text{izin}} = \frac{S}{150} = \frac{40\,000\text{ mm}}{150} \approx 266.67\text{ mm}$$

*(Not: Literatürde sık rastlanan $S/250$ veya $S/360$ gibi daha katı sınırlar ikincil duyarlılık senaryosu olarak değerlendirilebilir).*

---

## 3. Beşikten-Kapıya Gömülü Karbon ($ECO_2e$) Varsayımları

Gömülü karbon sınırları EN 15978 standardına göre **Beşikten-Kapıya (Cradle-to-Gate / Modül A1–A3)** olarak modellenir. Modelde kullanılan katsayılar literatür varsayımları olup, ICE v3.0 ve Zea Escamilla & Habert 2014 ile teyit edilmelidir:
- $EC_{\text{bambu}} = 0.35\text{ kg CO}_2\text{e/kg}$ (Varsayım; Zea Escamilla & Habert 2014 Tablo 8 teyit bekliyor).
- $EC_{\text{çelik}} = 2.10\text{ kg CO}_2\text{e/kg}$ (Varsayım; ICE v3.0 teyit bekliyor).
- $EC_{\text{harç}} = 0.18\text{ kg CO}_2\text{e/kg}$ (Varsayım; ICE v3.0 teyit bekliyor).

---

## 4. Meta-Sezgisel Optimizasyon Algoritmaları Havuzu

Kod altyapısında 16 meta-sezgisel optimizasyon algoritması (HS, BBO, WOA, DO, ABC, ACO, BSO, CSA, FA, GOA, TLBO, TSA, GWO, HBA, AO, SSO) bulunmaktadır. Bu havuzdan ön tarama ve hiperparametre duyarlılık çalışması (`04_Results/TUNING_STUDY.md`) sonucunda seçilecek **3 algoritma ([TUNING SONUCUNA GÖRE])** nihai 30 tohumluk deneysel kampanyada kullanılacaktır.
