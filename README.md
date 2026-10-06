# BambuDome — Multi-Objective Metaheuristic Optimization of Bamboo Geodesic Dome Structures

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![SAP2000 OAPI](https://img.shields.io/badge/SAP2000-OAPI-orange)](https://www.csiamerica.com/)
[![ISO 22156](https://img.shields.io/badge/Design%20Code-ISO%2022156-green)](https://www.iso.org/standard/77013.html)

---

## Proje Özeti

Bu çalışma, **354-elemanlı bambu geodezik kubbe** sistemlerini iki amaçlı optimizasyon çerçevesinde ele almaktadır:

| Amaç | Tanım |
|------|-------|
| **f₁ (min)** | Toplam yapısal ağırlık [kN] |
| **f₂ (min)** | Beşikten-Kapıya gömülü karbon [kg CO₂e] (bambu + çelik düğüm + harç) |

**Tasarım Kodu:** ISO 22156:2021 (çekme, basınç, Ylinen burkulma, λ ≤ 150, deplasman)  
**Analiz Platformu:** SAP2000 OAPI (Python / comtypes)  
**Malzeme:** *Guadua angustifolia* içi boş dairesel kesit (24 ayrık katalog)

---

## Algoritmalar

| Algoritma | Referans |
|-----------|---------|
| **NSGA-II** | Deb et al. (2002) — Evrensel Q1 kıyaslama |
| **MOABC** | Karaboga & Akay (2011) — Çok Amaçlı Yapay Arı Kolonisi |
| **MODBO** | Xue & Shen (2022) — Multi-Obj. Dung Beetle Optimizer |

---

## Klasör Yapısı

```
BambuDome/
├── 00_System/          # Ajan rolleri ve proje hafızası
├── 01_Literature/      # Literatür matrisi ve gap analizi
├── 02_Methods/         # Metodoloji ve matematiksel formülasyon
├── 03_Code_Execution/  # Python kaynak kodları (bu repo)
│   ├── bamboo_catalog.py          # 24 Guadua kesit kataloğu
│   ├── sap2000_bridge.py          # SAP2000 OAPI köprüsü
│   ├── iso22156_checks.py         # ISO 22156 tahkikleri
│   ├── carbon_calculator.py       # A1-A3 gömülü karbon
│   ├── checkpoint_manager.py      # Atomik JSON checkpoint
│   ├── multi_objective_optimizer.py  # NSGA-II / MOABC / MODBO
│   ├── main.py                    # Ana süreç yöneticisi
│   └── test_units.py              # SAP2000'siz birim testleri
├── 04_Results/         # Pareto çözümleri ve grafikler
└── 05_Drafts/          # Makale taslakları
```

---

## Kurulum & Çalıştırma

### Gereksinimler
```
Python 3.10+
SAP2000 v24+ (COM kaydı yapılmış)
comtypes, numpy, pandas, scipy, matplotlib
```

### Kurulum
```bash
pip install comtypes numpy pandas scipy matplotlib
```

### Duman Testi (SAP2000 bağlantısı)
```bash
cd 03_Code_Execution
python main.py --smoke-test
```

### Optimizasyon Çalıştırma
```bash
# Tek algoritma
python main.py --algo nsga2 --pop 40 --gen 100

# Tüm algoritmalar karşılaştırmalı
python main.py --algo all --pop 40 --gen 100

# Gizli SAP2000 (arka planda)
python main.py --algo all --hidden
```

### Birim Testleri (SAP2000 gerekmez)
```bash
python test_units.py
```

---

## Özellikler

- **Watchdog:** Her 100 analizde SAP2000 COM nesnesi yeniden başlatılır (bellek hijyeni)
- **Checkpoint:** Elektrik kesintisinde kaldığı iterasyondan otomatik devam
- **Dinamik Okuma:** Simetri grubu, eleman uzunluğu ve yük kombinasyonları SAP2000 modelinden okunur (hardcoding yok)
- **Ayrık Kesit:** 24 elemanlı katalog, tamsayı indeksiyle optimize edilir

---

## Lisans & Atıf

Akademik çalışma için geliştirilmiştir. Yayın bilgisi daha sonra eklenecektir.

> **Not:** SAP2000 model dosyası (`alara3v16.sdb`) telif hakkı nedeniyle repoya dahil edilmemiştir.
