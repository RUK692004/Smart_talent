import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div
      style={{
        width: "260px",
        minHeight: "100vh",
        background: "#1e293b",
        color: "white",
        padding: "20px",
        boxSizing: "border-box",
      }}
    >
      <h2 style={{ marginTop: 0 }}>Smart Talent</h2>

      <nav style={{ marginTop: "30px", display: "flex", flexDirection: "column", gap: "18px" }}>
        <Link to="/" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>
          Dashboard
        </Link>

        <Link to="/upload" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>
          Upload
        </Link>

        <Link to="/ranking" style={{ color: "white", textDecoration: "none", fontWeight: "500" }}>
          Ranking
        </Link>
      </nav>
    </div>
  );
}

export default Sidebar;