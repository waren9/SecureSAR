type Props = {
  shapValues: Record<string, number>;
};

function RiskExplanation({ shapValues }: Props) {
  const entries = Object.entries(shapValues).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));

  return (
    <section>
      <h2>Risk Explanation (SHAP)</h2>
      {entries.length === 0 ? (
        <p>No SHAP values available for this case.</p>
      ) : (
        <ul className="shap-list">
          {entries.map(([feature, value]) => (
            <li key={feature}>
              <span className="feature">{feature}</span>
              <span className={`value ${value >= 0 ? "pos" : "neg"}`}>{value.toFixed(3)}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default RiskExplanation;

