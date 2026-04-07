import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { deleteJD, deleteAllJDs } from "../../services/jdService";

function ActiveJDList({ jds = [], onRefresh }) {
  const navigate = useNavigate();
  const [toast, setToast] = useState("");

  const showToast = (message) => {
    setToast(message);
    setTimeout(() => setToast(""), 2500);
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm("Delete this job description?");
    if (!confirmDelete) return;

    try {
      await deleteJD(id);
      showToast("JD deleted successfully");
      onRefresh?.();
    } catch (err) {
      console.error("Failed to delete JD:", err);
      showToast("Failed to delete JD");
    }
  };

  const handleDeleteAll = async () => {
    const confirmDelete = window.confirm("Delete all job descriptions?");
    if (!confirmDelete) return;

    try {
      await deleteAllJDs();
      showToast("All JDs deleted successfully");
      onRefresh?.();
    } catch (err) {
      console.error("Failed to delete all JDs:", err);
      showToast("Failed to delete all JDs");
    }
  };

  if (!Array.isArray(jds) || jds.length === 0) {
    return (
      <div>
        <h3>Active Job Roles</h3>
        <p>No job descriptions available.</p>

        {toast && (
          <div style={toastStyle}>
            {toast}
          </div>
        )}
      </div>
    );
  }

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "12px",
          flexWrap: "wrap",
          gap: "12px",
        }}
      >
        <h3 style={{ margin: 0 }}>Active Job Roles</h3>

        <button
          onClick={handleDeleteAll}
          style={{
            padding: "8px 12px",
            background: "#dc2626",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "600",
          }}
        >
          Delete All JDs
        </button>
      </div>

      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
        {jds.map((jd) => {
          const parsed = jd.parsed_data || {};
          const title = jd.title || parsed.title || "Untitled Role";
          const skills = parsed.skills || jd.skills || [];

          return (
            <div
              key={jd.id}
              style={{
                padding: "16px",
                borderRadius: "12px",
                background: "#f8fafc",
                width: "280px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              }}
            >
              <h4 style={{ marginBottom: "10px", lineHeight: "1.3" }}>
                {title}
              </h4>

              <div style={{ marginBottom: "12px", minHeight: "36px" }}>
                {(skills || []).slice(0, 3).map((skill, i) => (
                  <span
                    key={i}
                    style={{
                      background: "#e2e8f0",
                      padding: "4px 10px",
                      borderRadius: "20px",
                      fontSize: "12px",
                      marginRight: "6px",
                      marginBottom: "6px",
                      display: "inline-block",
                    }}
                  >
                    {skill}
                  </span>
                ))}
              </div>

              <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                <button
                  onClick={() => navigate(`/ranking?jd=${jd.id}`)}
                  style={{
                    flex: 1,
                    padding: "8px",
                    background: "#2563eb",
                    color: "white",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontWeight: "600",
                  }}
                >
                  View Ranking
                </button>

                <button
                  onClick={() => handleDelete(jd.id)}
                  title="Delete JD"
                  style={{
                    width: "42px",
                    height: "42px",
                    background: "#dc2626",
                    color: "white",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontSize: "18px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  🗑
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {toast && (
        <div style={toastStyle}>
          {toast}
        </div>
      )}
    </div>
  );
}

const toastStyle = {
  position: "fixed",
  bottom: "24px",
  right: "24px",
  background: "#0f172a",
  color: "white",
  padding: "12px 16px",
  borderRadius: "10px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
  zIndex: 9999,
  fontWeight: "600",
};

export default ActiveJDList;