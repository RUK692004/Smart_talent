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
        background: "white",
        padding: "16px",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        display: "flex",
        gap: "20px",
        alignItems: "center",
        flexWrap: "wrap",
        marginTop: "20px",
      }}
    >
      <div>
        <label><strong>JD ID:</strong></label>
        <input
          type="number"
          value={jdId}
          onChange={(e) => setJdId(e.target.value)}
          placeholder="e.g. 3"
          style={{
            marginLeft: "10px",
            padding: "8px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
      </div>

      <button
        onClick={onLoadRanking}
        style={{
          padding: "10px 18px",
          background: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Load Ranking
      </button>

      <div>
        <label><strong>Minimum Score:</strong></label>
        <input
          type="number"
          value={minScore}
          onChange={(e) => setMinScore(e.target.value)}
          placeholder="e.g. 70"
          style={{
            marginLeft: "10px",
            padding: "8px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
      </div>

      <div>
        <label><strong>Skill:</strong></label>
        <input
          type="text"
          value={skillFilter}
          onChange={(e) => setSkillFilter(e.target.value)}
          placeholder="e.g. Python"
          style={{
            marginLeft: "10px",
            padding: "8px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
      </div>
    </div>
  );
}

export default FilterBar;