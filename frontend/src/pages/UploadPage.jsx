import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import { uploadResume } from "../services/resumeUploadService";
import { uploadJD } from "../services/jdService";

function UploadPage() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdTitle, setJdTitle] = useState("");
  const [jdDescription, setJdDescription] = useState("");
  const [jdSkills, setJdSkills] = useState("");
  const [jdKeywords, setJdKeywords] = useState("");
  const [jdExperience, setJdExperience] = useState("");

  const [resumeUploading, setResumeUploading] = useState(false);
  const [jdUploading, setJdUploading] = useState(false);
  const [resumeMessage, setResumeMessage] = useState("");
  const [jdMessage, setJdMessage] = useState("");

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      alert("Please select a resume file first.");
      return;
    }

    try {
      setResumeUploading(true);
      setResumeMessage("");

      const result = await uploadResume(resumeFile);
      console.log("Upload response:", result);

      setResumeMessage("Resume uploaded successfully.");
      setResumeFile(null);
    } catch (error) {
      console.error("Upload failed:", error);
      setResumeMessage("Failed to upload resume.");
    } finally {
      setResumeUploading(false);
    }
  };

  const handleJDUpload = async () => {
    if (!jdTitle.trim() || !jdDescription.trim()) {
      alert("Please fill in the required JD fields.");
      return;
    }

    try {
      setJdUploading(true);
      setJdMessage("");

      await uploadJD({
        title: jdTitle.trim(),
        description: jdDescription.trim(),
        skills: jdSkills.split(",").map((s) => s.trim()).filter(Boolean),
        keywords: jdKeywords.split(",").map((k) => k.trim()).filter(Boolean),
        experience_required: jdExperience.trim() || "0",
      });

      setJdMessage("JD uploaded successfully.");
      setJdTitle("");
      setJdDescription("");
      setJdSkills("");
      setJdKeywords("");
      setJdExperience("");
    } catch (error) {
      console.error("JD upload failed:", error);
      setJdMessage("Failed to upload JD.");
    } finally {
      setJdUploading(false);
    }
  };

  return (
    <PageLayout>
      {/* Header */}
      <div style={{ marginBottom: "28px" }}>
        <p style={{ margin: 0, color: "#6b7280", fontSize: "13px", fontWeight: "500" }}>
          Data Ingestion
        </p>
        <h1 style={{
          margin: "4px 0 0 0",
          fontSize: "28px",
          fontWeight: "700",
          color: "#1a1a2e",
          fontFamily: "'Georgia', serif",
        }}>
          Upload Resume & JD
        </h1>
        <p style={{ color: "#6b7280", margin: "8px 0 0 0", fontSize: "14px" }}>
          Upload candidate resumes and job descriptions for parsing and AI-powered ranking.
        </p>
      </div>

      {/* Two Column Layout */}
      <div style={{ display: "flex", gap: "24px", flexWrap: "wrap" }}>
        {/* Left - Resume Upload */}
        <div style={{ flex: "1", minWidth: "360px", maxWidth: "560px" }}>
          <div
            style={{
              background: "white",
              borderRadius: "16px",
              boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
              padding: "32px",
              border: "1px solid #e8e0d8",
            }}
          >
            <h2 style={{
              margin: "0 0 24px 0",
              fontSize: "18px",
              fontWeight: "700",
              color: "#1a1a2e",
              fontFamily: "'Georgia', serif",
            }}>
              Upload Resume
            </h2>

            {/* Drag & Drop Zone */}
            <div
              style={{
                border: "2px dashed #cbd5e1",
                borderRadius: "12px",
                padding: "40px 20px",
                textAlign: "center",
                background: "#faf8f5",
                marginBottom: "20px",
                transition: "all 0.2s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = "#d4a843";
                e.currentTarget.style.background = "#fffdf8";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = "#cbd5e1";
                e.currentTarget.style.background = "#faf8f5";
              }}
            >
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: "12px" }}>
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="12" y1="18" x2="12" y2="12" />
                <line x1="9" y1="15" x2="15" y2="15" />
              </svg>
              <p style={{ margin: "0 0 8px 0", fontWeight: "600", color: "#1a1a2e", fontSize: "15px" }}>
                Drag and drop or choose a resume
              </p>
              <p style={{ margin: 0, color: "#94a3b8", fontSize: "13px" }}>
                Supported formats: PDF, DOCX, JPG, PNG
              </p>

              <input
                type="file"
                accept=".pdf,.docx,.jpg,.jpeg,.png"
                onChange={(e) => setResumeFile(e.target.files[0] || null)}
                style={{ marginTop: "16px" }}
              />
            </div>

            {resumeFile && (
              <div style={{
                marginBottom: "16px",
                padding: "12px",
                background: "#faf8f5",
                borderRadius: "8px",
                border: "1px solid #e8e0d8",
                fontSize: "13px",
                color: "#1a1a2e",
              }}>
                Selected: <strong>{resumeFile.name}</strong> ({(resumeFile.size / 1024).toFixed(1)} KB)
              </div>
            )}

            <button
              onClick={handleResumeUpload}
              disabled={resumeUploading}
              style={{
                width: "100%",
                padding: "12px",
                borderRadius: "10px",
                border: "none",
                background: resumeUploading ? "#9ca3af" : "#d4a843",
                color: "white",
                cursor: resumeUploading ? "not-allowed" : "pointer",
                fontWeight: "700",
                fontSize: "14px",
                transition: "background 0.2s ease",
              }}
            >
              {resumeUploading ? "Uploading..." : "Upload Resume"}
            </button>

            {resumeMessage && (
              <div style={{
                marginTop: "12px",
                padding: "10px 14px",
                borderRadius: "8px",
                background: resumeMessage.includes("successfully") ? "#f0fdf4" : "#fef2f2",
                color: resumeMessage.includes("successfully") ? "#166534" : "#991b1b",
                fontSize: "13px",
                fontWeight: "600",
                border: `1px solid ${resumeMessage.includes("successfully") ? "#bbf7d0" : "#fecaca"}`,
              }}>
                {resumeMessage}
              </div>
            )}
          </div>
        </div>

        {/* Right - JD Upload */}
        <div style={{ flex: "1", minWidth: "360px", maxWidth: "560px" }}>
          <div
            style={{
              background: "white",
              borderRadius: "16px",
              boxShadow: "0 4px 20px rgba(0,0,0,0.06)",
              padding: "32px",
              border: "1px solid #e8e0d8",
            }}
          >
            <h2 style={{
              margin: "0 0 24px 0",
              fontSize: "18px",
              fontWeight: "700",
              color: "#1a1a2e",
              fontFamily: "'Georgia', serif",
            }}>
              Upload Job Description
            </h2>

            <input
              type="text"
              placeholder="Job Title *"
              value={jdTitle}
              onChange={(e) => setJdTitle(e.target.value)}
              style={{
                width: "100%",
                marginBottom: "12px",
                padding: "12px 14px",
                borderRadius: "10px",
                border: "1px solid #e0d8d0",
                fontSize: "14px",
                background: "#faf8f5",
                outline: "none",
                boxSizing: "border-box",
              }}
            />

            <textarea
              placeholder="Job Description *"
              value={jdDescription}
              onChange={(e) => setJdDescription(e.target.value)}
              style={{
                width: "100%",
                marginBottom: "12px",
                padding: "12px 14px",
                borderRadius: "10px",
                border: "1px solid #e0d8d0",
                fontSize: "14px",
                background: "#faf8f5",
                outline: "none",
                boxSizing: "border-box",
                minHeight: "100px",
                resize: "vertical",
              }}
            />

            <input
              type="text"
              placeholder="Skills (comma separated)"
              value={jdSkills}
              onChange={(e) => setJdSkills(e.target.value)}
              style={{
                width: "100%",
                marginBottom: "12px",
                padding: "12px 14px",
                borderRadius: "10px",
                border: "1px solid #e0d8d0",
                fontSize: "14px",
                background: "#faf8f5",
                outline: "none",
                boxSizing: "border-box",
              }}
            />

            <input
              type="text"
              placeholder="Keywords (comma separated)"
              value={jdKeywords}
              onChange={(e) => setJdKeywords(e.target.value)}
              style={{
                width: "100%",
                marginBottom: "12px",
                padding: "12px 14px",
                borderRadius: "10px",
                border: "1px solid #e0d8d0",
                fontSize: "14px",
                background: "#faf8f5",
                outline: "none",
                boxSizing: "border-box",
              }}
            />

            <input
              type="text"
              placeholder="Experience Required (e.g. 0-1, 3, 5+)"
              value={jdExperience}
              onChange={(e) => setJdExperience(e.target.value)}
              style={{
                width: "100%",
                marginBottom: "16px",
                padding: "12px 14px",
                borderRadius: "10px",
                border: "1px solid #e0d8d0",
                fontSize: "14px",
                background: "#faf8f5",
                outline: "none",
                boxSizing: "border-box",
              }}
            />

            <button
              onClick={handleJDUpload}
              disabled={jdUploading}
              style={{
                width: "100%",
                padding: "12px",
                borderRadius: "10px",
                border: "none",
                background: jdUploading ? "#9ca3af" : "#7c3aed",
                color: "white",
                cursor: jdUploading ? "not-allowed" : "pointer",
                fontWeight: "700",
                fontSize: "14px",
                transition: "background 0.2s ease",
              }}
            >
              {jdUploading ? "Uploading..." : "Upload JD"}
            </button>

            {jdMessage && (
              <div style={{
                marginTop: "12px",
                padding: "10px 14px",
                borderRadius: "8px",
                background: jdMessage.includes("successfully") ? "#f0fdf4" : "#fef2f2",
                color: jdMessage.includes("successfully") ? "#166534" : "#991b1b",
                fontSize: "13px",
                fontWeight: "600",
                border: `1px solid ${jdMessage.includes("successfully") ? "#bbf7d0" : "#fecaca"}`,
              }}>
                {jdMessage}
              </div>
            )}
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default UploadPage;