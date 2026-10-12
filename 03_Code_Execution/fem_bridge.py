"""
fem_bridge.py
SAP2000'siz dogrudan rijitlik yontemi ile pimli kafes (truss) cozucusu.

SAP2000Bridge ile ayni arayuzu sunar (open/close/define_*/read_*/update_sections/
run_analysis_and_read/watchdog), boylece main.py ve optimizer'a dokunmadan takilir.

Gecerlilik: Model yalniz UX,UY,UZ serbestlik derecelerine sahip, tum cubuklarin
uclarinda moment serbest -> lineer statik analizde SAP2000 ile ayni sonuc
(bkz. validate_sap.py ve test_fast_eval.py).

Girdi: truss_model.TrussModel (parametrik uretilmis).
"""

from __future__ import annotations
import os
# Bu makinede cok iplikli BLAS kucuk sistemlerde ~100x yavaslatiyor (309x309: 432 ms -> 3.5 ms).
# numpy ice aktarilmadan ONCE tek iplige sabitlenmeli. Kampanya zaten ayri surecler olarak kosar.
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import logging

import numpy as np

from bamboo_catalog import MATERIAL_PROPERTIES

logger = logging.getLogger(__name__)

from truss_model import TrussModel, model_from_s2k


class FEMBridge:
    def __init__(self, model, E_kPa: float | None = None, solver: str = "auto", **_ignored):
        """model: TrussModel veya .s2k dosya yolu."""
        self.model = model if isinstance(model, TrussModel) else model_from_s2k(model)
        self.E = E_kPa if E_kPa is not None else MATERIAL_PROPERTIES["E_mean"]
        self._analysis_count = 0
        self._combos_are_cases = True
        self._A: np.ndarray | None = None      # eleman kesit alanlari [m2]
        self._loaded = False
        self.solver_req = solver            # "auto" | "sparse" | "dense"
        self.solver = "dense"

    @property
    def n_nodes(self) -> int:
        return len(self.model.joint_names)

    # ------------------------------------------------------------------
    # Yasam dongusu (SAP2000Bridge ile uyumlu, cogu no-op)
    # ------------------------------------------------------------------
    def open(self) -> None:
        if self._loaded:
            return
        M = self.model
        self._joint_names = M.joint_names
        self._frame_names = M.frame_names
        self._fi, self._fj = M.fi, M.fj
        d = M.xyz[self._fj] - M.xyz[self._fi]
        self._L = np.linalg.norm(d, axis=1)
        self._e = d / self._L[:, None]
        self._free = np.flatnonzero(~M.fixed)
        self._F = M.F
        self._load_combos = list(M.case_names)
        self._group_names = list(M.group_names)
        self._group_members = M.group_members
        self._member_group = M.member_group
        self._member_lengths = {n: float(self._L[i]) for i, n in enumerate(self._frame_names)}
        self._A = np.ones(len(self._frame_names))
        nd = 3 * len(self._joint_names)
        di = (3 * self._fi)[:, None] + np.arange(3)          # (n,3)
        dj = (3 * self._fj)[:, None] + np.arange(3)
        self._di, self._dj = di, dj
        blocks = ((di, di), (dj, dj), (di, dj), (dj, di))
        self._kidx = np.concatenate([(a[:, :, None] * nd + b[:, None, :]).ravel()
                                     for a, b in blocks])
        self._ksgn = np.concatenate([np.full(di.shape[0] * 9, sg)
                                     for sg in (1.0, 1.0, -1.0, -1.0)])
        self._ee9 = (self._e[:, :, None] * self._e[:, None, :]).reshape(-1, 9)
        self._init_sparse(nd)
        self._loaded = True
        logger.info("FEM modeli: %d dugum, %d cubuk, %d grup, %d yuk durumu, %d serbest DOF.",
                    len(self._joint_names), len(self._frame_names), len(self._group_names),
                    len(self._load_combos), len(self._free))

    def close(self, save: bool = False) -> None:
        pass

    def watchdog(self, iter_no: int) -> None:
        pass

    def define_bamboo_material(self, *a, **k) -> None:
        pass

    def define_bamboo_sections(self, *a, **k) -> None:
        pass

    def read_groups_and_lengths(self):
        return self._group_names, self._member_lengths

    def read_load_combos(self) -> list[str]:
        return self._load_combos

    # ------------------------------------------------------------------
    # Optimizasyon dongusu
    # ------------------------------------------------------------------
    def update_sections(self, group_section_indices, catalog_df) -> None:
        if len(group_section_indices) != len(self._group_names):
            raise ValueError(
                f"Gen uzunlugu ({len(group_section_indices)}) grup sayisina "
                f"({len(self._group_names)}) esit degil."
            )
        for members, sec in zip(self._group_members, group_section_indices):
            self._A[members] = float(catalog_df.loc[int(sec)]["A_m2"])

    # ------------------------------------------------------------------
    # Dizi tabanli hizli arayuz (fast_eval.py kullanir)
    # ------------------------------------------------------------------
    @property
    def group_index(self) -> np.ndarray:
        """Her cubugun tasarim grubu indeksi (0-tabanli, gen sirasi)."""
        if getattr(self, "_gidx", None) is None:
            g = np.zeros(len(self._frame_names), dtype=int)
            for gi, mem in enumerate(self._group_members):
                g[mem] = gi
            self._gidx = g
        return self._gidx

    @property
    def member_lengths_arr(self) -> np.ndarray:
        return self._L

    def set_member_areas(self, A: np.ndarray) -> None:
        self._A = np.asarray(A, dtype=float)

    def _init_sparse(self, nd: int) -> None:
        """Serbest DOF'lar icin seyrek rijitlik yapisini bir kez hazirlar (scipy varsa)."""
        self.solver = "dense"
        if self.solver_req == "dense":
            return
        try:
            import scipy.sparse as sp                      # noqa: F401
            import scipy.sparse.linalg as spla             # noqa: F401
        except ImportError:
            if self.solver_req == "sparse":
                raise
            logger.warning("scipy yok -- yogun cozucu kullaniliyor (yavas).")
            return
        fmap = -np.ones(nd, dtype=np.int64)
        fmap[self._free] = np.arange(len(self._free))
        rows = self._kidx // nd
        cols = self._kidx % nd
        r, c = fmap[rows], fmap[cols]
        keep = (r >= 0) & (c >= 0)
        self._sp_sel = np.flatnonzero(keep)                # w dizisinde hangi girdiler serbest-serbest
        self._sp_r, self._sp_c = r[keep], c[keep]
        self._sp_n = len(self._free)
        if self.solver_req == "auto" and self._sp_n < 200:      # cok kucuk sistemde yogun LU daha hizli
            return
        self.solver = "sparse"

    def _solve(self):
        ndof = 3 * len(self._joint_names)
        k = self.E * self._A / self._L                       # [kN/m]
        w = np.tile((k[:, None] * self._ee9).ravel(), 4) * self._ksgn
        fr = self._free
        U = np.zeros((ndof, self._F.shape[1]))
        if self.solver == "sparse":
            import scipy.sparse as sp
            import scipy.sparse.linalg as spla
            K = sp.csc_matrix((w[self._sp_sel], (self._sp_r, self._sp_c)), shape=(self._sp_n, self._sp_n))
            try:
                # K simetrik pozitif tanimli: pivotsuz simetrik LU guvenli ve ~2.5x hizli
                lu = spla.splu(K, permc_spec="MMD_AT_PLUS_A", diag_pivot_thresh=0.0,
                               options=dict(SymmetricMode=True))
            except RuntimeError as exc:
                raise RuntimeError("Rijitlik matrisi tekil (mekanizma)") from exc
            U[fr] = lu.solve(self._F[fr])
        else:
            K = np.bincount(self._kidx, weights=w, minlength=ndof * ndof).reshape(ndof, ndof)
            try:
                U[fr] = np.linalg.solve(K[np.ix_(fr, fr)], self._F[fr])
            except np.linalg.LinAlgError as exc:
                raise RuntimeError("Rijitlik matrisi tekil (mekanizma)") from exc
        self._analysis_count += 1
        du = U[self._dj] - U[self._di]                       # (n,3,ncase)
        N = k[:, None] * np.einsum("nk,nkc->nc", self._e, du)   # (n,ncase) cekme +
        return U, N

    def analyze_arrays(self):
        """Doner: N (cubuk x yuk durumu, kN, cekme +) ve umax (tum dugum/yon/durumlarda
        en buyuk mutlak yer degistirme, m)."""
        U, N = self._solve()
        return N, float(np.abs(U).max())

    def run_analysis_and_read(self):
        """axial: {cubuk: en buyuk mutlak eksenel kuvvet [kN] (isaretli)},
        disp: {dugum: (U1,U2,U3) bilesen basina en buyuk mutlak [m]}  (SAP2000Bridge ile ayni arayuz)"""
        U, N = self._solve()
        pick = np.argmax(np.abs(N), axis=1)
        Nmax = N[np.arange(N.shape[0]), pick]
        axial = {n: float(Nmax[i]) for i, n in enumerate(self._frame_names)}

        Uj = U.reshape(len(self._joint_names), 3, -1)        # (nj,3,ncase)
        pj = np.argmax(np.abs(Uj), axis=2)
        Umax = np.take_along_axis(Uj, pj[:, :, None], axis=2)[:, :, 0]
        disp = {n: tuple(float(x) for x in Umax[i]) for i, n in enumerate(self._joint_names)}
        return axial, disp
