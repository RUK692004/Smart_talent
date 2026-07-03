function RecentUploadsTimeline({ resumes = [] }) {
  const rows = Array.isArray(resumes) ? resumes.slice(0, 5) : [];

  const steps = [
    { label: "Identified", color: "#d4a843" },
    { label: "Uploaded", color: "#10b981" },
    { label: "Processed", color: "#10b981" },
    { label: "Described", color: "#7c3aed" },
    { label: "Ranked", color: "#7c3aed" },
  ];

  return (
    <div
      style={{
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
        padding: "24px",
        border: "1px solid #e8e0d8",
      }}
    >
      <h3 style={{ margin: "0 0 20px 0", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" }}>
        Recent Uploads Timeline
      </h3>

      {/* Timeline */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "20px", position: "relative" }}>
        {/* Connecting line */}
        <div style={{
          position: "absolute",
          top: "50%",
          left: "6%",
          right: "6%",
          height: "2px",
          background: "#d4a843",
          opacity: 0.35,
          zIndex: 0,
          transform: "translateY(-50%)",
        }} />

        {steps.map((step, i) => (
          <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px", zIndex: 1 }}>
            <div style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              background: step.color,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
            }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
            <span style={{ fontSize: "10px", color: "#6b7280", fontWeight: "700", textTransform: "uppercase", letterSpacing: "0.5px" }}>
              {step.label}
            </span>
          </div>
        ))}
      </div>

      {/* Upload list */}
      <div>
        {rows.length === 0 ? (
          <p style={{ color: "#9ca3af", fontSize: "13px", textAlign: "center", padding: "16px" }}>
            No recent uploads.
          </p>
        ) : (
          rows.map((r, i) => (
            <div
              key={r.id || i}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "10px 0",
                borderBottom: i < rows.length - 1 ? "1px solid #f0ece6" : "none",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <div style={{
                  width: "8px",
                  height: "8px",
                  borderRadius: "50%",
                  background: "#10b981",
                  flexShrink: 0,
                }} />
                <span style={{ fontSize: "13px", color: "#1a1a2e", fontWeight: "500" }}>
                  {r.filename || "Unknown"}
                </span>
              </div>
              <span style={{ fontSize: "12px", color: "#9ca3af", fontWeight: "600" }}>
                {r.status || "Parsed"}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default RecentUploadsTimeline;