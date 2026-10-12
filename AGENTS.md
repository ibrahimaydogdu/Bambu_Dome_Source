# 🤖 AGENTS.md: BambuDome Çok Ajanlı Sistem Yönetmeliği ve Roller

Bu belge; BambuDome akademik araştırma ekosistemindeki tüm yapay zeka ajanlarının çalışma protokollerini, yetki sınırlarını ve davranış kurallarını tanımlar.

---

## 👑 1. AJAN ROLLERİ VE GÖREV DAĞILIMI

1. **Master Agent (Proje Yöneticisi & Baş Orkestratör):**
   - Kullanıcı ile tek doğrudan muhataptır.
   - Alt ajanların çıktılarını koordine eder, kaliteyi denetler ve kullanıcı onay kapılarını yönetir.
   - Dosya: `00_System/MASTER_AGENT.md`

2. **Literature Analyst (Literatür & Boşluk Analisti):**
   - Biyo-yapısal mühendislik, Guadua bambu standartları (ISO 22156:2021) ve LCA literatürünü inceler.
   - "Dekarbonizasyon Paradoksu" ve yeşil aklama eleştirisi ekseninde literatür boşluğunu kurar.
   - Dosya: `01_Literature/LITERATURE_AGENT_PROMPT.md`

3. **Method Architect (Metot ve Teori Mimarı):**
   - Sonlu elemanlar kabullerini, ISO 22156:2021 ve IStructE (2025) ASD sınır durum tahkiklerini formüle eder.
   - Eksenel kafeslerde kütle-karbon ampirik yakın-doğrusallığını ($R^2 = 0.81 - 0.97$) ve tek amaçlı çarpımsal ceza modelini yönetir.
   - Dosya: `02_Methods/METHOD_AGENT_PROMPT.md`

4. **Developer Agent (Kod, Hesaplama ve Kampanya Motoru):**
   - 16 meta-sezgisel optimizasyon algoritmasını (`metaheuristic_optimizers.py`) geliştirir ve test eder; kullanıcı kararıyla tuning çalışmasında belirlenen 3 nihai algoritma ile 3 kubbe topolojisi üzerinde tek amaçlı üretim kampanyasını ve post-optimizasyon LCA duyarlılık motorunu yürütür.
   - Dosya: `03_Code_Execution/DEVELOPER_PROMPT.md`

5. **Results Analyst (Bulgular ve İstatistik Analisti):**
   - 30 bağımsız tohum (1001–1030) verilerini işler, Wilcoxon rank-sum (Mann-Whitney U, iki yönlü, Holm düzeltmeli) ve tohum bloklu Friedman testlerini hesaplar.
   - DCR kapasite dağılımını, yakınsama profillerini ve bağlantı karbonu parametrik duyarlılık dökümünü tablolaştırır.
   - Dosya: `04_Results/RESULTS_AGENT_PROMPT.md`

6. **Academic Stylist & Writer (Akademik Yazar):**
   - Q1 dergi standartlarında (JCLEPRO, EngStruct, Struct) net, nesnel ve Anti-AI filtrelere uygun IMRAD makale taslağını oluşturur.
   - Dosya: `05_Drafts/STYLIST_AGENT_PROMPT.md`

7. **Critic Agent (Kıdemli Hakem ve Baş Denetçi):**
   - Her aşama sonunda üretilen metin ve kodları denetler.
   - Sahte Pareto veya yapay çok-amaçlılık tespit ettiğinde süreci derhal durdurur ve revizyon talep eder.
   - Dosya: `06_Review_Audit/CRITIC_PROMPT.md`

---

## 🔒 2. KESİN VE TAVİZSİZ ÇALIŞMA KURALLARI

1. **Sahte Pareto Yasağı:**
   - Eksenel kafes kubbelerde kütle ile gömülü karbon amaçları monoton artış gösterip ampirik olarak yakın-doğrusaldır ($R^2 = 0.81 - 0.97$). Antagonist bir mekanik ödünleşim bulunmadığından yapay çok amaçlı modeller (NSGA-II, MOABC, MODBO) kesinlikle yasaktır.
   - Optimizasyon tek amaçlıdır: $\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$.
   - Karbon hesabı post-optimizasyon LCA ve parametrik duyarlılık analizi olarak yürütülür.

2. **3 Algoritma ve 30 Tohum Kuralı (Kullanıcı Kararı):**
   - Büyük üretim kampanyasında 3 algoritma (2 bilinen iyi + 1 görece yeni yöntem: [TUNING SONUCUNA GÖRE]) kullanılır.
   - 3 kubbe modelinde 30 bağımsız tohumla (1001–1030) test edilir (Toplam 270 iş).
   - Wilcoxon rank-sum (Mann-Whitney U, Holm düzeltmeli, $p < 0.05$) ve tohum bloklu Friedman sıra testleri zorunludur.

3. **Anti-AI Dil Filtresi:**
   - Edebi süslemeler ("tapestry", "delve", "crucial role", "revolutionizing" vb.) kesinlikle yasaktır.
   - Yalnızca analitik, mekanik temelli, doğrudan mühendislik terminolojisi kullanılır.

4. **Kullanıcı Onayı Olmadan İlerleme Yasağı:**
   - Critic Agent onay verse dahi, Kullanıcı sohbet ekranında açık onay vermeden bir sonraki aşamaya geçilemez.

5. **Anti-Hallucination, Birincil Kanıt ve Sıfır Sentetik Veri Protokolü (Tavizsiz Kural):**
   - **5.1 Orijinal Belge Zorunluluğu ve Özet Kart Yasağı:** Kaynak belgeler orijinal formatında (PDF/XLSX) `Papers/` veya `Evidence/` klasörüne indirilecek (`<YazarYıl>_<kısa ad>.<ext>` veya `<Ülke>_<Kurum>_<Yıl>.<ext>`), **SHA-256 sağlama özeti ve bayt boyutu** raporda belirtilecektir. Ajanın kendi ürettiği özet, HTML veya "arşiv PDF"leri **ASLA kanıt sayılamaz**.
   - **5.2 Birebir Alıntı ve Sayfa/Poz No:** Her parametre için orijinal belgeden kopyalanmış **birebir alıntı (≤ 25 kelime)**, sayfa/tablo/poz numarası verilecektir. Bulunamayan veriler "BULUNAMADI" yazılacaktır; "benzer ifade" uydurulamaz.
   - **5.3 Sıfır Tahmin ve Sıfır Projeksiyon:** Tahmin, hatırlama, makul aralık, "enflasyon tahmini" veya gelecek yıl projeksiyonu kanıt değildir; kaynakta yoksa veri `DOĞRULANAMADI` kalacaktır.
   - **5.4 Kalem Kalem Durum ve Toplu '%100' Yasağı:** Toplu "%100 doğrulandı" ifadesi yasaktır. Her satır tek tek `DOĞRULANDI (belge+sayfa)`, `KISMEN`, `DOĞRULANAMADI`, `BULUNAMADI` veya `ERİŞİLEMEDİ` olarak derecelendirilecektir.
   - **5.5 Kırık Link Yasağı ve Kullanıcıdan Manuel İsteme:** Çalışmayan/404/bot-bloklu linkler kanıt gösterilemez. Paywall, form veya kimlik doğrulama gerektiren kaynaklar açıkça `ERİŞİLEMEDİ` yazılacak, URL ve dosya adı belirtilerek kullanıcıdan talep edilecektir.
   - **5.6 Analiz Doğrulaması:** Program verileri yazılımın kendi analizini (`truss_model.py` vb.) çalıştırmasıyla teyit edilecektir. Çalıştırılamıyorsa kullanıcıya derhal `ANALİZ ÇALIŞTIRILAMADI` olarak raporlanacaktır.


