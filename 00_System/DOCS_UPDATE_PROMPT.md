# DOCS GÜNCELLEME PROMPT'U (diğer yapay zekâ için)

Aşağıdaki değişiklikler kodda ve kullanıcı kararlarında kesinleşti. Proje belgelerindeki (README.md, AGENTS.md, 00_System, 01_Literature, 02_Methods, 03_Code_Execution/CAMPAIGN_EXECUTION_PLAN.md, 04_Results, 05_Drafts, 06_Review_Audit, PROJECT_STATE.md) eski ifadeleri bunlarla tutarlı hale getir. **Kodu değiştirme; yalnızca belgeleri düzelt.** Doğrulanmamış hiçbir sayı, atıf veya "kanıtlandı" ifadesi ekleme. Emin olmadığın yerde "varsayım" ya da "[DOĞRULANACAK]" yaz. Her düzeltmeyi PROJECT_STATE.md tur günlüğüne bir madde olarak kaydet.

## 1. Mekanik model: LRFD → ASD (ISO 22156 / IStructE Manual 2025)
Kaynak: IStructE, *Manual for the design of bamboo structures to ISO 22156:2021*, v1.0, Kasım 2025 (Papers klasöründe PDF).

| Konu | ESKİ (belgelerde geçen) | YENİ (kodda) |
|---|---|---|
| Tasarım yaklaşımı | LRFD, k_mod = 0,70, γ_M = 1,30 | **ASD**: X_izin = X_k · C_R · C_DF · C_T / FS (Manual Denk. 3.9, 6.5). ISO 22156 izinli gerilme esaslıdır; yük faktörü ve malzeme kısmi katsayısı yoktur. |
| Katsayılar | — | Servis Sınıfı 2: C_DF = 0,55 (kalıcı), 0,65 (geçici), 0,85 (anlık); FS = 2 (boyuna); C_R = 0,90 (tekil culm, muhafazakâr varsayım; Manual 1,1 diyor ≥4 paralel culm için); C_T = 1,0. Kapasite çarpanı k = C_R·C_DF·C_T/FS = 0,2475 / 0,2925 / 0,3825. |
| Yük kombinasyonları | 1,4D; 1,2D+1,6S+0,8W | ASCE 7-22 §2.4.1 ASD, faktörsüz: D; D+S; D+0,6W; D+0,75S+0,45W; 0,6D+0,6W (rüzgâr N ve P için). Süre sınıfı: D kalıcı, D+S geçici, rüzgârlı olanlar anlık. |
| Basınç (Ylinen) | β_c = 0,10 ("ISO 22156 Madde 7"), E_05 = 8500 MPa | **c = 0,8** (Manual Denk. 6.1, Ek. A6.2); P_e,k = π²·E_k·I·C_bow/(KL)²; C_bow = 1 − b₀/0,02, **b₀ = 0,01 (varsayım)**; K = 1,0 (kafes elemanı); allowable N_cr = N_cr,k·C_R·C_DF·C_T/FS. "β_c = 0,10 ISO 22156'dan" ifadesini her yerden kaldır (yanlıştı). |
| Elastisite modülü | E_mean = 11 000 MPa, E_05 = 8500 MPa | **E_k = 10 000 MPa** (Manual Tablo 4.4 şema alt sınırı, tüm D/t için geçerli). FEM rijitliği ve Ylinen P_e aynı E_k'yi kullanır. E_05 kavramı kullanılmıyor. |
| f_t,0,k | 45 MPa | **40 MPa** (Manual Tablo 4.4 şema). Not: Guadua için çekme karakteristik değeri Manual'da yok; 45 MPa aslında Guadua eğilme f_m,k idi. |
| f_c,0,k | 38 MPa | 37,8 MPa (Manual Tablo A3.4, Guadua, n = 922). |
| Yoğunluk | 700 kg/m³ | 700 kg/m³ (Manual Tablo 4.4 şema; Guadua ort. 680, Tablo A3.9). |
| Narinlik | λ ≤ 150 "ISO 22156'dan" | λ ≤ 150 **kaynağı doğrulanamadı, varsayım**. |
| Yer değiştirme sınırı | span/360 ("ASCE 7 sehim" vb.) | **span/150** (Manual örneği; ISO 22156 sehim sınırı vermez). 40 m için 267 mm. L/360 ve "ASCE 7 sehim" ifadelerini kaldır. SLS için ayrıca L/250 duyarlılık senaryosu önerilebilir (henüz koşulmadı). |
| Bağlantı kapasitesi | F_j,Rd = 120 kN (kaynaksız) | F_j,Rd = n_bolt · F_bolt,max = 2 × 26,6 = **53,2 kN**. F_bolt,max: Correal vd. 2021 (CBM 305), Tablo 4, Ø15,9 mm cıvata, tek bağlantı üst sınır **deney maksimum yükü** (tasarım değeri değil). **n_bolt = 2 (çapraz cıvata) varsayımdır, kaynağı yoktur.** Gerekçe: n_bolt = 1'de ribbed40'ta 1464 elemanın 231'i, kiewitt32'de 8'i, kesitten bağımsız olarak sınırı aşar (en büyük servis kuvveti 39,8 kN). Bu durumu "kısıtlayıcı varsayım ve duyarlılık konusu" olarak yaz. |

Doğrulanmış sonuç: tüm elemanlar en büyük kesitteyken (24) üç kubbe de uygun (en kötü D/C = 0,75); ağırlıklar geodesic16 20,9 kN, kiewitt32 84,5 kN, ribbed40 190 kN. Eski optimum ağırlıkları ("~4 kN", "~28 kN", "~58 kN" vb.) geçersizdir; belgelerde varsa sil.

## 2. Optimizasyon tasarımı (kullanıcı kararları)
- **Bütçe:** NFE = **1000 × tasarım değişkeni sayısı**, her algoritma için eşit: ribbed40 43 000 (43 grup), kiewitt32 22 000 (22 grup), geodesic16 23 000 (23 grup). Eski "pop = 40, gen = 100 (NFE ≈ 4040)" ifadelerini kaldır.
- **Algoritma sayısı: 16 → 3.** Kullanıcı kararı: 2 bilinen iyi + 1 görece yeni yöntem. Seçim `04_Results/TUNING_STUDY.md` duyarlılık çalışmasından gelecek (aday: ABC, ACO, DO, GWO, WOA, TLBO; tohum 2001–2005, nihai tohumlardan ayrı). **Seçim ve pop değerleri çalışma bitince kullanıcıdan/koddan alınacak; şimdilik "[TUNING SONUCUNA GÖRE]" yaz.** AGENTS.md kural 2 ("16 algoritma") ve ilgili tüm belgeler bu karara göre güncellenmeli (AGENTS.md'yi kullanıcı onayıyla değiştir; Master Agent bunu kullanıcıya sorsun).
- Eski pilot (16 algoritma, 4040 NFE) yakınsamamıştı (ribbed40'ta 3/16 koşu uygunsuz) ve eski parametrelerle koşulmuştu: sonuçlarını belgelerden çıkar.
- **İstatistik:** Wilcoxon **rank-sum (Mann-Whitney U)**, iki yönlü, **Holm düzeltmeli**, etki büyüklüğü A12; Friedman sıra testi (tohum bloklu) ayrıca. 30 bağımsız tohum (1001–1030). "Wilcoxon signed-rank" ifadelerini kaldır.
- **Kayıt ve devam:** her iş için checkpoint (RNG durumu dahil, kesilip devam eden koşu kesintisizle bit düzeyinde aynı sonucu verir; test edildi) ve **değerlendirme başına .npz** (gen, ağırlık, karbon, ceza). Analizler yeniden koşu gerektirmeden bu dosyalardan yapılır.
- Süre: ribbed40 işi 7 paralel işçide ~16 dk ölçüldü. Tam kampanya (3 algoritma × 3 kubbe × 30 tohum = 270 iş) tahmini ≈ 3,5–4 saat duvar saati (7 işçi). "1,5 saat" gibi eski tahminleri sil.

## 3. Tek amaçlı formülasyon (değişmedi, ama şunları düzelt)
- min f_pen = W_bambu·(1+P)^ε, ε = 2; P = Σ_gruplar max_{i∈g} max(DC_i − 1, 0) + max(u_max/u_izin − 1, 0). DC_i = max(çekme, Ylinen basınç, λ/150, bağlantı |N|/F_j,Rd).
- **"R² ≈ 0,99" ve "∇EC ∥ ∇W analitik ispatı" ifadelerini kaldır.** Ölçülen: sabit düğüm modelinde f₂ = 35,68·f₁ + sabit (tam doğrusal); kesite bağlı bağlantı karbon modelinde uygun örneklerde R² = 0,81–0,97 (corr 0,91–0,98), yani **yakın-doğrusal, ispatlanmış kolinearite değil**. Gerekçe: "ampirik olarak yakın-doğrusal; çok amaçlı Pareto cephesi tek noktaya/çok dar bir aralığa çöküyor" şeklinde yaz. Maliyet–karbon ikilisi (Tablo 1/2 fiyatlarıyla) de dejenere çıktı.
- Çubuk boyları: orijinal 354-elemanlı model 2,9–5,97 m çubuk içerir ve bambu için uygun değil; freq = 2 modelde 0,76–3,08 m. "4,2–4,8 m" / "1,8–2,4 m" ifadeleri yanlıştı. "1464 elemanlı model Saka 1991 40 m benchmark'ından türetilmiştir" ifadesi: *topoloji freq = 2 yoğunlaştırmasıdır; yükler ve geometri benchmark'tan uyarlanmıştır, birebir aynı model değildir* diye düzelt.
- Fiyat formülü: plan metnindeki 0,65·(D/0,08)^2,2 ile Tablo 1 (0,65/1,10/1,85/3,15/5,20 USD/m; D = 80…160 mm) çelişiyor (Tablo 1'e uyan üs ≈ 3,0). Tek bir ifade bırak.

## 4. Gömülü karbon (LCA) değerleri: hepsi doğrulanmamış varsayım
EC_bambu = 0,35, EC_çelik = 2,10, EC_harç = 0,18 kg CO₂e/kg; düğüm çeliği m_hub = 2 kg, uç başına 0,5 kg, harç ρ = 2100 kg/m³, L_inj = 2,5 D. Papers klasöründeki hiçbir PDF çelik/harç EC'sini vermiyor; Zea Escamilla & Habert 2014 bambu direği için kg/kg değil **mPt/m³** (IMPACT 2002+) veriyor (ρ = 100 kg/m³ alınmış, biyojenik karbon sayılmamış). Bu yüzden:
- "ICE v3.0 / Zea Escamilla'dan alındı" ifadelerini "varsayım; ICE v3.0 xlsx satırı ve ZE&H Tablo 8 ile teyit edilecek" yap.
- LCA duyarlılık raporu (`04_Results/LCA_SENSITIVITY_REPORT.md`) artık gerçek kampanya optimumlarından üretilir; **ön-yazılı sonuç cümleleri yok**. Eski pilotla üretilmiş "%67–75 bağlantı karbonu / %50–65 manşet bulgu" sayıları kaldırılmalı: en elverişsiz parametre kombinasyonunda bağlantı payı %43–52'ye düşüyor (kiewitt32'de %50 altı), yani "Dekarbonizasyon Paradoksu" iddiası parametrelere duyarlı. Manşet bulgu nihai kampanya sonrası hesaplanan sayıya göre yazılacak; **şimdi sayı verme**.
- `statistical_analysis.py` artık sentetik veri üretmez (eski `STATISTICAL_TEST_RESULTS.md` silindi; sahte veriyle üretilmişti). Gerçek kampanya bitene kadar belgelerde istatistik sonucu yok.

## 5. Atıflar (künyeler Papers PDF'leriyle teyit edildi)
- Paraskeva, Pradhan, Stoura, Dimitrakopoulos (2019), "Monotonic loading testing and characterization of new multi-full-culm bamboo to steel connections", *Constr. Build. Mater.* 201: 473–483, DOI 10.1016/j.conbuildmat.2018.12.198. **Kao Jue (Bambusa pervariabilis), M6 cıvata; Guadua ve F_j,Rd = 120 kN için kaynak DEĞİL.** Önceki başlık yanlıştı. "Paraskeva 2017, CBM 153, mortar-filled…" atfını **tamamen kaldır** (bulunamadı).
- Zea Escamilla & Habert (2014), "Environmental impacts of bamboo-based construction materials representing global production diversity", *J. Clean. Prod.* 69: 117–127, DOI 10.1016/j.jclepro.2014.01.067. Önceki başlık yanlıştı; "2014, 2017" içindeki 2017 doğrulanamadı → kaldır.
- Trujillo, Harries, Kaminski, Lopez (2025), *Manual for the design of bamboo structures to ISO 22156:2021*, IStructE, v1.0, ISBN 978-1-906335-97-7 (basılı) / 978-1-906335-82-3 (pdf). **"Trujillo 2021" doğrulanamadı → kaldır**; gerekirse Trujillo & Malkowska (2018), *CBM* 163: 9–20, DOI 10.1016/j.conbuildmat.2017.12.065 veya Bahtiar vd. (2021), *Eng. Struct.* 228: 111548.
- Correal, Prada, Suárez, Moreno (2021), "Bearing capacity of bolted-mortar infill connections in bamboo and yield model formulation", *CBM* 305: 124597, DOI 10.1016/j.conbuildmat.2021.124597 (Guadua; F_bolt,max için).
- Malkowska, Norman, Trujillo (2022), *CBM* 342: 127971 (Moso, çivi bağlantısı; Binder3.pdf) — doğrudan bir parametreyi desteklemez, ancak ISO sünekliği koşulları için anılabilir.
- Jones & Hammond (2019), *ICE Database V3.0*, Circular Ecology (sıra "Hammond & Jones" ile tutarsızdı; tek biçim seç).
- ISO 22156:2021: madde numaralarını (özellikle "Madde 7", "Madde 9") standart metninden teyit edilmeden yazma; Manual'daki denklem numaralarını (3.9, 6.1–6.5, Tablo 4.4, A3.4) tercih et.
- MOABC/NSGA-II/MODBO için atıf verilecekse yalnızca gerçek kaynak (NSGA-II: Deb vd. 2002, IEEE TEVC 6(2): 182–197); MOABC atfı doğrulanmamıştı, kaldır.

## 6. Genel kural
- Her belgede "kanıtlandı / eksiksiz / tam uyumlu" gibi ifadeleri, yalnızca kodda test edilmişse ve test adı belirtilebiliyorsa bırak.
- Sayı verirken kaynağı belirt: kod dosyası/satırı, Manual tablo/denklem numarası ya da `04_Results` dosyası.
- Bitirdiğinde, değiştirdiğin her dosyanın ve her ifadenin kısa bir listesini ver; kullanıcı onayı olmadan sonraki aşamaya geçme (AGENTS.md kural 4).
