from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import json

from src.utils.config import load_config
from src.utils.helpers import ensure_dir


@dataclass
class AuditEvent:
    event_type: str
    actor: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class AuditLogger:
    """
    Very simple JSONL-based audit logger suitable for demos and local runs.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        cfg = load_config()
        self.path = path or (cfg.data.processed_dir / "audit_log.jsonl")
        ensure_dir(self.path.parent)

    def log(self, event: AuditEvent) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), separators=(",", ":")) + "\n")


__all__ = ["AuditEvent", "AuditLogger"]

