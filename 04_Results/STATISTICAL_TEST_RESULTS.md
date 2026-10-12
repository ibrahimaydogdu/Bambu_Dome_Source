# 📊 BambuDome Meta-Sezgisel Kampanya Istatistiksel Degerlendirme Raporu

Bu rapor; Secilen meta-sezgisel optimizasyon algoritmalarinin (ABC, ACO, DO) 3 kubbe topolojisi ve 30 bagimsiz tohum
(1001–1030) uzerindeki stokastik performansini, Friedman sira testini ve Wilcoxon rank-sum (Mann-Whitney U, Holm duzeltmeli) ikili karsilastirmalarini icerir.

---

## 1. Betimsel Istatistikler (Descriptive Statistics)

| Model | Algorithm | Runs | Feasible | Weight_Best | Weight_Median | Weight_Mean | Weight_Std | Carbon_Mean | NFE_Mean | Time_s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| geodesic16 | ABC | 30 | 30/30 | 5.8004 | 5.8936 | 5.8801 | 0.0515 | 836.7110 | 23000.0 | 23.3031 |
| geodesic16 | ACO | 30 | 30/30 | 5.8418 | 6.1221 | 6.1828 | 0.3110 | 847.3371 | 23000.0 | 49.9032 |
| geodesic16 | DO | 30 | 30/30 | 6.1784 | 6.4482 | 6.4877 | 0.2094 | 890.9812 | 23000.0 | 32.3089 |
| kiewitt32 | ABC | 30 | 30/30 | 41.0582 | 41.0582 | 41.0582 | 7.23e-15 | 4829.0 | 22000.0 | 101.6357 |
| kiewitt32 | ACO | 30 | 30/30 | 41.0582 | 41.7614 | 42.2808 | 1.3928 | 4825.5 | 22000.0 | 127.6599 |
| kiewitt32 | DO | 30 | 30/30 | 41.3482 | 43.0455 | 42.9219 | 0.8757 | 4978.7 | 22000.0 | 110.3861 |
| ribbed40 | ABC | 30 | 30/30 | 66.3516 | 66.3652 | 66.4516 | 0.1939 | 10995.8 | 43000.0 | 729.8143 |
| ribbed40 | ACO | 30 | 30/30 | 66.3516 | 67.0505 | 66.9078 | 0.4741 | 10983.5 | 43000.0 | 826.0658 |
| ribbed40 | DO | 30 | 30/30 | 71.8031 | 74.3937 | 74.4041 | 1.3963 | 11828.7 | 43000.0 | 759.6666 |

---

## 2. Friedman Siralama Testi (Friedman Rank Test)

### Model: `geodesic16`
- **Friedman $\chi^2_F$:** 48.600
- **Asymptotic $p$-degeri:** 2.7967e-11 (p < 0.001, Guclu Anlamlilik)

**Algoritmalarin Ortalama Siralamalari (Mean Ranks - Dusuk sira daha basarilidir):**

| Algoritma | Ortalama Sira |
| --- | --- |
| ABC | 1.1000 |
| ACO | 2.0000 |
| DO | 2.9000 |

### Model: `kiewitt32`
- **Friedman $\chi^2_F$:** 38.264
- **Asymptotic $p$-degeri:** 4.9096e-09 (p < 0.001, Guclu Anlamlilik)

**Algoritmalarin Ortalama Siralamalari (Mean Ranks - Dusuk sira daha basarilidir):**

| Algoritma | Ortalama Sira |
| --- | --- |
| ABC | 1.2333 |
| ACO | 2.0333 |
| DO | 2.7333 |

### Model: `ribbed40`
- **Friedman $\chi^2_F$:** 49.160
- **Asymptotic $p$-degeri:** 2.1140e-11 (p < 0.001, Guclu Anlamlilik)

**Algoritmalarin Ortalama Siralamalari (Mean Ranks - Dusuk sira daha basarilidir):**

| Algoritma | Ortalama Sira |
| --- | --- |
| ABC | 1.2500 |
| ACO | 1.7500 |
| DO | 3.0000 |

---

## 3. Wilcoxon Rank-Sum (Mann-Whitney U) Karsilastirmalari

Isaret Notasyonu (Holm-duzeltmeli $p < 0.05$): `+` Kontrol algoritmasi istatistiksel olarak ustun, `-` Rakip ustun, `~` Anlamli fark yok.

### Model: `geodesic16`
| Comparison | Diff_Median | U_Stat | p_value | A12_rakip_kotu | Sig_005 | p_Holm |
| --- | --- | --- | --- | --- | --- | --- |
| ABC vs ACO | 0.2286 | 764.5000 | 3.40e-06 | 0.8494 | + | 3.40e-06 |
| ABC vs DO | 0.5546 | 900.0000 | 2.97e-11 | 1.0000 | + | 5.94e-11 |

### Model: `kiewitt32`
| Comparison | Diff_Median | U_Stat | p_value | A12_rakip_kotu | Sig_005 | p_Holm |
| --- | --- | --- | --- | --- | --- | --- |
| ABC vs ACO | 0.7032 | 690.0000 | 5.27e-06 | 0.7667 | + | 5.27e-06 |
| ABC vs DO | 1.9872 | 900.0000 | 1.21e-12 | 1.0000 | + | 2.42e-12 |

### Model: `ribbed40`
| Comparison | Diff_Median | U_Stat | p_value | A12_rakip_kotu | Sig_005 | p_Holm |
| --- | --- | --- | --- | --- | --- | --- |
| ABC vs ACO | 0.6852 | 682.5000 | 5.53e-04 | 0.7583 | + | 5.53e-04 |
| ABC vs DO | 8.0284 | 900.0000 | 2.84e-11 | 1.0000 | + | 5.67e-11 |
