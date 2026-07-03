import { useNavigate } from "react-router-dom";

function DataOnboarding() {
  const navigate = useNavigate();

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
      <h2 style={{ margin: "0 0 6px 0", fontSize: "20px", fontWeight: "700", color: "#1a1a2e", fontFamily: "'Georgia', serif" }}>
        Data Onboarding
      </h2>
      <p style={{ margin: "0 0 24px 0", color: "#6b7280", fontSize: "13px" }}>
        Use exquisitely designed drop zones that enable candidate ranking.
      </p>

      {/* Upload Resumes */}
      <div
        onClick={() => navigate("/upload")}
        style={{
          border: "2px dashed #e0d8d0",
          borderRadius: "14px",
          padding: "32px 20px",
          textAlign: "center",
          cursor: "pointer",
          background: "#faf8f5",
          marginBottom: "16px",
          transition: "all 0.2s ease",
          position: "relative",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = "#d4a843";
          e.currentTarget.style.background = "#fffdf8";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = "#e0d8d0";
          e.currentTarget.style.background = "#faf8f5";
        }}
      >
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d4a843" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
          <polyline points="10 9 9 9 8 9" />
        </svg>
        <p style={{ margin: "12px 0 4px 0", fontWeight: "700", color: "#1a1a2e", fontSize: "15px" }}>
          Upload Resumes
        </p>
        <p style={{ margin: 0, color: "#9ca3af", fontSize: "12px" }}>
          Exquisitely designed drop zones
        </p>
      </div>

      {/* Upload Job Descriptions */}
      <div
        onClick={() => navigate("/jd")}
        style={{
          border: "2px dashed #e0d8d0",
          borderRadius: "14px",
          padding: "32px 20px",
          textAlign: "center",
          cursor: "pointer",
          background: "#faf8f5",
          transition: "all 0.2s ease",
          position: "relative",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = "#7c3aed";
          e.currentTarget.style.background = "#faf5ff";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = "#e0d8d0";
          e.currentTarget.style.background = "#faf8f5";
        }}
      >
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
        </svg>
        <p style={{ margin: "12px 0 4px 0", fontWeight: "700", color: "#1a1a2e", fontSize: "15px" }}>
          Upload Job Descriptions
        </p>
        <p style={{ margin: 0, color: "#9ca3af", fontSize: "12px" }}>
          Exquisitely designed drop zones
        </p>
      </div>
    </div>
  );
}

export default DataOnboarding;