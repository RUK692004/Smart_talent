import { Link, useLocation } from "react-router-dom";

const menuItems = [
  {
    path: "/",
    label: "Dashboard",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" />
        <rect x="14" y="3" width="7" height="7" />
        <rect x="14" y="14" width="7" height="7" />
        <rect x="3" y="14" width="7" height="7" />
      </svg>
    ),
  },
  {
    path: "/upload",
    label: "Upload",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="17 8 12 3 7 8" />
        <line x1="12" y1="3" x2="12" y2="15" />
      </svg>
    ),
  },
  {
    path: "/ranking",
    label: "Ranking",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5C7 4 7 7 7 7" />
        <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5C17 4 17 7 17 7" />
        <path d="M4 22h16" />
        <path d="M10 22V8h4v14" />
        <path d="M10 8h4" />
      </svg>
    ),
  },
];

function Sidebar() {
  const location = useLocation();

  return (
    <div
      style={{
        width: "220px",
        minHeight: "100vh",
        background: "#1a1a2e",
        color: "white",
        padding: "28px 20px",
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ marginBottom: "40px" }}>
        <h1
          style={{
            margin: 0,
            fontSize: "24px",
            fontWeight: "700",
            color: "#d4a843",
            fontFamily: "'Georgia', serif",
            letterSpacing: "1px",
          }}
        >
          Smart Talent
        </h1>
      </div>

      <nav style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "14px",
                padding: "12px 16px",
                borderRadius: "10px",
                textDecoration: "none",
                color: isActive ? "#d4a843" : "#a0a0b8",
                background: isActive ? "rgba(212, 168, 67, 0.1)" : "transparent",
                fontWeight: isActive ? "600" : "400",
                fontSize: "15px",
                transition: "all 0.2s ease",
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = "rgba(255,255,255,0.05)";
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.background = "transparent";
                }
              }}
            >
              <span style={{ opacity: isActive ? 1 : 0.7 }}>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}

export default Sidebar;