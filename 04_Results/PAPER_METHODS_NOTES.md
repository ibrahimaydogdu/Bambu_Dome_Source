# Makale için yöntem notları (konuşulan kararlar; Methods/Appendix'e uyarlanacak)

## 1. Narinlik sınırı (λ_max)
- Kod: tüm elemanlara λ = KL/r ≤ 150 (basınç ve çekme), K = 1,0.
- Kaynak: NSR-10 Título G, G.12.9.2.6 (PDF s. 132) ve G.12.9.2.7.3 (s. 133): "Bajo ninguna circunstancia es aceptable trabajar con elementos de columna que tengan esbeltez mayor de 150." Sınır **yalnızca basınç elemanları (columnas)** içindir; çekme elemanı için NSR-10'da narinlik sınırı yoktur. IStructE Manual (ISO 22156) sabit bir λ sınırı vermez.
- **Makale cümlesi (öneri):** "A slenderness limit of λ = KL/r ≤ 150 was imposed on all members. NSR-10 (G.12.9.2) prescribes this limit for compression members only; applying it to tension members as well is a deliberately conservative modelling choice, and its effect is limited because slenderness governed only about 5–19 % of the design groups of the optimum designs (Fig. F4)."
  (Oran: `04_Results/figures/F4_governing_limit_states.png`; basınç hâkim, narinlik grupların yaklaşık %5–19'unu belirler.)

## 2. Bağlantı kapasitesi ve kısa elemanlar (sınırlama)
- Modelde bağlantı sınırı: F_j,Rd = n_bolt × F_bolt,adm × C_g = 4 × 13,25 kN × 0,93 = **49,3 kN** (NSR-10 Tabla G.12.11-2, Ø5/8" cıvata, D = 100 mm, çift kesme; Tabla G.12.11-3, 4 cıvata). Eleman başına bu sabit sınır kullanıldı; 270 optimum tasarımın tamamı uygundur (en yüksek bağlantı D/C: ribbed40 0,81).
- IStructE Manual zinciri (F_k × C_DF / FS_j, FS_j = 2,5 için süneklik 3,0) cıvata başına yaklaşık 3–5 kN verir (K faktörü Manual'de doğrulanamadı); NSR-10 izinli değerleri bunun ~3 katıdır. İki kaynak ve fark makalede tartışılmalı.
- **Elemanların gerçek cıvata ihtiyacı** (`joint_bolt_check.py`, [T10](tables/T10_joint_bolt_requirement.md)): eleman kuvvetleri düşük olduğundan çoğu eleman 1–2 cıvata ile taşınır (ribbed40: 813 eleman 1, 591 eleman 2, 60 eleman 3 cıvata; hiçbiri 4 gerektirmez).
- **Sınırlama (makalede açık yazılacak):** NSR-10 G.12.11.3.13 cıvata aralığını ≥ 150 mm ve uç mesafesini ≥ 150 mm (çekme) / 100 mm (basınç) ister. n cıvatalı iki uç için gereken boy L ≥ 2·(e + (n−1)·150) + 150 mm. Buna göre **yalnızca ribbed40'ta 12 eleman (%0,8), hepsi 0,76 m boyunda**, gereken cıvata sayısını (3) barındıramaz (gereken boy ≈ 1,05 m; bu elemanlardaki en büyük kuvvet 31,3 kN). geodesic16 ve kiewitt32'de hiçbir eleman yetersiz değildir (en kısa 2,09 m).
- **Gerekçe (neden sorusuna):** Bu 12 elemanın bağlantısı model dışında bırakılmadı; kapasite ölçütüne dahildir, yalnızca cıvata yerleşimi geometrik olarak sığmamaktadır. Çözüm detay düzeyindedir (ör. daha büyük çaplı cıvata, çelik manşon/ankraj veya bu elemanlar için daha uzun culm/çok-culm), optimizasyonun düğüm geometrisini ve bağlantı detayını değiştirmesi bu çalışmanın kapsamı dışındadır; tek eleman tipi ve yalnızca %0,8 oranında olduğu için sonuçları (ağırlık, karbon) belirgin etkilemez.

## 3. Gömülü karbon (A1–A3)
- EC_bambu = 0,30 kg CO₂e/kg (aralık 0,09–1,23), türetme: `04_Results/EC_BAMBOO_METHOD.md`. **Üretim alt sınırı (INBAR TR35, laminat panelin hasat + yerel nakliye adımları, 0,032 kg/kg) varsayımdır**: yuvarlak culm için doğrudan kaynak bulunamamıştır; makalede "assumed" olarak belirtilir ve duyarlılık aralığı verilir.
- EC_çelik boru 2,51 (welded pipe), bağlantı çeliği 2,38 (plate), harç 0,18 (1:3): ICE Educational V5.0 (Haziran 2026), `Evidence/ICE-Educational-V5.0/`.
- Kapsam: yalnızca beşikten kapıya (A1–A3); biyojenik depolama, kullanım, yıkım ve geri dönüşüm kredisi dahil değil.

## 4. Maliyet kapsamı
- **Yaşam döngüsü maliyeti (LCC) ve işçilik çalışmanın sınırıdır; gelecek çalışma olarak önerilir.** Yalnızca **malzeme maliyeti**: bambu culm + bağlantı çeliği + harç; karşılaştırma çeliği de yalnızca malzeme (boru ve bağlantı çeliği aynı malzeme fiyatıyla). Montaj/işçilik her iki yapıda da dışarıda.
- Fiyat kaynakları ve sınırlamalar: Endonezya (Jawa Tengah HSD 2024: bambu Ø6–8 cm, baja profil, grout), Hindistan (CPWD DSR 2023: çelik malzeme, grout). Yapısal çapta bambu fiyatı **doğrudan kaynaklı değildir**: Ø70 mm fiyatı (D/70)^α ile ölçeklendi (α = 2 temel, α = 3 duyarlılık). Hindistan/Türkiye bambu fiyatları Endonezya bambu/çelik oranından türetildi; üç ülke senaryosu bu yüzden bağımsız değildir.
- Harç: planda olduğu gibi **non-shrink grout** (fiyat: Jateng 'Semen Grout' 7.173–9.705 Rp/kg, DSR M-60 non-shrink 28 Rs/kg; EC: ICE 1:3 harç 0,18 kg/kg proxy olarak, rötresiz grout için doğrudan ICE satırı yoktur; varsayım).
- Sonuç (T9, malzeme düzeyi; 4 fiyat senaryosu × α ∈ {1,5; 2; 2,5; 3}): bambu/çelik malzeme maliyet oranı geodesic16 0,61–0,87, kiewitt32 0,87–1,39, ribbed40 0,98–1,34; yani malzeme düzeyinde bambu ve çelik maliyeti kabaca eşittir, bambu avantajı yalnızca küçük kubbede görülür. Bambu maliyetinin ~%41–70'i harçtan (non-shrink grout) gelir. Kolombiya senaryosu (Guadua 6 m: 38.500 COP, 2026; çap belirtilmemiş, D_ref = 120 mm varsayımı) en yüksek bambu fiyatını verir.

## 5. Çelik referans
- 354 elemanlı (orijinal) topoloji ve üç bambu geometrisi için çelik: 37 AISC borusu (SteelPipeSec), A36, ASD; aynı ASCE 7-22 ASD kombinasyonları, L/150 sehim.
- Literatür kontrolü (354MemberDome.pdf; Aydoğdu vd. taslağı; kubbe kaynağı Hasançebi vd. 2009): literatür koşullarında (faktörsüz D+S+W±, 11,1 cm) bizim modelimiz **135–136 kN**, literatür 151,1–155,8 kN (BSO/BBO/ABC). Çelik referansımız literatürden ~%10 hafiftir (bambu karşılaştırmasında muhafazakâr).
- Referans örnek ayrıntıları (354 elemanlı kubbe, yükler, çelik tasarımı) **Ek (Appendix)** bölümüne konur; ana metinde kısa özet. Duyarlılık çalışması (tuning) tablosu da Ek'e (`TUNING_STUDY.md`, `TUNING_STUDY_runs.csv`).
