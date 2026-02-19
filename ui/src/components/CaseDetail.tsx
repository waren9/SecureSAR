import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiClient } from "../services/apiClient";
import RiskExplanation from "./RiskExplanation";
import AuditLogView from "./AuditLogView";

type CaseDetailData = {
  id: string;
  customer_id: string;
  risk_score: number;
  risk_band: string;
  typologies: string[];
  triggered_rules: string[];
  shap_values?: Record<string, number>;
  narrative?: string;
  created_at?: string;
};

function CaseDetail() {
  const { caseId } = useParams();
  const [data, setData] = useState<CaseDetailData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    async function load() {
      if (!caseId) return;
      setLoading(true);
      setError(null);
      try {
        const resp = await apiClient.get<CaseDetailData>(`/api/cases/${caseId}`);
        setData(resp.data);
      } catch (e) {
        setError("Failed to load case details.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [caseId]);

  async function handleGenerateNarrative() {
    if (!caseId) return;
    setGenerating(true);
    setError(null);
    try {
      const resp = await apiClient.post<{ narrative: string }>(`/api/cases/${caseId}/generate-sar`);
      setData((prev) => (prev ? { ...prev, narrative: resp.data.narrative } : prev));
    } catch (e) {
      setError("Failed to generate SAR narrative.");
    } finally {
      setGenerating(false);
    }
  }

  if (loading) {
    return <div>Loading case…</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!data) {
    return <div>No case found.</div>;
  }

  return (
    <div className="layout-split">
      <div className="card">
        <h1>Case {data.id}</h1>
        <p>
          <strong>Customer:</strong> {data.customer_id}
        </p>
        <p>
          <strong>Risk score:</strong> {data.risk_score.toFixed(3)} ({data.risk_band})
        </p>
        <p>
          <strong>Typologies:</strong> {data.typologies.join(", ") || "None"}
        </p>
        <p>
          <strong>Rules:</strong> {data.triggered_rules.join(", ") || "None"}
        </p>
        <button onClick={handleGenerateNarrative} disabled={generating}>
          {generating ? "Generating narrative…" : "Generate SAR Narrative"}
        </button>
        <section className="narrative">
          <h2>SAR Narrative Draft</h2>
          {data.narrative ? <pre>{data.narrative}</pre> : <p>No narrative generated yet.</p>}
        </section>
      </div>
      <div className="card">
        <RiskExplanation shapValues={data.shap_values ?? {}} />
        <AuditLogView caseId={data.id} />
      </div>
    </div>
  );
}

export default CaseDetail;

