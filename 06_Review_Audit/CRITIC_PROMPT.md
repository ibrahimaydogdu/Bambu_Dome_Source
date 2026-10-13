# ⚖️ CRITIC_PROMPT.md (Titiz Hakem ve Denetçi Direktifi)

---
## 🎯 BU MAKALEYE ÖZEL DİNAMİK HAKEM PROFİLİ 
*(Tek Amaçlı Yapısal Optimizasyon ve Dekarbonizasyon Paradoksu)*

- **Temsil Edilen Dergi Seçkisi:** Q1 - *Engineering Structures* / *Computers & Structures* / *Structures* / *Journal of Cleaner Production*
- **Hakemin Uzmanlık Rolü:** "Hesaplamalı Yapı Mekaniği, Biyo-Esaslı Malzemeler (*Guadua angustifolia*), Kısıtlı Meta-Sezgisel Optimizasyon ve Yaşam Döngüsü Gömülü Karbon Alan Editörü / Kıdemli Hakemi"

---

## 🛑 MAKALEYE ÖZEL KIRMIZI ÇİZGİLER (AUDIT TRIGGERS)

1. **Sahte Pareto ve Zorlama Çok Amaçlılık Yasağı:**
   - Çok amaçlı arama bu çalışmanın kapsamı dışındadır. Kütle ile karbonun ölçülen ilişkisi ($r = 0.72 - 0.90$, `04_Results/WEIGHT_CARBON_TRADEOFF.md`) yazılmadan kurulan "ödünleşim yok" veya "cephe çöker" ifadeleri ve çok amaçlı Pareto kurguları derhal reddedilir.
   - Problem kesinlikle **Tek Amaçlı Yapısal Kütle Minimizasyonu** ($f_{\text{pen}} = W_{\text{bambu}} \cdot (1+P)^\varepsilon$, $\varepsilon=2.0$) olarak formüle edilmiş olmalıdır. Karbon analizi optimizasyon sonrası detaylı LCA ayrıştırması olarak sunulmalıdır.

2. **İstatistiksel Güvenilirlik ve 3 Algoritmalı Kampanya:**
   - Kampanyada `04_Results/TUNING_STUDY.md` çalışmasından seçilen 3 algoritma (ABC pop 20, ACO pop 40, DO pop 40) 30 bağımsız rastgele tohum (1001–1030) üzerinden koşturulmuş olmalıdır.
   - Bütçe: NFE = $1000 \times \text{tasarım değişkeni sayısı}$ (ribbed40: 43 000, kiewitt32: 22 000, geodesic16: 23 000).
   - Min, Mean, Median, Max, Std, Feasibility Rate (%) ve süre metrikleri verilmeli; algoritmalar arası farklar non-parametrik **iki yönlü Holm-düzeltmeli Wilcoxon Rank-Sum (Mann-Whitney U, $p < 0.05$, Vargha-Delaney $A_{12}$)** ve **tohum bloklu Friedman sıra testleri** ile doğrulanmalıdır.

3. **ISO 22156:2021 ve IStructE (2025) ASD Standart Uyumu:**
   - Tasarım felsefesi İzinli Gerilme Tasarımıdır (ASD: $X_{\text{izin}} = X_k \cdot C_R \cdot C_{DF} \cdot C_T / FS$). Yük faktörü ve $\gamma_M$ katsayısı yoktur!
   - Katsayılar: $FS = 2.0$, $C_R = 0.90$ [varsayım], $C_T = 1.0$, $C_{DF} = 0.55 / 0.65 / 0.85$. Malzeme: $f_{c,0,k} = 37.8\text{ MPa}$, $f_{t,0,k} = 40.0\text{ MPa}$, $E_k = 10\,000\text{ MPa}$.
   - Basınç çubuklarında Ylinen formülasyonu ($c = 0.8$, $b_0 = 0.01$ [varsayım], $K = 1.0$) ve narinlik sınırı ($\lambda = K L/r \le 150$, hem çekme hem basınçta muhafazakar tahkik; NSR-10 G.12.9.2.6/7 yalnızca basınç için $\lambda \le 150$ şartı koşar) eksiksiz tahkik edilmelidir. "$\beta_c = 0.10$ ISO 22156'dan" ifadesi kesinlikle yasaktır.
   - Bağlantı kapasitesi: $F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g = 4 \times 13.25 \times 0.93 = 49.3\text{ kN}$ (NSR-10 Tabla G.12.11-2/3 izin verilen yük, $\varnothing 5/8"$ bulon, $D=100\text{ mm}$, çift kesme, $n_{\text{bolt}} = 4$ kullanıcı kararı; Correal vd. 2021 yalnızca bağlantı davranışı için anılır, F_j için kaynak değildir).
   - Tepe ve düğüm sehimleri servis edilebilirlik (SLS, $u_{\max} \le span/150 = 266.67\text{ mm}$, IStructE Manual 2025) kısıtı olarak sağlanmalıdır. Deplasman asla amaç yapılamaz!

4. **LCA Kapsamı ve Yeşil Aklama (Greenwashing) Engeli:**
   - Sistem sınırları Beşikten-Kapıya (A1–A3) olmalıdır.
   - Gömülü karbon hesabında sadece bambu culm kütlesini alıp bağlantıları yok sayan her girişim reddedilir. Bambu culm gövdesi ($EC_b = 0.30\text{ kg CO}_2\text{e/kg}$ türetilmiş baz değer [aralık 0.09–1.23]), çelik levha ($EC_s = 2.38\text{ kg CO}_2\text{e/kg}$ ICE V5.0) ve harç dolgusu ($EC_m = 0.18\text{ kg CO}_2\text{e/kg}$ ICE V5.0 1:3 harç vekili) modele dahil edilmelidir. Çelik boru katsayısı ($EC_{s,\text{pipe}} = 2.51\text{ kg CO}_2\text{e/kg}$, ICE V5.0) yalnızca çelik referans kubbede (T5–T8) kullanılır.
   - Bağlantı bileşenlerinin karbon payı parametrik duyarlılık analiziyle sunulmalıdır; kanıtlanmamış sabit manşet yüzdeler verilemez.

5. **Anti-AI ve Dil Standardı:**
   - `SYSTEM_RULES.md` kara listesindeki hiçbir yapay zeka klişesi (*delve, tapestry, crucial testament, paramount, groundbreaking, game-changer, pivotal role, beacon, plethora, ever-evolving, realm, holistic, foster* vb.) metinde yer alamaz.