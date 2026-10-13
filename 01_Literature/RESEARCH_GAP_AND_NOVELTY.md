# 🎯 RESEARCH_GAP_AND_NOVELTY.md: Araştırma Boşluğu, Özgün Değer ve Metot Gerekçelendirmesi

## 1. Tespit Edilen Araştırma Boşluğu (Research Gap)

Geniş açıklıklı uzay kafes ve kubbe sistemleri, stadyum, sergi alanı ve hangar gibi büyük alanların örtülmesinde yaygın olarak kullanılmaktadır. Ancak mevcut akademik literatür incelendiğinde dört temel darboğaz ve metodolojik boşluk öne çıkmaktadır:

1. **Ölçek ve Malzeme Kısıtlılığı:**
   Literatürdeki geniş açıklıklı kubbe optimizasyonu çalışmaları (örn. Saka 1991, Hasançebi vd. 2009/2011, Kaveh ve Talatahari 2010 tarafından incelenen 354-elemanlı kubbe benchmarkları) standart çelik boru profiller ile yürütülmüştür (orijinal model 2.9–5.97 m çubuk boylarına sahip olup bambu narinliğini aşmaktadır). Yenilenebilir yapısal bambu (*Guadua angustifolia*) culmları ise çoğunlukla 6–15 metrelik küçük pavyonlarla sınırlı kalmıştır. 40 metrelik endüstriyel açıklıkta biyo-yapısal uzay kafes davranışı ve mesh adaptasyonu ($freq=2$, 1464 eleman, 0.76–3.08 m boylar) araştırılmamıştır.

2. **Modern Standart (ISO 22156:2021 & IStructE 2025) ASD Otomasyonu Eksikliği:**
   Bambu için uluslararası kabul gören güncel tasarım normu olan **ISO 22156:2021** ve yeni **IStructE (2025)** el kitabındaki İzin Verilen Gerilme Tasarımı (ASD) prensipleri ($X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$, Ylinen elastik kararsızlığı $c = 0.8$, $C_{\text{bow}} = 1 - b_0/0.02$, $b_0 = 0.01$ varsayım, $K = 1.0$, narinlik sınırı $\lambda \le 150$ çekme ve basınca uygulanır, bağlantı kapasitesi $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$ NSR-10 Tabla G.12.11-2/3 izinli yük ve $n_{\text{bolt}}=4$ kullanıcı kararı, SLS sehim $\text{span}/150$) sonlu elemanlar optimizasyon süreçlerine tam ve otomatik olarak entegre edilmemiştir.

3. **Literatürdeki Sahte Pareto Yanılgısı:**
   Kafes sistemlerde kütle ile karbonu yapay olarak iki ayrı çelişen amaçmış gibi ele alan çok amaçlı (multi-objective) çalışmalar bulunmaktadır. Oysa eksenel kafeslerde eleman hacminin küçültülmesi bambu kütlesini, bambu karbonunu ve kesit maliyetini aynı anda küçültür; her iki amaç da kesit boyutlarıyla monoton artar ($R^2 = 0.81 - 0.97$). Kütleyi azaltırken karbonu artıran antagonist bir mekanik ödünleşim mekanizması bulunmadığından Pareto cephesi tekil bir optimuma ya da çok dar bir banda çöker. Çok amaçlı algoritmaların sunduğu geniş cepheler ise henüz yakınsamamış algoritmik gürültüdür.

4. **"Dekarbonizasyon Paradoksu" ve Bağlantı Karbonu Duyarlılığı:**
   Mevcut yaşam döngüsü analizleri (LCA) çoğunlukla bambu gövdesinin biyojenik potansiyeline odaklanarak, gerçek bir mühendislik yapısında eksenel yükleri aktarmak için zorunlu olan **çelik düğüm göbekleri, saplamalar ve uç harç dolgularını** ihmal etmekte veya ikincil görmektedir. Geniş açıklıklı bir uzay kubbede gerçekçi beşikten-kapıya (A1–A3) sınırlarında bağlantı elemanlarının toplam karbon bütçesindeki ağırlığını ve parametrik duyarlılığını sistematik olarak ortaya koyan çalışma bulunmamaktadır.

---

## 2. Çalışmanın Özgün Değeri ve Temel Katkıları (Novelty & Contributions)

Bu çalışma, tespit edilen araştırma boşluklarını doldurmak üzere literatüre 4 temel bilimsel katkı sunar:

### Katkı 1: Çelikten Biyo-Kompozite Benchmark Adaptasyonu (40 m Açıklık)
Saka'nın (1991) 40 m açıklıklı çelik kubbe geometrisi ve ASCE 7 yükleri temel alınarak, bambunun narinlik kısıtı nedeniyle $freq=2$ yoğunlaştırması yapılmış ve 1464 elemanlı (çubuk boyları 0.76–3.08 m) biyo-yapısal bir uzay kubbe benchmarkı türetilmiştir.

### Katkı 2: IStructE (2025) & ISO 22156 (2021) ASD Tasarım Otomasyonu
ASCE 7-22 §2.4.1 ASD faktörsüz yük kombinasyonları altında doğrudan rijitlik matrisi ile çekme ($f_{t,k} = 40\text{ MPa}$), Ylinen kararlılığı ($c = 0.8$, $f_{c,k} = 37.8\text{ MPa}$, $E_k = 10,000\text{ MPa}$), narinlik ($\lambda \le 150$, çekme ve basınca uygulanır), mafsal kapasitesi ($F_{j,Rd} = 49.3\text{ kN}$, NSR-10 Tabla G.12.11-2/3) ve servis deplasman ($u \le \text{span}/150$) sınır durumları doğrudan analitik çözücüye entegre edilmiştir.

### Katkı 3: "Dekarbonizasyon Paradoksu" ve Parametrik Duyarlılık Analizi
Biyo-yapısal uzay kafes kubbede hibrit bağlantı elemanlarının (çelik göbek ve harç dolgusu) gömülü karbon bilançosundaki belirleyici ağırlığı ortaya konmuş ve $L_{\text{inj}}/D \in [1.5, 3.5]$, $EC_{\text{steel}}$ ve $EC_{\text{bamboo}}$ parametreleri taranarak duyarlılık sınırları belirlenmiştir (Temel durumda bağlantı payı %74.1–%82.1; birleşik elverişsiz parametre ucunda kiewitt32'de %45.3'e düşerek duyarlılık sergiler).

### Katkı 4: Kütle ve Karbonun Ampirik Yakın-Doğrusallığı ve Stokastik Kıyaslama
Kütle ve karbon amaçları arasındaki ampirik yakın-doğrusallık ($R^2 = 0.81 - 0.97$; ampirik, ispatlanmış kolinearite değil) ölçülerek sahte Pareto modelleri elenmiştir. Titiz tek amaçlı optimizasyon çerçevesinde tuning çalışmasıyla belirlenen 3 meta-sezgisel algoritma (ABC, ACO, DO); 30 bağımsız tohum (1001–1030), NFE = $1000 \times N_{\text{grup}}$ bütçesi, Mann-Whitney U (iki yönlü, Holm düzeltmeli, A12 etki büyüklüğü) ve tohum bloklu Friedman sıra testleri eşliğinde karşılaştırılmıştır.

---

## 3. Metot Seçim Gerekçelendirmesi (Rationale via Literature)

1. **Neden Tek Amaçlı Formülasyon?**
   Eksenel kafeslerde kütle ile karbon amaçları monoton artış gösterip ampirik olarak yakın-doğrusaldır ($R^2 = 0.81 - 0.97$). Antagonist bir mekanik ödünleşim mekanizması bulunmadığından çok amaçlı Pareto arayışı metodolojik olarak geçersizdir. Mühendislik optimizasyonunun amacı; kısıtları tam sağlayan ($P=0$) en hafif yapıyı bulmak, ardından bu tasarım üzerinde detaylı LCA ayrıştırması ve parametrik duyarlılık analizini yürütmektir.

2. **Neden Tuning Temelli 3 Meta-Sezgisel Algoritma?**
   - 16 yöntemlik meta-sezgisel havuz (`metaheuristic_optimizers.py`) geliştirilmiş ve test edilmiştir.
   - 30 tohumluk büyük üretim kampanyasında adil ve odaklı bir karşılaştırma yürütmek amacıyla, hiper-parametre duyarlılık çalışmasından (`04_Results/TUNING_STUDY.md`) elde edilen performansa göre **2 bilinen iyi + 1 görece yeni algoritma** seçilmiştir: **ABC (pop 20), ACO (pop 40), DO (pop 40)**.
