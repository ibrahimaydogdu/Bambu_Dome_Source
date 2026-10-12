# 🛡️ Anti-Hallucination, Birincil Kanıt ve Sıfır Sentetik Veri Protokolü (GENELLEŞTİRİLMİŞ VE KESİN KURAL)

Bu belge; BambuDome ve gelecekteki tüm araştırma, veri toplama, maliyet, LCA ve akademik çalışmalarda yapay zekâ ajanları tarafından **istisnasız ve tavizsiz** uygulanacak birleşik doğruluk protokolüdür. Bir sonraki aramalarda benzer ihlallere kesinlikle izin verilmez.

---

## 🔒 1. ORİJİNAL BELGE ZORUNLULUĞU VE AJAN-ÜRETİMİ "ÖZET/KANIT" YASAĞI
1. **Orijinal Format İndirme:**
   - Veri kaynağı olan belge **orijinal biçiminde** (yayıncının resmî PDF'i, Excel XLSX/CSV tablosu veya tescilli kurum bülteni) doğrudan indirilerek ilgili klasöre (`Papers/` veya `Evidence/`) konulacaktır.
   - İsimlendirme standardı: `<YazarYıl>_<kısa ad>.<uzantı>` veya `<Ülke>_<Kurum>_<Yıl>.<uzantı>`.
2. **Ajan Üretimi "Kanıt" Yasağı (Tavizsiz):**
   - Ajanın kendi ürettiği HTML'den dönüştürülmüş özet kartları, tek sayfalık bilgi fişleri veya yapay "arşiv PDF'leri" **ASLA kanıt sayılamaz ve kanıt klasörlerine konulamaz.**
   - Yalnızca ilgili kurum/yayıncı tarafından fiilen üretilmiş orijinal birincil belge kanıttır.
3. **Kriptografik Doğrulama (SHA-256 ve Boyut):**
   - İndirilen her orijinal belgenin **tam bayt boyutu** ve **SHA-256 sağlama özeti (hash)** raporda zorunlu olarak listelenecektir.

---

## 🔍 2. DOĞRUDAN BİREBİR ALINTI VE SAYFA/POZ NO KURALI
1. **Birebir Metin / Değer:**
   - Her veri satırı için: Orijinal belgeden kopyalanmış **birebir alıntı (≤ 25 kelime)**, tam poz/kalem kodu, tablo veya hücre adresi yazılmalıdır.
   - Yorumlanmış, benzerleştirilmiş veya hafızadan tamamlanmış ifadeler yasaktır.
2. **Kaynakta Yoksa "BULUNAMADI":**
   - Belgede aranan parametre tam olarak yer almıyorsa "benzer ifade" uydurulamaz; doğrudan `BULUNAMADI` yazılır.

---

## 🚫 3. SIFIR TAHMİN, SIFIR PROJEKSİYON VE SIFIR SENTETİK VERİ
1. **Tahmin / Projeksiyon Yasağı:**
   - "Genel kabul", "makul piyasa beklentisi", "enflasyon tahmini", "2026/2027 projeksiyonu" kanıt değildir.
   - Yalnızca fiilen yayımlanmış resmî liste veya hakemli ölçüm değeri geçerlidir.
2. **Sentetik Sayı Yasağı:**
   - Yazılım kendi analizini (`truss_model.py` vb.) bizzat çalıştırıp teyit edecektir. Çalıştırılamıyorsa kullanıcıya derhal `ANALİZ ÇALIŞTIRILAMADI` olarak raporlanacaktır.
   - Literatür ve piyasa verilerinde birincil kaynağı bulunamayan değerler `DOĞRULANAMADI` kalacaktır.

---

## 📊 4. MADDELERE ÖZEL AYRI DURUM BİLDİRİMİ VE TOPLU "%100" YASAĞI
1. **Toplu "%100 Doğrulandı" İfadeleri KESİNLİKLE YASAKTIR:**
   - Bütün listeyi toptan onaylayan ifadeler kullanılmayacaktır.
2. **Kalem Kalem Durum:**
   - Her veri satırı için ayrı ayrı şu durum kodlarından biri atanacaktır:
     - `DOĞRULANDI (belge adı + sayfa/poz no)`
     - `KISMEN (açıklama ve eksik yön)`
     - `DOĞRULANAMADI (belgede değer yer almıyor)`
     - `BULUNAMADI (aranan kalem resmî kaynakta mevcut değil)`
     - `ERİŞİLEMEDİ (404, üyelik/giriş duvarı, paywall)`

---

## 🌐 5. BAĞLANTI SAĞLIĞI VE ERİŞİLEMEZLİK PROTOKOLÜ
1. **Çalışmayan Link Kanıt Gösterilemez:**
   - 404, DNS hatası veya bot engeli veren bağlantılar kesinlikle kanıt olarak sunulamaz.
   - Hound MCP, CrossRef ve `curl`/urllib ile taranıp HTTP 200 doğrulaması yapılacaktır.
2. **Kullanıcıdan Açık Talep:**
   - Ücretli (paywall), form/üyelik veya kimlik doğrulama gerektiren kaynaklar `ERİŞİLEMEDİ` olarak işaretlenir; sayfa linki ve dosya tam adı belirtilerek kullanıcıdan manuel indirmesi talep edilir.

---

## 📋 6. STANDART RAPORLAMA ÇIKTILARI
Her araştırma turunda iki temel çıktı zorunludur:
1. `*_EVIDENCE_*.md`: İndirilen belgeler tablosu (Ad, Boyut, SHA-256, URL) + Bulgular tablosu (Belge, Sayfa/Poz, Birebir Alıntı, Durum) + Kullanıcının manuel yapması gerekenler.
2. `*_SOURCES_*.csv`: Standart sütunlu makinece okunabilir kaynak matrisi.
