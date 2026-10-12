# FİYAT KAYNAKLARI ARAŞTIRMASI (diğer yapay zekâ için): Hindistan ve Kolombiya

**Amaç:** Maliyet analizi tek ülkeye bağlı kalmasın. Elimizde **Türkiye** için gerçek bir resmî belge var (`Evidence/2026-a-ustos-in-aat-birim-fiyatlar-…pdf`, ÇŞB 2026 Ağustos). Hindistan ve Kolombiya için **orijinal resmî veya yayımlanmış fiyat belgelerini bul ve indir**. Fiyatları ben (Claude Code) belgeden çıkarıp doğrulayacağım. Sen belgeyi bulup indireceksin ve nerede ne yazdığını işaretleyeceksin.

## Değişmez kurallar (1. ve 2. turda ihlal edilenler)
1. **Orijinal belgeyi olduğu gibi indir** (PDF/XLSX), `Evidence/` klasörüne koy: `IN_CPWD_DSR_<yıl>.pdf`, `CO_<kurum>_<yıl>.pdf` gibi adlandır. **SHA-256 ve bayt boyutunu** raporda yaz. Kendi yazdığın özet, HTML sayfası veya "arşiv PDF'i" **kanıt değildir**; böyle bir dosya koyma.
2. Bir belgeye **ulaşamazsan** "ERİŞİLEMEDİ" yaz, nedenini (404, giriş gerekli, ücretli) belirt ve kullanıcıdan manuel indirmesini iste. Çalışmayan bağlantıyı kanıt gösterme.
3. Fiyat bilgisini belgeden **birebir** aktar: belge dosya adı + sayfa no + kalem/poz no + tanım (kopya metin) + birim fiyat + birim + yıl/ay + KDV durumu + montaj/işçilik dahil mi. Belgede bulamazsan "BULUNAMADI". **Tahmin, hatırlama, yaklaşık değer, "proyeksiyon" yasak.** 2026 gibi gelecek yıl için ancak yayımlanmış resmî liste varsa değer ver.
4. Toplu "%100 doğrulandı" ifadeleri yasak. Her kalem için ayrı durum: `DOĞRULANDI (belge+sayfa)` / `KISMEN` / `BULUNAMADI` / `ERİŞİLEMEDİ`.
5. Çıktı: `04_Results/PRICE_EVIDENCE_IN_CO.md` ve `04_Results/PRICE_SOURCES_IN_CO.csv` (sütunlar: ülke, yıl, ay, kalem, poz/kalem no, tanım, değer, birim, para birimi, KDV (dahil/hariç), montaj dahil mi (E/H), belge dosyası, sayfa, SHA-256). Mevcut `PRICE_SCENARIOS.csv` ve `PARAMETER_EVIDENCE*.md` dosyalarını değiştirme.

## İş 1: Hindistan (resmî birim fiyat çizelgesi)
- **CPWD Delhi Schedule of Rates (DSR)**: Hindistan Merkezi Kamu Bayındırlık Dairesi (cpwd.gov.in). Çevre/inşaat birim fiyatlarının en güncel iki sürümü (örn. DSR 2021, DSR 2023 veya 2024/2025 güncellemesi). Hangi sürümlerin yayımlandığını ve **hangi dilimde** (Cilt 1 Civil, Cilt 2 Electrical) olduğunu belirt.
- Gerekli kalemler (Civil volume; "Structural steel work" / "Steel work in built-up sections / tubular trusses" bölümü):
  - Yapısal çelik **boru (tubular) kafes/makas** imalat ve montaj birim fiyatı (Rs/kg veya Rs/quintal)
  - Çelik **bağlantı elemanları** (gusset, hub, cıvata, somun) imalatı
  - **Rötresiz/non-shrink grout** veya cement grout birim fiyatı (Rs/kg veya Rs/m³)
  - **Bambu** kalemi: CPWD bambu direk/yapısal bambu içeren bir kalem var mı? Yoksa "National Bamboo Mission" veya bir eyalet (Assam, Kerala, Maharashtra) **Schedule of Rates**'inde yapısal bambu direk birim fiyatı (Rs/m, çap kademesiyle) **belgesiyle** ver.
- Her belge için **para birimi ve yıl** belirt; USD'ye çevrilecekse resmî kur kaynağını (RBI referans kuru, yıl ortalaması) ayrı bir belgeyle (RBI sayfa/PDF) sun.

## İş 2: Kolombiya (resmî/yayımlanmış fiyat kaynakları)
Aşağıdaki türlerde belge ara; **hepsi erişilemezse** bunu açıkça yaz:
- **Guadua (bambu) fiyatı:** Kolombiya'da yapısal Guadua fiyatını yayımlayan resmî veya sektör kaynağı: ör. **SENA**, **INBAR Kolombiya**, **Corporación Autónoma Regional (CARDER, CRQ)** Guadua raporları, **Fedebambu/Fedeguadua**, **MinAgricultura/Ministerio de Comercio** Guadua cadena raporları, üniversite tezleri (örn. Universidad Nacional, Universidad de los Andes) Guadua yapı maliyeti analizleri. Çap kademesi (basa/sobrebasa/cepa) ve boy (6 m) ile **COP/adet veya COP/m**. Üretici web sitesinin ana sayfası yetmez: **fiyat listesinin kendisi** (PDF/Tablo/ekran görüntüsü + URL + tarih) gerekir.
- **Çelik ve harç fiyatı:** **DANE** (Departamento Administrativo Nacional de Estadística) yayımladığı **ICCV** (Índice de Costos de la Construcción de Vivienda) veya **ICCP** bültenleri, **Camacol** fiyat raporları, **Cámara Colombiana de la Construcción**, ya da resmî birim fiyat analizi (ör. **IDU**, **INVIAS** "Precios Unitarios", **Alcaldía de Bogotá IDU Lista de Precios**). Yapısal çelik boru, bağlantı çeliği ve cement grout kalemleri.
- Fiyat yılını belirt; kuru **Banco de la República (TRM)** yıllık ortalama belgesiyle ver.

## İş 3: Her ülke için senaryo çerçevesi
Her ülke için, belgelerde bulduğun fiyatlardan **şu oranları hesapla** (hesabı satır satır göster; payda 0 ise "hesaplanamaz"):
- r_culm/çelik = culm fiyatı (USD/m, D ≈ 120 mm) ÷ çelik boru fiyatı (USD/kg)
- r_bağlantı/boru = bağlantı çeliği fiyatı ÷ boru çelik fiyatı
- r_harç/boru = harç fiyatı ÷ boru çelik fiyatı
**Belirtmen gereken sınırlamalar:** fiyatın kapsamı (montaj, işçilik, kâr, nakliye dahil mi); çelik fiyatı boru malzemesi mi yoksa "yerine konulmuş karkas" mı; bambu fiyatı kuru/emprenyeli mi.

## Teslim ve kontrol
- İndirilen tüm belgelerin tablosu (ad, boyut, SHA-256, kaynak URL, erişim tarihi).
- Her fiyat kalemi: bulundu/bulunamadı + belge sayfası + kopya metin.
- En sonda "Kullanıcının elle yapması gerekenler" listesi (giriş gerektiren siteler, ücretli yayınlar, kimlik doğrulama).
- Claude Code teslim sonrası: belgeleri açıp her sayfa/kalemi tek tek kontrol edecek; eşleşmeyen satırı "REDDEDİLDİ" işaretleyecek.
