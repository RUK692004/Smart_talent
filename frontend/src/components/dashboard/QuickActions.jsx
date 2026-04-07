import { useNavigate } from "react-router-dom";

function ActionButton({ label, onClick, color }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "10px 16px",
        borderRadius: "10px",
        border: "none",
        background: color,
        color: "white",
        cursor: "pointer",
        fontWeight: "600",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      {label}
    </button>
  );
}

function QuickActions() {
  const navigate = useNavigate();

  return (
    <div>
      <h3 style={{ marginBottom: "12px" }}>Quick Actions</h3>

      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <ActionButton
          label="Upload Resume"
          onClick={() => navigate("/upload")}
          color="#2563eb"
        />
        <ActionButton
          label="Upload JD"
          onClick={() => navigate("/jd")}
          color="#7c3aed"
        />
        <ActionButton
          label="View Ranking"
          onClick={() => navigate("/ranking")}
          color="#16a34a"
        />
      </div>
    </div>
  );
}

export default QuickActions;