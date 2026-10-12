"""
truss_model.py
Kafes (truss) modeli: veri yapisi, .s2k okuyucusu, parametrik kubbe uretici ve
yayili yuk -> dugum yuku dagitimi.

Kaynak: Saka (1991) ve Hasancebi vd. (40 m kubbe benchmarki):
  - 40 m aciklik, 8.28 m yukseklik, 127 dugum, 354 cubuk, 22 tasarim grubu
  - Olu yuk 0.2 kN/m2, kar 0.83 kN/m2 (yatay iz dusum alani uzerine)
  - Ruzgar (Denk. 27): pw = qh*G*Cp - qh*GCpi   (+ = yuzeye dogru)
      qh = 1.115 kN/m2, G = 0.85, Cp = 0.0105 | -0.907 | -0.5
      (ruzgar alti ceyrek | orta yarim | ruzgar ustu ceyrek; x yonunde 10/20/10 m)
      GCpi = -0.18 (yuk durumu II, WIND_N), +0.18 (yuk durumu III, WIND_P)
    Sekil 11'deki sayilar formulle ayni buyuklukte ama iki durumda karismis;
    formul esas alinmistir.
"""

from __future__ import annotations
import collections
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

IN_TO_M = 0.0254
KIP_TO_KN = 4.4482216152605

# ---------------------------------------------------------------------------
# Referans (354 elemanli) kubbe profili -- .s2k'dan olculmus halka degerleri
# ---------------------------------------------------------------------------
RING_R = [20.0, 17.28, 14.50, 11.67, 8.79, 5.88, 2.94, 0.0]                   # [m]
RING_Z = [0.0, 2.17493, 4.02552, 5.55179, 6.73464, 7.59316, 8.10828, 8.27998]  # [m]
RING_N = [24, 24, 24, 24, 12, 12, 6, 1]                                        # dugum/halka

# Yuk sabitleri (PDF)
P_DEAD = 0.2      # kN/m2
P_SNOW = 0.83     # kN/m2
QH, G_GUST = 1.115, 0.85                     # kN/m2, -
CP = (0.0105, -0.907, -0.5)                  # ruzgar alti | orta | ruzgar ustu
GCPI = {"WIND_N": -0.18, "WIND_P": +0.18}    # II: negatif, III: pozitif ic basinc
WIND_PRESSURE = {                            # kN/m2, + = yuzeye dogru (Denk. 27)
    name: tuple(QH * G_GUST * cp - QH * gcpi for cp in CP) for name, gcpi in GCPI.items()
}
WIND_ZONE_X = 10.0   # [m] bolge sinirlari x = -10 ve +10 (aciklik 40 m)
# .s2k'daki yuk durumlari (kullanicinin modeli): ad -> {yuk deseni: faktor}
LOAD_CASES = {   # ASD kombinasyonlari (ASCE 7-22 Md. 2.4.1; yuk faktorsuz, ISO 22156 izinli gerilme esasi)
    "D":                {"DEAD": 1.0},
    "D+S":              {"DEAD": 1.0, "SNOW": 1.0},
    "D+0.6WN":          {"DEAD": 1.0, "WIND_N": 0.6},
    "D+0.6WP":          {"DEAD": 1.0, "WIND_P": 0.6},
    "D+0.75S+0.45WN":   {"DEAD": 1.0, "SNOW": 0.75, "WIND_N": 0.45},
    "D+0.75S+0.45WP":   {"DEAD": 1.0, "SNOW": 0.75, "WIND_P": 0.45},
    "0.6D+0.6WN":       {"DEAD": 0.6, "WIND_N": 0.6},
    "0.6D+0.6WP":       {"DEAD": 0.6, "WIND_P": 0.6},
}
# Yuk suresi sinifi (en kisa sureli yuk belirler): ISO 22156 / Manual C_DF secimi
CASE_DURATION = {
    "D": "permanent", "D+S": "transient",
    "D+0.6WN": "instantaneous", "D+0.6WP": "instantaneous",
    "D+0.75S+0.45WN": "instantaneous", "D+0.75S+0.45WP": "instantaneous",
    "0.6D+0.6WN": "instantaneous", "0.6D+0.6WP": "instantaneous",
}


@dataclass
class TrussModel:
    joint_names: list[str]
    xyz: np.ndarray                       # (nj,3) [m]
    frame_names: list[str]
    fi: np.ndarray                        # (nf,) baslangic dugum indeksi
    fj: np.ndarray                        # (nf,) bitis dugum indeksi
    fixed: np.ndarray                     # (3*nj,) bool -- tutulu DOF
    case_names: list[str]
    F: np.ndarray                         # (3*nj, ncase) [kN]
    group_names: list[str]
    group_members: list[np.ndarray]       # her grup icin cubuk indeksleri
    patterns: dict[str, np.ndarray] = field(default_factory=dict)  # (nj,3) [kN]
    span_m: float = 40.0                  # aciklik [m]

    @property
    def disp_limit_m(self) -> float:
        """Izin verilen yer degistirme: aciklik / disp_limit_ratio (MATERIAL_PROPERTIES; 150 -> 40 m icin 26.7 cm)."""
        from bamboo_catalog import MATERIAL_PROPERTIES
        return round(self.span_m / MATERIAL_PROPERTIES["disp_limit_ratio"], 3)

    @property
    def member_group(self) -> dict[str, str]:
        return {self.frame_names[m]: g
                for g, mem in zip(self.group_names, self.group_members) for m in mem}


# ---------------------------------------------------------------------------
# .s2k okuyucu
# ---------------------------------------------------------------------------
_KV = re.compile(r'(\w+)=("[^"]*"|\S+)')


def parse_s2k(path: Path) -> dict[str, list[dict[str, str]]]:
    tables: dict[str, list[dict[str, str]]] = {}
    cur = None
    pending = ""
    for raw in Path(path).read_text(encoding="latin-1").splitlines():
        line = raw.rstrip()
        if pending:
            line = pending + " " + line.strip()
            pending = ""
        if line.endswith(" _"):
            pending = line[:-2]
            continue
        s = line.strip()
        if s.startswith("TABLE:"):
            cur = tables.setdefault(s.split('"')[1], [])
        elif s.startswith("END TABLE DATA"):
            cur = None
        elif cur is not None and "=" in s:
            cur.append({k: v.strip('"') for k, v in _KV.findall(s)})
    return tables


def model_from_s2k(path) -> TrussModel:
    T = parse_s2k(Path(path))
    jr = T["JOINT COORDINATES"]
    names = [r["Joint"] for r in jr]
    jidx = {n: i for i, n in enumerate(names)}
    xyz = np.array([[float(r["GlobalX"]), float(r["GlobalY"]), float(r["GlobalZ"])]
                    for r in jr]) * IN_TO_M
    fr = T["CONNECTIVITY - FRAME"]
    fnames = [r["Frame"] for r in fr]
    fidx = {n: i for i, n in enumerate(fnames)}
    fi = np.array([jidx[r["JointI"]] for r in fr])
    fj = np.array([jidx[r["JointJ"]] for r in fr])

    fixed = np.zeros(3 * len(jr), dtype=bool)
    for r in T["JOINT RESTRAINT ASSIGNMENTS"]:
        j = jidx[r["Joint"]]
        for k, key in enumerate(("U1", "U2", "U3")):
            if r[key] == "Yes":
                fixed[3 * j + k] = True

    pats: dict[str, np.ndarray] = {}
    for r in T["JOINT LOADS - FORCE"]:
        v = pats.setdefault(r["LoadPat"], np.zeros((len(jr), 3)))
        v[jidx[r["Joint"]]] += np.array([float(r["F1"]), float(r["F2"]), float(r["F3"])]) * KIP_TO_KN
    cases: dict[str, np.ndarray] = {}
    for r in T["CASE - STATIC 1 - LOAD ASSIGNMENTS"]:
        if r["LoadType"] == "Load pattern":
            cases.setdefault(r["Case"], np.zeros((len(jr), 3)))
            cases[r["Case"]] += float(r["LoadSF"]) * pats[r["LoadName"]]
    cnames = list(cases)
    F = np.column_stack([cases[c].reshape(-1) for c in cnames])

    grp: dict[str, list[str]] = {}
    for r in T["GROUPS 2 - ASSIGNMENTS"]:
        if r["ObjectType"] == "Frame":
            grp.setdefault(r["GroupName"], []).append(r["ObjectLabel"])
    gnames = sorted(grp, key=lambda s: (0, int(s)) if s.isdigit() else (1, s))
    gmem = [np.array([fidx[m] for m in grp[g]]) for g in gnames]
    return TrussModel(names, xyz, fnames, fi, fj, fixed, cnames, F, gnames, gmem, pats)


# ---------------------------------------------------------------------------
# Parametrik kubbe uretici
# ---------------------------------------------------------------------------
def _pchip(x, y, xq):
    """Monoton parcali kubik Hermite (Fritsch-Carlson); x artan olmali."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    h = np.diff(x); d = np.diff(y) / h
    m = np.zeros_like(y)
    for k in range(1, len(x) - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    m[0], m[-1] = d[0], d[-1]
    xq = np.atleast_1d(xq).astype(float)
    k = np.clip(np.searchsorted(x, xq) - 1, 0, len(x) - 2)
    t = (xq - x[k]) / h[k]
    h00, h10 = 2*t**3 - 3*t**2 + 1, t**3 - 2*t**2 + t
    h01, h11 = -2*t**3 + 3*t**2, t**3 - t**2
    return h00*y[k] + h10*h[k]*m[k] + h01*y[k+1] + h11*h[k]*m[k+1]


def _rings(freq: int):
    """(r, z, n) listesi, tabandan tepeye. freq=1 -> referans 354 elemanli kubbe."""
    r_ref, z_ref = np.array(RING_R[::-1]), np.array(RING_Z[::-1])   # r artan
    rings = []
    for k in range(len(RING_R) - 1):
        n_out = RING_N[k] * freq if RING_N[k] > 1 else 1
        rings.append((RING_R[k], RING_Z[k], n_out))
        for j in range(1, freq):                       # ara halkalar (dis halka sayisiyla)
            r = RING_R[k] + (RING_R[k + 1] - RING_R[k]) * j / freq
            z = float(_pchip(r_ref, z_ref, r)[0])
            rings.append((r, z, n_out))
    rings.append((RING_R[-1], RING_Z[-1], 1))
    return rings


def generate_dome(freq: int = 1) -> tuple[list[tuple], list[tuple], list[str]]:
    """Dugum ve cubuk listesi uretir.
    Doner: (joints[(ring_idx, i, x, y, z)], frames[(a, b, sinif)], sinif_adlari_sirali)
    Sinif = ayni yapisal gruba giren cubuk turu (ring k / strip k meridyen / capraz...)."""
    rings = _rings(freq)
    joints, jid = [], {}
    for ri, (r, z, n) in enumerate(rings):
        for i in range(n):
            phi = 2 * math.pi * i / n
            jid[(ri, i)] = len(joints)
            joints.append((ri, i, r * math.sin(phi), r * math.cos(phi), z))
    frames = []
    for ri, (r, z, n) in enumerate(rings):
        if n >= 3:                                         # halka cubuklari
            for i in range(n):
                frames.append((jid[(ri, i)], jid[(ri, (i + 1) % n)], f"R{ri:02d}ring"))
        if ri + 1 < len(rings):                            # serit (ri -> ri+1)
            m = rings[ri + 1][2]
            tag = f"R{ri:02d}"
            for k in range(n):
                if m == 1:
                    frames.append((jid[(ri, k)], jid[(ri + 1, 0)], tag + "spoke"))
                elif n == m:
                    frames.append((jid[(ri, k)], jid[(ri + 1, k)], tag + "mer"))
                    frames.append((jid[(ri, k)], jid[(ri + 1, (k + 1) % m)], tag + "dia"))
                elif n == 2 * m:
                    if k % 2 == 0:
                        frames.append((jid[(ri, k)], jid[(ri + 1, k // 2)], tag + "mer"))
                    else:
                        frames.append((jid[(ri, k)], jid[(ri + 1, (k - 1) // 2)], tag + "dl"))
                        frames.append((jid[(ri, k)], jid[(ri + 1, ((k + 1) // 2) % m)], tag + "dr"))
                else:
                    raise ValueError(f"Desteklenmeyen serit: {n}->{m}")
    classes = []
    for _, _, c in frames:
        if c not in classes:
            classes.append(c)
    return joints, frames, classes


# ---------------------------------------------------------------------------
# Yayili yuk -> dugum yuku
# ---------------------------------------------------------------------------
def _faces(fi, fj, nj):
    adj = collections.defaultdict(set)
    for i, j in zip(fi, fj):
        adj[int(i)].add(int(j)); adj[int(j)].add(int(i))
    return sorted({tuple(sorted((i, j, k))) for i in adj for j in adj[i]
                   for k in adj[i] & adj[j]})


def distribute_loads(xyz, fi, fj, span_m: float,
                     p_dead=P_DEAD, p_snow=P_SNOW, wind=WIND_PRESSURE,
                     zone_x=None, normalize_plan: bool = True) -> dict[str, np.ndarray]:
    """Yayili yukleri (kN/m2) ucgen yuzlerin 1/3 alani ile dugumlere dagitir.

    DEAD/SNOW: yatay iz dusum alani uzerinde, -z yonunde. Toplam, p*pi*(span/2)^2
               olacak sekilde normalize edilir (egri cati izdusumu daire).
    WIND     : yuzey alani uzerinde, yuzeye dik (basinc + = yuzeye dogru).
               Bolge, ucgen yuzun merkezinin x koordinatina gore secilir."""
    if zone_x is None:
        zone_x = span_m / 4.0                           # 10/20/10 m @ 40 m aciklik
    nj = len(xyz)
    faces = _faces(fi, fj, nj)
    A_plan = np.zeros(nj)
    Vz = {name: np.zeros((nj, 3)) for name in wind}    # basinc * alan vektoru
    for i, j, k in faces:
        a, b, c = xyz[i], xyz[j], xyz[k]
        n = 0.5 * np.cross(b - a, c - a)
        if n[2] < 0:
            n = -n                                      # dis normal (yukari)
        A_plan[[i, j, k]] += n[2] / 3.0
        xc = (a[0] + b[0] + c[0]) / 3.0                 # bolge: yuz merkezinin x'i
        zone = 0 if xc < -zone_x else (2 if xc > zone_x else 1)
        for name, pz in wind.items():
            Vz[name][[i, j, k]] += -pz[zone] * n / 3.0  # + basinc = yuzeye dogru
    if normalize_plan:                                  # egri cati izdusumu daire
        A_plan *= math.pi * (span_m / 2) ** 2 / A_plan.sum()
    pats = {}
    for name, p in (("DEAD", p_dead), ("SNOW", p_snow)):
        F = np.zeros((nj, 3)); F[:, 2] = -p * A_plan
        pats[name] = F
    pats.update(Vz)
    return pats


def assemble_cases(pats: dict[str, np.ndarray], cases=LOAD_CASES):
    names = list(cases)
    F = np.column_stack([sum(f * pats[p] for p, f in cases[c].items()).reshape(-1)
                         for c in names])
    return names, F


def model_from_geometry(xyz, edges, classes, supports, span_m: float,
                        normalize_plan: bool = True) -> TrussModel:
    """Genel kurucu. xyz (nj,3) [m]; edges [(a,b)]; classes [etiket] (cubuk basina);
    supports: mesnetli dugum indeksleri. Ayni etiketli cubuklar tek tasarim grubu olur."""
    xyz = np.asarray(xyz, float)
    names = [str(i + 1) for i in range(len(xyz))]
    fi = np.array([a for a, _ in edges]); fj = np.array([b for _, b in edges])
    fnames = [str(i + 1) for i in range(len(edges))]
    fixed = np.zeros(3 * len(xyz), dtype=bool)
    for i in supports:
        fixed[3 * i: 3 * i + 3] = True
    order = []
    for c in classes:
        if c not in order:
            order.append(c)
    cls_arr = np.array([str(c) for c in classes]); order = [str(c) for c in order]
    gnames = [str(i + 1) for i in range(len(order))]
    gmem = [np.flatnonzero(cls_arr == c) for c in order]
    pats = distribute_loads(xyz, fi, fj, span_m, normalize_plan=normalize_plan)
    cn, F = assemble_cases(pats)
    return TrussModel(names, xyz, fnames, fi, fj, fixed, cn, F, gnames, gmem, pats, span_m)


def build_dome_model(freq: int = 1, span_m: float = 40.0) -> TrussModel:
    """Ribbed (Schwedler tipi) kubbe: freq=1 -> 354-elemanli referans; freq=2 -> ribbed40."""
    joints, frames, classes = generate_dome(freq)
    xyz = [[x, y, z] for _, _, x, y, z in joints]
    supports = [i for i, (ri, *_r) in enumerate(joints) if ri == 0]
    return model_from_geometry(xyz, [(a, b) for a, b, _ in frames], [c for _, _, c in frames],
                               supports, span_m)
