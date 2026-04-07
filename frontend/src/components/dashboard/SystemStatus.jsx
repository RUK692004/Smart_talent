function Badge({ label, value, color, textColor = "white" }) {
  return (
    <div
      style={{
        padding: "10px 16px",
        borderRadius: "10px",
        background: color,
        color: textColor,
        fontWeight: "700",
        boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
      }}
    >
      {label}: {value}
    </div>
  );
}

function SystemStatus({ stats }) {
  return (
    <div>
      <h3 style={{ marginBottom: "12px" }}>System Status</h3>

      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <Badge label="Parsed" value={stats.parsed} color="#16a34a" />
        <Badge label="Failed" value={stats.failed} color="#dc2626" />
        <Badge label="Pending" value={stats.pending} color="#f59e0b" />
      </div>
    </div>
  );
}

export default SystemStatus;