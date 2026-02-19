import { useEffect, useState } from "react";
import { apiClient } from "../services/apiClient";

type Props = {
  caseId: string;
};

type AuditEvent = {
  timestamp: string;
  event_type: string;
  actor: string;
  details: Record<string, unknown>;
};

function AuditLogView({ caseId }: Props) {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const resp = await apiClient.get<AuditEvent[]>(`/api/cases/${caseId}/audit-log`);
        setEvents(resp.data);
      } catch (e) {
        setError("Failed to load audit log.");
      }
    }
    load();
  }, [caseId]);

  return (
    <section>
      <h2>Audit Log</h2>
      {error && <div className="error">{error}</div>}
      {events.length === 0 ? (
        <p>No audit events recorded yet.</p>
      ) : (
        <ul className="audit-list">
          {events.map((e, idx) => (
            <li key={idx}>
              <div>
                <strong>{e.event_type}</strong> by {e.actor}
              </div>
              <div className="timestamp">{e.timestamp}</div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default AuditLogView;

