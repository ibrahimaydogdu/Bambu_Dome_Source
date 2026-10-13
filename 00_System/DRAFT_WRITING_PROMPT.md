# AŞAMA 5 — MAKALE TASLAĞI YAZIM PROMPT'U (diğer yapay zekâ için) — 2026-10-13

> **NOT (2026-10-13):** Bu prompt'la üretilen ilk taslak bağımsız denetimde geçersiz bulundu (uydurma yükler, kombinasyonlar, formüller, senaryolar ve kaynakça başlıkları; gizli yer işaretleri; yanlış kaynak satır numaraları). Taslak Master Agent tarafından yeniden yazıldı (`05_Drafts/manuscript/`). Bu prompt yeniden kullanılacaksa: (1) olgu tablosu §3 düzeltildi ancak yük değerleri, kombinasyonlar, formüller ve yöntem ayrıntıları yazar tarafından kodla (`truss_model.py`, `fast_eval.py`, `bamboo_catalog.py`) tek tek karşılaştırılmalı; (2) yer işaretleri görünür metin olmalı, HTML yorumunda saklanmamalı; (3) kaynak satır numarası yerine dosya ve tablo adı verilmeli; (4) ICE Educational V5.0 araştırma kullanımını dışlıyor, EC kaynağı karara bağlanmadan karbon sayıları nihai sayılmaz.

Görev: BambuDome çalışmasının İngilizce Q1 makale taslağını (IMRAD) yazmak. Aşama 3–4 sonuçları kullanıcı tarafından onaylandı; bütün sayılar `04_Results/` içinde hazır. **Senin işin yeni sonuç üretmek değil, var olan sonuçları doğru ve sade biçimde yazıya dökmek.** Taslak bittikten sonra Master Agent (Claude) her cümleyi ve her sayıyı kaynağıyla karşılaştıracak.

Başlık (çalışma başlığı): *Sizing Optimization of Guadua Bamboo Space Domes and the Share of Connection Steel and Grout in Embodied Carbon*. Hedef dergi henüz seçilmedi; genel Elsevier biçimini kullan.

---

## 1. KESİN KURALLAR

1. **Yalnızca şu klasöre yaz:** `05_Drafts/manuscript/`. Başka hiçbir dosyayı değiştirme, silme veya yeniden adlandırma. Kod, tablo, şekil, CSV/JSON/NPZ, `C:\BambuDome_campaign\`, `Papers/`, `Evidence/`, `MEMORY.md`, `AGENTS.md`, `00_System/` korumalıdır. Betik çalıştırma, yeni betik yazma.
2. **Sıfır uydurma:** Her sayı, `04_Results/` dosyalarında veya §3'teki olgu tablosunda birebir bulunmalı. Bulunmuyorsa yazma; `[DATA NEEDED: ...]` koy. Yuvarlarken en az kaynaktaki anlamlı basamağı koru (5.800 → 5.80 kN uygundur; 66.352 → 66 kN uygun değildir).
3. **Sıfır uydurma atıf:** Yalnızca §4'teki kaynaklara atıf yap. Başka bir kaynağa ihtiyaç varsa `[REF NEEDED: konu]` yaz; künye, DOI, sayfa, yıl uydurma. Bir kaynağa belirli bir bulgu atfediyorsan o bulgu PDF'te olmalı; emin değilsen `[REF CHECK]` ekle.
4. **Her sayının kaynağını işaretle:** Sayının hemen ardından HTML yorumu koy: `5.80 kN<!-- T1 -->`, `74.1–82.1%<!-- LCA_SENSITIVITY_REPORT.md:24 -->`. Ayrıca `05_Drafts/manuscript/NUMBERS_TRACE.md` dosyasında her sayıyı `dosya | cümle | değer | kaynak dosya:satır/tablo` olarak listele.
5. **Abartı yok:** "proves", "demonstrates conclusively", "for the first time", "novel framework", "paradigm" gibi iddialar yasak. Sonuçlar bu üç kubbe, bu katalog ve bu varsayımlar için geçerlidir; öyle yaz.
6. **Paradoks koşulludur:** Bağlantı karbon payı temel senaryoda %74.1–82.1, birleşik elverişsiz uçta %45.3–57.7'dir (kiewitt32'de %50 altı). "Connections always dominate" yazma.
7. **Kullanma:** kampanya JSON'larındaki `best_embodied_carbon_kgCO2e`, `global_best_*.json` `carbon`, `STATISTICAL_TEST_RESULTS.md` `Carbon_Mean` sütunu (eski EC ile kaydedildi). Karbon sayıları yalnız `LCA_SENSITIVITY_REPORT.md` ve T5–T8'den.
8. **Maliyet yalnız T9/T9a'dan.** T5–T8'de maliyet yok; eski "Tablo 1 USD/m" fiyatlarını kullanma. Üç ülke senaryosu bağımsız değildir (bambu fiyatı Endonezya oranından türetildi); tek senaryo + α duyarlılığı olarak sun.
9. **Anti-AI dil filtresi (AGENTS.md kural 3):** Yasak sözcük ve kalıplar: *delve, tapestry, crucial, pivotal, paramount, robust (istatistik dışı), seamless, leverage, harness, unlock, unveil, groundbreaking, revolutionize, cutting-edge, state-of-the-art, holistic, synergy, intricate, myriad, plethora, landscape (mecaz), realm, navigate (mecaz), underscore, showcase, notably, Moreover/Furthermore ile başlayan ardışık cümleler, "It is worth noting that", "plays a crucial role", "In today's world"*. Kısa, edilgen olmayan, mühendislik dili kullan.
10. **Sonraki aşamaya geçme, commit atma.**

---

## 2. ÇIKTI DOSYALARI (`05_Drafts/manuscript/`)

| Dosya | İçerik | Yaklaşık uzunluk (rehber) |
|---|---|---|
| `00_title_abstract_highlights.md` | Başlık, Abstract (≤ 250 sözcük), 3–5 Highlights (her biri ≤ 85 karakter), 5–6 keywords | — |
| `01_introduction.md` | Sorun, literatür boşluğu, katkılar, makale düzeni | ~1200 sözcük |
| `02_methods.md` | Model, kısıtlar, optimizasyon, istatistik, LCA, maliyet, çelik referans | ~2500 sözcük |
| `03_results.md` | Algoritma performansı, optimum tasarımlar, sınır durumlar, karbon, malzeme karşılaştırması, maliyet | ~2500 sözcük |
| `04_discussion.md` | Paradoksun koşulları, çelik karşılaştırması, sınırlamalar | ~1800 sözcük |
| `05_conclusions.md` | Numaralı, sayısal sonuçlar; gelecek çalışma | ~350 sözcük |
| `06_figure_table_captions.md` | F1–F5 ve kullanılan tablolar için açıklamalar | — |
| `07_references.md` | Yalnızca metinde atıf yapılan §4 kaynakları | — |
| `NUMBERS_TRACE.md` | Kural 4'teki sayı izleme listesi | — |
| `OPEN_ITEMS.md` | Bütün `[DATA NEEDED]`, `[REF NEEDED]`, `[REF CHECK]` yerleri | — |

Yazım sırası: Methods → Results → Discussion → Introduction → Conclusions → Abstract.

---

## 3. OLGU TABLOSU (bunların dışına çıkma; ayrıntı için kaynak dosyayı oku)

Önce şunları tamamen oku: `MEMORY.md`, `00_System/DOCS_UPDATE_PROMPT.md` (§0–§8 ve §7a), `04_Results/PAPER_METHODS_NOTES.md`, `04_Results/EC_BAMBOO_METHOD.md`, `04_Results/LCA_SENSITIVITY_REPORT.md`, `04_Results/STATISTICAL_TEST_RESULTS.md`, `04_Results/TUNING_STUDY.md`, `04_Results/tables/T1…T10*.md`, `04_Results/campaign_final/README.md`.

**Model ve kısıtlar** (kaynak: `bamboo_catalog.py`, DOCS_UPDATE_PROMPT §1–2)
- Üç kubbe AYNI açıklıkta değildir: ribbed40 40 m açıklık, 8.28 m yükseklik (505 düğüm, 1464 çubuk, 43 grup, L 0.76–3.08 m); kiewitt32 32 m, 6.6 m (169, 456, 22, L 2.09–3.55 m); geodesic16 nominal 16 m, en büyük plan çapı 16.77 m, 3.72 m (46, 115, 23, L 2.24–2.96 m). Sehim sınırı kubbe başına açıklık/150 = 266.7 / 213.3 / 106.7 mm. Kaynak: `dome_types.py` PRESETS, `geometry_report`. Metinde adlar: **Ribbed, Kiewitt, Geodesic**; ilk geçişte kod adı ve grup sayısıyla tanımla.
- Katalog: 24 Guadua kesiti, D 80–160 mm, t 6–22 mm.
- ASD (IStructE Manual 2025 / ISO 22156): X_allow = X_k·C_R·C_DF·C_T/FS; FS = 2; C_R = 0.90 (varsayım); C_DF 0.55/0.65/0.85; C_T = 1.0; E_k = 10 GPa; f_t,0,k = 40 MPa; f_c,0,k = 37.8 MPa; ρ = 700 kg/m³; Ylinen c = 0.8; b₀ = 0.01 (varsayım, C_bow = 0.5); K = 1; λ ≤ 150 tüm elemanlara (NSR-10 yalnız basınç için ister → muhafazakâr); sehim span/150 = 266.7 mm.
- Bağlantı: F_j,Rd = 4 × 13.25 × 0.93 = 49.3 kN (NSR-10 Tabla G.12.11-2/3, Ø5/8" cıvata, izinli yük).
- Yükler: ASCE 7-22 ASD faktörsüz 8 kombinasyon; yük değerleri DOCS_UPDATE_PROMPT §2.

**Optimizasyon** (T1, TUNING_STUDY, STATISTICAL_TEST_RESULTS)
- min f_pen = W·(1+P)^2; P tanımı DOCS_UPDATE_PROMPT §3.
- ABC (pop 20), ACO (pop 40), DO = **Dandelion Optimizer** (Zhao et al. 2022; pop 40). Tuning tohumları 2001–2005, nihai tohumlar 1001–1030; NFE = 1000 × değişken sayısı.
- 270/270 uygun. En iyi ağırlıklar 5.800 / 41.058 / 66.352 kN (ABC; ACO Kiewitt ve Ribbed'de aynı değere ulaştı).
- Friedman χ²_F = 48.60 / 38.26 / 49.16; Mann-Whitney U (Holm), α = 0.05: ABC her kubbede ACO ve DO'dan anlamlı derecede iyi, p_Holm ≤ 5.53×10⁻⁴, A12 = 0.758–1.000.
- SAP2000 doğrulaması: bağıl fark ≤ 1.3×10⁻¹³; max D/C 0.9959 / 0.9923 / 0.99995.
- Sınır durumlar (T4, F4): basınç hâkim; narinlik grupların ~%5–19'u; çekme D/C ≤ 0.43; u/u_lim ≤ 0.14; bağlantı D/C ≤ 0.807.

**Karbon** (LCA_SENSITIVITY_REPORT, EC_BAMBOO_METHOD, T5–T8)
- EC: bambu 0.30 (türetilmiş; aralık 0.09–1.23, alt sınır varsayım), bağlantı çeliği 2.38, harç 0.18 (rötresiz grout için proxy), çelik boru 2.51 (yalnız çelik referans). Biyojenik karbon hariç.
- Bağlantı payı: temel %74.1–82.1 (yalnız çelik %39.0–57.3); birleşik elverişsiz uç ribbed40 %57.7, geodesic16 %53.9, kiewitt32 %45.3.

**Çelik referans ve malzeme** (T5, T6, PAPER_METHODS_NOTES)
- Çelik üye ağırlıkları: Reference (354 elemanlı çelik kubbe) 129.0, Ribbed 104.7, Kiewitt 60.7, Geodesic 11.4 kN.
- Aynı geometride bambu/çelik: ağırlık 0.51 / 0.68 / 0.63; CO₂e 0.25 / 0.28 / 0.35 (Geodesic / Kiewitt / Ribbed).
- Üye ağırlığı ≠ sistem ağırlığı: bağlantı çeliği ve harç dahil toplam sistem ağırlığı Ribbed bambu 277.2 kN, Reference çelik 135.0 kN (T5 "Total system weight").
- Literatür kontrolü: faktörsüz koşullarda bizim çelik model 135–136 kN, literatür 151.1–155.8 kN → çelik referansımız ~%10 hafif (muhafazakâr).

**Maliyet** (T9, T9a): bambu/çelik malzeme maliyeti oranı Geodesic 0.61–0.87, Kiewitt 0.87–1.39, Ribbed 0.98–1.34; harç bambu maliyetinin %41.6–73.4'ü.

**Bağlantı detayı** (T10): Ribbed'de 12 eleman (%0.82, L = 0.76 m) gereken cıvataları NSR-10 aralık kuralına göre barındıramaz.

**Sınırlamalar (Discussion'da hepsi yazılacak):** yalnız malzeme maliyeti (işçilik/LCC yok); λ ≤ 150'nin çekmeye de uygulanması; EC_bambu alt sınırı varsayım; bambu fiyatı ve çap üssü belirsiz, senaryolar bağımsız değil; Ribbed'de 12 kısa eleman; C_R ve b₀ varsayım; grout EC proxy; üye vs sistem ağırlığı; bağlantılar eksenel mafsal kabul edildi; malzeme özelliklerinde doğal değişkenlik modellenmedi.

**Şekiller** (`04_Results/figures/`, açıklamalar DOCS_UPDATE_PROMPT §7a): F1 best profiles, F2 convergence, F3 box plots, F4 governing limit states, F5 weight, F5 CO₂e. F5 maliyet şekli yok.

---

## 4. İZİN VERİLEN KAYNAKLAR

Künyesi teyitli (kullanılabilir):
- Trujillo, Harries, Kaminski, Lopez (2025), *Manual for the design of bamboo structures to ISO 22156:2021*, IStructE, v1.0 (`Papers/IStructE2023_Manual_Bamboo_ISO22156.pdf`).
- ISO 22156:2021, *Bamboo structures — Structural design*.
- NSR-10 Título G (2010), Colombia (`Papers/NSR-10_Titulo_G.pdf`).
- Correal, Prada, Suárez, Moreno (2021), *CBM* 305: 124597 — yalnız bağlantı davranışı.
- Paraskeva, Pradhan, Stoura, Dimitrakopoulos (2019), *CBM* 201: 473–483.
- Zea Escamilla & Habert (2014), *J. Clean. Prod.* 69: 117–127.
- Zea Escamilla et al. (2018), *Sustainability* — "Industrial or Traditional Bamboo Construction? Comparative LCA of Bamboo-Based Buildings" (cilt/sayfa PDF'ten al).
- Restrepo, Becerra, Tibaquirá (2016), *J. Clean. Prod.* — bamboo boards in Colombia (`Papers/1-s2.0-S0959652616300622-main.pdf`; cilt/sayfa PDF'ten al).
- Archila, Kaminski, Trujillo, Zea Escamilla, Harries (2018), *Materials and Structures* — bamboo reinforced concrete review (PDF'ten al).
- Malkowska, Norman, Trujillo (2022), *CBM* 342: 127971.
- Vogtländer et al. (2010) ve van der Lugt et al. (2006): künyeyi `Papers/` PDF'inden al; alamazsan `[REF CHECK]`.
- Circular Ecology, ICE Database Educational V5.0 (June 2026) — yazar sırası `[REF CHECK]`.
- ASCE 7-22.

Künyesi yok (atıf gerekiyorsa `[REF NEEDED]` yaz, uydurma): ABC, ACO ve Dandelion Optimizer orijinal makaleleri; Hasançebi et al. 2009 (354 elemanlı kubbe); AISC ASD-89; INBAR TR35; Mann-Whitney / Holm / Friedman / Vargha-Delaney yöntem kaynakları; Saka 1991.

`Papers/Dome354Member_Optimization.pdf` kullanıcının kendi yayımlanmamış taslağıdır; atıf yapma, yalnız arka plan bilgisi olarak kullan.

---

## 5. TESLİM

Bitirince şunları raporla: oluşturduğun dosyalar ve sözcük sayıları; `OPEN_ITEMS.md` özeti; olgu tablosuyla kaynak dosyalar arasında gördüğün çelişkiler (çözme, yalnız bildir). Sonraki aşamaya geçme.
