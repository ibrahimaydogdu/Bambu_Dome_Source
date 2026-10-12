"""
aisc_pipes.py
Literatur (354MemberDome.pdf) celik tasarim ornegindeki 37 AISC boru kesiti (kullanicinin SAP2000 .s2k tablosundan; inc birimli)
ve AISC-ASD (1989) izinli gerilme kontrolu. Alüminyum kismi kapsam disidir.

Kaynak veri: kullanicinin SteelPipeSec.txt / FRAME SECTION satirlari (A [in2], R [in], T = dis cap [in], kalinlik [in]).
"""
from __future__ import annotations
import math
import numpy as np
import pandas as pd

IN = 0.0254
# (ad, A[in2], R[in], OD[in], t[in])  -- kullanici dosyasindaki siraya gore (indeks 1..37)
PIPES = [
    ("P.5", .25, .2607681, .84, .109), ("PX.5", .32, .25, .84, .147), ("P.75", .333, .3333333, 1.05, .113),
    ("PX.75", .433, .3223757, 1.05, .154), ("P1", .494, .4196586, 1.315, .133), ("PX1", .639, .4072888, 1.315, .179),
    ("P1.25", .669, .5398887, 1.66, .14), ("P1.5", .799, .6228844, 1.9, .145), ("PX1.25", .881, .5241067, 1.66, .191),
    ("P2", 1.07, .7889423, 2.375, .154), ("PX1.5", 1.07, .6045002, 1.9, .2), ("PX2", 1.48, .765824, 2.375, .218),
    ("P2.5", 1.7, .9486833, 2.875, .203), ("P3", 2.23, 1.163727, 3.5, .216), ("PX2.5", 2.25, .9237604, 2.875, .276),
    ("PXX2", 2.66, .70177, 2.375, .436), ("P3.5", 2.68, 1.336904, 4.0, .226), ("PX3", 3.02, 1.134936, 3.5, .3),
    ("P4", 3.17, 1.510218, 4.5, .237), ("PX3.5", 3.68, 1.306339, 4.0, .318), ("PXX2.5", 4.03, .843895, 2.875, .552),
    ("P5", 4.3, 1.880129, 5.563, .258), ("PX4", 4.41, 1.47619, 4.5, .337), ("PXX3", 5.47, 1.046453, 3.5, .6),
    ("P6", 5.58, 2.244068, 6.625, .28), ("PX5", 6.11, 1.840622, 5.563, .375), ("PXX4", 8.1, 1.374369, 4.5, .674),
    ("P8", 8.4, 2.937848, 8.625, .322), ("PX6", 8.4, 2.195775, 6.625, .432), ("PXX5", 11.3, 1.72437, 5.563, .75),
    ("P10", 11.9, 3.678235, 10.75, .365), ("PX8", 12.8, 2.877716, 8.625, .5), ("P12", 14.6, 4.371451, 12.75, .375),
    ("PXX6", 15.6, 2.061553, 6.625, .864), ("PX10", 16.1, 3.628733, 10.75, .5), ("PX12", 19.2, 4.342138, 12.75, .5),
    ("PXX8", 21.3, 2.757831, 8.625, .875),
]

# Literaturdeki celik optimum cozumlerinden biri (SteelPipeSec.txt ikinci blok; 22 tasarim degiskeni, indeks 1..37)
LIT_STEEL_DESIGN = [10, 18, 19, 18, 18, 18, 18, 18, 18, 18, 18, 17, 18, 18, 15, 18, 16, 18, 17, 18, 14, 18]


def aisc37_catalog() -> pd.DataFrame:
    rows = []
    for i, (n, A, R, D, t) in enumerate(PIPES, start=1):
        rows.append(dict(idx=i, name=n, D_m=D * IN, t_m=t * IN, A_m2=A * IN ** 2, r_m=R * IN))
    return pd.DataFrame(rows).set_index("idx", drop=False)


def asd89_compression_allowable(lam, fy, e):
    """AISC-ASD (1989) izinli basinc gerilmesi Fa [fy ile ayni birim]. lam = KL/r."""
    lam = np.maximum(np.asarray(lam, float), 1.0)
    cc = math.sqrt(2.0 * math.pi ** 2 * e / fy)
    fs = 5.0 / 3.0 + 3.0 * lam / (8.0 * cc) - lam ** 3 / (8.0 * cc ** 3)
    fa_inel = (1.0 - lam ** 2 / (2.0 * cc ** 2)) * fy / fs
    fa_el = 12.0 * math.pi ** 2 * e / (23.0 * lam ** 2)
    return np.where(lam < cc, fa_inel, fa_el)
