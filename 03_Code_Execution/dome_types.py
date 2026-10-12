"""
dome_types.py
Makale ornekleri icin kubbe uretecleri ve hazir ayarlar (preset).

  ribbed40   : Saka (1991) tabanli Schwedler/ribbed kubbe, freq=2 (benchmark turevi)
  geodesic16 : ikosahedron tabanli geodezik kubbe, 16 m aciklik (orijinal, kucuk)
  kiewitt32  : Kiewitt tipi lamella kubbe, 32 m aciklik (orijinal, buyuk)

Ortak ilkeler: ayni birim yukler (truss_model), ayni LRFD kombinasyonlari, ayni 24 kesitlik
katalog; yukseklik/aciklik ~0.2 (benchmark 8.28/40 = 0.207; Cp katsayilariyla tutarli);
cubuk boyu ust siniri 4 m (bambu govdesi).
"""

from __future__ import annotations
import collections
import math

import numpy as np

from truss_model import TrussModel, build_dome_model, model_from_geometry

MAX_MEMBER_M = 4.0


# ---------------------------------------------------------------------------
# Geodezik kubbe (ikosahedron, sinif I, frekans v)
# ---------------------------------------------------------------------------
def _icosahedron():
    p = (1 + 5 ** 0.5) / 2
    V = np.array([(-1, p, 0), (1, p, 0), (-1, -p, 0), (1, -p, 0), (0, -1, p), (0, 1, p),
                  (0, -1, -p), (0, 1, -p), (p, 0, -1), (p, 0, 1), (-p, 0, -1), (-p, 0, 1)], float)
    V /= np.linalg.norm(V, axis=1)[:, None]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
         (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
         (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    return V, F


def _rot_axis_to_z(V, axis):
    axis = np.asarray(axis, float); axis = axis / np.linalg.norm(axis)
    z = np.array([0, 0, 1.0]); v = np.cross(axis, z); s = np.linalg.norm(v); c = float(axis @ z)
    if s < 1e-12:
        return V
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return V @ (np.eye(3) + K + K @ K * ((1 - c) / s ** 2)).T


def _geodesic_sphere(v: int):
    """Birim kure uzerinde 5-kat eksen +z olacak sekilde dugumler ve kenarlar."""
    V0, F = _icosahedron()
    V = _rot_axis_to_z(V0, V0[0])
    pts, idx, faces = [], {}, []

    def add(p):
        p = p / np.linalg.norm(p); key = tuple(np.round(p, 6))
        if key not in idx:
            idx[key] = len(pts); pts.append(p)
        return idx[key]

    for a, b, c in F:
        g = {}
        for i in range(v + 1):
            for j in range(v + 1 - i):
                g[(i, j)] = add((i * V[a] + j * V[b] + (v - i - j) * V[c]) / v)
        for i in range(v + 1):
            for j in range(v + 1 - i):
                if (i + 1, j) in g and (i, j + 1) in g:
                    faces.append((g[(i, j)], g[(i + 1, j)], g[(i, j + 1)]))
                if (i + 1, j) in g and (i, j + 1) in g and (i + 1, j + 1) in g:
                    faces.append((g[(i + 1, j)], g[(i + 1, j + 1)], g[(i, j + 1)]))
    return np.array(pts), faces


def generate_geodesic(span_m: float = 12.0, v: int = 5, colat_deg: float = 48.0):
    """Kesilmis geodezik kubbe (5-kat eksen tepede). colat_deg enlemine kadar olan ucgenler
    tutulur; kesim siniri tirtikli (zigzag) olur ve sinirdaki TUM dugumler mesnetlenir.
    Doner: (xyz, edges, classes, supports).
    Gruplar: ayni uzunluk + ayni enlem + ayni 72 derecelik dilim konumu (C5 yorungesi);
    ayna goruntuleri ayri grup olur (ruzgar x yonunde, ayna simetrisi yok)."""
    P, F = _geodesic_sphere(v)
    colat = np.degrees(np.arccos(np.clip(P[:, 2], -1, 1)))
    F = [f for f in F if max(colat[list(f)]) <= colat_deg + 1e-6]
    used = sorted({i for f in F for i in f}); new = {o: n for n, o in enumerate(used)}
    cnt = collections.Counter()
    for f in F:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])):
            cnt[tuple(sorted((a, b)))] += 1
    sup_old = sorted({i for e, c in cnt.items() if c == 1 for i in e})
    # yaricap: sinirdaki dugumlerin yatay yaricap ortalamasi aciklik/2 olacak sekilde
    r_unit = np.mean([math.hypot(P[i, 0], P[i, 1]) for i in sup_old])
    R = (span_m / 2.0) / r_unit
    X = P[used] * R
    X[:, 2] -= min(P[i, 2] for i in sup_old) * R                  # en alcak mesnet z = 0
    edges = [(new[a], new[b]) for (a, b) in sorted(cnt)]
    supports = [new[i] for i in sup_old]
    classes = []
    for a, b in edges:
        pa, pb = P[used[a]], P[used[b]]
        mid = (pa + pb) / 2
        L = np.linalg.norm(pa - pb)
        mc = math.degrees(math.acos(mid[2] / np.linalg.norm(mid)))
        az = math.degrees(math.atan2(mid[0], mid[1])) % 72.0
        classes.append((round(L, 4), round(mc, 1), round(az % 72.0, 1)))
    uniq = sorted(set(classes), key=lambda c: (-c[1], c[2], c[0]))
    rank = {c: f"{i:03d}" for i, c in enumerate(uniq)}
    return X, edges, [rank[c] for c in classes], supports


# ---------------------------------------------------------------------------
# Kiewitt tipi kubbe: n kose, m halka; halka i'de n*i dugum
# ---------------------------------------------------------------------------
def generate_kiewitt(span_m: float = 28.0, rise_m: float = 5.8, n: int = 8, m: int = 6,
                     power: float = 1.0):
    a = span_m / 2.0
    R = (a * a + rise_m * rise_m) / (2.0 * rise_m)
    th_base = math.asin(a / R)
    zc = R * math.cos(th_base)
    ids = {(0, 0): 0}; xyz = [[0.0, 0.0, R - zc]]
    for i in range(1, m + 1):
        th = th_base * (i / m) ** power
        for k in range(n * i):
            phi = 2 * math.pi * k / (n * i)
            ids[(i, k)] = len(xyz)
            xyz.append([R * math.sin(th) * math.sin(phi), R * math.sin(th) * math.cos(phi),
                        R * math.cos(th) - zc])
    edges, classes, seen = [], [], set()

    def add(u, w, cls):
        key = frozenset((u, w))
        if key not in seen:
            seen.add(key); edges.append((u, w)); classes.append(cls)

    for k in range(n):
        add(ids[(0, 0)], ids[(1, k)], "S00spoke")
    for i in range(1, m + 1):
        for k in range(n * i):
            add(ids[(i, k)], ids[(i, (k + 1) % (n * i))], f"S{i:02d}ring")
    for i in range(1, m):
        for s in range(n):
            for j in range(i + 1):
                A = ids[(i, (s * i + j) % (n * i))]
                B0 = ids[(i + 1, (s * (i + 1) + j) % (n * (i + 1)))]
                B1 = ids[(i + 1, (s * (i + 1) + j + 1) % (n * (i + 1)))]
                rib_a = j in (0, i)
                add(A, B0, f"S{i:02d}{'rib' if (j == 0) else 'rad'}")
                add(A, B1, f"S{i:02d}{'rib' if (j == i) else 'dia'}")
    supports = [ids[(m, k)] for k in range(n * m)]
    return np.array(xyz), edges, classes, supports


# ---------------------------------------------------------------------------
# Hazir ayarlar
# ---------------------------------------------------------------------------
PRESETS = {
    "ribbed40":   dict(kind="ribbed", span=40.0, freq=2),
    # 12 m'de kisitlar baglayici degil (en kucuk kesitler bile uygun); 16 m en kucuk anlamli aciklik
    "geodesic16": dict(kind="geodesic", span=16.0, v=5, colat=50.0),
    "kiewitt32":  dict(kind="kiewitt", span=32.0, rise=6.6, n=8, m=6),
}


def build_preset(name: str) -> TrussModel:
    c = PRESETS[name]
    if c["kind"] == "ribbed":
        return build_dome_model(c["freq"], c["span"])
    if c["kind"] == "geodesic":
        xyz, edges, cls, sup = generate_geodesic(c["span"], c["v"], c["colat"])
    else:
        xyz, edges, cls, sup = generate_kiewitt(c["span"], c["rise"], c["n"], c["m"])
    return model_from_geometry(xyz, edges, cls, sup, c["span"], normalize_plan=(c["kind"] != "geodesic"))


def geometry_report(model: TrussModel) -> dict:
    d = model.xyz[model.fj] - model.xyz[model.fi]
    L = np.linalg.norm(d, axis=1)
    span = 2 * np.hypot(model.xyz[:, 0], model.xyz[:, 1]).max()
    return dict(nodes=len(model.xyz), members=len(L), groups=len(model.group_names),
                supports=int(model.fixed.sum() // 3), Lmin=float(L.min()), Lmax=float(L.max()),
                span=float(span), rise=float(model.xyz[:, 2].max()),
                rise_span=float(model.xyz[:, 2].max() / span))
