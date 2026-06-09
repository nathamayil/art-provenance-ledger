import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

const API = import.meta.env.VITE_API_BASE_URL;

export default function ImageUploader({ onResult }) {
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const { data } = await axios.post(`${API}/api/analyze`, formData);
      onResult(data);
    } catch (err) {
      setError("Analysis failed. Make sure the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [onResult]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    maxFiles: 1
  });

  return (
    <div>
      <div {...getRootProps()} className={`dropzone ${isDragActive ? "active" : ""}`}>
        <input {...getInputProps()} />
        {preview
          ? <img src={preview} alt="Uploaded preview" className="preview" />
          : <p>Drop an AI-generated image here, or click to select</p>
        }
      </div>
      {loading && <p className="loading">Analyzing style fingerprint...</p>}
      {error   && <p className="loading" style={{ color: "#e05" }}>{error}</p>}
    </div>
  );
}