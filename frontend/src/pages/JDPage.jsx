import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PageLayout from "../components/layout/PageLayout";
import { getAllJDs, uploadJD, deleteJD } from "../services/jdService";

function JDPage() {
  const navigate = useNavigate();

  const [jds, setJDs] = useState([]);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [skills, setSkills] = useState("");
  const [keywords, setKeywords] = useState("");
  const [experience, setExperience] = useState("");

  useEffect(() => {
    loadJDs();
  }, []);

  const normalizeJDs = (data) => {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data?.jds)) return data.jds;
    if (Array.isArray(data?.jd)) return data.jd;
    if (Array.isArray(data?.data)) return data.data;
    if (Array.isArray(data?.job_descriptions)) return data.job_descriptions;
    if (data?.jd && typeof data.jd === "object") return [data.jd];
    return [];
  };

  const loadJDs = async () => {
    try {
      const data = await getAllJDs();
      const jdList = normalizeJDs(data);
      setJDs(jdList);
    } catch (err) {
      console.error("Failed to load JDs:", err);
      setJDs([]);
    }
  };

  const handleUpload = async () => {
    if (!title.trim() || !description.trim()) {
      alert("Please fill all required fields");
      return;
    }

    try {
      await uploadJD({
        title: title.trim(),
        description: description.trim(),
        skills: skills
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        keywords: keywords
          .split(",")
          .map((k) => k.trim())
          .filter(Boolean),
        experience_required: experience.trim() || "0",
      });

      setTitle("");
      setDescription("");
      setSkills("");
      setKeywords("");
      setExperience("");

      await loadJDs();
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteJD(id);
      await loadJDs();
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  return (
    <PageLayout>
      {/* Header */}
      <div style={{ marginBottom: "28px" }}>
        <p style={{ margin: 0, color: "#6b7280", fontSize: "13px", fontWeight: "500" }}>
          Job Management
        </p>
        <h1 style={{
          margin: "4px 0 0 0",
          fontSize: "28px",
          fontWeight: "700",
          color: "#1a1a2e",
          fontFamily: "'Georgia', serif",
        }}>
          Job Descriptions
        </h1>
        <p style={{ color: "#6b7280", margin: "8px 0 0 0", fontSize: "14px" }}>
          Create structured job descriptions for more accurate AI-powered ranking.
        </p>
      </div>

      <div style={{ display: "flex", gap: "24px", flexWrap: "wrap" }}>
        {/* Upload Form */}
        <div style={{ flex: "1", minWidth: "360px", maxWidth: "560px" }}>
          <div
            style={{
              background: "white",
              borderRadius: "16px",
              boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
              padding: "28px",
              border: "1px solid #e8e0d8",
            }}
          >
            <h3 style={{ margin: "0 0 20px 0", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" }}>
              Upload New JD
            </h3>

            <input
              type="text"
              placeholder="Job Title *"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={inputStyle}
            />

            <textarea
              placeholder="Job Description *"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              style={{
                ...inputStyle,
                minHeight: "120px",
                resize: "vertical",
              }}
            />

            <input
              type="text"
              placeholder="Skills (comma separated, e.g. Python, FastAPI, PostgreSQL)"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              style={inputStyle}
            />

            <input
              type="text"
              placeholder="Keywords (comma separated, e.g. backend, API, cloud)"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              style={inputStyle}
            />

            <input
              type="text"
              placeholder="Experience Required (e.g. 0-1, 3, 5+)"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              style={{ ...inputStyle, maxWidth: "280px" }}
            />

            <button
              onClick={handleUpload}
              style={{
                padding: "12px 28px",
                borderRadius: "10px",
                border: "none",
                background: "#d4a843",
                color: "white",
                cursor: "pointer",
                fontWeight: "700",
                fontSize: "14px",
                transition: "background 0.2s ease",
              }}
              onMouseEnter={(e) => { e.currentTarget.style.background = "#c49a33"; }}
              onMouseLeave={(e) => { e.currentTarget.style.background = "#d4a843"; }}
            >
              Upload JD
            </button>
          </div>
        </div>

        {/* JD List */}
        <div style={{ flex: "2", minWidth: "360px" }}>
          <div style={{ marginBottom: "16px" }}>
            <h3 style={{ margin: "0 0 6px 0", fontSize: "16px", fontWeight: "700", color: "#1a1a2e" }}>
              All Job Descriptions
            </h3>
            <p style={{ color: "#6b7280", margin: 0, fontSize: "13px" }}>
              Review uploaded roles and jump directly to candidate ranking.
            </p>
          </div>

          {jds.length === 0 ? (
            <div
              style={{
                background: "white",
                borderRadius: "16px",
                boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
                padding: "40px",
                border: "1px solid #e8e0d8",
                color: "#9ca3af",
                textAlign: "center",
              }}
            >
              No Job Descriptions yet. Upload one to get started.
            </div>
          ) : (
            <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
              {jds.map((jd) => {
                const parsed = jd.parsed_data || {};
                const displayTitle = jd.title || parsed.title || "Untitled JD";
                const displayDescription = jd.description || parsed.description || "No description available.";
                const displayExperience = jd.experience_required ?? parsed.experience_required ?? "0";
                const displaySkills = Array.isArray(jd.skills)
                  ? jd.skills
                  : Array.isArray(parsed.skills)
                  ? parsed.skills
                  : [];

                return (
                  <div
                    key={jd.id}
                    style={{
                      background: "white",
                      borderRadius: "16px",
                      padding: "20px",
                      width: "300px",
                      boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
                      border: "1px solid #e8e0d8",
                      transition: "all 0.2s ease",
                    }}
                    onMouseEnter={(e) => { e.currentTarget.style.boxShadow = "0 8px 30px rgba(0,0,0,0.1)"; }}
                    onMouseLeave={(e) => { e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,0.06)"; }}
                  >
                    <h4 style={{ margin: "0 0 10px 0", fontSize: "15px", fontWeight: "700", color: "#1a1a2e", lineHeight: "1.3" }}>
                      {displayTitle}
                    </h4>

                    <p style={{
                      color: "#6b7280",
                      fontSize: "13px",
                      lineHeight: "1.5",
                      minHeight: "60px",
                      margin: "0 0 12px 0",
                    }}>
                      {displayDescription.length > 120
                        ? displayDescription.slice(0, 120) + "..."
                        : displayDescription}
                    </p>

                    <p style={{ fontSize: "12px", color: "#6b7280", margin: "0 0 10px 0" }}>
                      Experience Required: <strong>{displayExperience}</strong>
                    </p>

                    <div style={{ marginBottom: "14px", minHeight: "28px" }}>
                      {displaySkills.length > 0 ? (
                        displaySkills.slice(0, 3).map((skill, index) => (
                          <span key={index} style={{
                            display: "inline-block",
                            background: "#f0fdf4",
                            color: "#166534",
                            padding: "3px 8px",
                            borderRadius: "4px",
                            marginRight: "4px",
                            marginBottom: "4px",
                            fontSize: "11px",
                            fontWeight: "600",
                          }}>
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span style={{ fontSize: "12px", color: "#9ca3af" }}>No skills listed</span>
                      )}
                    </div>

                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                      <button
                        onClick={() => navigate(`/ranking?jd=${jd.id}`)}
                        style={{
                          padding: "8px 16px",
                          borderRadius: "8px",
                          border: "none",
                          background: "#d4a843",
                          color: "white",
                          cursor: "pointer",
                          fontWeight: "600",
                          fontSize: "13px",
                        }}
                      >
                        View Ranking
                      </button>

                      <button
                        onClick={() => handleDelete(jd.id)}
                        style={{
                          padding: "8px 16px",
                          borderRadius: "8px",
                          border: "1px solid #fecaca",
                          background: "white",
                          color: "#dc2626",
                          cursor: "pointer",
                          fontWeight: "600",
                          fontSize: "13px",
                        }}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  marginBottom: "12px",
  padding: "12px 14px",
  borderRadius: "10px",
  border: "1px solid #e0d8d0",
  fontSize: "14px",
  boxSizing: "border-box",
  outline: "none",
  background: "#faf8f5",
  transition: "border-color 0.2s ease",
};

export default JDPage;