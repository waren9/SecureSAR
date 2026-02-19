from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json
import logging


logger = logging.getLogger("securesar")


def ensure_dir(path: Path) -> None:
    """
    Ensure a directory exists.
    """
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Dict[str, Any]) -> None:
    """
    Write a dictionary to disk as UTF‑8 JSON.
    """
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    """
    Read JSON file into a dictionary. Returns {} if file does not exist.
    """
    if not path.exists():
        logger.warning("JSON file %s does not exist; returning empty dict", path)
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def setup_logging(level: int = logging.INFO) -> None:
    """
    Basic logging configuration suitable for local development.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

