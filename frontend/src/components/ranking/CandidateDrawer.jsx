function CandidateDrawer({ candidate, onClose }) {
  if (!candidate) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: "fixed",
          inset: 0,
          background: "rgba(0,0,0,0.4)",
          zIndex: 999,
        }}
      />

      {/* Drawer */}
      <div
        style={{
          position: "fixed",
          top: 0,
          right: 0,
          width: "420px",
          maxWidth: "100%",
          height: "100vh",
          background: "white",
          boxShadow: "-4px 0 12px rgba(0,0,0,0.15)",
          padding: "24px",
          overflowY: "auto",
          zIndex: 1000,
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <h2 style={{ margin: 0 }}>Candidate Details</h2>

          <button
            onClick={onClose}
            style={{
              border: "none",
              background: "#e2e8f0",
              padding: "8px 12px",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            ✕
          </button>
        </div>

        {/* Basic Info */}
        <div
          style={{
            background: "#f8fafc",
            padding: "16px",
            borderRadius: "10px",
            marginBottom: "20px",
          }}
        >
          <h3 style={{ marginTop: 0 }}>
            {candidate.name || "Unknown Candidate"}
          </h3>

          <p><strong>Score:</strong> {candidate.score ?? 0}%</p>
          <p><strong>Experience:</strong> {candidate.experience ?? 0} years</p>
        </div>

        {/* Skills */}
        <div style={{ marginBottom: "20px" }}>
          <h3>Skills</h3>

          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {(candidate.skills || []).length > 0 ? (
              candidate.skills.map((skill, index) => (
                <span
                  key={index}
                  style={{
                    background: "#dbeafe",
                    color: "#1e3a8a",
                    padding: "6px 12px",
                    borderRadius: "20px",
                    fontSize: "13px",
                  }}
                >
                  {skill}
                </span>
              ))
            ) : (
              <p style={{ color: "#64748b" }}>No skills listed.</p>
            )}
          </div>
        </div>

        {/* AI Justification */}
        <div style={{ marginBottom: "20px" }}>
          <h3>AI Justification</h3>

          <div
            style={{
              background: "#f8fafc",
              borderLeft: "4px solid #2563eb",
              padding: "14px",
              borderRadius: "8px",
              color: "#334155",
              lineHeight: "1.6",
            }}
          >
            {candidate.justification || "No justification available."}
          </div>
        </div>

        {/* Optional Sections */}
        {candidate.summary && (
          <Section title="Summary" content={candidate.summary} />
        )}

        {candidate.ranking_reason && (
          <Section title="Ranking Reason" content={candidate.ranking_reason} />
        )}

        {candidate.experience_depth && (
          <Section title="Experience Depth" content={candidate.experience_depth} />
        )}
      </div>
    </>
  );
}

function Section({ title, content }) {
  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>{title}</h3>
      <p style={{ color: "#334155", lineHeight: "1.6" }}>{content}</p>
    </div>
  );
}

export default CandidateDrawer;