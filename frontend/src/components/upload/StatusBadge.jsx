function StatusBadge({ status }) {
  let bgColor = "#cbd5e1";
  let textColor = "#0f172a";
  let text = status;

  if (status === "success") {
    bgColor = "#bbf7d0";
    textColor = "#166534";
  }

  if (status === "failed") {
    bgColor = "#fecaca";
    textColor = "#991b1b";
  }

  if (status === "uploading") {
    bgColor = "#bfdbfe";
    textColor = "#1d4ed8";
  }

  return (
    <span
      style={{
        background: bgColor,
        color: textColor,
        padding: "8px 14px",
        borderRadius: "20px",
        fontSize: "14px",
        fontWeight: "bold",
        display: "inline-block",
      }}
    >
      {text}
    </span>
  );
}

export default StatusBadge;