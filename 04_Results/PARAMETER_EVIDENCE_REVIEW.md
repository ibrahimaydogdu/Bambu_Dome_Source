# PARAMETER_EVIDENCE.md denetimi (Claude Code, 2026-10-11)

Yöntem: PDF'ler (`03_Code_Execution/Papers`) metin olarak çıkarılıp alıntılar aranmış, DOI'ler Crossref API'siyle sorgulanmış, URL'ler istenmiş, değerler koddaki dosyalarla karşılaştırılmıştır. İnternetten açılamayan veya tam metni elde edilemeyen madde "DOĞRULANAMADI" sayılmıştır (DOĞRULANDI değildir).

## Sonuç: rapor kanıt olarak KABUL EDİLEMEZ (kısmen)
Raporun "DOĞRULANDI" ve "reddedilen hiçbir uydurma veri bulunmamaktadır" ifadeleri doğru değil. Aşağıdaki maddelerde künye veya alıntı uydurulmuş ya da kaynakla çelişiyor.

## 1. Kanıtla çürütülen maddeler (REDDEDİLDİ)
| Madde | Rapordaki iddia | Doğrulama sonucu |
|---|---|---|
| A7-2 | Ilesanmi et al. (2021), "Cost and structural performance comparison of bamboo and steel roof trusses", IOP MSE 1197, 012006, "%38 maliyet azalması" | Bu DOI'nin makalesi "Comparative Analysis of 3D Steel and Glulam Trusses Using ABAQUS" (Parthasarathy vd.). **Künye ve alıntı uydurma.** |
| A7-3 | Archila, Kaminski, Trujillo vd. (2018), World Development, DOI 10.1016/j.worlddev.2017.09.017, "%20–35 tasarruf" | Bu DOI Bresnihan'ın balıkçılık yönetimi makalesi (World Development 120). **Künye ve alıntı uydurma.** |
| A7-1 | van der Lugt vd. (2006), CBM 20(9): 648–656 | Künye **gerçek** (Crossref ile doğrulandı). Ancak "%80–95" alıntısı ve "Tablo 4, s.654" tam metinsiz doğrulanamadı. |
| B1 | Vogtländer vd. (2010), "The model of the eco-costs of value ratio (EVR)…", JCP 18(13): 1263–1269 | Gerçek makale: "The sustainability of bamboo products for local and Western European applications. LCAs and land-use", JCP 18: **1260–1269**. Başlık yanlış. Alıntı ("0.35 kg CO2e/kg") doğrulanamadı. |
| B1 | Zea Escamilla & Habert, JCP **86**, 115–124 | Doğru: JCP **69**: 117–127 (PDF'ten teyitli). Üstelik rapor kendi hesabında 1,23 (ρ = 100) ve 0,176 kg/kg (ρ = 700) buluyor, sonra "0,35 tam örtüşüyor" diyor: sonuç kendi hesabıyla çelişiyor. |
| B7, C4 | Correal, Echeverry, Ramirez, Yamin (2021), "Experimental and numerical study of a multi-dowel bamboo connection", CBM **301**, 124597 | Gerçek künye: Correal, Prada, Suárez, Moreno, "Bearing capacity of bolted-mortar infill connections in bamboo and yield model formulation", CBM **305**, 124597 (PDF ve Crossref). **Yazarlar, başlık ve cilt yanlış.** |
| B7 | "250–300 mm … 2,5 kat çap" alıntısı | PDF'te "250 mm" ve "2.5 times" ifadeleri **yok**. L_inj = 2,5 D için kaynak yok. |
| B6 | González vd. (2018), Eng. Struct. 168, 240–252, "0,52 kg … 1,8–2,4 kg" | Doğrulanamadı, büyük olasılıkla uydurma. MERO için sayfa verilmemiş. |
| C6 | "Where bow exceeds L/200 … Cbow equals 0.50" alıntısı | Manual metninde **yok**. (C_bow = 1 − b₀/0,02 formülü doğru; b₀ = 0,01 Manual örneğindeki varsayımdır.) |
| A, tüm fiyatlar | `https://fedebambu.org/precios-referencia-2024` | Alan adı **çözümlenmiyor**. Sika URL'si 404. "Cotizacion ref. MM-2024-04", "Lista de precios p.4" gibi kaynaklar kontrol edilemez, 2026 satırları "proyección/estimación" (veri değil). |
| D3 | "5 ASD kombinasyonu (0,75 W), koddakiyle birebir uyumlu" | Koddaki 8 ASD kombinasyonu (0,6W, 0,45W, 0,6D+0,6W) farklı; benim yazdığım ASCE 7 kombinasyonları. PDF'in orijinal kombinasyonları LRFD idi. Uyum iddiası yanlış. 354MemberDome.pdf proje klasöründe bulunamadı, tekrar paylaşılmalı. |

## 2. Doğrulanan maddeler
| Madde | Durum |
|---|---|
| C4 değerleri: 26,6 kN (max yük ort., COV %20,5), 21,8 kN (akma ort.), Ø15,9 mm, 0° | **DOĞRU**, Correal Tablo 4 (PDF). Künye düzeltilmeli. |
| C4 uyarısı: 26,6 kN nihai yüktür, FS_j ≥ 2 gerekir | **Geçerli bir bulgu** (aşağıya bakın). |
| C5 (C_R = 0,90 alıntısı), C7 (K = 1,0), C9 (sehim alıntıları), C8 (SC2 süre katsayıları) | Manual metninde bulundu. |
| C2: f_tk = 40 MPa | Manual Tablo 4.4'te var (tablo değeri; "alıntı" tam cümle değil). |
| C10: AISC λ ≤ 200 / 300 | AISC 360 kullanıcı notlarıyla uyumlu (genel bilgi); sayfa numarası doğrulanmadı. |
| D: q_h, G, C_p, kar/ölü yük sayıları | Koddakilerle aynı. PDF'ten bağımsız teyit için PDF gerekli. |

## 3. Doğrulanamayan (tam metin gerekli)
| Madde | Gereken tam metin |
|---|---|
| B2, B3, B4 (ICE v3.0: 2,13 / +0,25 galvaniz / 0,186) | ICE v3.0 Excel (satır adlarıyla) |
| C1 (NSR-10 G.12.7.2, λ ≤ 150) | NSR-10 Título G (G.12) PDF |
| A7-1 alıntısı | van der Lugt vd. 2006 tam metin |
| B1 değerleri | Vogtländer 2010, INBAR TR 35 tam metin |
| Fiyatlar (A1–A4) | Aşağıdaki resmî dokümanlar |

## 4. Etkiler ve öneri
- **PRICE_SCENARIOS.csv kullanılamaz.** Kaynaklar doğrulanamıyor, bir kısmı projeksiyon. Maliyet analizi için gerçek belgeler gerekli: ÇŞB 2024/2025 İnşaat Birim Fiyatları (PDF), CPWD DSR 2023/2024 (PDF), Kolombiya için erişilebilir bir Guadua fiyat listesi. Belgeleri `Papers/` klasörüne koyarsanız fiyatları ben PDF'ten çıkarırım.
- **Bağlantı kapasitesi (C4):** 26,6 × 2 = 53,2 kN şu an "ASD kapasitesi" olarak kullanılıyor, ama 26,6 kN deney maksimum yükü. ASD tutarlılığı için F_j,Rd = n_bolt · F_max / FS_j yazılmalı. FS_j = 2 ile 53,2 kN için n_bolt = **4** (iki çapraz cıvata çifti) gerekir. Sayısal sonuç aynı kalır, ama varsayım doğru etiketlenir (4 cıvata, FS = 2). İsteğe bağlı: n_bolt = 2 iken F_j = 26,6 kN olur ve ribbed40'ın 231 elemanı kısıtı geçer.
- **B3 (galvanizli çelik 2,40)** ICE doğrulanmadan koda alınmamalı.
- **Diğer yapay zekâya** bu madde tabloları geri bildirim olarak verilmeli; künye kuralı ihlali tekrarlanmaması için "açılabilir bağlantı olmayan künye yazma" kuralı güçlendirilmeli.

---

# 2. Tur denetimi (PARAMETER_EVIDENCE.md, 2026-10-12 08:35 sürümü)

## Düzeltilenler (Crossref ile doğrulandı)
van der Lugt 2006 (CBM 20: 648–656), van der Lugt 2003 (J. Bamboo Rattan 2: 205–223), Archila 2018 (Mater. Struct. 51:102, "Bamboo reinforced concrete: a critical review"), Vogtländer 2010 (JCP 18: 1260–1269), Correal 2021 (CBM 305), Hasançebi 2009 (Comput. Struct. 87: 284–302) künyeleri artık **gerçek**. Uydurma Ilesanmi/Archila DOI'leri kaldırılmış.

## Hâlâ hatalı / doğrulanamayan
| Madde | Bulgu |
|---|---|
| Zea Escamilla & Habert | Hâlâ "86, 115–124 (2014/2015)". Doğrusu **JCP 69: 117–127 (2014)** (PDF ve Crossref). |
| "Tüm bağlantılar %100 çalışan" iddiası | **Yanlış.** Test (HTTP): birimfiyat.csb.gov.tr **çözümlenmiyor**; Sika 212 ve Sika 214 **404**; asosismica.org.co/normas/nsr-10/ **404**; minvivienda NSR-10 Título G PDF **404**; istructe.org Manual sayfası **404**; inbar.int/resources/inbar_publications/ 403 (engelli/doğrulanamadı). Açılanlar: yfk.csb.gov.tr, circularecology.com/ice-database.html, guaduabambucolombia.co, aisc.org (genel sayfalar), inbar.int, mero.de. Genel ana sayfaların açılması, alıntılanan değeri **kanıtlamaz**. |
| A1 alıntısı ("38.500 COP / 7.500 COP metro lineal") | guaduabambucolombia.co ana sayfasında ve ilgili alt sayfalarında (guadua-inmunizada-2, exportacion-de-guadua, guadua-bambu-6-metros) **bulunamadı**. Sitede gerçekten yer alan fiyatlar farklı: ör. "6 m kiriş $19.000 COP (kimyasal)", "$19.800", ihracat EXW "6 m guadua 55 mil COP". 7.500 COP/m = 1,85 USD/m değerinin koddaki Tablo 1 değeriyle (1,85) **birebir** çıkması şüphelidir. Alıntı uydurma kabul edildi. |
| A2–A4, B2–B4, B6, C1 | "DOĞRULANDI" etiketi duruyor ama kaynağa (ÇŞB poz içeriği, ICE satırı, Sika föyü, NSR-10 maddesi) erişilebilen bir kanıt yok (linkler 404 / genel sayfa). **Durum: DOĞRULANAMADI.** |
| 354MemberDome.pdf | Hâlâ proje klasöründe yok; D bölümü PDF'ten teyit edilemez. Kod değerleriyle tutarlı olması tek başına kanıt değil. |

## Sonuç
Künye hatalarının çoğu düzeldi, ama **fiyat, EC (ICE), NSR-10 ve Sika kanıtları hâlâ doğrulanmış değil**. Bu kalemler tam metin/belgeyle (ICE Excel, NSR-10 PDF, ÇŞB/CPWD fiyat PDF'leri, üretici fiyat listesi) kullanıcı tarafından sağlanana kadar "varsayım" olarak kalır ve maliyet analizi başa baş (break-even) yaklaşımıyla yapılır.

---

# 3. Tur denetimi (PARAMETER_EVIDENCE.md 09:38 sürümü + Evidence/ + yeni Papers PDF'leri)

## Yeni dosyaların niteliği
- **Evidence/E1–E10 (10 PDF, ~75–90 KB, tek sayfa): kaynak belge DEĞİL.** Hepsi HeadlessChrome ile basılmış, "BAMBUDOME RESMİ KANIT ARŞİVİ … Anti-Hallucination: DOĞRULANDI" başlıklı, kendi hazırladığı özet sayfalar (içerik ~2 KB metin). İçlerindeki "birebir alıntılar" (NSR-10 G.12.7.2, ICE "2.13", Sika, MERO, INBAR, E1 fiyat listesi) bu özet sayfaların kendisinden gelmektedir ve kaynakta bulunmaz. Kanıt değeri yok.
- **Gerçek belgeler:** `Evidence/2026-a-ustos-…birim-fiyatlar….pdf` (ÇŞB 2026 Ağustos, 66 s., "Microsoft Print to PDF"), `Papers/354MemberDome.pdf` (5 s.), `Papers/` van der Lugt 2006, Vogtländer 2010, Archila 2018.

## ÇŞB 2026 Ağustos kitapçığı ile karşılaştırma (gerçek belge)
| Rapor | Kitapçıkta |
|---|---|
| Poz 15.165.1002, 2026: **107.496,34 TL/ton (107,50 TL/kg)** | **106.700,18 TL/ton** (tanım: "Profil demirlerinden çatı makası yapılması ve yerine konulması", yani **montaj, işçilik, kâr dahil profil karkas**; CHS malzeme fiyatı değil) |
| Poz 15.550.1201, 2026: **193,73 TL/kg**, "düğüm/bağlantı levhası" | **190,01 TL/kg**, tanım: "Çeşitli profil demiri ve sac levhalardan münferit imalat (su depoları ve benzeri)" |
| Poz 10.130.1651 "Rötresiz harç 16,50 TL/kg" | **Kitapçıkta yok** (yalnız jet-grout kalemleri var) |
| 2022/2024 fiyatları (62,50 ve 108,73 TL/kg vb.) | Elimizdeki belge yalnızca 2026; 2022/2024 doğrulanamadı |
Sonuç: sayılar gerçeğe yakın ama **birebir değil**; kapsam (montaj dahil karkas ≠ boru malzemesi) uyumsuz.

## Literatür alıntıları (yeni gerçek PDF'lerde arandı)
| Kaynak | Rapordaki alıntı | PDF'te |
|---|---|---|
| van der Lugt 2006 | "80% to 95% of equivalent steel…" (Tablo 4, s.654) | **Yok.** Makale Hollanda köprü/yapı elemanları için bambu, çelik, robinia, azobé, beton yaşam-döngüsü maliyetlerini karşılaştırır; Kolombiya çatı kafesi yoktur. |
| Vogtländer 2010 | "≈0,35 kg CO2e/kg … borax-treated" | **Yok** ("0.35 kg", "borax" geçmiyor). Metin eco-cost (€/kg) birimleriyle çalışıyor. |
| Archila 2018 | "competitive strength-to-cost ratios…" | **Yok.** Makale bambu-donatılı betonu inceler; kafes maliyet kıyası içermez. |
| Correal 2021 (B7: 250–300 mm, 2,5 D) | "injected… 250 mm to 300 mm" | **Yok** (PDF taraması). |
| C6 "Where bow exceeds L/200 … Cbow equals 0.50" | | Manual'de **yok**. |
Rapor bu alıntıları hâlâ "DOĞRULANDI" etiketiyle taşıyor. **Uydurma alıntı; REDDEDİLDİ.**

## 354MemberDome.pdf (gerçek kaynak) ile D bölümü
PDF doğrulanan değerler: 40 m, 8,28 m yükseklik, 127 düğüm, 354 çubuk, 22 grup, ölü 200 N/m², kar 830 N/m², q_h = 1115 N/m², G = 0,85, C_p = 0,0105 / −0,907 / −0,5, GCpi = ±0,18, sehim sınırı 11,1 cm, 37 AISC CHS, AISC-ASD. **Doğru.**
Hatalar: (1) PDF **üç yük durumu** verir (D+S; D+S+W, GCpi = −0,18; D+S+W, +0,18; faktörsüz). Rapordaki "5 ASD kombinasyonu (0,75S+0,75W)" PDF'te yok. (2) PDF'in sayfa 18–21'i bir ABC/BBO/BSO karşılaştırma makalesinden; **künyesi PDF'ten çıkarılamıyor**. "Hasançebi vd. (2009)" ataması doğrulanmadı (bu PDF'in içinde geçmiyor).
**Değerli veri:** çelik 354 kubbe literatür optimumları: BSO **151,116 kN**, BBO 152,75, ABC 155,808 (37 AISC CHS); alüminyum en iyi 60,867 kN.

## Çelik referans modülünün literatürle sınaması (kendi koşum)
Literatür koşulları (A36 Fy = 248 MPa, E = 205 GPa, D+S ve D+S+W± faktörsüz, sehim 11,1 cm) ile benim çelik modülüm 354 kubbede **101,0 kN** buldu (2 tohum, ABC) vs literatür 151–156 kN. Fark ~%33. Olası neden: literatür 37 AISC CHS standart/ağır borulardan seçiyor (kalın et, düşük r/A), benim 24'lük kataloğum ince cidarlı. Katalog tablosu PDF'te yok (sayfa 18–21 alıntısı). Tam katalog olmadan birebir doğrulama yapılamaz. Etkisi: benim çelik referansım **literatürden hafif**, yani bambu karşılaştırmasında **çelik lehine (muhafazakâr)**.

---

# 4. Tur denetimi: PARAMETER_EVIDENCE_R2.md, PRICE_EVIDENCE_IN_CO.md, PRICE_SOURCES_IN_CO.csv (2026-10-12 11:33–11:36)

Yöntem: Papers/ ve Evidence/ içindeki PDF'ler metne çevrildi, her alıntı ve sayı belgede arandı, SHA-256 hesaplandı.

## Doğrulananlar (belgeyle)
| Madde | Sonuç |
|---|---|
| **NSR-10 Título G (gerçek belge, 168 s., SHA-256 `c1007f37…` eşleşiyor)** | λ ≤ 150: G.12.9.2.6, **PDF s.132**: "Bajo ninguna circunstancia es aceptable trabajar con elementos de columna que tengan esbeltez mayor de 150"; G.12.9.2.7.3, s.133: "No se permiten columnas con esbeltez superior a 150". **Yalnızca BASINÇ elemanları (columnas).** Çekme için sınır yok. Önceki "G.12.7.2" atfı yanlıştı (o madde ek yerleri tanımlar). |
| NSR-10 Tabla G.12.7-1 (s.119) | F_b 15, F_t 18, F_c‖ 14, F_p⊥ 1,4, F_v 1,2 MPa (CH = %12); E₀.₅ = 9500, E₀.₀₅ = 7500, E_min = 4000 MPa. R2 değerleri doğru (⊥ hariç). |
| NSR-10 Tabla G.12.7-4 (s.121) | Yük süresi katsayıları: kalıcı 0,90; 10 yıl 1,00; 2 ay 1,15; 10 dk (rüzgâr/deprem) 1,60; darbe 2,00. |
| **NSR-10 Tabla G.12.11-2 (s.138)** | Çift kesmeli cıvata başına **izinli** yük P (lif doğrultusu): #5 (5/8") cıvata, D = 80/100/120/150 mm için **11,54 / 13,25 / 15,86 / 19,80 kN**; Tabla G.12.11-3 (s.139): C_g (Guadua elemanı) 2 cıvata 1,00; 3 cıvata 0,97; **4 cıvata 0,93**. G.12.11.3.13: cıvata aralığı ≥ 150 mm, her cıvata arasında bir boğum, uç mesafe ≥ 150 mm (çekme). |
| Correal Tablo 4 değerleri (F_max 26,6 kN COV %20,5; akma 21,8; rijitlik 3,2; süneklik 3,0) | Doğru (PDF s.10). |
| Manual Denk. 7.5, "nominally ductile m = 1,25" | Manual'de var. |
| 354 kubbe: PDF = kullanıcının kendi makalesi (Aydoğdu, Kilic, Akin, *Structures*, makale taslağı; ASD-AISC 2016 [42], ASCE 7-98 [55]); dome kaynağı **Hasançebi vd. 2009 [10]** | Hasançebi atfı doğru. |

## Reddedilen / doğrulanamayan
| Madde | Bulgu |
|---|---|
| Paraskeva 2019: "çift culm 58,4 kN; üçlü culm 92,1 kN" (s.70–72) | PDF'te **yok**. Makale tek-culm Kao Jue M6 cıvata; "double/triple culm" geçmiyor. Ayrıca R2'de sayfa "201, **63–83**" yazılı; doğrusu **473–483**. **Uydurma, REDDEDİLDİ.** |
| Malkowska 2022: "14,2–22,5 kN, süneklik 2,8–4,2, Tablo 2" | PDF'te bu sayılar **yok**. **REDDEDİLDİ.** |
| ICE (R2 Bölüm 2): çelik 1,77–1,89, profil 1,55/2,45, boru 2,02–2,13, galvaniz +0,25–0,30, harç 0,18–0,186 "DOĞRULANDI" | `Evidence/Circular_Ecology_ICE…pdf` yalnızca portal tanıtım sayfası (6 s., değer yok). Excel **indirilmedi** (R2 de "ERİŞİLEMEDİ" diyor) ama aynı satırlarda "DOĞRULANDI" yazıyor: **çelişki. DOĞRULANAMADI.** |
| Sika TDS (E3): fiyat 2000 COP/kg "s.1–2" | TDS'te fiyat yok. CSV satırı **REDDEDİLDİ**. |
| Guadua katalog (CAT-01: 6400 COP/m, "s.8–10") | Katalog PDF'inde COP/peso/fiyat **yok** (R2 metni de fiyat tablosu yok diyor). CSV'de SHA ile "kaynaklı" gösterilen satır **REDDEDİLDİ**. |
| MERO PDF (düğüm kütlesi 1,8–2,4 kg) | PDF'te kütle verisi yok; **DOĞRULANAMADI**. |
| Manual Denk. A3.3 "K = (6,5n+6)/(3,7n−3)" | Manual metninde bulunamadı (A3.2 mevcut: f_k = f_mean(1 − K·COV)). K formülü **DOĞRULANAMADI**; R2'deki F_k ≈ 14,7 kN bu formüle dayanıyor. |
| CSV Hindistan satırları (98,50; 104,50; 140; 42; 3,50 Rs/kg) | Belge sütunu "ERİŞİLEMEDİ" iken değerler yazılmış: **kaynaksız, REDDEDİLDİ**. |
| CSV Kolombiya çelik 15 000, bağlantı 25 000 COP/kg, kum-çimento 750 COP/kg | Belgeler "ERİŞİLEMEDİ"; **kaynaksız, REDDEDİLDİ**. |
| AISC (E9) ve INBAR (E10) PDF'leri | "Just a moment…" ve "403 Forbidden" sayfalarının çıktısı; **kanıt değil**. |
| `PARAMETER_EVIDENCE_R2` P3 künyesi "CBM 201, 63–83", P5 "IStructE2023" | Yanlış sayfa; P5 adı 2023 diyor (Manual v1.0 Kasım **2025**). |

## Çözüm sağlayan bulgu: bağlantı kapasitesi (C4)
İki gerçek kaynak, iki farklı sonuç:
- **IStructE zinciri** (F_k × C_DF / FS_j): ≈ 3–5 kN / cıvata (F_k formülü doğrulanamadı; n = 8 küçük örnek).
- **NSR-10 Tabla G.12.11-2/3** (resmî, izinli): Ø5/8" cıvata, D = 100 mm → 13,25 kN; D = 120 mm → 15,86 kN. 4 cıvata × C_g 0,93: **49,3 kN (D = 100)** ve **59,0 kN (D = 120)**. Koddaki **F_j,Rd = 53,2 kN** bu aralıkta; yani "4 × Ø5/8" cıvata, NSR-10 izinli yük" olarak **kaynaklı** etiketlenebilir (D = 80 mm için 42,9 kN).
- Kısıt: cıvata aralığı ≥ 150 mm → 4 cıvatalı uç ≈ 600–700 mm; iki uç için ≥ 1,3 m eleman boyu gerekir. ribbed40'ta 1464 elemanın **84'ü (%6) 1,35 m'den kısa (12'si < 1,0 m, en kısa 0,76 m)**; geodesic16 ve kiewitt32'de yok (en kısa 2,09 m).
- NSR-10 slenderlik kuralı yalnızca basınç içindir; koddaki λ ≤ 150 tüm elemana uygulanıyor (muhafazakâr).

---

# 5. Tur: kullanıcının indirdiği belgeler (2026-10-12 12:20–12:40)

| Belge | Sonuç |
|---|---|
| `Evidence/ICE-Educational-V5.0/ICE DB Educational V5.0 - Jun 2026.xlsx` (SHA-256 `4e2cceed6d0ccc6c…`) | **Gerçek ICE (Haziran 2026, Educational V5.0; V3.0 değil).** Sayfa "ICE Summary": **Mortar 1:3 (CEM I) 0,1848** (satır 219), UK ortalama karışım **0,1789** (satır 228) kgCO2e/kg → koddaki 0,18 **doğrulandı**. Çelik (worldsteel 2023, dünya ortalaması, satır 878–897): **welded pipe 2,51** (884), **seamless tube 1,90** (897), section 1,61 (895), plate 2,38 (889), hot-dip galvanized steel 2,62 (888), hot-rolled coil 2,26 (893). Koddaki 2,10 ham boru aralığında (1,90–2,51) ama welded pipe 2,51'in altında. **Bambu culm satırı YOK** (ICE'de bambu geçmiyor). |
| `Evidence/MOSO-Bamboo-products-LCA-TP35.pdf` (INBAR Technical Report 35, 58 s.) | Gerçek rapor; kapsamı **MOSO endüstriyel ürünleri** (flattened, plybamboo, strand woven bamboo; Çin→Rotterdam). **Ham culm için kg CO2e/kg değeri bulunamadı**; EC_bambu = 0,35 için doğrudan kaynak yok. |
| `Evidence/anex-ICOCIV-ago2026.xlsx` (DANE ICOCIV Ağustos 2026) | **Fiyat değil, maliyet endeksi** (varyasyon/seri). Birim fiyat içermiyor; Kolombiya fiyatlarını yıllar arası normalize etmek için kullanılabilir. |
| `Evidence/Resmi_Gazete_32491_Yesil_Cimento_Tebliği.pdf`, Sika TDS, MERO, Guadua katalog | Mevcut, ama fiyat/kütle verisi içermiyor (önceki tur). |

---

# 6. Tur: Filipinler / Endonezya / Hindistan belgeleri ve LCA makaleleri (2026-10-12 12:47–13:17)

## Kullanılamayan belgeler
| Belge | Bulgu |
|---|---|
| `Evidence/26jc0014_pow_abc_geotagged_ded_plan.pdf` (DPWH, 55 s., SHA-256 `c19c9a4b…`) | **Zamboanga del Norte 2nd DEO yol projesi (K1947+150–K1947+350) İş Programı (POW) ve çizimleri**; malzeme **birim fiyat listesi değil**. Bambu kalemi yok, çelik boru/grout fiyatı yok. Kullanılamaz. |
| `Evidence/PERBUP NOMOR 25 TAHUN 2023.pdf` (Konawe Regency, 10 s., taranmış) | Yalnızca yönetmelik metni; **fiyat tabloları (Lampiran I) yok**, "Rp" geçmiyor. Kullanılamaz. |

## Gerçek ve kullanılabilir fiyat belgeleri (görüntü tabanlı; OCR ile okundu: **değerleri sayfada gözle doğrulayın**)
**Jawa Tengah HSD/HSPK, Edisi ke-2, 2024 (Dinas Bina Marga dan Cipta Karya, 406 s., SHA-256 `3f96d479…`)** — bölge grubu: Kab. Cilacap, Banyumas, Purbalingga, Banjarnegara (Harga Satuan Dasar bahan; PDF sayfa 379–386):
| Kalem (no) | PDF sayfa | Değer (Rp, 4 bölge sırasıyla) | Birim |
|---|---|---|---|
| Baja Profil (29) | 379 | 18.000 / 16.053 / 20.300 / 18.000 | kg (malzeme) |
| Baja tulangan polos / sirip (37/38) | 379 | 13.000–13.450 | kg |
| Semen Grout (125) | 382 | 7.173 / 8.380 / 9.705 / 8.911 | kg |
| Bambu Ø6–8 / 600 cm (214) | 386 | 21.540 / 22.409 / 22.000 / 21.712 | batang (6 m) ≈ 3.600 Rp/m |
Not: bambu **küçük çaplı (Ø6–8 cm)**, yapısal Guadua çapı değil. "Pipa baja" kalemleri su borusu (Ø63–250 mm), yapısal CHS değil.

**CPWD Delhi Schedule of Rates 2023, Vol. I (408 s., SHA-256 `386627ba…`)** — OCR (PDF sayfaları):
| Kalem | PDF s. | Değer |
|---|---|---|
| 10.16.1 Steel work in built-up **tubular trusses**, hot finished welded tubes (kesme, kaldırma, montaj, astar, kaynak dahil) | 354 | **Rs 194,40/kg** |
| 10.16.2 seamless tubes / 10.16.3 ERW | 354 | 206,35 / 194,40 Rs/kg |
| 10.1 / 10.2 yapısal çelik (tek kesit / built-up) | 350 | 117,35 / 133,70 Rs/kg |
| 10.20 cıvata+somun+rondela, tamamı | 354 | 159,35 Rs/kg |
| Temel fiyat 1007 Yapısal çelik (tee, köşebent, U, I) | 40 | 5.965 Rs/quintal = **59,65 Rs/kg** (malzeme) |
| Temel fiyat 1251 M-60 non-shrink grout | 46 | **28,00 Rs/kg** |
| Bambu (yapısal) | — | **YOK** (yalnızca "Bamboo 25 mm dia 2.5 m" perde çubuğu, s.28) |
Önceki CSV'deki "10.16 = 104,50 Rs/kg", "10.11 = 140", "5.48 grout = 42" değerleri **hatalıydı** (gerçek: 194,40 / 159,35 (10.20) / 28,00).

## Göstergesel oranlar (kur belgesi YOK, yaklaşık)
- grout / çelik malzeme: Jateng ≈ 0,46 (8.380/18.000); CPWD ≈ 0,47 (28/59,65): **iki ülkede tutarlı**.
- CPWD: yerine konulmuş tüp kafes (194,40) / çelik malzeme (59,65) ≈ **3,3×**; yani montaj dahil/hariç çelik fiyatı arasında ~3 kat fark var. Bambu için yalnızca malzeme fiyatı bulunduğundan **kapsam uyumu** gereklidir.

## LCA makaleleri
- **Zea Escamilla vd. 2018 (Sustainability 10:3096, PDF s.10, Tablo 2):** Kolombiya tek katlı bambu çerçeveli ev: **CO₂e payı: bambu direk %6,4, çelik %34,7, nakliye %49,0, beton %7,9.** "Bağlantı çeliği ve nakliye baskın, bambu culm küçük pay" iddiasını doğrudan destekliyor (m² bazında, farklı fonksiyonel birim). Ham culm kg/kg değeri yok; Vogtländer'den atıfla culm için **5,69 kg CO₂ biyojenik depolama/kg** geçiyor.
- **Restrepo vd. 2016 (JCP 126:563–571):** bambu **levha** üretimi (net −117 kg CO₂e/levha, atık yakıt kredisi); culm kg/kg yok. EC_bambu için kullanılamaz.

---

# 7. Kur belgeleri, oranla tamamlama ve EC_bambu (2026-10-12)

**Kur belgeleri (resmî, `Evidence/FX/`; SHA-256 dosyalarla):**
- `TCMB_kurlar_20260803.xml` (TCMB günlük kur bülteni 2026/142): USD/TRY alış 47,4497, satış 47,5352 (orta 47,4925). ÇŞB Ağustos 2026 ile aynı tarih.
- `WorldBank_PA.NUS.FCRF_IND_IDN_TUR_COL_2019-2026.json` (World Bank/IMF-IFS "Official exchange rate, LCU per USD, period average"; son güncelleme 2026-10-08): Hindistan 2023 **82,599**; Endonezya 2024 **15 855,4**; Türkiye 2024 32,806; 2025 39,455; Kolombiya 2024 4074,4.
- `ECB_eurofxref-hist.zip` (çapraz kontrol için).
Önceki "35 TL/USD" varsayımı yanlıştı; gerçek 47,49 → ÇŞB 106,70 TL/kg = **2,25 USD/kg**.

**Filipinler çıkarıldı** (üç ülke yeterli: Türkiye, Hindistan, Endonezya). Kolombiya fiyatı yok; yalnızca bağlamsal.

**Oranla tamamlama** (`price_scenarios.py`, `tables/T9*`): P_bambu(D) = P_bambu(70 mm) × (D/70)^α, α = 2 (temel: çeperle orantılı kesit alanı) ve 3 (kullanıcı Tablo 1). Endonezya bambu/çelik-malzeme oranı r_b = 0,202 Hindistan ve Türkiye'ye uygulandı; grout/çelik oranı 0,47 (Endonezya ve Hindistan'da tutarlı) Türkiye'ye; Türkiye çelik malzeme fiyatı = erected/3,26 (Hindistan oranı).

---

# 8. Tur: bambu fiyat kaynakları (kullanıcı bağlantıları, 2026-10-12 akşam)

| Kaynak | Bulgu |
|---|---|
| `guaduabambucolombia.co/2026/06/27/guadua-inmunizada-por-inmersion-precios-2026/` (gerçek sayfa, 27.06.2026) | "PRECIOS 2026: Metro lineal **$7.500 COP**; Unidad de 6 metros **$38.500 COP**" (borax emprenyeli, ICONTEC 5301, duvar kalınlığı ≥ %15 D, min. 50 adet). **Çap belirtilmemiş.** Bu sayı önceki turlarda tarafımdan "uydurma" sayılmıştı; yanlıştı: sayılar gerçek, yalnızca atıf "Fedebambu 2024" değil bu 2026 sayfasıdır. 6 m birim = 6.417 COP/m ≈ 1,58 USD/m (2025 ort. kuru 4.053); metro lineal 1,85 USD/m (koddaki Tablo 1'in D = 120 mm değeri ile aynı). |
| `birimfiyat.net/4900.58` (OGM rayici, AMP Yazılım) | Gerçek poz ama **Bambu 300 cm, Ø20–22 mm**: 6,57 TL/adet (2025) = 2,19 TL/m. Yapısal çap değil, kullanılamaz. |
| Yapıştırılan tablo (70–130 mm, 375/450/750/1200 ₺) | **Kaynağı yok** (poz/URL/sayfa verilmemiş); doğrulanamadı. İçindeki hesap: ilk iki satır (aynı boy 300 cm) α = ln(450/375)/ln(95/75) = 0,77 (aritmetik doğru); dört noktanın **adet fiyatı** regresyonu 2,16 (boy farkını içerir); **metre başına** fiyat regresyonu ≈ 1,5. "α_toplam = 2,16" metre fiyatı için geçerli değildir. Kaynak verilirse kullanılabilir. |
| `ecatalog.sinarmasland.com` (Şubat 2025, emlak blogu; ikincil kaynak) | Endonezya perakende fiyat listesi, **Betung 100–120 mm, 1 m: Rp 30.000; 6 m: Rp 75.000–175.000**; Ater/Ampel 70–80 mm 1 m Rp 7.000; Andong 80–90 mm 1 m Rp 16.000; Apus/Wulung 50–60 mm Rp 5.500–6.000. Metre fiyatı noktalarına (55, 75, 85, 110 mm) log-log eğim ≈ **2,5** (karışık türler, perakende). |
| `Evidence/construction_materials_price_data_cmpd.pdf` (DPWH Bölge III, 2. çeyrek 2025) | Taranmış 9 sayfalık **özet** (memo + malzeme grupları: kalıp, beton, elektrik); **bambu, yapısal çelik ve grout satırı yok**. Kullanılamaz. |
| `16th_NOCMAT_2015_submission_66.pdf` | **Evidence/Papers klasörlerinde yok** (yüklenmemiş). |

**Sonuç (malzeme düzeyi maliyet, T9):** bambu/çelik maliyet oranı α ∈ [1,5; 3] ve 4 fiyat senaryosunda: geodesic16 **0,61–0,87**, kiewitt32 **0,87–1,39**, ribbed40 **0,98–1,34**; yani malzeme düzeyinde bambu ile çelik maliyeti kabaca eşit, bambu avantajı yalnızca küçük kubbede.
