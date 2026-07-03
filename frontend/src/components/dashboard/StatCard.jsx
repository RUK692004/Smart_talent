function StatCard({ title, value, accent = "#d4a843", bgColor = "#fffdf8", circuit = true }) {
  return (
    <div
      style={{
        background: bgColor,
        padding: "24px",
        borderRadius: "16px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
        width: "100%",
        maxWidth: "280px",
        border: `1px solid ${accent}40`,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Circuit pattern overlay */}
      {circuit && (
        <div
          style={{
            position: "absolute",
            bottom: 0,
            right: 0,
            width: "100px",
            height: "80px",
            opacity: 0.08,
          }}
        >
          <svg viewBox="0 0 100 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 70 L10 50 L30 50 L30 30 L50 30" stroke={accent} strokeWidth="1.5" />
            <path d="M70 10 L70 30 L50 30" stroke={accent} strokeWidth="1.5" />
            <circle cx="50" cy="30" r="3" fill={accent} />
            <circle cx="10" cy="50" r="3" fill={accent} />
            <circle cx="70" cy="10" r="3" fill={accent} />
            <path d="M80 70 L80 50 L95 50" stroke={accent} strokeWidth="1.5" />
            <circle cx="95" cy="50" r="2" fill={accent} />
          </svg>
        </div>
      )}

      <p
        style={{
          margin: 0,
          color: "#6b7280",
          fontSize: "13px",
          fontWeight: "600",
          textTransform: "uppercase",
          letterSpacing: "0.5px",
        }}
      >
        {title}
      </p>

      <h2
        style={{
          marginTop: "12px",
          marginBottom: 0,
          fontSize: "36px",
          color: "#1a1a2e",
          fontWeight: "700",
          fontFamily: "'Georgia', serif",
        }}
      >
        {value}
      </h2>
    </div>
  );
}

export default StatCard;