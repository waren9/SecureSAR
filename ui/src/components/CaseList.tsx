import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiClient } from "../services/apiClient";

type CaseSummary = {
  id: string;
  customer_id: string;
  risk_score: number;
  risk_band: string;
  created_at?: string;
};

function CaseList() {
  const [cases, setCases] = useState<CaseSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const resp = await apiClient.get<CaseSummary[]>("/api/cases/high-risk");
        setCases(resp.data);
      } catch (e) {
        setError("Failed to load cases. Is the API running?");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return <div>Loading high-risk cases…</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="card">
      <h1>High-Risk Cases</h1>
      {cases.length === 0 ? (
        <p>No high-risk cases found.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Customer</th>
              <th>Risk Score</th>
              <th>Band</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {cases.map((c) => (
              <tr key={c.id}>
                <td>
                  <Link to={`/cases/${c.id}`}>{c.id}</Link>
                </td>
                <td>{c.customer_id}</td>
                <td>{c.risk_score.toFixed(3)}</td>
                <td>{c.risk_band}</td>
                <td>{c.created_at ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default CaseList;

