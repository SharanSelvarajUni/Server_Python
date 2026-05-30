from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ClientRecord:
    ip: str
    port: int
    status: str = "Connected"
    connected_at: datetime = field(default_factory=datetime.utcnow)
    total_processing_time: float = 0.0
