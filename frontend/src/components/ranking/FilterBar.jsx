function FilterBar({
  jdId,
  setJdId,
  onLoadRanking,
  minScore,
  setMinScore,
  skillFilter,
  setSkillFilter,
}) {
  return (
    <div
      style={{
        display: "flex",
        gap: "16px",
        alignItems: "flex-end",
        flexWrap: "wrap",
      }}
    >
      <div>
        <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#6b7280", marginBottom: "6px" }}>
          JD ID
        </label>
        <input
          type="number"
          value={jdId}
          onChange={(e) => setJdId(e.target.value)}
          placeholder="e.g. 3"
          style={{
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid #e0d8d0",
            fontSize: "14px",
            background: "white",
            outline: "none",
            width: "120px",
          }}
        />
      </div>

      <button
        onClick={onLoadRanking}
        style={{
          padding: "10px 24px",
          background: "#d4a843",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontWeight: "700",
          fontSize: "14px",
          transition: "background 0.2s ease",
        }}
        onMouseEnter={(e) => { e.currentTarget.style.background = "#c49a33"; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = "#d4a843"; }}
      >
        Load Ranking
      </button>

      <div>
        <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#6b7280", marginBottom: "6px" }}>
          Minimum Score
        </label>
        <input
          type="number"
          value={minScore}
          onChange={(e) => setMinScore(e.target.value)}
          placeholder="e.g. 70"
          style={{
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid #e0d8d0",
            fontSize: "14px",
            background: "white",
            outline: "none",
            width: "120px",
          }}
        />
      </div>

      <div>
        <label style={{ display: "block", fontSize: "12px", fontWeight: "600", color: "#6b7280", marginBottom: "6px" }}>
          Skill
        </label>
        <input
          type="text"
          value={skillFilter}
          onChange={(e) => setSkillFilter(e.target.value)}
          placeholder="e.g. Python"
          style={{
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid #e0d8d0",
            fontSize: "14px",
            background: "white",
            outline: "none",
            width: "140px",
          }}
        />
      </div>
    </div>
  );
}

export default FilterBar;