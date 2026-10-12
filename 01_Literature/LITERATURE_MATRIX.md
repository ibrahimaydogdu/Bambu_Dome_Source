# 📊 LITERATURE_MATRIX.md: Tematik Literatür Sınıflandırma ve Karşılaştırma Matrisi

Bu matris, **Bambu Uzay Kafes Kubbelerin Tek Amaçlı Yapısal Optimizasyonu ve Dekarbonizasyon Paradoksu (ISO 22156 & Doğrudan Rijitlik / SAP2000 FEA)** çalışması kapsamında taranan uluslararası Q1/SCI literatürünü 4 temel metodolojik tema altında sentezler.

---

## 🏗️ Tema A: Bambu Yapısal Mekaniği, Bağlantı Sistemleri ve Standartlar

| Yazar & Yıl | İncelenen Sistem / Numune | Malzeme / Tür | Temel Bulgular / Kısıtlar | Bu Çalışmadaki Yeri ve Rolü |
| :--- | :--- | :--- | :--- | :--- |
| **ISO 22156:2021** | Yapısal bambu tasarım standardı | Doğal culm bambu | İzin verilen gerilme (ASD) esaslı tasarım. Yük faktörü ve malzeme kısmi katsayısı yoktur; süre ve servis faktörleri kullanılır. Narinlik sınırı $\lambda \le 150$ (kaynağı doğrulanmadı, varsayım). | Kodlama ve kısıt fonksiyonlarının birincil normatif çerçevesi. |
| **Trujillo, Harries, Kaminski, Lopez (2025)** | ISO 22156 uygulama kılavuzu (IStructE Manual v1.0) | *Guadua angustifolia*, *Phyllostachys edulis* | ASD kapasite denklemleri (Denk. 3.9, 6.5), Ylinen kararlılığı ($c = 0.8$, Denk. 6.1), $E_k = 10,000\text{ MPa}$, $f_{c,k} = 37.8\text{ MPa}$, $f_{t,k} = 40\text{ MPa}$, sehim sınırı örneği $\text{span}/150$. | Ayrık kesit kütüphanesi (Tablo 4.4, A3.4) ve ASD tasarım formülasyonu. |
| **Harries et al. (2012, 2017)** | Tam gövde (full-culm) bambu basınç elemanları | *Guadua angustifolia* | Bambu gövdede narinlik, lif boyuna elastik kararsızlık ve anizotropik davranış. | Basınç çubuklarında sütun kararlılık ve Ylinen denklemlerinin mekanik temeli. |
| **Correal, Prada, Suárez, Moreno (2021)** | Harç dolgulu cıvatalı bağlantılar (*CBM* 305: 124597) | *Guadua angustifolia*, Ø15.9 mm cıvata | Çift kesmeli harç dolgulu bağlantılarda eksenel yük aktarımı; tek bağlantı deney maksimum yükü $F_{\text{bolt},\max} = 26.6\text{ kN}$. | Mafsal eksenel kapasite sınırı ($F_{j,Rd} = 2 \times 26.6 = 53.2\text{ kN}$, $n_{\text{bolt}}=2$ varsayım). |
| **Paraskeva, Pradhan, Stoura, Dimitrakopoulos (2019)** | Çoklu culm-çelik bağlantılar (*CBM* 201: 473–483) | *Bambusa pervariabilis* (Kao Jue), M6 cıvata | Düğüm noktalarında eksenel yük aktarımı ve sünek göçme modları (Guadua ve harçlı mafsal için birincil kaynak değildir). | Mafsallı düğüm davranışı ve süneklik modellemesi incelemesi. |
| **Moran et al. (2017, 2021)** | Bambu kafes yapısal davranışı | Guadua kafesler | Düğüm davranışı, sehim tahkiki ve sonlu elemanlar modellemesi. | Kafes modelleme kabulleri ve servis edilebilirlik sınır durumu. |

---

## ⚙️ Tema B: Geniş Açıklıklı Kafes ve Kubbe Sistemlerde Meta-Sezgisel Optimizasyon

| Yazar & Yıl | İncelenen Sistem / Benchmark | Kullanılan Algoritmalar | Amaç Fonksiyonları & Kısıtlar | Bu Çalışmadaki Yeri ve Rolü |
| :--- | :--- | :--- | :--- | :--- |
| **Saka (1991)** | 40 m açıklıklı uzay kubbe | Klasik matematiksel / ayrık optimizasyon | Çelik profiller için minimum ağırlık; gerilme ve deplasman kısıtları. Orijinal model 2.9–5.97 m çubuk boylarıyla bambu narinliğini aşar. | 40 m açıklık ve yükleme referansı; $freq=2$ ile 1464 elemanlı (0.76–3.08 m) biyo-yapısal model türetilmiştir. |
| **Hasançebi et al. (2009, 2011)** | Geniş açıklıklı kubbeler | GA, PSO, SA, HS, ES, ACO | Sizing optimizasyonu, minimum ağırlık, gerilme ve stabilite tahkikleri. | Çelik kütle kıyaslama verisi; meta-sezgisel stokastik performans baz çizgisi. |
| **Kaveh & Talatahari (2010)** | Braced dome, uzay kafesler | BB-BC, HPSACO, Sezgisel yöntemler | Ayrık profil seçimi, deplasman ve gerilme kısıtları. | Geometrik gruplama (member grouping) ve simetri eksenlerinin belirlenmesi. |
| **Carbas (2016)** | Geniş açıklıklı kubbe kafes sistemler | Firefly, Bat Algorithm, Cuckoo Search | Geodezik ve Schwedler kubbe ağırlık minimizasyonu. | Algoritmik yakınsama hızı ve ceza fonksiyonu (penalty function) yaklaşımları. |
| **Geem et al. (2001) / Simon (2008)** | Ayrık kafes mühendislik optimizasyonu | Harmony Search (HS), Biogeography-Based (BBO) | Ayrık katalog seçimi, kısıtlı tek amaçlı ağırlık minimizasyonu. | 16 meta-sezgisel optimizasyon algoritması motorumuzun köklü kıyaslama üyeleri. |
| **Karaboga (2005) / Mirjalili et al. (2014, 2016)** | Biyo-esinli ve sürü optimizasyonu | ABC, GWO, WOA | Karmaşık multimodal arama uzaylarında küresel keşif ve yerel sömürü. | Aday optimizasyon yöntemleri havuzu ([TUNING SONUCUNA GÖRE] 3 nihai algoritma seçilecektir). |

---

## 🌿 Tema C: Yapısal Sistemlerde Gömülü Karbon ($ECO_2e$) ve Yaşam Döngüsü Analizi (LCA)

| Yazar & Yıl | Kapsam / Malzeme | Karbon Sınırı / Metodoloji | Temel Çıkarım / Emisyon Faktörleri | Bu Çalışmadaki Yeri ve Rolü |
| :--- | :--- | :--- | :--- | :--- |
| **Jones & Hammond (2019) / ICE v3.0** | İnşaat malzemeleri envanteri (ICE) | Beşikten-Kapıya (A1-A3) | Çelik profil: $\sim 1.80 - 2.45\text{ kg } CO_2e/\text{kg}$; Harç: $\sim 0.15 - 0.22\text{ kg } CO_2e/\text{kg}$. | Çelik ve bağlantı harcı gömülü karbon katsayıları (varsayım; ICE v3.0 ile teyit edilecek). |
| **Zea Escamilla & Habert (2014)** | Bambu esaslı yapı sistemlerinin çevresel etkisi (*JCLEPRO* 69: 117–127) | Beşikten-Kapıya (A1-A3), IMPACT 2002+ | Bambu direği için mPt/m³ verisi (ρ=100 kg/m³ alınmış, biyojenik karbon sayılmamış). Bağlantı plakalarının kritik rolü. | Bambu gövde emisyon katsayısı ($EC_{\text{bambu}} = 0.35$, varsayım; Tablo 8 ile teyit edilecek). |
| **van der Lugt et al. (2006, 2018)** | Endüstriyel ve doğal bambu LCA | Cradle-to-gate / Cradle-to-grave | Bambu hasadı ve işlenmesi: $\sim 0.20 - 0.50\text{ kg } CO_2e/\text{kg}$; Biyojenik depolama dinamikleri. | Doğal culm karbon salınımı modellemesinin literatür temeli. |
| **Eleftheriadis et al. (2018)** | Yapısal optimizasyonda gömülü karbon | LCA ve yapısal tasarım | Hibrit malzeme kullanımında bağlantı ve ikincil bileşenlerin toplam çevresel bütçedeki belirleyici rolü. | Post-optimizasyon LCA modelinde bağlantı emisyonlarının baskınlığının teorik gerekçesi. |

---

## 💻 Tema D: FEA Hesaplamalı Otomasyonu ve Doğrudan Rijitlik Çözücüsü

| Yazar & Yıl | Entegrasyon Mimarisi | Sonlu Elemanlar Platformu | Otomasyon Fonksiyonları | Bu Çalışmadaki Yeri ve Rolü |
| :--- | :--- | :--- | :--- | :--- |
| **Computers and Structures, Inc. (CSI)** | SAP2000 Open Application Programming Interface | SAP2000 OAPI (COM) | Model geometrisi tanımlama, kesit atama, analiz kilidi yönetimi, iç kuvvet ($N$) ve deplasman ($u$) okuma. | Doğrudan rijitlik çözücüsünün tam doğrulanması ve çapraz sağlama referansı. |
| **Gao et al. (2020) / Torii et al. (2017)** | Python - FEA optimizasyon arayüzü | Python / OAPI | Meta-sezgisel popülasyon bireylerinin vektörel analizi, süre optimizasyonu, bellek yönetimi. | Vektörel doğrudan rijitlik analiz stratejisi. |

---

## 📌 Sentez Özeti
Literatürdeki bu 4 bağımsız araştırma ekseni analiz edildiğinde; **bambu mekaniği ve ISO 22156 / IStructE (2025) ASD tasarım standardı**, **40 m geniş açıklıklı biyo-yapısal kubbe optimizasyonu (Saka 1991 benchmarkından türetilen 1464 elemanlı model)**, **tuning ile seçilen 3 meta-sezgisel yöntemin 30 bağımsız tohumla istatistiksel kıyaslaması (Wilcoxon rank-sum & Friedman)** ve **bağlantı emisyonlarının parametrik duyarlılığı** şimdiye kadar aynı potada birleştirilmemiştir. Bu ayrıklık, çalışmanın temel araştırma boşluğunu oluşturmaktadır.
