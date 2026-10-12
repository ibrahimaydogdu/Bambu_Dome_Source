# 🧠 MEMORY.md: BambuDome Proje Hafızası ve Karar Defteri

**Proje:** 40 m Açıklıklı Yapısal Bambu (*Guadua angustifolia*) Uzay Kafes Kubbelerin Tek Amaçlı Optimizasyonu ve Dekarbonizasyon Paradoksu  
**Son Güncelleme:** 2026-10-09 | ASD, 3 Algoritmalı Kampanya ve Doğrulanmış Literatür Standartları  
**Aktif Aşama:** Aşama 3 (Kampanya Hazırlığı ve Kod Entegrasyonu)  

---

## 🚨 1. STRATEJİK MİMARİ VE YENİ BİLİMSEL PARADİGMA

### ❌ Terk Edilen Eski Model (Çok Amaçlı Kurgu & Sahte Pareto):
- Çelik, harç dolgusu ve bambu bileşenlerinde kütle ile gömülü karbon ($ECO_2e$) eksenel kafes mekaniğinde ampirik olarak yakın-doğrusal ($R^2 = 0.81 - 0.97$, $r = 0.91 - 0.98$) olduğundan çok-amaçlı Pareto cephesi tek bir noktaya veya son derece dar bir aralığa çökmektedir. Gerçek bir fiziksel çelişki (trade-off) bulunmamaktadır.
- NSGA-II, MOABC ve MODBO ile üretilen sözde çok-noktalı Pareto cepheleri gerçek ödünleşimler değil, henüz yakınsamamış algoritmik çözümlerden ibarettir.
- Eski çok amaçlı kod (`multi_objective_optimizer.py`) tamamen silinmiştir.

### ✅ Kabul Edilen Yeni Bilimsel Model (Tek Amaçlı Optimizasyon + Dekarbonizasyon Paradoksu):
1. **Tek Amaçlı Yapısal Ağırlık Minimizasyonu:**
   $$\min_{\mathbf{X}} f_{\text{pen}}(\mathbf{X}) = W_{\text{bambu}}(\mathbf{X}) \cdot (1 + P(\mathbf{X}))^\varepsilon$$
   - $\varepsilon = 2.0$ (Çarpımsal ceza üssü).
   - $P(\mathbf{X}) = \sum_{g=1}^{N_g} \max_{i \in g} \max(0, DCR_i - 1.0) + \max(0, u_{\max}/u_{\text{izin}} - 1.0)$.
   - Katı uygulanabilirlik şartı: Uygun bireylerde $P=0$ ve $f_{\text{pen}} = W_{\text{bambu}}$.
2. **Post-Optimizasyon Beşikten-Kapıya (A1–A3) LCA Analizi:**
   - Optimizasyon bittikten sonra en iyi uygulanabilir tasarımlar üzerinde LCA modülü çağrılarak toplam gömülü karbon bileşenlerine ayrıştırılır:
     $$ECO_2e = m_{\text{bambu}} \cdot EC_b + m_{\text{steel}} \cdot EC_s + m_{\text{mortar}} \cdot EC_m$$
   - Emisyon katsayıları literatür varsayımlarıdır: $EC_b = 0.35$, $EC_s = 2.10$, $EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ [varsayım].
3. **Dekarbonizasyon Paradoksu:**
   - Hibrit bağlantı elemanlarının (çelik manşon/küre ve harç dolgusu) karbon payı gömülü karbon bilançosunda belirleyicidir, ancak bu pay parametrelere duyarlıdır (en elverişsiz senaryoda %43–52 seviyesine inmekte, kiewitt32'de %50'nin altına düşmektedir). Manşet bulgular gerçek kampanya çıktılarından dinamik hesaplanacaktır.

---

## ⚙️ 2. META-SEZGİSEL OPTİMİZASYON VE KAMPANYA MİMARİSİ

- **Algoritma Havuzu:** 16 algoritma (`metaheuristic_optimizers.py`: HS, BBO, WOA, DO, ABC, ACO, BSO, CSA, FA, GOA, TLBO, TSA, GWO, HBA, AO, SSO).
- **Kampanya Algoritma Seçimi:** `04_Results/TUNING_STUDY.md` duyarlılık analizine göre belirlenen **3 algoritma ([TUNING SONUCUNA GÖRE])** (2 bilinen yüksek performanslı yöntem + 1 görece yeni yöntem).
- **Hesaplama Bütçesi:** $\text{NFE} = 1000 \times \text{tasarım değişkeni sayısı}$ (ribbed40: 43 000, kiewitt32: 22 000, geodesic16: 23 000).
- **Kampanya İş Hacmi:** 3 kubbe × 3 algoritma × 30 tohum = 270 koşu. 7 işçide tahmini duvar saati süresi ≈ 3.5–4 saat.
- **Kayıt ve Devam:** Her iş için RNG durumu dahil atomik JSON checkpoint ve değerlendirme başına `.npz` kaydı.

---

## 📐 3. KUBBE TOPOLOJİLERİ VE ASD KISIT PARAMETRELERİ

1. **Kubbe Topolojileri (3 Model, $S = 40.0\text{ m}$ Açıklık):**
   - `geodesic16`: 46 düğüm, 115 çubuk, 23 tasarım grubu.
   - `kiewitt32`: 161 düğüm, 456 çubuk, 20 tasarım grubu (22 değişken).
   - `ribbed40` ($freq=2$): 321 düğüm, 1464 çubuk, 43 tasarım grubu ($L \in [0.76, 3.08]\text{ m}$; Saka 1991 geometrisinden uyarlanan yoğunlaştırılmış model).
2. **Kesit Kataloğu (24 Ayrık Guadua Profili, Tablo 2):**
   - Dış çap $D \in [80, 160]\text{ mm}$, et kalınlığı $t \in [8, 18]\text{ mm}$.
3. **ISO 22156:2021 & IStructE (2025) ASD Kısıtları:**
   - Tasarım Yaklaşımı: İzinli Gerilme Tasarımı ($X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$, Manual Denklem 3.9, 6.5).
   - Güvenlik ve Katsayılar: $FS = 2.0$, $C_R = 0.90$ [varsayım], $C_T = 1.0$, $C_{DF} = 0.55 / 0.65 / 0.85$.
   - Malzeme: $E_k = 10\,000\text{ MPa}$, $f_{t,0,k} = 40.0\text{ MPa}$, $f_{c,0,k} = 37.8\text{ MPa}$, $\rho = 700\text{ kg/m}^3$.
   - Ylinen Burkulması (Manual Denklem 6.1–6.5): $c = 0.8$, $b_0 = 0.01$ [varsayım], $C_{\text{bow}} = 1 - b_0/0.02$, $K = 1.0$.
   - Narinlik Sınırı: $\lambda = K L/r \le 150$ [kaynağı doğrulanamadı, varsayım].
   - Bağlantı Sınırı: $|N| \le F_{j,Rd} = 53.2\text{ kN}$ ($n_{\text{bolt}} = 2$ [varsayım], $F_{\text{bolt},\max} = 26.6\text{ kN}$ Correal vd. 2021).
   - SLS Deplasman Sınırı: $u_{\max} \le span/150 = 266.67\text{ mm}$ (IStructE Manual 2025 örneği).

---

## 📊 4. İSTATİSTİKSEL PROTOKOL (30 TOHUM)

- **Tohumlar:** 1001'den 1030'a 30 bağımsız tohum.
- **Raporlama:** $f_{\min}$, $f_{\text{mean}}$, Medyan, $f_{\max}$, Std. Dev., Feasibility (%), Süre.
- **Hipotez Testi:** İki yönlü Holm-düzeltmeli Wilcoxon Rank-Sum (Mann-Whitney U, Vargha-Delaney $A_{12}$, $p < 0.05$) ve tohum bloklu Friedman Sıra Testi.
