import { useState, useMemo } from "react";
import { downloadResume } from "../../services/resumeService";

function IntelligentRanking({ candidates = [], onFilter }) {
  const [jdId, setJdId] = useState("4");
  const [minScore, setMinScore] = useState(90);
  const [skill, setSkill] = useState("");

  const filteredCandidates = useMemo(() => {
    return candidates.filter((c) => {
      const score = c.score ?? 0;
      const skills = Array.isArray(c.matched_skills) ? c.matched_skills : [];

      const matchesScore = score >= minScore;
      const matchesSkill = skill.trim() === "" || skills.some((s) => String(s).toLowerCase().includes(skill.toLowerCase()));

      return matchesScore && matchesSkill;
    });
  }, [candidates, minScore, skill]);

  const topCandidate = filteredCandidates.length > 0 ? filteredCandidates[0] : null;

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
      {/* Header */}
      <div style={{ marginBottom: "20px" }}>
        <h2 style={{ margin: "0 0 4px 0", fontSize: "20px", fontWeight: "700", color: "#1a1a2e", fontFamily: "'Georgia', serif" }}>
          Intelligent Ranking
        </h2>
        <p style={{ margin: 0, color: "#6b7280", fontSize: "13px" }}>
          View ranked candidates, filter results, and inspect AI fit summaries.
        </p>
      </div>

      {/* Green Filter Panel - No sliders */}
      <div style={{
        background: "#065f46",
        borderRadius: "12px",
        padding: "18px",
        display: "flex",
        gap: "16px",
        flexWrap: "wrap",
        marginBottom: "20px",
      }}>
        {/* JD ID */}
        <div style={{ flex: 1, minWidth: "120px" }}>
          <label style={{ display: "block", fontSize: "11px", color: "#a7f3d0", fontWeight: "700", marginBottom: "6px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
            JD ID
          </label>
          <input
            value={jdId}
            onChange={(e) => setJdId(e.target.value)}
            style={{
              width: "100%",
              padding: "8px 12px",
              borderRadius: "8px",
              border: "1px solid rgba(255,255,255,0.2)",
              fontSize: "13px",
              background: "rgba(255,255,255,0.1)",
              color: "white",
              outline: "none",
              boxSizing: "border-box",
            }}
          />
        </div>

        {/* Minimum Score */}
        <div style={{ flex: 1, minWidth: "120px" }}>
          <label style={{ display: "block", fontSize: "11px", color: "#a7f3d0", fontWeight: "700", marginBottom: "6px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
            Minimum Score
          </label>
          <input
            value={minScore}
            onChange={(e) => setMinScore(Number(e.target.value))}
            style={{
              width: "100%",
              padding: "8px 12px",
              borderRadius: "8px",
              border: "1px solid rgba(255,255,255,0.2)",
              fontSize: "13px",
              background: "rgba(255,255,255,0.1)",
              color: "white",
              outline: "none",
              boxSizing: "border-box",
            }}
          />
        </div>

        {/* Skill */}
        <div style={{ flex: 1, minWidth: "120px" }}>
          <label style={{ display: "block", fontSize: "11px", color: "#a7f3d0", fontWeight: "700", marginBottom: "6px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
            Skill
          </label>
          <select
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
            style={{
              width: "100%",
              padding: "8px 12px",
              borderRadius: "8px",
              border: "1px solid rgba(255,255,255,0.2)",
              fontSize: "13px",
              background: "rgba(255,255,255,0.1)",
              color: skill ? "white" : "#a7f3d0",
              outline: "none",
              boxSizing: "border-box",
              cursor: "pointer",
            }}
          >
            <option value="" style={{ color: "#1a1a2e" }}>All Skills</option>
            <option value="html" style={{ color: "#1a1a2e" }}>HTML</option>
            <option value="css" style={{ color: "#1a1a2e" }}>CSS</option>
            <option value="javascript" style={{ color: "#1a1a2e" }}>JavaScript</option>
            <option value="react" style={{ color: "#1a1a2e" }}>React</option>
            <option value="python" style={{ color: "#1a1a2e" }}>Python</option>
          </select>
        </div>
      </div>

      {/* Candidate Section */}
      {topCandidate ? (
        <div style={{ display: "flex", gap: "20px", alignItems: "flex-start" }}>
          {/* Left - Candidate Info */}
          <div style={{ flex: 1, minWidth: 0 }}>
            {/* Avatar + Name + Score */}
            <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "12px" }}>
              <div style={{
                width: "42px",
                height: "42px",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #d4a843, #c49a33)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "white",
                fontWeight: "700",
                fontSize: "18px",
                fontFamily: "'Georgia', serif",
                flexShrink: 0,
              }}>
                {topCandidate.name ? topCandidate.name.charAt(0).toUpperCase() : "?"}
              </div>
              <div style={{ minWidth: 0 }}>
                <p style={{ margin: 0, fontWeight: "700", color: "#1a1a2e", fontSize: "15px" }}>{topCandidate.name || "Unknown"}</p>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "4px" }}>
                  <div style={{ width: "80px", height: "6px", borderRadius: "3px", background: "#f0ece6", overflow: "hidden" }}>
                    <div style={{ width: `${Math.min(topCandidate.score || 0, 100)}%`, height: "100%", borderRadius: "3px", background: "linear-gradient(90deg, #3b82f6, #10b981)" }} />
                  </div>
                  <span style={{ fontWeight: "700", color: "#1a1a2e", fontSize: "14px" }}>{topCandidate.score || 0}</span>
                </div>
              </div>
            </div>

            {/* Skill Badges */}
            <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "12px", maxWidth: "360px" }}>
              {(topCandidate.matched_skills || []).slice(0, 5).map((skill, i) => (
                <span key={i} style={{
                  padding: "4px 10px",
                  borderRadius: "6px",
                  background: "#f0fdf4",
                  color: "#166534",
                  fontSize: "12px",
                  fontWeight: "600",
                }}>
                  {skill}
                </span>
              ))}
            </div>

            {/* AI Fit Summary - Always visible */}
            <div style={{
              background: "#faf8f5",
              borderRadius: "10px",
              padding: "12px 14px",
              border: "1px solid #e8e0d8",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "8px" }}>
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#d4a843"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="20" x2="18" y2="10" />
                  <line x1="12" y1="20" x2="12" y2="4" />
                  <line x1="6" y1="20" x2="6" y2="14" />
                </svg>
                <span style={{ fontSize: "13px", fontWeight: "700", color: "#d4a843" }}>AI Fit Summary</span>
              </div>
              <p style={{ fontSize: "12px", color: "#6b7280", lineHeight: "1.6", margin: 0 }}>
                {topCandidate.justification || "The AI automatically generates a detailed skill-fit summary to minimize manual review and provide recruiter insights."}
              </p>
            </div>
          </div>

          {/* Right - Profile Card */}
          <div style={{
            width: "180px",
            borderRadius: "12px",
            overflow: "hidden",
            border: "1px solid #e8e0d8",
            flexShrink: 0,
          }}>
            {/* Green header with avatar */}
            <div style={{
              height: "64px",
              background: "linear-gradient(135deg, #065f46, #047857)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              position: "relative",
            }}>
              <div style={{
                width: "48px",
                height: "48px",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #d4a843, #c49a33)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "white",
                fontWeight: "700",
                fontSize: "20px",
                fontFamily: "'Georgia', serif",
                border: "3px solid white",
              }}>
                {topCandidate.name ? topCandidate.name.charAt(0).toUpperCase() : "?"}
              </div>
            </div>

            {/* Profile details */}
            <div style={{ padding: "12px" }}>
              <p style={{ margin: 0, fontWeight: "700", color: "#1a1a2e", fontSize: "13px" }}>{topCandidate.name || "Unknown"}</p>
              <button
                onClick={async () => {
                  try {
                    const blob = await downloadResume(topCandidate.resume_id);
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = topCandidate.filename || "resume.pdf";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                  } catch (err) {
                    console.error("Download failed:", err);
                    alert("Failed to download resume.");
                  }
                }}
                style={{
                  marginTop: "8px",
                  width: "100%",
                  padding: "8px 12px",
                  borderRadius: "8px",
                  border: "1px solid #d4a843",
                  background: "transparent",
                  color: "#d4a843",
                  cursor: "pointer",
                  fontWeight: "600",
                  fontSize: "12px",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "#d4a843";
                  e.currentTarget.style.color = "white";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "transparent";
                  e.currentTarget.style.color = "#d4a843";
                }}
              >
                Download Resume
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div style={{ textAlign: "center", padding: "32px", color: "#9ca3af", fontSize: "13px" }}>
          No candidates match the selected filters.
        </div>
      )}
    </div>
  );
}

export default IntelligentRanking;