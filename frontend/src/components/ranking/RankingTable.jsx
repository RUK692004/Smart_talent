function RankingTable({ candidates = [], onSelectCandidate }) {
  const getScoreStyles = (score) => {
    if (score >= 85) {
      return {
        background: "#bbf7d0",
        color: "#166534",
      };
    }

    if (score >= 70) {
      return {
        background: "#fde68a",
        color: "#92400e",
      };
    }

    return {
      background: "#fecaca",
      color: "#991b1b",
    };
  };

  return (
    <div
      style={{
        marginTop: "20px",
        background: "white",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        overflowX: "auto",
      }}
    >
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f8fafc", textAlign: "left" }}>
            <th style={{ padding: "14px" }}>Rank</th>
            <th style={{ padding: "14px" }}>Candidate</th>
            <th style={{ padding: "14px" }}>Score</th>
            <th style={{ padding: "14px" }}>Skills</th>
            <th style={{ padding: "14px" }}>Experience</th>
            <th style={{ padding: "14px" }}>AI Justification</th>
          </tr>
        </thead>

        <tbody>
          {candidates.length === 0 ? (
            <tr>
              <td
                colSpan="6"
                style={{
                  padding: "24px",
                  textAlign: "center",
                  color: "#64748b",
                }}
              >
                No candidates found for this JD.
              </td>
            </tr>
          ) : (
            candidates.map((candidate, index) => {
              const score = candidate.score ?? 0;
              const scoreStyles = getScoreStyles(score);
              const skills = Array.isArray(candidate.skills)
                ? candidate.skills
                : [];
              const justification =
                candidate.justification || "No justification available";

              return (
                <tr
                  key={candidate.id || index}
                  onClick={() => onSelectCandidate?.(candidate)}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background =
                      index === 0 ? "#dbeafe" : "#f8fafc";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background =
                      index === 0 ? "#eff6ff" : "white";
                  }}
                  style={{
                    borderTop: "1px solid #e2e8f0",
                    cursor: "pointer",
                    background: index === 0 ? "#eff6ff" : "white",
                    fontWeight: index === 0 ? "600" : "normal",
                    transition: "background 0.2s ease",
                  }}
                >
                  <td style={{ padding: "14px" }}>
                    {index === 0 ? "🏆 1" : index + 1}
                  </td>

                  <td style={{ padding: "14px" }}>
                    {candidate.name || "Unknown"}
                  </td>

                  <td style={{ padding: "14px" }}>
                    <span
                      style={{
                        padding: "6px 12px",
                        borderRadius: "20px",
                        fontWeight: "bold",
                        background: scoreStyles.background,
                        color: scoreStyles.color,
                      }}
                    >
                      {score}%
                    </span>
                  </td>

                  <td style={{ padding: "14px" }}>
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "6px",
                      }}
                    >
                      {skills.length > 0 ? (
                        skills.slice(0, 5).map((skill, i) => (
                          <span
                            key={i}
                            style={{
                              background: "#e2e8f0",
                              padding: "4px 10px",
                              borderRadius: "20px",
                              fontSize: "12px",
                            }}
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span style={{ fontSize: "12px", color: "#94a3b8" }}>
                          No skills listed
                        </span>
                      )}
                    </div>
                  </td>

                  <td style={{ padding: "14px" }}>
                    {candidate.experience ?? 0} years
                  </td>

                  <td style={{ padding: "14px", color: "#334155" }}>
                    {justification.length > 80
                      ? justification.slice(0, 80) + "..."
                      : justification}
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