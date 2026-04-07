import { deleteResumeById, deleteAllResumes } from "../../services/resumeService";

function StatusBadge({ status }) {
  const normalized = (status || "Parsed").toLowerCase();

  let background = "#dcfce7";
  let color = "#166534";

  if (normalized === "failed") {
    background = "#fee2e2";
    color = "#991b1b";
  } else if (normalized === "pending") {
    background = "#fef3c7";
    color = "#92400e";
  }

  return (
    <span
      style={{
        background,
        color,
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "12px",
        fontWeight: "700",
      }}
    >
      {status || "Parsed"}
    </span>
  );
}

function RecentUploads({ resumes, onRefresh }) {
  const rows = Array.isArray(resumes) ? resumes : [];

  const handleDeleteOne = async (id) => {
    try {
      await deleteResumeById(id);
      onRefresh?.();
    } catch (error) {
      console.error("Failed to delete resume:", error);
    }
  };

  const handleDeleteAll = async () => {
    const confirmed = window.confirm("Delete all resumes?");
    if (!confirmed) return;

    try {
      await deleteAllResumes();
      onRefresh?.();
    } catch (error) {
      console.error("Failed to delete all resumes:", error);
    }
  };

  return (
    <div>
      <div
        style={{
          marginBottom: "12px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "12px",
        }}
      >
        <div>
          <h3 style={{ marginBottom: "6px" }}>Recent Uploads</h3>
          <p style={{ color: "#64748b", margin: 0 }}>
            Latest resumes processed by the system.
          </p>
        </div>

        <button
          onClick={handleDeleteAll}
          style={{
            padding: "8px 12px",
            borderRadius: "8px",
            border: "none",
            background: "#dc2626",
            color: "white",
            cursor: "pointer",
            fontWeight: "600",
          }}
        >
          Delete All
        </button>
      </div>

      <div
        style={{
          background: "white",
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          overflowX: "auto",
        }}
      >
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f8fafc", textAlign: "left" }}>
              <th style={{ padding: "14px" }}>Filename</th>
              <th style={{ padding: "14px" }}>Role</th>
              <th style={{ padding: "14px" }}>Date</th>
              <th style={{ padding: "14px" }}>Status</th>
              <th style={{ padding: "14px" }}>Action</th>
            </tr>
          </thead>

          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td
                  colSpan="5"
                  style={{ padding: "20px", textAlign: "center", color: "#64748b" }}
                >
                  No recent uploads available.
                </td>
              </tr>
            ) : (
              rows.map((r) => (
                <tr key={r.id} style={{ borderTop: "1px solid #e2e8f0" }}>
                  <td style={{ padding: "14px" }}>{r.filename}</td>
                  <td style={{ padding: "14px" }}>{r.job_role || "N/A"}</td>
                  <td style={{ padding: "14px" }}>{r.batch_date || "N/A"}</td>
                  <td style={{ padding: "14px" }}>
                    <StatusBadge status={r.status || "Parsed"} />
                  </td>
                  <td style={{ padding: "14px" }}>
                    <button
                      onClick={() => handleDeleteOne(r.id)}
                      style={{
                        padding: "6px 10px",
                        borderRadius: "8px",
                        border: "none",
                        background: "#dc2626",
                        color: "white",
                        cursor: "pointer",
                        fontWeight: "600",
                      }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RecentUploads;