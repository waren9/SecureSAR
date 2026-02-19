from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any, Optional

from pydantic import BaseModel


class CaseSummary(BaseModel):
  id: str
  customer_id: str
  risk_score: float
  risk_band: str
  created_at: Optional[datetime] = None


class CaseDetail(BaseModel):
  id: str
  customer_id: str
  risk_score: float
  risk_band: str
  typologies: List[str]
  triggered_rules: List[str]
  shap_values: Dict[str, float]
  narrative: Optional[str] = None
  created_at: Optional[datetime] = None


class NarrativeResponse(BaseModel):
  narrative: str


class AuditEventModel(BaseModel):
  timestamp: str
  event_type: str
  actor: str
  details: Dict[str, Any]


