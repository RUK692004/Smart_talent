function RankingTable({ candidates = [], onSelectCandidate }) {
  const getScoreStyles = (score) => {
    if (score >= 85) {
      return { background: "#bbf7d0", color: "#166534" };
    }
    if (score >= 70) {
      return { background: "#fde68a", color: "#92400e" };
    }
    return { background: "#fecaca", color: "#991b1b" };
  };

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #f0ece6" }}>
            <th style={{ padding: "14px 12px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Rank</th>
            <th style={{ padding: "14px 12px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Candidate</th>
            <th style={{ padding: "14px 12px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Score</th>
            <th style={{ padding: "14px 12px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Skills</th>
            <th style={{ padding: "14px 12px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Experience</th>
            <th style={{ padding: "14px 12px", textAlign: "left", fontSize: "12px", fontWeight: "700", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>AI Justification</th>
          </tr>
        </thead>

        <tbody>
          {candidates.length === 0 ? (
            <tr>
              <td colSpan="6" style={{ padding: "40px 20px", textAlign: "center", color: "#9ca3af" }}>
                No candidates found for this JD.
              </td>
            </tr>
          ) : (
            candidates.map((candidate, index) => {
              const score = candidate.score ?? 0;
              const scoreStyles = getScoreStyles(score);
              const skills = Array.isArray(candidate.skills) ? candidate.skills : [];
              const justification = candidate.justification || "No justification available";

              return (
                <tr
                  key={candidate.id || index}
                  onClick={() => onSelectCandidate?.(candidate)}
                  onMouseEnter={(e) => { e.currentTarget.style.background = "#faf8f5"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = "transparent"; }}
                  style={{
                    borderBottom: "1px solid #f0ece6",
                    cursor: "pointer",
                    transition: "background 0.2s ease",
                  }}
                >
                  <td style={{ padding: "14px 12px" }}>
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

                  <td style={{ padding: "14px 12px" }}>
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
                        {candidate.name ? candidate.name.charAt(0).toUpperCase() : "?"}
                      </div>
                      <span style={{ fontWeight: "600", color: "#1a1a2e", fontSize: "14px" }}>
                        {candidate.name || "Unknown"}
                      </span>
                    </div>
                  </td>

                  <td style={{ padding: "14px 12px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <div style={{
                        width: "80px",
                        height: "6px",
                        borderRadius: "3px",
                        background: "#f0ece6",
                        overflow: "hidden",
                      }}>
                        <div style={{
                          width: `${score}%`,
                          height: "100%",
                          borderRadius: "3px",
                          background: "linear-gradient(90deg, #3b82f6, #10b981)",
                        }} />
                      </div>
                      <span style={{
                        padding: "2px 8px",
                        borderRadius: "6px",
                        fontWeight: "700",
                        fontSize: "13px",
                        background: scoreStyles.background,
                        color: scoreStyles.color,
                      }}>
                        {score}%
                      </span>
                    </div>
                  </td>

                  <td style={{ padding: "14px 12px" }}>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                      {skills.length > 0 ? (
                        skills.slice(0, 5).map((skill, i) => (
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
                        ))
                      ) : (
                        <span style={{ fontSize: "12px", color: "#9ca3af" }}>No skills listed</span>
                      )}
                    </div>
                  </td>

                  <td style={{ padding: "14px 12px", fontSize: "14px", color: "#6b7280" }}>
                    {candidate.experience ?? 0} years
                  </td>

                  <td style={{ padding: "14px 12px", color: "#6b7280", fontSize: "13px", maxWidth: "200px" }}>
                    <div style={{ display: "flex", alignItems: "flex-start", gap: "6px" }}>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginTop: "2px", flexShrink: 0 }}>
                        <line x1="18" y1="20" x2="18" y2="10" />
                        <line x1="12" y1="20" x2="12" y2="4" />
                        <line x1="6" y1="20" x2="6" y2="14" />
                      </svg>
                      <span>
                        {justification.length > 80 ? justification.slice(0, 80) + "..." : justification}
                      </span>
                    </div>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}

export default RankingTable;