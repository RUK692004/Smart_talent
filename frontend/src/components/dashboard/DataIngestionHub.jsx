import { useNavigate } from "react-router-dom";

function DataIngestionHub() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
        padding: "24px",
        border: "1px solid #e8e0d8",
        flex: 1,
      }}
    >
      <h3
        style={{
          margin: "0 0 20px 0",
          fontSize: "16px",
          fontWeight: "700",
          color: "#1a1a2e",
        }}
      >
        Data Ingestion Hub
      </h3>

      <div style={{ display: "flex", gap: "16px" }}>
        <div
          onClick={() => navigate("/upload")}
          style={{
            flex: 1,
            border: "2px dashed #d4a843",
            borderRadius: "12px",
            padding: "28px 20px",
            textAlign: "center",
            cursor: "pointer",
            background: "#fffdf8",
            transition: "all 0.2s ease",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#fff8ee";
            e.currentTarget.style.borderColor = "#c49a33";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "#fffdf8";
            e.currentTarget.style.borderColor = "#d4a843";
          }}
        >
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#d4a843" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="12" y1="18" x2="12" y2="12" />
            <line x1="9" y1="15" x2="15" y2="15" />
          </svg>
          <p style={{ margin: "12px 0 0 0", fontWeight: "600", color: "#1a1a2e", fontSize: "14px" }}>
            Upload Resume
          </p>
        </div>

        <div
          onClick={() => navigate("/jd")}
          style={{
            flex: 1,
            border: "2px dashed #7c3aed",
            borderRadius: "12px",
            padding: "28px 20px",
            textAlign: "center",
            cursor: "pointer",
            background: "#faf5ff",
            transition: "all 0.2s ease",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#f3e8ff";
            e.currentTarget.style.borderColor = "#6d28d9";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "#faf5ff";
            e.currentTarget.style.borderColor = "#7c3aed";
          }}
        >
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
          <p style={{ margin: "12px 0 0 0", fontWeight: "600", color: "#1a1a2e", fontSize: "14px" }}>
            Upload JD
          </p>
        </div>
      </div>
    </div>
  );
}

export default DataIngestionHub;