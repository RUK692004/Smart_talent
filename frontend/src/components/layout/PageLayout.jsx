import Sidebar from "./Sidebar";

function PageLayout({ children }) {
  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "linear-gradient(135deg, #faf8f5 0%, #f5f0eb 100%)",
      }}
    >
      <Sidebar />

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <div style={{ padding: "28px 32px", flex: 1 }}>
          {children}
        </div>
      </div>
    </div>
  );
}

export default PageLayout;