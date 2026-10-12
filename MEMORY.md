# 🧠 MEMORY.md: BambuDome Proje Hafızası ve Karar Defteri (taşınabilir; başka PC'de devam için)

**Proje:** 40 m açıklıklı yapısal bambu (*Guadua angustifolia*) uzay kafes kubbelerin tek amaçlı optimizasyonu ve "dekarbonizasyon paradoksu".
**Son güncelleme:** 2026-10-13 | **Aşama:** kampanya TAMAMLANDI, sonuç tabloları/şekilleri üretildi; makale yazımı ve belge senkronizasyonu bekliyor.
**Depo:** `github.com/ibrahimaydogdu/Bambu_Dome_Source` (dal `main`). Commit `4f9eb84`: tüm kod + `04_Results` + notlar. PDF/XLSX kaynaklar, `.sdb`, ham kampanya kayıtları depoda YOK (bkz. §8).

---

## 1. Bilimsel model (kesinleşmiş kararlar)
- Tek amaçlı: min f_pen = W_bambu·(1+P)^ε, ε = 2; P = Σ_gruplar max_{i∈g} max(DC_i−1,0) + max(u_max/u_izin−1,0). DC = max(çekme, Ylinen basınç, λ/150, bağlantı |N|/F_j,Rd). Çok amaçlı (NSGA-II/MOABC/MODBO) yasak: kütle–karbon yakın-doğrusal (R² 0,81–0,97), "∇EC∥∇W ispatı" iddiası YOK.
- **ISO 22156 / IStructE Manual 2025 ASD:** X_izin = X_k·C_R·C_DF·C_T/FS (Denk. 3.9, 6.5). FS = 2; C_R = 0,90 (varsayım); C_DF (SC2) = 0,55 / 0,65 / 0,85; E_k = 10 GPa; f_t,0,k = 40 MPa (Tablo 4.4); f_c,0,k = 37,8 MPa (Tablo A3.4); ρ = 700; Ylinen c = 0,8; b₀ = 0,01 (varsayım, C_bow = 0,5); K = 1; sehim L/150.
- **λ_max = 150**: tüm elemanlara uygulanır; NSR-10 G.12.9.2.6/7 (PDF s.132–133) yalnızca BASINÇ için ister → muhafazakâr (makalede belirtilecek, cümle PAPER_METHODS_NOTES.md'de).
- **Bağlantı:** F_j,Rd = 4 cıvata × 13,25 kN × 0,93 = **49,3 kN** (NSR-10 Tabla G.12.11-2/3, Ø5/8", D = 100 mm). 270 tasarımın tamamı uygun (en yüksek bağlantı D/C 0,81, ribbed40). IStructE zinciri cıvata başına ~3–5 kN verir (K formülü doğrulanamadı); fark makalede tartışılacak. Sınırlama: ribbed40'ta 12 eleman (%0,8, hepsi 0,76 m) gereken 3 cıvatayı NSR-10 aralık kuralına göre barındıramaz (gereken boy ≈ 1,05 m); `joint_bolt_check.py`, T10.
- **Yükler:** ASCE 7-22 ASD faktörsüz 8 kombinasyon (D; D+S; D+0,6W±; D+0,75S+0,45W±; 0,6D+0,6W±); süre sınıfı D permanent, D+S transient, rüzgârlılar instantaneous. Referans 354 kubbe yükleri (354MemberDome.pdf = kullanıcının *Structures* taslağı, kubbe kaynağı Hasançebi vd. 2009): ölü 200 N/m², kar 830, q_h 1115, G 0,85, C_p 0,0105/−0,907/−0,5, GCpi ±0,18.
- **Kubbeler:** ribbed40 (freq 2: 505 düğüm, 1464 çubuk, 43 grup, L 0,76–3,08 m), kiewitt32 (169, 456, 22), geodesic16 (46, 115, 23). Orijinal 354 elemanlı topoloji bambu için uygun değil (çubuk 5,97 m).
- **Katalog:** 24 Guadua kesiti (D 80–160 mm, t/D 0,06–0,16; Tablo 2).
- **Kapsam:** yalnızca A1–A3 gömülü karbon + MALZEME maliyeti. LCC ve işçilik yok (sınırlama, gelecek çalışma). Biyojenik karbon hariç.

## 2. Kampanya (bitti, 2026-10-09/10)
- Algoritmalar (tuning'e göre): **ABC (pop 20), ACO (pop 40), DO (pop 40)**; NFE = 1000 × değişken (ribbed40 43 000, kiewitt32 22 000, geodesic16 23 000); 30 tohum (1001–1030); 270 iş, 3 sa 20 dk, **hepsi uygun**. Tuning: tohum 2001–2005, 6–8 aday, pop 20/40/80 (TUNING_STUDY.md, TUNING_STUDY_runs.csv → Ek).
- En iyi ağırlık [kN]: geodesic16 **5,800**, kiewitt32 **41,058**, ribbed40 **66,352** (hepsi ABC, tohum 1001). ABC > ACO > DO; Mann-Whitney U Holm p ≤ 6e-4, A12 0,76–1,0 (STATISTICAL_TEST_RESULTS.md). kiewitt32'de ABC 30/30 aynı çözüm.
- Sınırlayıcılar (T4, F4): basınç grupların %80–95'ini belirler; narinlik ~%5–19; çekme D/C ≤ 0,43; sehim oranı ≤ 0,14.
- SAP2000 doğrulaması (en iyi 3 tasarım): fark ≤ 1e-13; max D/C 0,9959 / 0,9923 / 0,99995, P = 0.
- Kesinti-devam (RNG dahil bit-özdeş, test edildi) + değerlendirme başına .npz.

## 3. Çelik referans (T5–T8)
37 AISC borusu (SteelPipeSec), A36, ASD-89, aynı 8 ASD kombinasyonu, L/150. 354 kubbe 129,0 kN; ribbed40 104,7; kiewitt32 60,7; geodesic16 11,4. Literatür kontrolü (faktörsüz D+S+W±, 11,1 cm): bizim 135–136 kN vs literatür 151,1 (BSO)/152,8/155,8 → çelik referansımız ~%10 hafif (bambu için muhafazakâr). Aynı geometride bambu/çelik: ağırlık 0,51 / 0,68 / 0,63; CO₂e ≈ 0,25–0,35; malzeme maliyeti 0,61–1,39 (yalnız T9; aşağıya bakın). **Üye ağırlığı ≠ sistem ağırlığı**: bağlantı çeliği + harç dahil bambu sistemi daha ağır (ribbed40: 277 vs 129 kN).

## 4. Gömülü karbon (kg CO₂e/kg)
ICE Educational V5.0 (Haz 2026, `Evidence/ICE-Educational-V5.0`): çelik boru **2,51** (welded pipe), bağlantı çeliği **2,38** (plate), harç **0,18** (1:3; rötresiz grout için ICE satırı yok → proxy varsayım). **EC_bambu = 0,30** türetilmiş (üretim 0,092 + 300 km nakliye 0,21; aralık 0,09–1,23), alt sınır VARSAYIM (kaynak yok) → `EC_BAMBOO_METHOD.md`. Sonuç: ribbed40'ta bağlantı payı (çelik+harç) ≈ %82; en elverişsiz uçta %45–58 (kiewitt32 %50 altı) → paradoks parametreye duyarlı. Zea Escamilla vd. 2018 (Tablo 2): Kolombiya bambu çerçeveli evde CO₂e: bambu direk %6,4, çelik %34,7, nakliye %49.

## 5. Maliyet (malzeme düzeyi; `price_scenarios.py`, T9)
Belgeler: Jawa Tengah HSD 2024 (baja profil 18.000 Rp/kg, grout ~8.500 Rp/kg, bambu Ø6–8 cm ~3.650 Rp/m), CPWD DSR 2023 (çelik malzeme 59,65 Rs/kg, M-60 non-shrink grout 28 Rs/kg), ÇŞB Ağustos 2026 (yalnız montajlı çelik), Kolombiya Guadua 2026 (6 m = 38.500 COP; çap belirtilmemiş, D_ref = 120 mm varsayımı). Kurlar: TCMB 03.08.2026 USD/TRY 47,4925; World Bank/IMF: INR 2023 82,599, IDR 2024 15.855, COP 2025 4.053. Bambu çap ölçekleme (D/D_ref)^α, α ∈ {1,5–3}, temel 2. Harç = non-shrink grout (planda böyle). Sonuç: bambu/çelik malzeme maliyeti geodesic16 0,61–0,87, kiewitt32 0,87–1,39, ribbed40 0,98–1,34 (≈ eşit). Üç ülke senaryosu BAĞIMSIZ DEĞİL (bambu fiyatı Endonezya oranından türetildi) → makalede tek senaryo + α duyarlılığı olarak sunulacak. Harç, bambu maliyetinin %41–70'i.

## 6. Anti-hallucination dersleri (AGENTS.md §5)
- Diğer yapay zekâ defalarca uydurma künye/alıntı üretti ve kendi hazırladığı "arşiv PDF"lerini kanıt saydı; hepsi reddedildi (`04_Results/PARAMETER_EVIDENCE_REVIEW.md` §1–8). Yalnızca orijinal belge + sayfa + birebir alıntı kabul.
- Yanlış çıkan eski iddialar (belgelerden silinmeli): LRFD/k_mod/γ_M, β_c = 0,10, E_05 = 8500, f_t = 45, F_j = 120 kN, span/360, "R² ≈ 0,99", "∇EC∥∇W", Paraskeva 2017 CBM 153 başlığı/künyesi, Trujillo 2021, Zea&Habert 2014 başlığı/cilt (doğrusu JCP 69:117–127), 35 TL/USD, Hindistan 10.16 = 104,50 Rs/kg (doğrusu 194,40).
- Düzeltme: "7.500 COP/m, 38.500 COP/6 m" sayıları GERÇEK (guaduabambucolombia.co 27.06.2026 sayfası); yanlış olan eski "Fedebambu 2024" atfıydı.

## 7. Bekleyen işler
1. **Belge senkronizasyonu:** `00_System/DOCS_UPDATE_PROMPT.md` diğer yapay zekâya uygulatılıp README, PROJECT_STATE, CAMPAIGN_EXECUTION_PLAN, 02_Methods, 04/05/06 belgeleri güncel parametrelerle tutarlı hale getirilmeli (AGENTS.md zaten güncel). Bu prompt hâlâ ESKİ F_j (53,2/n=2) ve EC (0,35, 2,10) değerlerini içerir; önce prompt'ta F_j = 49,3 (n = 4, NSR-10), EC değerleri (ICE V5.0, EC_bambu 0,30), malzeme düzeyi maliyet ve sonuçlar güncellenmeli.
2. **Kolombiya Guadua 6 m fiyatının çapı** (üreticiden), yapıştırılan Türkiye bambu tablosunun (70–130 mm, 375/450/750/1200 ₺) kaynağı (poz/URL), `16th_NOCMAT_2015_submission_66.pdf` (klasörlerde yok, yüklenecek).
3. Ham kampanya kayıtlarının (`C:\BambuDome_campaign\full\results`, ~135 MB .npz) arşivlenmesi (Zenodo/Release).
4. Makalede açık yazılacak sınırlamalar: işçilik/LCC yok; λ_max basınç için; EC_bambu alt sınırı varsayım; bambu fiyatı ve çap-üssü belirsiz; ribbed40'ta 12 kısa eleman bağlantı detayı; C_R, b₀ varsayım; rötresiz grout EC proxy; üye vs sistem ağırlığı.
5. Referans örnek (354 kubbe, yükler, çelik tasarım) ve tuning tabloları → **Ek (Appendix)**.

## 8. BİR SONRAKİ ADIM (başka PC'de)
1. Depoyu klonla; `Papers/` ve `Evidence/` PDF-XLSX dosyalarını elle kopyala; `C:\BambuDome_campaign\{full,steel_ref_aisc37,tuning}` sonuç klasörlerini aynı yola koy (ya da `results_report.py --campaign ... --steel ...` ile göster). Paketler: numpy scipy pandas matplotlib openpyxl pymupdf (SAP2000 için comtypes + SAP2000). Testler: `python test_fast_eval.py`, `python test_units.py`.
2. `00_System/DOCS_UPDATE_PROMPT.md`'yi (yukarıdaki F_j/EC/maliyet düzeltmeleriyle) güncelleyip diğer yapay zekâya uygulat; ardından Critic denetimi (AGENTS.md kural 4: kullanıcı onayı olmadan aşama geçilmez).
3. Makale taslağı: Methods (PAPER_METHODS_NOTES.md, EC_BAMBOO_METHOD.md) → Results (T1–T10, F1–F5) → Discussion (dekarbonizasyon paradoksu, sınırlamalar). Şekil/tablo kodu: `03_Code_Execution/results_report.py`, `price_scenarios.py`, `joint_bolt_check.py`, `statistical_analysis.py`, `lca_sensitivity_analysis.py`.

## 8a. 2026-10-13 kararları (bu PC)
- Yeni PC kurulumu tamam: 270 koşu, steel_ref_aisc37 ve tuning kopyalandı; testler geçti; `results_report.py` tabloları bu PC'de aynen üretiyor (fark ≤ 3e-14).
- `DOCS_UPDATE_PROMPT.md` Rev. 2 yazıldı (F_j 49,3, ICE V5.0, korumalı alan kuralları). PROJECT_STATE.md belge senkronizasyonunda baştan yazılacak; Aşama 3–4 kullanıcı onayı "Bekleniyor".
- Kampanya `config.json` karbon ayarı eski EC (0,35/2,10) ile kaydedildi → `results/*.json` karbon alanları, `global_best_*.json` `carbon` ve `STATISTICAL_TEST_RESULTS.md` `Carbon_Mean` atıf yapılmaz; geçerli karbon LCA raporu ve T5–T8. Ağırlıklar etkilenmez.
- Şekiller makale biçimine getirildi (16 cm, Times New Roman 11 pt, otomatik yazı çakışma kontrolü, siyah-beyaz desenler; adlar Geodesic/Kiewitt/Ribbed/Reference steel). **Maliyet yalnızca T9/T9a'da**: F5 maliyet şekli ve T5–T8 maliyet sütunları kaldırıldı (eski Tablo 1 fiyatlarına dayanıyordu).

- Belge senkronizasyonu diğer yapay zekâya uygulatıldı, korumalı alana dokunmadı; çıktısı satır satır denetlendi ve 22 belgede 57 düzeltme yapıldı (DO = **Dandelion Optimizer**, Zhao vd. 2022 — "Dragonfly" yanlış; Correal 26,6 kN F_j kaynağı değil; 2,51 yalnız çelik referans; b₀/C_R varsayım; paradoks koşullu: en elverişsiz uç %45,3–57,7). En büyük kesit (24 = D160/t22) kontrolü güncel kodla: D/C 0,807, 20,9 / 84,5 / 190,3 kN. Katalog t = 6–22 mm. Kullanılmayan `culm_cost_per_meter` (kaynaksız Tablo 1 formülü) silindi.

## 9. Dosya haritası
`04_Results/`: tables/T1–T10, figures/F1–F5, STATISTICAL_TEST_RESULTS.md, LCA_SENSITIVITY_REPORT.md, EC_BAMBOO_METHOD.md, PAPER_METHODS_NOTES.md, PARAMETER_EVIDENCE_REVIEW.md (denetim günlüğü), campaign_final/ (özet CSV, en iyi tasarımlar, çelik referans). `03_Code_Execution/`: fem_bridge.py, truss_model.py, dome_types.py, fast_eval.py, metaheuristic_optimizers.py, run_full_campaign.py, steel_reference.py, aisc_pipes.py, tuning_study.py, sap_export.py, bamboo_catalog.py (tüm malzeme parametreleri).
