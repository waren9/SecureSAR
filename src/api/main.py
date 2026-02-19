from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import CaseSummary, CaseDetail, NarrativeResponse, AuditEventModel
from src.services.securesar_service import service


app = FastAPI(title="SecureSAR API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/api/cases/high-risk", response_model=list[CaseSummary])
async def list_high_risk_cases() -> list[CaseSummary]:
    cases = service.list_high_risk_cases()
    return [CaseSummary(**c) for c in cases]


@app.get("/api/cases/{case_id}", response_model=CaseDetail)
async def get_case(case_id: str) -> CaseDetail:
    case = service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    # narrative is optional and initially empty
    return CaseDetail(**case, narrative=None)


@app.post("/api/cases/{case_id}/generate-sar", response_model=NarrativeResponse)
async def generate_sar(case_id: str) -> NarrativeResponse:
    narrative = service.generate_narrative(case_id, actor="Analyst_1")
    if narrative is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return NarrativeResponse(narrative=narrative)


@app.get("/api/cases/{case_id}/audit-log", response_model=list[AuditEventModel])
async def case_audit_log(case_id: str) -> list[AuditEventModel]:
    events = service.get_audit_log_for_case(case_id)
    return [AuditEventModel(**e) for e in events]


