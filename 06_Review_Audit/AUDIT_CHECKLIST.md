# 📋 AUDIT_CHECKLIST.md (Resmi Hakem Denetim Cetveli)

Bu belge, Critic Agent'ın herhangi bir bölüme onay vermeden önce eksiksiz olarak doğrulamak ZORUNDA olduğu kontrol listesidir. Hakem, ürettiği denetim raporunda bu maddelerin her birini `[EVET / HAYIR]` ve somut gerekçelerle beyan etmek zorundadır.

---

## 🛑 BÖLÜM 1: GENEL VE BİÇİMSEL KRİTERLER (HER AŞAMA İÇİN ZORUNLU)
- [ ] **Anti-AI İhlali Yok:** Metinde `SYSTEM_RULES.md` kara listesindeki kelimeler (*delve, tapestry, crucial testament, paramount, game-changer, pivotal role, beacon, plethora, ever-evolving, realm, holistic, foster* vb.) kesinlikle kullanılmamış.
- [ ] **Nesnel Ton:** Aşırı iddialı (*revolutionary, astonishing, unprecedented*) sıfatlar yerine ölçülebilir, sayısal ve kanıta dayalı ifadeler kullanılmış.
- [ ] **Hafıza Tutarlılığı:** `PROJECT_STATE.md`'de daha önceki turlarda reddedilen hatalar aynen tekrarlanmamış.

---

## 📚 BÖLÜM 2: AŞAMA BAZLI KRİTERLER

### A. Literatür ve Giriş Aşaması (`01_Literature`)
- [ ] **Gerçek Araştırma Boşluğu (Research Gap):** Gösterilen eksiklik yapay değil; bambu kubbe sistemlerinde ISO 22156 / IStructE (2025) ASD standart kısıtları, eksenel kafeslerde kütle-karbon ampirik yakın-doğrusallığı ($R^2 = 0.81 - 0.97$), sahte Pareto yanılgısı ve bağlantı elemanı kaynaklı Dekarbonizasyon Paradoksu parametrik duyarlılığı literatür temeline oturtulmuş mu?
- [ ] **Tematik Sınıflandırma:** Kaynaklar kronolojik dizilmemiş; Bambu Mekaniği/ASD Tasarımı, Kubbe Optimizasyonu, Gömülü Karbon/LCA ve Hesaplamalı FEA Otomasyonu temalarına göre gruplanmış mı?
- [ ] **Özgün Değerin (Novelty) Netliği:** Çalışmanın literatüre sunacağı yenilik (ASD standardı ve biyo-yapısal mesh adaptasyonu, Dekarbonizasyon Paradoksu duyarlılığı, titiz stokastik optimizasyon) somut maddelerle ilan edilmiş mi?

### B. Metodoloji Aşaması (`02_Methods`)
- [ ] **2 Katmanlı Yapı:** Destekleyici standart yöntemler (Katman 1: 3D kubbe FEA modelleme prensipleri, ISO 22156 / IStructE 2025 ASD formülasyonu, A1–A3 LCA modeli, kıyaslama algoritmaları) ile önerilen yöntem (Katman 2: Çarpımsal ceza fonksiyonlu tek amaçlı yapısal ağırlık optimizasyonu, 3 algoritmalı kampanya mimarisi) net ayrılmış mı?
- [ ] **Sahte Pareto Yasağı ve Tek Amaçlı Formülasyon:** Kütle-karbon ampirik yakın-doğrusallığı ($R^2 = 0.81 - 0.97$) açıklanmış; problem kesin olarak $\min f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$ ($\varepsilon = 2.0$) tek amaçlı ağırlık minimizasyonu olarak formüle edilmiş mi?
- [ ] **ASD Formül Bütünlüğü (IStructE Manual 2025 / ISO 22156):** İzinli gerilme tasarımı ($X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$, $FS=2$, $C_R=0.90$ [varsayım]), çekme ($DCR_{\text{tens}} \le 1.0$), Ylinen kusur parametreli ($c = 0.8$, $b_0 = 0.01$ [varsayım]) Euler burkulması ($DCR_{\text{buck}} \le 1.0$), narinlik sınırı ($\lambda \le 150$, hem çekme hem basınçta muhafazakar tahkik; NSR-10 G.12.9.2.6/7 yalnızca basınç için $\lambda \le 150$ şartı koşar), bağlantı sınırı ($F_{j,Rd} = 49.3\text{ kN}$, $n_{\text{bolt}}=4$, NSR-10 Tabla G.12.11-2/3 izin verilen yük) ve servis deplasmanı ($u_{\max} \le S/150 = 266.67\text{ mm}$) denklemleri eksiksiz tanımlanmış mı?
- [ ] **Ayrık Kesit Eşleme:** 24 elemanlı Guadua angustifolia kataloğundan tamsayı indeks eşleme operatörü matematiksel olarak verilmiş mi?

### C. Kod ve Simülasyon Aşaması (`03_Code_Execution`)
- [ ] **FEA & Rijitlik Çözücü Doğruluğu:** Doğrudan rijitlik çözücüsü SAP2000 sonuçlarıyla eksenel kuvvet, deplasman ve DCR bazında doğrulanmış mı?
- [ ] **3 Algoritmalı Kampanya Tasarımı:** Kampanyada `04_Results/TUNING_STUDY.md` duyarlılık analizinden seçilen 3 nihai algoritma (ABC pop 20, ACO pop 40, DO pop 40) koşturuluyor mu?
- [ ] **Hesaplama Bütçesi:** Değerlendirme sayısı bütçesi $\text{NFE} = 1000 \times \text{tasarım değişkeni sayısı}$ kuralına uygun mu?
- [ ] **Kampanya Güvenliği ve Checkpoint:** 30 bağımsız tohum (1001–1030) x 3 kubbe x 3 algoritma = 270 koşu için deterministik RNG checkpoint ve değerlendirme başına `.npz` kaydı tutulmuş mu?

### D. Bulgular ve Tartışma Aşaması (`04_Results`)
- [ ] **30 Tohum İstatistiksel Titizliği:** Her model ve 3 algoritma için Min, Mean, Median, Max, Standart Sapma, Feasibility Oranı (%) ve CPU süreleri tam verilmiş mi?
- [ ] **İstatistiksel Hipotez Testleri:** İki yönlü Holm-düzeltmeli Wilcoxon Rank-Sum / Mann-Whitney U ($p < 0.05$, Vargha-Delaney $A_{12}$) ve tohum bloklu Friedman sıra testleri hesaplanmış mı?
- [ ] **Dekarbonizasyon Paradoksu ve Parametrik Duyarlılık:** Bağlantı bileşenlerinin payı parametrik duyarlılık çerçevesinde incelenmiş, ön-yazılı sabit yüzdelerden kaçınılmış mı?
- [ ] **Kolinierite Doğrulaması:** Kütle vs. karbon dağılım grafiğinde $R^2 = 0.81 - 0.97$ korelasyon ile Pareto cephesinin tek noktaya / dar aralığa çöktüğü ampirik olarak gösterilmiş mi?
- [ ] **Dürüst Kısıtlar (Limitations):** Malzeme doğal varyasyonu, $n_{\text{bolt}}=4$ cıvata kabulü ve ribbed40'ta 12 kısa elemanın (%0.82) 3 cıvatayı boyuna sığdıramama geometrik kısıtı, mafsal idealleştirmesi ve LCA envanter varsayımları açıkça tartışılmış mı?

---

## 🎯 BÖLÜM 3: ÇALIŞMAYA ÖZEL TEKNİK KRİTERLER
- [ ] **Gömülü Karbon Sınırı (LCA):** Beşikten-kapıya (A1–A3) sınırlar içinde bambu gövde ($EC_b = 0.30\text{ kg CO}_2\text{e/kg}$ türetilmiş baz değer), çelik levha ($EC_s = 2.38\text{ kg CO}_2\text{e/kg}$ ICE V5.0) ve harç dolgusu ($EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ ICE V5.0 1:3 harç vekili) literatür ve veritabanı kabulleri olarak belirtilmiş mi? Çelik boru katsayısı (2.51) yalnızca çelik referans kubbede (T5–T8) mi kullanılmış?
- [ ] **Narinlik Sınırı:** Hiçbir bambu elemanı (çekme ve basınç) $\lambda > 150$ sınırını aşmamış mı? [NSR-10 G.12.9.2'ye göre çekmeye uygulanması bilinçli muhafazakar bir kabüldür].
- [ ] **Birim Tutarlılığı:** Analiz (kN, m), gerilme (MPa, kPa) ve karbon (kg $CO_2e$) birimleri arasında tam tutarlılık sağlanmış mı?