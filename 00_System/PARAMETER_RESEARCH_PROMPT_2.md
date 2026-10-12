# PARAMETRE ARAŞTIRMASI 2. TUR (diğer yapay zekâ için): kanıt kurallarını sıkılaştırılmış hâli

> [!NOTE]
> Bu belge tarihsel 2. tur araştırma promptudur. Araştırma ve denetimler sonucunda kesinleşen güncel parametreler ($F_{j,Rd} = 49.3\text{ kN}$ NSR-10, ICE V5.0 Haziran 2026, $EC_b = 0.30\text{ kg CO}_2\text{e/kg}$, seçilen 3 algoritma: ABC, ACO, DO) için `00_System/DOCS_UPDATE_PROMPT.md` (Rev. 2) ve `PROJECT_STATE.md` belgelerine bakınız.

**Bağlam:** 1. turdaki `04_Results/PARAMETER_EVIDENCE.md` Claude Code denetiminden geçti (`04_Results/PARAMETER_EVIDENCE_REVIEW.md`, 1–3. bölümler). Sonuç: uydurma alıntılar ve **kendi ürettiğin "arşiv" PDF'leri** (`Evidence/E1–E10`, tek sayfa HeadlessChrome çıktısı, kaynak belge değil) kanıt sayılmadı. Bu turda aşağıdaki 3 iş kaldı. Kodu ve diğer belgeleri değiştirme.

## Değişmez kurallar
1. **Kaynak belgeyi olduğu gibi indir** (orijinal PDF/XLSX), `Papers/` klasörüne koy (dosya adı: `<YazarYıl>_<kısa ad>.<uzantı>`), **SHA-256 ve bayt boyutunu** raporda yaz. Kendi yazdığın özet/HTML/PDF'i "kanıt" olarak KOYMA. İndiremediysen `ERİŞİLEMEDİ` yaz ve kullanıcıdan iste; bağlantı çalışmıyorsa o bağlantıyı "kanıt" olarak verme.
2. **Her alıntı için**: PDF/XLSX dosya adı + sayfa (veya sayfa adı/hücre adresi) + **belgeden kopyalanmış birebir metin** (≤ 25 kelime). Alıntıyı belgede bulamazsan `BULUNAMADI` yaz; "benzer ifade" yazma.
3. Tahmin, hatırlama, "genel kabul" ve "makul aralık" **kanıt değildir**. Kaynakta yoksa o parametre `DOĞRULANAMADI` kalır.
4. Her sonuç satırı için tek tek durum ver: `DOĞRULANDI (belge + sayfa)` / `KISMEN` / `DOĞRULANAMADI` / `ERİŞİLEMEDİ`. **Toplu "%100 doğrulandı" ifadeleri yasak.**
5. Çıktı dosyası: `04_Results/PARAMETER_EVIDENCE_R2.md` (yeni dosya; eskisini üzerine yazma). Her indirilen belgenin yanında "Claude Code doğrulaması için: şu sayfaya bak" notu olsun.

## İş 1: ICE Database v3.0 (Excel) — EC_çelik, EC_bağlantı çeliği, EC_harç
Kaynak: Circular Ecology ICE Database V3.0 (Jones & Hammond, Kasım 2019). Ücretsiz Excel indirmesi form gerektirebilir; yapabiliyorsan indir, yapamıyorsan **kullanıcıya hangi dosyayı hangi sayfadan indireceğini** yaz.
Gerekli satırlar (sayfa adı, satır numarası, sütun başlığı ve değer; "A1–A3, kg CO2e/kg"):
- Çelik: genel (general), boru/tüp (pipe/tube), profil/section, `recycled content` ve `virgin` ayrımı
- Galvaniz (hot-dip galvanising) ilavesi
- Harç/grout: `mortar` (1:3 gibi), mümkünse `cement-based grout`
- Bambu satırı var mı? (varsa değer ve sınırı: biyojenik karbon dahil/hariç)
Sonunda: koddaki değerler (çelik 2,10 ; harç 0,18) ile karşılaştırma tablosu.

## İş 2: NSR-10 Título G (Kolombiya) — narinlik sınırı ve Guadua tasarım kuralları
Resmî kaynak (AIS, MinVivienda veya Colombian Congress/SECOP üzerinden barındırılan **orijinal** PDF); önceki turda verilen `minvivienda.gov.co/.../040112_titulo_g_0.pdf` ve `asosismica.org.co/normas/nsr-10/` bağlantıları **404** veriyor. Çalışan resmî bir PDF bul (Título G, Capítulo G.12), `Papers/NSR-10_Titulo_G.pdf` olarak koy.
Bulunacak (madde no, sayfa, birebir İspanyolca metin):
- Basınç elemanı için **maksimum narinlik** (G.12.x) ve etkin boy katsayısı K
- Çekme elemanı narinlik sınırı varsa
- Guadua için izinli gerilmeler (f_t, f_c, E) ve **servis/yük süresi** katsayıları
- Eksenel basınç için burkulma formülü (Euler/Ylinen benzeri) ve kullanılan katsayılar
Sonuç: koddaki λ_max = 150 desteklenir mi, hangi madde (varsa), hangi koşulda?

## İş 3: Bağlantı kapasitesi — n_bolt ve FS_j (en kritik)
Kodda: F_j,Rd = n_bolt × F_bolt,max = 2 × 26,6 = 53,2 kN (Correal vd. 2021, CBM 305, Tablo 4: Ø15,9 mm, 0°, ortalama maks. yük 26,6 kN, COV %20,5, süneklik ort. 3,0). Bu ortalama nihai yüktür; **ASD izinli kapasite** için IStructE Manual (Papers/ klasöründeki PDF) şu zinciri tanımlar: karakteristik değer F_k (Denk. A3.9 / Md. 10.12.1) × C_DF / FS_j, FS_j = 3,0 (m < 1,5), 2,5 (1,5 ≤ m < 4), 2,0 (m ≥ 4) (Manual Denk. 7.5).
Yapılacaklar:
1. Manual'da Denk. 7.5, Md. 7 ve Ek. A7 / Md. 10.12'yi **birebir** kopyala (sayfa numaralarıyla); F_k nasıl hesaplanıyor (n = 8 numune, COV = %20,5) açıkla.
2. Bu zincirle Correal'ın 15,9 mm cıvata sonucu için **izinli kapasiteyi** hesapla (C_DF = 0,55 / 0,65 / 0,85 için ayrı ayrı); hesap adımlarını ver. (Claude Code ön hesabı: F_k ≈ 16 kN, FS_j = 2,5 → bağlantı başına ≈ 3,6–5,6 kN. Bunu bağımsız olarak doğrula veya çürüt.)
3. Guadua'da **birden çok cıvatalı** harç dolgulu uç bağlantılarının **toplam kapasitesi** yayımlanmış mı? En az 3 deneysel çalışma bul (Papers/ içine koy): cıvata sayısı, çap, dolgu boyu, toplam maksimum yük, süneklik, kaynak sayfası. 4, 6, 8 cıvatalı ya da çelik manşon/ankraj gibi alternatif uç bağlantılarının toplam kapasitesi ne? Tek culmun uç bölgesi (örneğin Ø100 mm) bu kadar cıvatayı taşıyabilir mi (dizilim/aralık kuralları: Manual Tablo 7.x)?
4. Sonuç tablosu: "uzay kafes düğüm bağlantısı ≥ 40 kN eksenel izinli kuvvet taşıyabilir mi?" sorusuna belgelere dayalı cevap. Cevap hayırsa: çok-culm elemanlar (Manual çok-culmlu üye hükümleri) veya farklı uç bağlantı tipleri için yayımlanmış kapasite verilerini ver.

## Teslim
`04_Results/PARAMETER_EVIDENCE_R2.md`: üç iş, her biri için "indirilen belgeler tablosu (ad, boyut, SHA-256, kaynak URL)" + "bulgular tablosu (belge, sayfa, birebir metin, durum)" + "çözülemeyenler".
