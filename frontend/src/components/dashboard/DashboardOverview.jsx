function DashboardOverview({ stats = { parsed: 0, failed: 0, pending: 0 } }) {
  const percentage = stats.parsed > 0 ? 90 : 0;
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div
      style={{
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
        padding: "24px",
        border: "1px solid #e8e0d8",
        flex: 1,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Circuit pattern */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          width: "120px",
          height: "100px",
          opacity: 0.05,
        }}
      >
        <svg viewBox="0 0 120 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10 80 L10 60 L40 60 L40 30 L70 30" stroke="#6366f1" strokeWidth="1.5" />
          <path d="M80 10 L80 40 L50 40" stroke="#6366f1" strokeWidth="1.5" />
          <circle cx="70" cy="30" r="3" fill="#6366f1" />
          <circle cx="10" cy="60" r="3" fill="#6366f1" />
          <circle cx="80" cy="10" r="3" fill="#6366f1" />
          <path d="M90 85 L90 65 L110 65" stroke="#6366f1" strokeWidth="1.5" />
          <circle cx="110" cy="65" r="2" fill="#6366f1" />
        </svg>
      </div>

      <h3
        style={{
          margin: "0 0 20px 0",
          fontSize: "16px",
          fontWeight: "700",
          color: "#1a1a2e",
        }}
      >
        Dashboard Overview
      </h3>

      <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
        {/* Circular Gauge */}
        <div style={{ position: "relative", width: "120px", height: "120px", flexShrink: 0 }}>
          <svg width="120" height="120" viewBox="0 0 120 120">
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="10"
            />
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke="url(#gaugeGradient)"
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              transform="rotate(-90 60 60)"
            />
            <defs>
              <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#3b82f6" />
                <stop offset="100%" stopColor="#10b981" />
              </linearGradient>
            </defs>
          </svg>
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              textAlign: "center",
            }}
          >
            <span style={{ fontSize: "24px", fontWeight: "700", color: "#1a1a2e" }}>
              {percentage}%
            </span>
          </div>
        </div>

        {/* Stats */}
        <div style={{ flex: 1 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
            <div>
              <p style={{ margin: 0, fontSize: "12px", color: "#6b7280", fontWeight: "600" }}>Parsed</p>
              <p style={{ margin: "4px 0 0 0", fontSize: "18px", fontWeight: "700", color: "#1a1a2e" }}>{stats.parsed || 0}</p>
            </div>
            <div>
              <p style={{ margin: 0, fontSize: "12px", color: "#6b7280", fontWeight: "600" }}>Failed</p>
              <p style={{ margin: "4px 0 0 0", fontSize: "18px", fontWeight: "700", color: "#ef4444" }}>{stats.failed || 0}</p>
            </div>
            <div>
              <p style={{ margin: 0, fontSize: "12px", color: "#6b7280", fontWeight: "600" }}>Pending</p>
              <p style={{ margin: "4px 0 0 0", fontSize: "18px", fontWeight: "700", color: "#f59e0b" }}>{stats.pending || 0}</p>
            </div>
            <div>
              <p style={{ margin: 0, fontSize: "12px", color: "#6b7280", fontWeight: "600" }}>Counts</p>
              <p style={{ margin: "4px 0 0 0", fontSize: "18px", fontWeight: "700", color: "#1a1a2e" }}>{(stats.parsed || 0) + (stats.failed || 0) + (stats.pending || 0)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DashboardOverview;