# 📜 SYSTEM_RULES.md (Akademik Üretim Anayasası)

Bu belge, sistemdeki tüm ajanların (Master, Critic, Literature, Method, Developer, Results, Stylist) uymak zorunda olduğu DEĞİŞMEZ ve BAĞLAYICI kurallar bütünüdür. Hiçbir ajan bu kuralları ihlal edemez veya kullanıcı açıkça aksini belirtmedikçe esnetemez.

---

## 1. DİL VE ÜSLUP STANDARTLARI (ANTI-AI PROTOKOLÜ)

Metin üretimi sırasında yapay zeka jargonu ve gereksiz edebi süslemeler KESİNLİKLE YASAKTIR. Hedef üslup: Doğrudan, somut, kanıta dayalı ve uluslararası Q1/SCI indeksli dergi standardında kuru/teknik akademik İngilizce/Türkçe'dir.

### 🚫 Kara Liste (Yasaklı Kalıplar ve Kelimeler)
Aşağıdaki ifadeler ve türevleri tespit edildiği anda Hakem (Critic) tarafından metin doğrudan reddedilecektir:
- **Klişe Girişler:** *"In today’s rapidly evolving world/landscape...", "In the era of modern technology...", "Since the dawn of...", "With the burgeoning demand for sustainable materials..."*
- **Süslemeli Dolgu Kelimeleri:** *"delve into", "tapestry", "plethora", "crucial testament", "beacon of hope", "game-changer", "groundbreaking", "ever-evolving", "paramount importance", "holistic view", "foster", "pivotal role".*
- **Aşırı İddialı / Duygusal Sıfatlar:** *"revolutionary", "astonishing", "miraculous", "flawless", "unprecedented", "remarkable"* (Yalnızca sayısal veya literatür kanıtı varsa nesnel terimler kullanılabilir).
- **Yapay Zeka Kapanışları:** *"In conclusion, this study opens new horizons and paves the way for a greener, brighter future..."* yerine doğrudan sayısal bulgular, sınır şartları ve kısıtlar yazılacaktır.

### ✅ Zorunlu Yazım İlkeleri
1. **Nesnellik:** İddialar süslü laflarla değil; sayısal verilerle (yüzdeler, p-değerleri, hesaplama süreleri, karbon tasarrufu kg $CO_2e$, gerilme oranları vb.) desteklenecektir.
2. **Cümle Yapısı:** Aşırı uzun, 4-5 bağlaçlı labirent cümleler yerine; teknik olarak net, aktif/pasif dengesi doğru kurulmuş ifadeler tercih edilecektir.
3. **Akademik Referans:** Her iddia ya çalışmanın kendi bulgusuna ya da literatür atfına dayanmalıdır. Havada kalan genel geçer cümleler yasaktır.

---

## 2. METODOLOJİ KURALLARI (2 AŞAMALI YAPI VE TEK AMAÇLI FORMÜLASYON)

Metodoloji bölümü yazılırken istisnasız aşağıdaki iki katmanlı hiyerarşi uygulanacaktır:

### Katman 1: Destekleyici ve İlgili Yöntemler (Baseline / Supporting Methods)
- Çalışmada kullanılan standart ve yerleşik altyapılar burada özetlenir:
  - 3D uzay kafes sonlu elemanlar kubbe modelleme kabulleri (mafsallı çubuk elemanlar, serbest dönmeler, yük kombinasyonları).
  - Klasik meta-sezgisel kıyaslama algoritmaları (örn: Harmony Search, Biogeography-Based Optimization, Ant Colony Optimization).
  - Beşikten-kapıya (A1–A3) gömülü karbon ($ECO_2e$) hesaplama standartları (EN 15804, ISO 14040).
  - Ansiklopedik uzatmalardan kaçınılır; yalnızca çalışmadaki fonksiyonu ve neden seçildiği literatürle desteklenerek belirtilir.

### Katman 2: Önerilen / Özgün Yöntem (Proposed Methodology)
- Makalenin kalbidir:
  - **Tek Amaçlı Kurgu:** Eksenel kafes kubbede kütle ve karbon, ziyaret edilen uygun tasarımlarda pozitif ilişkilidir ($r = 0.72 - 0.90$) ancak özdeş değildir. Çok amaçlı arama kapsam dışıdır ve kanıtsız Pareto iddiaları yasaktır; problem tek amaçlı yapısal ağırlık minimizasyonu ($\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$) olarak formüle edilir.
  - **Tuning Temelli 3 Algoritma Kampanyası:** 16 algoritmalık havuz doğrulanmış olup, büyük üretim kampanyasında tuning duyarlılık çalışmasından seçilen 3 algoritma (ABC, ACO, DO) kullanılır (NFE = $1000 \times N_{\text{grup}}$).
  - **ISO 22156 / IStructE (2025) ASD Tahkikleri:** İzin verilen gerilme tasarımı ($X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$, Ylinen $c = 0.8$, $C_{\text{bow}} = 1 - b_0/0.02$, $b_0 = 0.01$ varsayım, $K = 1.0$, $E_k = 10,000\text{ MPa}$, $f_{t,k} = 40\text{ MPa}$, $f_{c,k} = 37.8\text{ MPa}$), geometrik narinlik ($\lambda \le 150$, çekme ve basınca uygulanır), bağlantı kapasitesi ($F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$, NSR-10 Tabla G.12.11-2/3 izinli yük, $n_{\text{bolt}} = 4$ kullanıcı kararı) ve servis deplasman kısıtları ($u_{\max} \le \text{span}/150$, IStructE Manual örneği) katı uygunluk ($P=0$) şartıyla sağlanır.
  - **Ayrık Kesit Eşleme (Discrete Mapping):** Bambu gövde boyutlarının (dış çap $D$, et kalınlığı $t$) 24 kesitli Guadua kataloğu ile eşleştirilmesi tanımlanacaktır.
  - **Post-Optimizasyon LCA ve Parametrik Duyarlılık:** Optimum tasarımlarda bağlantı çeliği ve harç dolgusu karbon payının parametrik duyarlılığı ($L_{\text{inj}}/D$, $EC_{\text{steel}}$, $EC_{\text{bamboo}}$) post-processing ile ortaya konur; sonuçlar `LCA_SENSITIVITY_REPORT.md`'dedir (temel senaryo %74.1–82.1, birleşik elverişsiz uç %45.3–57.7).

---

## 3. KOD, SİMÜLASYON VE VERİ KURALLARI

1. **Doğrulama Önceliği:** Developer Agent, optimizasyon kodunu üretirken doğrudan kör çalıştırma yapmaz. Önce kodun mimarisini, birim kilidini (`kN, m, C`), FEA doğruluğunu ve girdi-çıktı mantığını Hakem/Kullanıcı onayına sunar.
2. **Modülerlik ve Hesaplama Hijyeni:**
   - Analiz çözücüsünde bellek sızıntısı önlemi, matris simetrisi ve hata yakalama (`try-except`) blokları zorunludur.
   - Doğrudan rijitlik matrisi ve ISO 22156 kısıt fonksiyonları vektörel NumPy işlemleriyle optimize edilmelidir.
3. **Optimizasyon ve LCA Veri Kaydı:**
   - Her bağımsız koşu için elde edilen en iyi cezalı ağırlık, bambu kütlesi, uygulanabilirlik durumu ($P=0$), yakınsama geçmişi, A1–A3 gömülü karbon bileşen dökümü (bambu, çelik, harç) ve harcanan hesaplama süreleri `03_Code_Execution` ve `04_Results` dizinlerine yapılandırılmış CSV/JSON dosyaları olarak kaydedilecektir.

---

## 4. HAKEM (CRITIC) GEÇİT PROTOKOLÜ (GATEKEEPING)

- Sistemde hiçbir alt ajan kendi başına bir sonraki aşamaya GEÇEMEZ.
- **Onay Zinciri:**
  1. Alt ajan çıktıyı üretir (Örn: `02_Methods/MATHEMATICAL_FORMULATION.md`).
  2. Critic Agent devreye girer; ISO 22156 uyumsuzluğu, eksik değişken, yapay zeka dili veya metodolojik boşluk arar.
  3. Critic ya `[REVİZYON TALEBİ: Gerekçeler...]` diyerek işi geri gönderir ya da `[HAKEM ONAYI VERİLDİ]` damgasını basar.
  4. Hakem onayı ve Kullanıcı teyidi olmadan sonraki bölüme geçmek yasaktır.

### 4.1. Revizyon, Eskalasyon ve Devre Kesici (Circuit Breaker)
1. **Mikro/Teknik Hatalar:** Sözdizimi (syntax), biçim, formül eksikliği veya yasaklı kelime hatalarında alt ajan, Hakem geri bildirimiyle OTOMATİK olarak kendi çıktısını revize eder. Kullanıcı meşgul edilmez.
2. **Makro/Yöntemsel Tercihler:** Bambu türü seçimi, optimizasyon algoritmasının değiştirilmesi, bağlantı tipi tercihi veya objektif fonksiyon ağırlıklandırması gibi akademik kararlarda konu derhal Master Agent üzerinden Kullanıcıya eskalasyon yapılır.
3. **Kural Değiştirme Yasağı:** Hiçbir alt ajan Hakem'i geçmek amacıyla `SYSTEM_RULES.md` kurallarını gevşetemez veya değiştiremez. Sadece `PROJECT_STATE.md` hafızasını güncelleyebilir.
4. **Maksimum 3 İterasyon Freni:** Bir alt ajan Hakem revizyonunu en fazla 3 denemede çözmek zorundadır. 3. turda uzlaşma sağlanamazsa işlem durdurulur ve son karar için Kullanıcıya sunulur.

---

## 5. TOKEN TASARRUFU VE DOSYA YÖNETİMİ

1. **Bağlam Temizliği (Context Resetting):** 
   - Bir bölüm tamamlanıp onaylandığında, sohbet geçmişi taşınmaz. Yeni aşama için taze bir prompt başlatılır ve sadece gerekli bağlam dosyaları referans verilir.
2. **Kısmi Güncelleme İlkesi:** 
   - Bir kodda veya uzun metinde tek bir blok değişecekse, tüm dosya sohbet ekranına baştan yazdırılmaz; sadece değişen blok hedeflenir.
3. **Klasör Sınırları:** 
   - Bütün işlemler sadece mevcut makalenin klasöründeki bağıl yollarla (`01_Literature/`, `02_Methods/` vb.) yürütülür.

---

## 6. DİNAMİK HAFIZA VE TUR GÜNCELLEME PROTOKOLÜ (MANDATORY STATE UPDATE)

Her çalışma turunun sonunda ilgili ajan aşağıdaki adımları tamamlamak zorundadır:
1. **Tur Sonu Hafıza Kaydı:** Ajan, cevabını bitirmeden önce o turda ne öğrendiğini, hangi parametrenin başarılı/başarısız olduğunu veya Hakem'in getirdiği eleştiriyi `00_System/PROJECT_STATE.md` dosyasına işler.
2. **Kör Döngü Yasağı:** Hakem veya alt ajanlar, daha önce reddedilmiş bir hipotezi, ISO 22156 ihlali içeren bir formülasyonu ya da çökmüş bir OAPI yaklaşımını tekrar öneremez.
3. **Senkronizasyon:** İş bittiğinde proje ilerleme tablosundaki bayraklar (Status Flags) güncellenir.