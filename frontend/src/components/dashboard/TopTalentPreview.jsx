import { useNavigate } from "react-router-dom";

function TopTalentPreview({ candidates, jdId, loading = false }) {
  const navigate = useNavigate();
  const topCandidates = Array.isArray(candidates) ? candidates.slice(0, 3) : [];

  return (
    <div>
      <div style={{ marginBottom: "12px" }}>
        <h2 style={{ marginBottom: "6px" }}>Top Talent</h2>
        <p style={{ color: "#64748b", margin: 0 }}>
          Best-ranked candidates from the latest active role.
        </p>
      </div>

      {loading ? (
        <div
          style={{
            background: "white",
            padding: "18px",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            color: "#64748b",
          }}
        >
          Loading top talent...
        </div>
      ) : topCandidates.length === 0 ? (
        <div
          style={{
            background: "white",
            padding: "18px",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            color: "#64748b",
          }}
        >
          No ranked candidates available yet.
        </div>
      ) : (
        <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
          {topCandidates.map((c, index) => {
            const skills = Array.isArray(c?.skills)
              ? c.skills
              : Array.isArray(c?.matched_skills)
              ? c.matched_skills
              : Array.isArray(c?.top_skills)
              ? c.top_skills
              : [];

            const score = Number(
              c?.score ??
                c?.compatibility_score ??
                c?.match_score ??
                c?.similarity_score ??
                0
            );

            const name =
              c?.name ||
              c?.candidate_name ||
              c?.filename ||
              c?.resume_name ||
              "Unknown Candidate";

            const justification =
              c?.justification ||
              c?.ai_justification ||
              c?.summary_of_fit ||
              c?.reason ||
              "No summary available.";

            return (
              <div
                key={c?.id || c?.resume_id || index}
                style={{
                  background: "white",
                  padding: "18px",
                  borderRadius: "12px",
                  width: "280px",
                  boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "10px",
                    gap: "10px",
                  }}
                >
                  <h4 style={{ margin: 0, lineHeight: "1.3" }}>{name}</h4>

                  <span
                    style={{
                      background:
                        score >= 70
                          ? "#dcfce7"
                          : score >= 40
                          ? "#fef3c7"
                          : "#fee2e2",
                      color:
                        score >= 70
                          ? "#166534"
                          : score >= 40
                          ? "#92400e"
                          : "#991b1b",
                      padding: "4px 10px",
                      borderRadius: "999px",
                      fontSize: "12px",
                      fontWeight: "700",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {score}%
                  </span>
                </div>

                <div style={{ marginBottom: "10px", minHeight: "34px" }}>
                  {skills.length > 0 ? (
                    skills.slice(0, 3).map((skill, i) => (
                      <span
                        key={i}
                        style={{
                          display: "inline-block",
                          background: "#eef2ff",
                          color: "#3730a3",
                          padding: "4px 8px",
                          borderRadius: "6px",
                          marginRight: "6px",
                          marginBottom: "6px",
                          fontSize: "12px",
                        }}
                      >
                        {String(skill)}
                      </span>
                    ))
                  ) : (
                    <span style={{ fontSize: "12px", color: "#94a3b8" }}>
                      No skills listed
                    </span>
                  )}
                </div>

                <p
                  style={{
                    marginTop: "8px",
                    fontSize: "14px",
                    color: "#475569",
                    lineHeight: "1.5",
                    minHeight: "64px",
                  }}
                >
                  {justification.length > 100
                    ? justification.slice(0, 100) + "..."
                    : justification}
                </p>

                <button
                  onClick={() =>
                    navigate(jdId ? `/ranking?jd=${jdId}` : "/ranking")
                  }
                  style={{
                    marginTop: "8px",
                    padding: "8px 12px",
                    borderRadius: "8px",
                    border: "none",
                    background: "#2563eb",
                    color: "white",
                    cursor: "pointer",
                    fontWeight: "600",
                  }}
                >
                  View Ranking
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default TopTalentPreview;