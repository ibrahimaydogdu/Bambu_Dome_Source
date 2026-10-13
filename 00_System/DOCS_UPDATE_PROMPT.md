# DOCS GÜNCELLEME PROMPT'U (diğer yapay zekâ için) — Revizyon 2 (2026-10-12)

Aşağıdaki değerler kodda, kampanya çıktılarında ve kullanıcı kararlarında kesinleşti. Proje belgelerindeki eski ifadeleri bunlarla tutarlı hale getir.

**KORUMALI ALAN (kesin yasak):** Kodlar korumaya alındı. Aşağıdakilere yazma, onları silme, yeniden adlandırma veya yeniden üretme:
- `03_Code_Execution/` altındaki `.py`, `.bat` dosyaları ve test dosyaları (DEVELOPER_PROMPT.md ve CAMPAIGN_EXECUTION_PLAN.md dışında hiçbir dosya),
- `04_Results/tables/`, `04_Results/figures/`, `04_Results/campaign_final/`, `*.csv`, `*.json`, `*.npz`,
- `C:\BambuDome_campaign\` altındaki her şey,
- `Papers/`, `Evidence/`, `MEMORY.md`, `AGENTS.md`.

Hiçbir betiği çalıştırma, yeni betik yazma, yeni sayı/tablo/şekil üretme. **Sentetik, örnek, "temsili", tahmini veya yer tutucu sayı kesinlikle yasak.** Bir belgede gereken sayı bu prompt'ta yoksa uydurma; "[DOĞRULANACAK]" yaz ve çıktı listende belirt. Kod veya veri değişikliği gerektiğini düşünüyorsan yapma, yalnızca öneri olarak yaz. Bütün değişiklikler `git diff` ile denetlenecek: korumalı alanda tek satırlık bir değişiklik bile olursa bütün çıktın reddedilir.

**Kurallar:**
- **Yalnızca belgeleri (.md) düzelt.**
- Bu prompt'ta olmayan hiçbir sayı, atıf veya "kanıtlandı" ifadesi ekleme. Emin olmadığın yerde "varsayım" ya da "[DOĞRULANACAK]" yaz (AGENTS.md §5).
- Her sayının yanına kaynağını yaz: kod dosyası, `04_Results` dosyası/tablosu veya Manual/NSR-10 tablo/denklem numarası. Kaynak sütunu bu prompt'ta verilmiştir.
- Toplu "%100 doğrulandı / eksiksiz / tam uyumlu" ifadesi yasak (AGENTS.md §5.4).
- **Kullanıcı onayı yazma.** Hiçbir belgede "Kullanıcı Onayı: Onaylandı" ifadesini kullanıcının sohbette verdiği açık bir onaya dayanmadan yazma (AGENTS.md kural 4).
- Kendi ürettiğin özet, HTML veya PDF'i kanıt olarak gösterme (AGENTS.md §5.1).

---

## 0. Durum özeti (belgelerde "planlanan" diye geçen şeyler artık yapıldı)

| Konu | Doğru ifade | Kaynak |
|---|---|---|
| Kampanya | 3 kubbe × 3 algoritma (ABC, ACO, DO) × 30 tohum (1001–1030) = 270 iş, **270/270 uygun** (P = 0). 2026-10-09 19:53–23:15 (3 sa 21 dk), 7 işçi. | `C:\BambuDome_campaign\full\campaign.log`, `04_Results/tables/T1` |
| Çelik referans | 120 koşu (AISC 37 boru), tamamlandı | `04_Results/campaign_final/steel_reference_aisc37_summary.csv` |
| Tuning | Algoritma seçimi yapıldı: **ABC (pop 20), ACO (pop 40), DO (pop 40)** | `04_Results/TUNING_STUDY.md`, `campaign config.json` `pop_map` |
| İstatistik | Friedman + Mann-Whitney U (Holm) hesaplandı | `04_Results/STATISTICAL_TEST_RESULTS.md` |
| LCA ve duyarlılık | Gerçek optimumlarla hesaplandı | `04_Results/LCA_SENSITIVITY_REPORT.md`, T5–T8 |
| Maliyet | Malzeme düzeyinde, 4 ülke senaryosu × α | `04_Results/tables/T9`, `T9a`, `price_scenarios.py` |
| Aktif iş | Belge senkronizasyonu (bu prompt), ardından Critic denetimi, ardından makale taslağı (`05_Drafts/`) | `MEMORY.md` §7–8 |

"[TUNING SONUCUNA GÖRE]" yer tutucusunu ABC, ACO, DO ile değiştir. **İstisna AGENTS.md:** bu dosyayı kendin değiştirme; önerilen metni çıktı listende ver, kullanıcı onaylarsa uygulanır.

---

## 1. Mekanik model: ISO 22156 / IStructE Manual 2025 ASD

Kaynak: IStructE, *Manual for the design of bamboo structures to ISO 22156:2021*, v1.0, 2025 (`Papers/IStructE2023_Manual_Bamboo_ISO22156.pdf`, `Evidence/IStructE_Manual_...pdf`). Kodda: `03_Code_Execution/bamboo_catalog.py` `MATERIAL_PROPERTIES`.

| Konu | ESKİ (belgelerde geçen, sil) | YENİ (kodda) |
|---|---|---|
| Tasarım yaklaşımı | LRFD, k_mod = 0,70, γ_M = 1,30 | **ASD**: X_izin = X_k · C_R · C_DF · C_T / FS (Manual Denk. 3.9, 6.5). Yük faktörü ve malzeme kısmi katsayısı yok. |
| Katsayılar | — | Servis Sınıfı 2: C_DF = 0,55 (kalıcı) / 0,65 (geçici) / 0,85 (anlık); FS = 2; **C_R = 0,90 (tekil culm, varsayım; Manual ≥4 paralel culm için 1,1)**; C_T = 1,0. k = C_R·C_DF·C_T/FS = 0,2475 / 0,2925 / 0,3825. |
| Yük kombinasyonları | 1,4D; 1,2D+1,6S+0,8W | ASCE 7-22 §2.4.1 ASD, faktörsüz **8 kombinasyon**: D; D+S; D+0,6W±; D+0,75S+0,45W±; 0,6D+0,6W± (rüzgâr iki yönlü). Süre sınıfı: D kalıcı, D+S geçici, rüzgârlılar anlık. |
| Basınç (Ylinen) | β_c = 0,10 ("ISO 22156 Madde 7"), E_05 = 8500 MPa | **c = 0,8** (Manual Denk. 6.1, Ek A6.2); P_e,k = π²·E_k·I·C_bow/(KL)²; C_bow = 1 − b₀/0,02, **b₀ = 0,01 (varsayım) → C_bow = 0,5**; K = 1,0. "β_c = 0,10 ISO 22156'dan" ifadesini her yerden kaldır. |
| E | E_mean = 11 000, E_05 = 8500 MPa | **E_k = 10 000 MPa** (Manual Tablo 4.4). FEM ve Ylinen aynı E_k'yi kullanır. |
| f_t,0,k | 45 MPa | **40 MPa** (Manual Tablo 4.4 şema; Guadua'ya özel çekme verisi yok) |
| f_c,0,k | 38 MPa | **37,8 MPa** (Manual Tablo A3.4, Guadua, n = 922) |
| Yoğunluk | — | 700 kg/m³ (Manual Tablo 4.4; Guadua ort. 680, Tablo A3.9) |
| Narinlik | λ ≤ 150 "ISO 22156'dan" | λ ≤ 150, **çekme ve basınç dahil tüm elemanlara uygulanır**. NSR-10 G.12.9.2.6/7 (PDF s.132–133) bu sınırı yalnızca basınç için ister; bizim uygulamamız bilinçli olarak muhafazakâr (`04_Results/PAPER_METHODS_NOTES.md`). |
| Sehim | span/360, "ASCE 7 sehim" | **span/150** (Manual örneği; ISO 22156 sehim sınırı vermez). Kubbe açıklığına göre 40 / 32 / 16 m için 266,7 / 213,3 / 106,7 mm. |
| **Bağlantı kapasitesi** | 120 kN (kaynaksız) **ve** 2 × 26,6 = 53,2 kN (n_bolt = 2, Correal vd. 2021 deney maksimumu) | **F_j,Rd = n_bolt · F_bolt,adm · C_g = 4 × 13,25 × 0,93 = 49,3 kN.** F_bolt,adm: NSR-10 Tabla G.12.11-2 (PDF s.138), Ø5/8" (#5) cıvata, çift kesme, lif doğrultusu, D = 100 mm, **izinli yük**. C_g: Tabla G.12.11-3 (s.139), 4 cıvata. n_bolt = 4 kullanıcı kararıdır. Correal 2021 artık F_j için kaynak değildir; yalnızca bağlantı davranışı için anılabilir. |

**Bağlantıyla ilgili doğrulanmış sonuçlar (yaz):**
- 270 optimum tasarımın tamamı bağlantı sınırını sağlar. En yüksek bağlantı D/C 0,807 (ribbed40, en büyük eksenel kuvvet 39,8 kN) (`T4`, `global_best_ribbed40.json`).
- IStructE Manual zinciriyle cıvata başına ~3–5 kN çıkıyor ve K formülü doğrulanamadı. NSR-10 değeriyle arasındaki fark makalede tartışılacak: [DOĞRULANACAK], sayı verme.
- Sınırlama: ribbed40'ta 1464 elemandan **12'si (%0,82, hepsi L = 0,76 m)** gereken cıvata sayısını NSR-10 aralık kuralına göre barındıramaz (`T10`, `joint_bolt_check.py`). En büyük kuvvet bu elemanlarda 31,25 kN. geodesic16 ve kiewitt32'de bu sorun yok.

---

## 2. Kubbe modelleri (eski düğüm sayıları yanlıştı)

Kaynak: `campaign.log` ön kontrol satırları, `dome_types.py`.

| Model | Düğüm | Çubuk | Tasarım grubu | L_max | Not |
|---|---|---|---|---|---|
| ribbed40 (freq = 2) | **505** | 1464 | 43 | 3,08 m | L 0,76–3,08 m. "321 düğüm" yanlış, sil. |
| kiewitt32 | **169** | 456 | 22 | 3,55 m | "161 düğüm" yanlış, sil. |
| geodesic16 | 46 | 115 | 23 | 2,96 m | |

- Orijinal 354 elemanlı topoloji 2,9–5,97 m çubuk içerir ve bambu için uygun değildir. "4,2–4,8 m" / "1,8–2,4 m" ifadeleri yanlıştı.
- ribbed40: *topoloji freq = 2 yoğunlaştırmasıdır; yükler ve geometri Saka 1991 benchmark'ından uyarlanmıştır, birebir aynı model değildir.*
- Referans 354 kubbe yükleri (`Papers/Dome354Member_Optimization.pdf`, kullanıcının taslağı; kubbe kaynağı Hasançebi vd. 2009): ölü 200 N/m², kar 830 N/m², q_h 1115 N/m², G 0,85, C_p 0,0105 / −0,907 / −0,5, GCpi ±0,18.
- Katalog: 24 Guadua kesiti, D 80–160 mm, t 6–22 mm (`bamboo_catalog.py` RAW_CATALOG_DATA, Tablo 2; kesit 24 = D 160 / t 22 mm). "t 8–18 mm" yanlıştı.

---

## 3. Optimizasyon ve kampanya

- Formülasyon: min f_pen = W_bambu·(1+P)^ε, ε = 2; P = Σ_gruplar max_{i∈g} max(DC_i − 1, 0) + max(u_max/u_izin − 1, 0); DC_i = max(çekme, Ylinen basınç, λ/150, |N|/F_j,Rd).
- Bütçe: NFE = 1000 × tasarım değişkeni (ribbed40 43 000, kiewitt32 22 000, geodesic16 23 000), her algoritmaya eşit. "pop = 40, gen = 100 (NFE ≈ 4040)" ifadesini sil.
- Tuning: tohum 2001–2005 (nihai tohumlardan ayrı), pop 20/40/80 (`TUNING_STUDY.md`, `TUNING_STUDY_runs.csv`, makalede Ek'e gidecek). Eski LRFD parametreli tuning (`TUNING_STUDY_oldparams_LRFD.md`) geçersizdir, atıf yapma.
- Eski pilot (16 algoritma, 4040 NFE, eski parametreler) sonuçlarını belgelerden çıkar.
- Kayıt: checkpoint (RNG dahil; kesilip devam eden koşu bit düzeyinde aynı sonucu verir, test edildi) ve değerlendirme başına `.npz`.

**Sonuçlar (T1, `STATISTICAL_TEST_RESULTS.md`):**

| Kubbe | En iyi [kN] | Bulan | ABC medyan / ort. / std [kN] | Friedman χ²_F (p) | Ortalama sıralar ABC / ACO / DO |
|---|---|---|---|---|---|
| geodesic16 | **5,800** | ABC (s1001) | 5,894 / 5,880 / 0,051 | 48,60 (2,8·10⁻¹¹) | 1,10 / 2,00 / 2,90 |
| kiewitt32 | **41,058** | ABC (s1001); ACO da aynı değere ulaştı | 41,058 / 41,058 / 0,000 (30/30 aynı çözüm) | 38,26 (4,9·10⁻⁹) | 1,23 / 2,03 / 2,73 |
| ribbed40 | **66,352** | ABC (s1001); ACO da aynı değere ulaştı | 66,365 / 66,452 / 0,194 | 49,16 (2,1·10⁻¹¹) | 1,25 / 1,75 / 3,00 |

- Mann-Whitney U (iki yönlü, Holm): ABC her kubbede ACO ve DO'dan anlamlı derecede iyi. **p_Holm ≤ 5,53·10⁻⁴**, A12 = 0,758–1,000. "p < 0,001" ifadesi ribbed40 ABC–ACO için yanlıştır (p_Holm = 5,53·10⁻⁴); "p ≤ 6·10⁻⁴" yaz. "Wilcoxon signed-rank" ifadesini sil.
- Sınırlayıcı durumlar (T4, F4): basınç (Ylinen) grupların çoğunu belirler; narinlik ~%5–19; çekme D/C ≤ 0,43; u/u_izin ≤ 0,14.
- SAP2000 doğrulaması (en iyi 3 tasarım, `global_best_*.json`): eksenel kuvvet ve deplasman bağıl farkı ≤ 1,3·10⁻¹³. max D/C (FEM = SAP) 0,9959 / 0,9923 / 0,99995, P = 0.

---

## 4. Kütle–karbon ilişkisi

- **"R² ≈ 0,99" ve "∇EC ∥ ∇W analitik ispatı" ifadelerini kaldır.** Doğru ifade: sabit düğüm modelinde f₂, f₁'in tam doğrusal fonksiyonudur (corr = 1,000, `test_fast_eval.py`). Kesite bağlı bağlantı modelinde, kampanyada ziyaret edilen uygun tasarımlarda r = 0,72–0,90 (R² = 0,52–0,80; `04_Results/WEIGHT_CARBON_TRADEOFF.md`); en hafif tasarımın karbonu bulunan en düşüğün %1,6–6,7 üstündedir. Eski "R² = 0,81–0,97" aralığı üretilemedi. "Cephe çöker" veya "ödünleşim yok" yazma; ölçülen değerleri yaz.

---

## 5. Gömülü karbon (A1–A3, biyojenik karbon hariç)

| Parametre | ESKİ (sil) | YENİ | Kaynak / durum |
|---|---|---|---|
| EC_bambu | 0,35 | **0,30 kg CO₂e/kg** (aralık 0,09–1,23) | Türetilmiş: üretim 0,092 + 300 km nakliye 0,21. Alt sınır **varsayım**, kaynağı yok (`04_Results/EC_BAMBOO_METHOD.md`) |
| EC_çelik (bağlantı) | 2,10 | **2,38** ("Steel, Plate") | ICE Educational V5.0, Haziran 2026 (`Evidence/ICE-Educational-V5.0`) |
| EC_çelik boru (çelik referans) | — | **2,51** ("Steel, welded pipe") | ICE V5.0 |
| EC_harç | 0,18 | 0,18 | ICE V5.0 harç 1:3. Rötresiz grout için ICE'de satır yok, bu yüzden **proxy varsayım** |
| Bağlantı modeli | — | m_hub = 2,0 kg/düğüm; uç başına 0,5 kg; harç ρ = 2100 kg/m³ (non-shrink grout); L_inj = 2,5·D | `fast_eval.py` `CarbonModel` — **varsayım** |

"ICE v3.0'dan alındı" ifadelerini ICE V5.0 ile değiştir. Künye: Circular Ecology, *ICE Database Educational V5.0*, Haziran 2026 (`Evidence/ICE-Educational-V5.0/ICE DB Educational V5.0 - Jun 2026.xlsx`). Yazar adları "Please Read First" PDF'inde geçmiyor → yazar sırası [DOĞRULANACAK].

**Sonuçlar (`LCA_SENSITIVITY_REPORT.md`):**
- Temel senaryo: bağlantı bileşenleri (çelik + harç) toplam gömülü karbonun **%74,1–82,1**'i. Yalnızca çelik %39,0–57,3.
- Birleşik elverişsiz uç (L_inj = 1,5D, EC_çelik = 1,2, EC_bambu = 0,47, EC_harç = 0,12 birlikte): bağlantı payı ribbed40 %57,7, geodesic16 %53,9, **kiewitt32 %45,3**. Paradoks iddiası parametreye duyarlıdır. Bunu "paradoks her koşulda geçerli" diye yazma.
- Eski "%67–75" ve "%43–52" sayılarını sil (eski pilot/eski parametreler).
- Literatür desteği: Zea Escamilla vd. 2018 (Tablo 2). Kolombiya bambu çerçeveli evde CO₂e payları bambu direk %6,4, çelik %34,7, nakliye %49.

**Uyarı (yeni):** Kampanya koşulurken `config.json` karbon ayarı eski değerlerle kaydedildi (ec_bamboo 0,35, ec_steel 2,10). Bu yüzden şu alanlardaki karbon değerleri **eski EC ile hesaplanmıştır, atıf yapma**: `results/*.json` `best_embodied_carbon_kgCO2e`, `global_best_*.json` `carbon`, `STATISTICAL_TEST_RESULTS.md` `Carbon_Mean` sütunu ve `campaign.log` ön kontroldeki corr(W, ECO2e). Ağırlık sonuçları etkilenmez, çünkü amaç fonksiyonu yalnızca ağırlıktır. Geçerli karbon sayıları yalnızca `LCA_SENSITIVITY_REPORT.md` ve T5–T8'dedir. `LCA_SENSITIVITY_REPORT.md` 24. satırdaki "EC değerleri doğrulanmamış varsayımdır" ifadesini düzelt: EC_çelik ve EC_harç ICE V5.0'dan, EC_bambu türetilmiş, harç proxy.

---

## 6. Çelik referans (T5–T8)

- 37 AISC borusu, A36, ASD-89, aynı 8 ASD kombinasyonu, L/150 (`steel_reference.py`, `aisc_pipes.py`).
- Üye ağırlığı [kN]: 354 kubbe 129,0; ribbed40 104,7; kiewitt32 60,7; geodesic16 11,4 (T5).
- Literatür kontrolü: faktörsüz D+S+W±, 11,1 cm koşullarında bizim model 135–136 kN, literatür 151,1–155,8 kN. Çelik referansımız ~%10 hafif, yani bambu lehine değil, muhafazakâr (`PAPER_METHODS_NOTES.md` satır 29).
- Aynı geometride bambu/çelik oranları (T6): üye ağırlığı 0,51 / 0,68 / 0,63 (geodesic16 / kiewitt32 / ribbed40); CO₂e 0,25 / 0,28 / 0,35.
- **Üye ağırlığı ≠ sistem ağırlığı.** Bağlantı çeliği ve harç dahil edildiğinde bambu sistemi daha ağırdır (ribbed40: 277,2 kN bambu sistemi vs 129,0 kN çelik sistem; T5). Belgelerde "bambu kubbe çelikten hafif" ifadesi varsa bu ayrımı ekle.

---

## 7. Maliyet (yalnız MALZEME düzeyi; işçilik ve LCC kapsam dışı)

- Belgeler: Jawa Tengah HSD 2024; CPWD DSR 2023 Vol. 1 (çelik 59,65 Rs/kg, M-60 non-shrink grout 28 Rs/kg); ÇŞB Ağustos 2026 (yalnız montajlı çelik); Kolombiya Guadua 2026 (6 m = 38.500 COP, **çap belirtilmemiş, D_ref = 120 mm varsayım**). Kurlar: TCMB 03.08.2026 USD/TRY 47,4925; World Bank/IMF INR 2023 82,599, IDR 2024 15.855, COP 2025 4.053.
- Çap ölçekleme (D/D_ref)^α, α ∈ {1,5; 2; 2,5; 3}, temel 2.
- Sonuç (T9), bambu/çelik malzeme maliyeti oranı: geodesic16 0,61–0,87; kiewitt32 0,87–1,39; ribbed40 0,98–1,34. Yani kiewitt32 ve ribbed40'ta kabaca eşit. Harç, bambu malzeme maliyetinin %41,6–73,4'ü.
- **Üç ülke senaryosu bağımsız değildir** (bambu fiyatı Endonezya oranından türetildi). Makalede tek senaryo + α duyarlılığı olarak sunulacak. "Çok ülkeli bağımsız doğrulama" gibi yazma.
- Eski fiyat formülü 0,65·(D/0,08)^2,2 ve "Tablo 1 USD/m" fiyatlarını sil.
- **Maliyet yalnızca T9/T9a'da sunulur (kullanıcı kararı, 2026-10-13).** `F5_material_cost.png` kaldırıldı. T5, T6, T7 ve T8'den maliyet sütunları ve satırları çıkarıldı, çünkü eski Tablo 1 fiyatlarına dayanıyorlardı. Belgelerde "F5 maliyet şekli", "T5/T6 maliyet oranı" veya 0,58 / 0,81 / 0,75 gibi bambu/çelik maliyet oranları geçiyorsa sil ve T9'a yönlendir.

## 7a. Şekiller (2026-10-13 sürümü)

- Şekil seti: F1 (en iyi kesit profilleri), F2 (yakınsama), F3 (kutu grafikleri), F4 (belirleyici sınır durumları), F5 ağırlık ve F5 CO₂e (iki şekil). F5 maliyet şekli yok.
- Şekillerde kubbe adları **Geodesic, Kiewitt, Ribbed** biçimindedir. 354 elemanlı çelik kubbe **"Reference steel"** olarak geçer. Metinde de aynı adları kullan, numarayı ilk geçtiği yerde tanımla, örneğin "Geodesic dome (geodesic16; 23 design groups)".
- F1 açıklaması: *"Lightest feasible design among 90 runs per dome (3 algorithms × 30 seeds), obtained by ABC; ACO reached the same weight for Kiewitt and Ribbed."* "ABC en iyi olduğu için referans alındı" gibi yazma: şekil algoritmadan bağımsız olarak en hafif tasarımı gösterir.
- F3 sembolleri: noktalar tek tek koşular, turuncu çizgi medyan, yeşil üçgen ortalama, içi boş daire aykırı değer (>1,5 IQR).
- F5 açıklamasında "Reference steel = 354 elemanlı çelik ribbed kubbe (Hasançebi vd. 2009 geometrisi)" tanımını ver.

---

## 8. Atıflar (künyeler Papers PDF'leriyle teyit edildi)

- Trujillo, Harries, Kaminski, Lopez (2025), *Manual for the design of bamboo structures to ISO 22156:2021*, IStructE, v1.0, ISBN 978-1-906335-97-7 / 978-1-906335-82-3 (pdf). **"Trujillo 2021" atfını kaldır.**
- NSR-10 Título G (Colombia), Tabla G.12.11-2, G.12.11-3, G.12.9.2.6/7 (`Papers/NSR-10_Titulo_G.pdf`).
- Correal, Prada, Suárez, Moreno (2021), *CBM* 305: 124597, DOI 10.1016/j.conbuildmat.2021.124597. Artık F_j için kaynak değil.
- Paraskeva vd. (2019), *CBM* 201: 473–483, DOI 10.1016/j.conbuildmat.2018.12.198 (Kao Jue, M6). "Paraskeva 2017, CBM 153" atfını **tamamen kaldır**.
- Zea Escamilla & Habert (2014), *J. Clean. Prod.* 69: 117–127, DOI 10.1016/j.jclepro.2014.01.067.
- Zea Escamilla vd. (2018) (`Papers/2018 Zea et al....pdf`), Tablo 2.
- ICE Database Educational V5.0 (Haziran 2026), Circular Ecology (yazar sırası [DOĞRULANACAK]).
- NSGA-II'ye atıf gerekirse yalnızca Deb vd. 2002, IEEE TEVC 6(2): 182–197. MOABC atfını kaldır.
- ISO 22156:2021 madde numaralarını standart metninden teyit etmeden yazma; Manual denklem/tablo numaralarını tercih et.
- **Evidence uyarısı:** `Evidence/` içindeki şu beş dosya tarayıcıdan basılmış web sayfasıdır (Chrome/Skia PDF): `AISC_360_Steel_Standards_Official_Portal.pdf`, `Circular_Ecology_ICE_Database_v3_Official.pdf`, `Guadua_Bambu_Colombia_Official_Web_Catalogue.pdf`, `INBAR_Publications_LCA_Official_Portal.pdf`, `MERO_TSK_Space_Structures_Official.pdf`. Bunları "resmî belge" veya "standart" diye gösterme. Yalnızca "web sayfası, URL + erişim tarihi" olarak an. Guadua fiyatı için kaynak: guaduabambucolombia.co, 27.06.2026 sayfası. "Fedebambu 2024" atfı yanlıştı, sil.

---

## 9. Belgelerden silinecek yanlış eski iddialar (tam liste)

LRFD / k_mod / γ_M; β_c = 0,10; E_05 = 8500; f_t = 45 MPa; F_j = 120 kN; **F_j = 53,2 kN, n_bolt = 2, F_bolt,max = 26,6 kN**; **EC_bambu = 0,35, EC_çelik = 2,10**; ICE v3.0; span/360; "R² ≈ 0,99"; "∇EC∥∇W"; 321 / 161 düğüm; eski optimum ağırlıklar ("~4 / ~28 / ~58 kN" ve tüm-24 kesit ağırlıkları 20,9 / 84,5 / 190 kN'u "optimum" diye gösteren yerler); Paraskeva 2017 CBM 153; Trujillo 2021; Zea & Habert 2014'ün eski başlığı ve "2017"; 35 TL/USD; Hindistan 10.16 = 104,50 Rs/kg (doğrusu 194,40); "Fedebambu 2024"; "1,5 saat" kampanya süresi; "Wilcoxon signed-rank"; "[TUNING SONUCUNA GÖRE]".

---

## 10. Dosya iş listesi

Eski ifade taramasında eşleşme bulunan belgeler (eşleşme sayısına göre). Hepsini kontrol et:

`06_Review_Audit/agent_02_reviewer.md`, `03_Code_Execution/CAMPAIGN_EXECUTION_PLAN.md`, `01_Literature/RESEARCH_GAP_AND_NOVELTY.md`, `00_System/system_architecture.md`, `06_Review_Audit/CRITIC_PROMPT.md`, `04_Results/agent_04_results.md`, `04_Results/RESULTS_AGENT_PROMPT.md`, `02_Methods/agent_03_methodology.md`, `02_Methods/TIER1_BASELINE_METHODS.md`, `02_Methods/MATHEMATICAL_FORMULATION.md`, `00_System/PIPELINE_AND_ROLES.md`, `README.md`, `06_Review_Audit/REVIEW_LOG/Review_Round_02_Methods.md`, `06_Review_Audit/AUDIT_CHECKLIST.md`, `05_Drafts/agent_06_writer.md`, `03_Code_Execution/DEVELOPER_PROMPT.md`, `02_Methods/TIER2_PROPOSED_METHODOLOGY.md`, `02_Methods/METHOD_AGENT_PROMPT.md`, `01_Literature/agent_01_intro_literature.md`, `01_Literature/LITERATURE_MATRIX.md`, `01_Literature/INTRODUCTION_SECTION_DRAFT.md`, `00_System/SYSTEM_RULES.md`, `00_System/PARAMETER_RESEARCH_PROMPT.md`, `00_System/PARAMETER_RESEARCH_PROMPT_2.md`, `00_System/MASTER_AGENT.md`, `05_Drafts/agent_05_discussion.md`, `04_Results/LCA_SENSITIVITY_REPORT.md` (yalnız 24. satır açıklaması), `00_System/PROJECT_STATE.md`.

Dokunma: `MEMORY.md` (kullanıcının hafıza dosyası), `04_Results/PARAMETER_EVIDENCE*.md` ve `REVIEW_LOG` dosyalarındaki geçmiş tur kayıtları (tarihsel kayıttır; yalnızca başına "geçersiz değerler §9'a bakın" notu ekleyebilirsin), `TUNING_STUDY_oldparams_LRFD.md`, `Evidence/OCRBambu.md`, tüm kod ve tablolar.

**`00_System/PROJECT_STATE.md` özel talimatı (baştan yeniden yaz):**
- Aşama tablosu: 0–2 Tamamlandı. 3 (kod + kampanya) ve 4 (sonuçlar, istatistik, LCA, maliyet) **iş olarak tamamlandı, Kullanıcı Onayı sütunu: "Bekleniyor"**. 5 (belge senkronizasyonu + taslak) Aktif. 6 Beklemede. Kullanıcı onayı yalnızca kullanıcı sohbette açıkça onaylarsa "Onaylandı" olur.
- Tur günlüğüne "Round 9 — Belge senkronizasyonu (DOCS_UPDATE_PROMPT Rev. 2)" ekle ve her değişikliği bir madde olarak yaz.
- Yapılacaklar: Critic denetimi; makale taslağı (Methods → Results → Discussion); kullanıcıdan istenen veriler (Kolombiya Guadua 6 m fiyatının çapı, Türkiye bambu tablosunun kaynağı, `16th_NOCMAT_2015_submission_66.pdf`); ham kampanya kayıtlarının arşivi (~146 MB, Zenodo/Release); makalede yazılacak sınırlamalar (işçilik/LCC yok, λ_max'ın çekmeye de uygulanması, EC_bambu alt sınırı varsayım, bambu fiyatı ve çap üssü belirsiz, ribbed40'ta 12 kısa eleman, C_R ve b₀ varsayım, grout EC proxy, üye vs sistem ağırlığı).

**AGENTS.md (değiştirme, öner):** Kural 2'deki "[TUNING SONUCUNA GÖRE]" yerine "ABC, ACO (bilinen) + DO (görece yeni)" yazılması. Method Architect satırındaki "ASD sınır durum tahkiklerini formüle eder" ifadesi aynı kalabilir. Önerini çıktı listende ayrı başlıkla ver.

---

## 11. Çıktı biçimi

Bitirince şunları ver:
1. Değiştirdiğin her dosya için eski → yeni ifade listesi (dosya:satır).
2. "[DOĞRULANACAK]" olarak bıraktığın her yer.
3. AGENTS.md için önerdiğin metin.
4. Bu prompt'la çelişen bir şey bulduysan ayrı bir başlık altında yaz. Kendin çözme.

Sonraki aşamaya geçme. Critic denetimi ve kullanıcı onayı bekleniyor (AGENTS.md kural 4).
