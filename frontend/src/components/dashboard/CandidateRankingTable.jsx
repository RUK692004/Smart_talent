import { useNavigate } from "react-router-dom";

function CandidateRankingTable({ candidates = [], jdId }) {
  const navigate = useNavigate();

  const rows = Array.isArray(candidates) ? candidates.slice(0, 5) : [];

  return (
    <div
      style={{
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
        padding: "24px",
        border: "1px solid #e8e0d8",
        marginTop: "24px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <h3 style={{ margin: 0, fontSize: "16px", fontWeight: "700", color: "#1a1a2e" }}>
          Candidate Ranking
        </h3>
        {jdId && (
          <button
            onClick={() => navigate(`/ranking?jdId=${jdId}`)}
            style={{
              padding: "8px 16px",
              borderRadius: "8px",
              border: "1px solid #d4a843",
              background: "transparent",
              color: "#d4a843",
              cursor: "pointer",
              fontWeight: "600",
              fontSize: "13px",
            }}
          >
            View All
          </button>
        )}
      </div>

      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #f0ece6" }}>
              <th style={{ padding: "12px 8px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Rank</th>
              <th style={{ padding: "12px 8px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Candidate</th>
              <th style={{ padding: "12px 8px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Score</th>
              <th style={{ padding: "12px 8px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Skills</th>
              <th style={{ padding: "12px 8px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Experience</th>
              <th style={{ padding: "12px 8px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>AI Justification</th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ padding: "40px 20px", textAlign: "center", color: "#9ca3af" }}>
                  No candidates ranked yet. Upload resumes and create a JD to get started.
                </td>
              </tr>
            ) : (
              rows.map((c, index) => (
                <tr key={c.resume_id || index} style={{ borderBottom: "1px solid #f0ece6" }}>
                  <td style={{ padding: "14px 8px" }}>
                    <span style={{
                      display: "inline-flex",
                      alignItems: "center",
                      justifyContent: "center",
                      width: "28px",
                      height: "28px",
                      borderRadius: "50%",
                      background: index === 0 ? "#d4a843" : index === 1 ? "#9ca3af" : index === 2 ? "#cd7f32" : "#f0ece6",
                      color: index < 3 ? "white" : "#6b7280",
                      fontWeight: "700",
                      fontSize: "13px",
                    }}>
                      {index + 1}
                    </span>
                  </td>
                  <td style={{ padding: "14px 8px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                      <div style={{
                        width: "32px",
                        height: "32px",
                        borderRadius: "50%",
                        background: "linear-gradient(135deg, #d4a843, #c49a33)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "white",
                        fontWeight: "700",
                        fontSize: "14px",
                      }}>
                        {c.name ? c.name.charAt(0).toUpperCase() : "?"}
                      </div>
                      <span style={{ fontWeight: "600", color: "#1a1a2e", fontSize: "14px" }}>{c.name || "Unknown"}</span>
                    </div>
                  </td>
                  <td style={{ padding: "14px 8px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <div style={{
                        width: "80px",
                        height: "6px",
                        borderRadius: "3px",
                        background: "#f0ece6",
                        overflow: "hidden",
                      }}>
                        <div style={{
                          width: `${c.score || 0}%`,
                          height: "100%",
                          borderRadius: "3px",
                          background: "linear-gradient(90deg, #3b82f6, #10b981)",
                        }} />
                      </div>
                      <span style={{ fontWeight: "700", color: "#1a1a2e", fontSize: "14px" }}>{c.score || 0}</span>
                    </div>
                  </td>
                  <td style={{ padding: "14px 8px" }}>
                    <div style={{ display: "flex", gap: "4px", flexWrap: "wrap" }}>
                      {(c.matched_skills || []).slice(0, 3).map((skill, i) => (
                        <span key={i} style={{
                          padding: "2px 8px",
                          borderRadius: "4px",
                          background: "#f0fdf4",
                          color: "#166534",
                          fontSize: "11px",
                          fontWeight: "600",
                        }}>
                          {skill}
                        </span>
                      ))}
                      {(c.matched_skills || []).length > 3 && (
                        <span style={{ fontSize: "11px", color: "#9ca3af" }}>+{c.matched_skills.length - 3}</span>
                      )}
                    </div>
                  </td>
                  <td style={{ padding: "14px 8px", fontSize: "14px", color: "#6b7280" }}>
                    {c.candidate_years ? `${c.candidate_years} yrs` : "N/A"}
                  </td>
                  <td style={{ padding: "14px 8px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="20" x2="18" y2="10" />
                        <line x1="12" y1="20" x2="12" y2="4" />
                        <line x1="6" y1="20" x2="6" y2="14" />
                      </svg>
                      <span style={{ fontSize: "12px", color: "#6b7280" }}>AI</span>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Search Filters */}
      <div style={{
        marginTop: "20px",
        display: "flex",
        gap: "12px",
        flexWrap: "wrap",
        padding: "16px",
        background: "#faf8f5",
        borderRadius: "10px",
      }}>
        <input
          placeholder="JD ID"
          style={{
            padding: "8px 14px",
            borderRadius: "8px",
            border: "1px solid #e0d8d0",
            fontSize: "13px",
            background: "white",
            outline: "none",
            flex: 1,
            minWidth: "100px",
          }}
        />
        <input
          placeholder="e.g. 70"
          style={{
            padding: "8px 14px",
            borderRadius: "8px",
            border: "1px solid #e0d8d0",
            fontSize: "13px",
            background: "white",
            outline: "none",
            flex: 1,
            minWidth: "100px",
          }}
        />
        <input
          placeholder="e.g. 3"
          style={{
            padding: "8px 14px",
            borderRadius: "8px",
            border: "1px solid #e0d8d0",
            fontSize: "13px",
            background: "white",
            outline: "none",
            flex: 1,
            minWidth: "100px",
          }}
        />
      </div>
    </div>
  );
}

export default CandidateRankingTable;