import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import UploadDropzone from "../components/upload/UploadDropzone";
import { uploadResume } from "../services/resumeUploadService";

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a resume file first.");
      return;
    }

    try {
      setUploading(true);
      setMessage("");

      const result = await uploadResume(selectedFile);
      console.log("Upload response:", result);

      setMessage("Resume uploaded successfully.");
      setSelectedFile(null);
    } catch (error) {
      console.error("Upload failed:", error);
      setMessage("Failed to upload resume.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <PageLayout>
      <div style={{ marginBottom: "24px" }}>
        <h1 style={{ marginBottom: "8px" }}>Upload Resume</h1>
        <p style={{ color: "#64748b", margin: 0 }}>
          Upload candidate resumes for parsing and ranking.
        </p>
      </div>

      <div
        style={{
          background: "white",
          borderRadius: "14px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          padding: "24px",
        }}
      >
        <UploadDropzone
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
        />

        {selectedFile && (
          <div
            style={{
              marginTop: "18px",
              background: "#f8fafc",
              borderRadius: "10px",
              padding: "14px",
            }}
          >
            <p style={{ margin: 0, fontWeight: "600" }}>
              Selected File: {selectedFile.name}
            </p>
            <p style={{ margin: "6px 0 0 0", color: "#64748b", fontSize: "14px" }}>
              Size: {(selectedFile.size / 1024).toFixed(1)} KB
            </p>
          </div>
        )}

        <div style={{ marginTop: "18px", display: "flex", gap: "12px" }}>
          <button
            onClick={handleUpload}
            disabled={uploading}
            style={{
              padding: "10px 18px",
              borderRadius: "10px",
              border: "none",
              background: uploading ? "#94a3b8" : "#2563eb",
              color: "white",
              cursor: uploading ? "not-allowed" : "pointer",
              fontWeight: "600",
            }}
          >
            {uploading ? "Uploading..." : "Upload Resume"}
          </button>

          {selectedFile && (
            <button
              onClick={() => {
                setSelectedFile(null);
                setMessage("");
              }}
              style={{
                padding: "10px 18px",
                borderRadius: "10px",
                border: "none",
                background: "#e2e8f0",
                color: "#0f172a",
                cursor: "pointer",
                fontWeight: "600",
              }}
            >
              Clear
            </button>
          )}
        </div>

        {message && (
          <div
            style={{
              marginTop: "16px",
              padding: "12px 14px",
              borderRadius: "10px",
              background:
                message.includes("successfully") ? "#dcfce7" : "#fee2e2",
              color:
                message.includes("successfully") ? "#166534" : "#991b1b",
              fontWeight: "600",
            }}
          >
            {message}
          </div>
        )}
      </div>
    </PageLayout>
  );
}

export default UploadPage;