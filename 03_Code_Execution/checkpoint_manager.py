"""
checkpoint_manager.py
Atomik JSON Checkpoint / Resume Yoneticisi
==========================================
Elektrik kesintisi veya kilitlenme durumunda kaldigi iterasyondan
otomatik devam etmeyi saglar.

Ozellikler:
  - Her iterasyonda atomik yazma (gecici dosya + rename)
  - Popülasyon + Pareto arsivi + iter numarasi kaydedilir
  - Bozuk checkpoint dosyasi otomatik temizlenir
  - Basit JSON serialization (numpy -> list donüsümü)
"""

from __future__ import annotations
import json
import os
import tempfile
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


def _numpy_to_python(obj: Any) -> Any:
    """numpy turlerini JSON-serializeble Python turlerine donusturur."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, dict):
        return {k: _numpy_to_python(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_numpy_to_python(i) for i in obj]
    return obj


class CheckpointManager:
    """
    Atomik JSON checkpoint okuma/yazma yoneticisi.

    Kullanim:
        ckpt = CheckpointManager("checkpoint.json")
        state = ckpt.load()   # None donerse sifirdan basla
        if state:
            start_iter = state["iter"]
            population = np.array(state["population"])
            ...
        # Iterasyon ici:
        ckpt.save({
            "iter": iter_no,
            "population": population.tolist(),
            "archive_obj": archive_obj.tolist(),
            "archive_sol": archive_sol.tolist(),
            "best_f1": float(best_f1),
            "best_f2": float(best_f2),
        })
    """

    def __init__(self, checkpoint_path: str | Path):
        self.checkpoint_path = Path(checkpoint_path)

    def load(self) -> dict | None:
        """Checkpoint dosyasini yukler. Yoksa veya bozuksa None dondurur."""
        if not self.checkpoint_path.exists():
            logger.info("Checkpoint bulunamadi -- sifirdan baslanacak.")
            return None
        try:
            with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            logger.info(
                "Checkpoint yuklendi: iter=%d, tarih=%s",
                state.get("iter", "?"),
                state.get("timestamp", "?"),
            )
            return state
        except (json.JSONDecodeError, KeyError, OSError) as exc:
            logger.warning("Bozuk checkpoint dosyasi (siliniyor): %s", exc)
            try:
                self.checkpoint_path.unlink()
            except OSError:
                pass
            return None

    def save(self, state: dict) -> None:
        """
        Checkpoint'i atomik olarak kaydeder.
        Gecici dosyaya yazar, sonra rename ile yeni dosyaya tasir.
        """
        state = _numpy_to_python(state)
        state["timestamp"] = datetime.now().isoformat()

        dir_ = self.checkpoint_path.parent
        try:
            dir_.mkdir(parents=True, exist_ok=True)
            # Gecici dosya ayni dizinde olusturulur
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".tmp",
                dir=str(dir_),
                delete=False,
                encoding="utf-8",
            ) as tf:
                json.dump(state, tf, ensure_ascii=False, indent=2)
                tmp_path = tf.name
            # Atomik rename (Windows uyumlu)
            if self.checkpoint_path.exists():
                self.checkpoint_path.unlink()
            os.rename(tmp_path, str(self.checkpoint_path))
            logger.debug("Checkpoint kaydedildi: iter=%d", state.get("iter", "?"))
        except OSError as exc:
            logger.error("Checkpoint yazma hatasi: %s", exc)

    def delete(self) -> None:
        """Mevcut checkpoint dosyasini siler (optimizasyon tamamlaninca)."""
        if self.checkpoint_path.exists():
            self.checkpoint_path.unlink()
            logger.info("Checkpoint silindi: %s", self.checkpoint_path)
