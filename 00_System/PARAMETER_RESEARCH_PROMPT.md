# PARAMETRE ARAŞTIRMASI PROMPT'U (diğer yapay zekâ için)

> [!NOTE]
> Bu belge tarihsel 1. tur araştırma promptudur. Araştırma ve denetimler sonucunda kesinleşen güncel parametreler ($F_{j,Rd} = 49.3\text{ kN}$ NSR-10, ICE V5.0 Haziran 2026, $EC_b = 0.30\text{ kg CO}_2\text{e/kg}$, seçilen 3 algoritma: ABC, ACO, DO) için `00_System/DOCS_UPDATE_PROMPT.md` (Rev. 2) ve `PROJECT_STATE.md` belgelerine bakınız.

**Görev:** Aşağıdaki tablodaki her parametre için, kodda şu an kullanılan değerin **kaynaklı** karşılığını bul. Kodu ve proje belgelerini değiştirme; yalnızca araştırma raporu üret (`04_Results/PARAMETER_EVIDENCE.md`). Çıktıyı Developer/Results Agent'a değil kullanıcıya teslim et; doğrulamayı Claude Code oturumu yapacak.

## Kanıt kuralları (ihlal edilirse madde geçersiz sayılır)
1. **Hafızadan değer yazma.** Her sayı, açıp okuduğun bir kaynaktan gelmeli (makale, standart, rapor, veritabanı, fiyat listesi).
2. Her değer için şu 6 alanı ver: **(a) değer ve birim, (b) kaynak künyesi (yazar, yıl, başlık, dergi/yayıncı) + DOI veya URL, (c) sayfa / tablo / denklem numarası, (d) kaynaktan birebir alıntı (≤ 25 kelime, tırnak içinde), (e) kapsam (hangi ürün/ülke/yıl/sistem sınırı), (f) durum: DOĞRULANDI (tam metni okudum) / KISMEN (özet veya ikincil kaynak) / BULUNAMADI.**
3. Kaynak "dolaylı" ise (başka bir makalenin aktarması) bunu belirt ve birincil kaynağı da ara.
4. Tek bir sayı yerine **düşük / temel / yüksek** aralık ver (duyarlılık analizi için). Aralığı hangi kaynaklar belirliyor yaz.
5. Fiyatlarda **ülke, yıl, para birimi, KDV dahil mi, birim (kg, m, m³)** zorunlu. USD'ye çevirdiysen kuru ve tarihi yaz. Resmî/ticari fiyat listesi, ihale birim fiyat cetveli veya yayımlanmış maliyet çalışması kullan. Tek ülke yerine A bölümündeki **çok ülkeli senaryo yaklaşımını** uygula.
6. Bulamadığını açıkça "BULUNAMADI" yaz; tahmin üretme. Uydurma künye yasak (daha önce iki künye yanlış çıktı).
7. Okunabilen PDF'leri `Papers/` klasörüne kaydetmeyi öner (kullanıcı koyacak); metin kopyalayıp yapıştırma.

## A. Maliyet parametreleri: ÇOK ÜLKELİ SENARYO YAKLAŞIMI (kullanıcı kararı; en yüksek öncelik)
Tek bir ülkenin fiyatını "doğru fiyat" olarak kullanmayacağız (ISO 22156 ve mekanik ülkeden bağımsız; fiyat değil). Sonuç, fiyattan bağımsız **başa baş (break-even)** değerleriyle ve **3 ülke × 2–3 yıl senaryosuyla** raporlanacak. Senin görevin bu senaryoları kaynaklı fiyatlarla doldurmak.

**A0. Senaryo seçimi.** Üç ülke öner ve gerekçelendir: (1) Guadua üreten bir ülke (Kolombiya veya Ekvador), (2) resmî birim fiyat cetveli bulunan ülke (Türkiye: Çevre, Şehircilik ve İklim Değişikliği Bakanlığı birim fiyatları), (3) üçüncü bir ülke (Hindistan veya Endonezya veya Çin; bambu ve çelik fiyatları ayrı yayımlanan biri). Her ülke için 2–3 yıl (ör. 2022, 2024, 2025/2026). Seçimi yapmadan önce kullanıcıya sor.

**A1–A4. Her ülke × yıl için şu fiyatlar** (hepsi tablo halinde, bölüm başındaki 6 alan kuralıyla):
| # | Kalem | Birim | Notlar |
|---|---|---|---|
| A1 | Guadua (veya yerel yapısal bambu) culm, çap kademeleri D = 80–160 mm | USD/m ve yerel para/m | Çap–fiyat ilişkisi (en az 3 çap). Koddaki Tablo 1 (0,65 / 1,10 / 1,85 / 3,15 / 5,20 USD/m) kaynağı nedir? Bulunursa bağla, bulunmazsa "kaynaksız, kullanıcıya ait" yaz. |
| A2 | Yapısal çelik boru / CHS (S355 veya yerel karşılığı), işçilik dahil ve hariç | USD/kg | Üretim ve nakliye dahil/hariç belirt |
| A3 | Bağlantı çeliği (hub, saplama, somun, pul), işlenmiş | USD/kg | |
| A4 | Rötresiz grout / çimento harcı | USD/kg | |
| A5 | Montaj işçiliği (bambu ve çelik kafes için ayrı, varsa) | % veya USD | İsteğe bağlı |
Her fiyat için: ülke, yıl, ay, para birimi, KDV dahil mi, birim, kur (kaynak ve tarih) ve **tek bir baz yıla enflasyon düzeltmesi** (kullanılan endeks: TÜFE/PPI veya çelik fiyat endeksi; kaynağı ile). Mutlak fiyatları USD'ye çevir ama yerel para değerini de koru.

**A6. Fiyat oranları** (her senaryo için hesapla, hakem savunması için asıl çıktı):
- r_culm/steel = culm fiyatı (USD/m, D = 120 mm) ÷ çelik boru fiyatı (USD/kg)
- r_conn/tube = bağlantı çeliği fiyatı ÷ boru fiyatı
- r_mortar/tube = harç ÷ boru fiyatı
Bu oranlar ülkeler arasında ne kadar değişiyor? Oranlar kararlıysa tek bir referans oran seçilebilir.

**A7. Destekleyici literatür.** Bambu yapı ile çelik/betonarme yapı maliyetini karşılaştıran yayımlanmış çalışmaları bul (en az 3, mümkünse Guadua veya yapısal bambu, ülkeleri farklı). Her biri için: ülke, yıl, karşılaştırılan sistem, rapor edilen bambu/çelik maliyet oranı (birebir alıntı ve sayfa). Amaç mutlak fiyat almak değil, hesabımızdaki bambu/çelik maliyet oranının (şu an 0,70–0,96 aralığında) **makul olup olmadığını** kontrol etmek ve tartışmayı desteklemek. Kapsam farklarını (aynı yapı mı, hangi sistem sınırı) açıkça yaz.

**A8. Çap–fiyat eğrisi.** Culm fiyatı çapla hangi üsle artıyor? (Tablo 1'den çıkan üs ≈ 3,0; plan metni 2,2 diyordu.) Yayımlanmış veya piyasa verisinden bir eğri çıkar; yoksa "BULUNAMADI" yaz.

## B. Gömülü karbon (A1–A3) parametreleri
| # | Parametre | Koddaki değer | Aranan |
|---|---|---|---|
| B1 | EC bambu (Guadua culm, işlenmiş, kurutulmuş/koruyucu işlemli) | 0,35 kgCO₂e/kg | **kg/kg biçiminde** değer; Zea Escamilla & Habert 2014 mPt/m³ veriyor, dönüşümü nasıl yapılır? Biyojenik karbon dahil/hariç ayrı ver. Ek kaynaklar: Vogtländer vd., van der Lugt vd., Ecoinvent bambu kayıtları |
| B2 | EC yapısal çelik boru / profil | 2,10 | ICE v3.0 (Jones & Hammond 2019) "steel, tube/section" satırı; EPD (Worldsteel, Türk üreticiler EPD'leri) |
| B3 | EC bağlantı çeliği (dökme/dövme, galvaniz) | 2,10 | ICE ve EPD satırı; galvaniz ilavesi |
| B4 | EC rötresiz harç / çimento harcı | 0,18 | ICE v3.0 "mortar" / "grout" satırı, çimento oranı |
| B5 | Harç yoğunluğu | 2100 kg/m³ | Ürün veri sayfası |
| B6 | Çelik çubuk ucu / düğüm hub kütlesi | 0,5 kg/uç, 2,0 kg/düğüm | Yayımlanmış bambu uzay kafes veya benzeri düğüm detaylarından kütle; yoksa BULUNAMADI |
| B7 | Harç enjeksiyon boyu L_inj | 2,5·D | Bambu mortar-infill bağlantı deneylerinde dolgu boyu (Correal 2021, Trujillo & Malkowska 2018 vb.) |

## C. Mekanik / yönetmelik parametreleri
| # | Parametre | Koddaki değer | Aranan |
|---|---|---|---|
| C1 | λ_max (narinlik sınırı) | 150 | **ISO 22156:2021 madde numarası** ve metni (basınç/çekme için ayrı mı?). Bulunamazsa Eurocode 5 / başka bambu standardı (NSR-10 Título G, Hindistan NBC) |
| C2 | Guadua boyuna çekme karakteristik dayanımı f_t,0,k | 40 MPa (Manual Tablo 4.4 şema) | Guadua çekme deneyleri (ör. Correal, Ghavami, Gonzalez, Trujillo) karakteristik/ortalama + COV |
| C3 | Guadua E (basınç, eğilme) | E_k = 10 GPa | Manual Tablo A3.9: E_c = 21,8 GPa (COV 0,29); hangi E rijitlik analizi için uygun? Yayımlanmış kafes/çatı örnekleri |
| C4 | Bağlantı kapasitesi F_bolt,max, n_bolt | 26,6 kN × 2 | Çapraz çift cıvata harç dolgulu Guadua bağlantısı deneyleri: toplam kapasite, tasarım (allowable) değeri nasıl türetilir (Manual Ek. 7, FS_j) |
| C5 | C_R (redundancy) | 0,90 | ISO 22156 Madde 5.4 metni: ne zaman 1,1? Kafes sistemi için geçerli mi? |
| C6 | b₀ (başlangıç eğriliği) ve C_bow | b₀ = 0,01 | ISO 22156/Manual Denk. 3.4 ve sınır değer |
| C7 | Etkin boy katsayısı K | 1,0 | Manual Tablo 6.1 / ISO Tablo 8: kafes elemanı |
| C8 | Servis sınıfı ve C_DF | SC2: 0,55 / 0,65 / 0,85 | ISO 22156 Tablo 3 birebir; hangi servis sınıfı örtülü yapı için uygun? |
| C9 | Kubbe/kafes çatı yer değiştirme sınırı | L/150 | Kubbe ve kafes çatılar için sehim sınırı (Eurocode 3 NA, AISC Design Guide 3, TBDY/TS 498, ASCE 7 Ek. C) ve bambu için öneri |
| C10 | Referans çelik: AISC 360 ASD, S355, λ ≤ 200 (basınç), 300 (çekme) | | AISC 360-16/22 Md. D1/E2 kullanıcı notları; çelik kafes kubbe literatür optimumları (Saka 1991 vb.) ile ağırlık kıyası |

## D. Referans model ve yükler (KULLANICI KARARI: ek araştırma YAPMA)
Referans modelin yükleri için literatürde ayrı kaynak aranmayacak. Yük değerleri ve rüzgâr parametreleri kullanıcının sağladığı **354MemberDome.pdf** (Saka 354 elemanlı, 40 m açıklıklı kubbe) belgesinden alınır ve makalede yalnızca bu belge atıf olarak verilir. Görevin: bu PDF'teki rüzgâr (Denk. 27 yöntemi), kar ve ölü yük parametrelerini sayfa/tablo numarasıyla `PARAMETER_EVIDENCE.md` içine, "koddaki değerle uyumlu mu" sütunuyla birlikte aktar. Referans örnek ayrıntıları (354 elemanlı kubbe, yükler, çelik referans tasarımı) makale **ana metnine değil Ek (Appendix) bölümüne** konur; ana metinde bir cümlelik özet ve ekin işaretlenmesi yeterlidir. Saka 1991 optimum ağırlıklarını ve diğer ek literatürü arama.

## Teslim formatı
- `04_Results/PARAMETER_EVIDENCE.md`: her satır için yukarıdaki 6 alan; en üstte **özet tablo** (parametre | koddaki değer | önerilen düşük/temel/yüksek | durum).
- Ayrıca "kod değiştirmeyi gerektiren" maddeleri ayrı listele (ör. koddaki değer kaynağın aralığı dışındaysa).
- Kullanıcıdan netleştirilecek sorular (A0 ülke ve yıl seçimi, enflasyon endeksi) listesini en sona ekle.
- **Fiyat çıktısı için ayrıca** `04_Results/PRICE_SCENARIOS.csv` üret: sütunlar ülke, yıl, kalem, değer, birim, USD değeri, baz yıl USD değeri, kaynak, sayfa; bu dosya Claude Code tarafında maliyet tablolarını ve başa baş analizini yeniden üretmek için doğrudan okunacak.
- Doğrulamayı Claude Code yapacak: her alıntıyı kaynakla karşılaştıracak, uyuşmayan veya kaynağı açılamayan maddeyi "REDDEDİLDİ" işaretleyecek. Bu yüzden DOI/URL ve sayfa numaraları eksiksiz olmalı.
