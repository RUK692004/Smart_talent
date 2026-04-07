function StatCard({ title, value, accent = "#2563eb" }) {
  return (
    <div
      style={{
        background: "white",
        padding: "22px",
        borderRadius: "14px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        width: "240px",
        borderTop: `4px solid ${accent}`,
      }}
    >
      <p
        style={{
          margin: 0,
          color: "#64748b",
          fontSize: "14px",
          fontWeight: "600",
        }}
      >
        {title}
      </p>

      <h2
        style={{
          marginTop: "14px",
          marginBottom: 0,
          fontSize: "34px",
          color: "#0f172a",
        }}
      >
        {value}
      </h2>
    </div>
  );
}

export default StatCard;