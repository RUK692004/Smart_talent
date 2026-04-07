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
        experience_required: Number(experience) || 0,
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
      <div style={{ marginBottom: "24px" }}>
        <h1 style={{ marginBottom: "8px" }}>Job Descriptions</h1>
        <p style={{ color: "#64748b", margin: 0 }}>
          Create structured job descriptions for more accurate ranking.
        </p>
      </div>

      <div
        style={{
          background: "white",
          borderRadius: "14px",
          boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
          padding: "24px",
          maxWidth: "760px",
        }}
      >
        <h3 style={{ marginTop: 0, marginBottom: "18px" }}>Upload JD</h3>

        <input
          type="text"
          placeholder="Job Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={inputStyle}
        />

        <textarea
          placeholder="Job Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{
            ...inputStyle,
            minHeight: "140px",
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
          type="number"
          placeholder="Experience Required (years)"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          style={{ ...inputStyle, maxWidth: "260px" }}
        />

        <button onClick={handleUpload} style={primaryButton}>
          Upload JD
        </button>
      </div>

      <div style={{ marginTop: "32px" }}>
        <div style={{ marginBottom: "12px" }}>
          <h3 style={{ marginBottom: "6px" }}>All Job Descriptions</h3>
          <p style={{ color: "#64748b", margin: 0 }}>
            Review uploaded roles and jump directly to candidate ranking.
          </p>
        </div>

        {jds.length === 0 ? (
          <div
            style={{
              background: "white",
              borderRadius: "12px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              padding: "18px",
              color: "#64748b",
            }}
          >
            No Job Descriptions yet. Upload one to get started.
          </div>
        ) : (
          <div
            style={{
              display: "flex",
              gap: "16px",
              flexWrap: "wrap",
            }}
          >
            {jds.map((jd) => {
              const parsed = jd.parsed_data || {};
              const displayTitle = jd.title || parsed.title || "Untitled JD";
              const displayDescription =
                jd.description || parsed.description || "No description available.";
              const displayExperience =
                jd.experience_required ?? parsed.experience_required ?? 0;
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
                    borderRadius: "12px",
                    padding: "18px",
                    width: "310px",
                    boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
                    transition: "0.2s ease",
                  }}
                >
                  <h4 style={{ marginTop: 0, marginBottom: "10px", lineHeight: "1.3" }}>
                    {displayTitle}
                  </h4>

                  <p
                    style={{
                      color: "#475569",
                      fontSize: "14px",
                      lineHeight: "1.5",
                      minHeight: "64px",
                    }}
                  >
                    {displayDescription.length > 120
                      ? displayDescription.slice(0, 120) + "..."
                      : displayDescription}
                  </p>

                  <p style={{ fontSize: "13px", color: "#64748b", marginBottom: "10px" }}>
                    Experience Required: {displayExperience} years
                  </p>

                  <div style={{ marginBottom: "14px", minHeight: "36px" }}>
                    {displaySkills.length > 0 ? (
                      displaySkills.slice(0, 3).map((skill, index) => (
                        <span key={index} style={tagStyle}>
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span style={{ fontSize: "12px", color: "#94a3b8" }}>
                        No skills listed
                      </span>
                    )}
                  </div>

                  <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                    <button
                      onClick={() => navigate(`/ranking?jd=${jd.id}`)}
                      style={primarySmallButton}
                    >
                      View Ranking
                    </button>

                    <button
                      onClick={() => handleDelete(jd.id)}
                      style={dangerSmallButton}
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
    </PageLayout>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  marginBottom: "12px",
  padding: "12px 14px",
  borderRadius: "10px",
  border: "1px solid #cbd5e1",
  fontSize: "14px",
  boxSizing: "border-box",
};

const primaryButton = {
  padding: "10px 18px",
  borderRadius: "10px",
  border: "none",
  background: "#2563eb",
  color: "white",
  cursor: "pointer",
  fontWeight: "600",
};

const primarySmallButton = {
  padding: "8px 12px",
  borderRadius: "8px",
  border: "none",
  background: "#2563eb",
  color: "white",
  cursor: "pointer",
  fontWeight: "600",
};

const dangerSmallButton = {
  padding: "8px 12px",
  borderRadius: "8px",
  border: "none",
  background: "#dc2626",
  color: "white",
  cursor: "pointer",
  fontWeight: "600",
};

const tagStyle = {
  display: "inline-block",
  background: "#eef2ff",
  color: "#3730a3",
  padding: "4px 8px",
  borderRadius: "6px",
  marginRight: "6px",
  marginBottom: "6px",
  fontSize: "12px",
};

export default JDPage;