function UploadDropzone({ selectedFile, setSelectedFile }) {
  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  return (
    <div
      style={{
        border: "2px dashed #94a3b8",
        borderRadius: "14px",
        padding: "48px 20px",
        textAlign: "center",
        background: "#f8fafc",
      }}
    >
      <h3 style={{ marginBottom: "10px" }}>
        {selectedFile ? "File Selected" : "Drag and drop or choose a resume"}
      </h3>

      <p style={{ color: "#64748b", marginBottom: "16px" }}>
        Supported formats: PDF, DOCX, JPG, PNG
      </p>

      <input
        type="file"
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
        onChange={handleFileChange}
      />
    </div>
  );
}

export default UploadDropzone;