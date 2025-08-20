import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  CircularProgress,
  MenuItem,
} from "@mui/material";
import axios from "axios";

export default function PredictionForm() {
  const [formData, setFormData] = useState({
    patient_name: "", // added
    age: "",
    tumor_size: "",
    grade: "",
    er: "",
    pr: "",
    her2: "",
  });

  // New: prediction mode dropdown
  const [predictTarget, setPredictTarget] = useState("auto");

  const ENDPOINTS = {
    auto: "http://localhost:5000/predict_all",
    chemotherapy: "http://localhost:5000/predict_chemo",
    radiotherapy: "http://localhost:5000/predict_radio",
    hormone: "http://localhost:5000/predict_hormone",
  };

  const [prediction, setPrediction] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Generate a 5-character alphanumeric ID
  const genId = (len = 5) => {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    if (window.crypto?.getRandomValues) {
      const buf = new Uint32Array(len);
      window.crypto.getRandomValues(buf);
      return Array.from(buf, (n) => alphabet[n % alphabet.length]).join("");
    }
    let out = "";
    for (let i = 0; i < len; i++) {
      out += alphabet[Math.floor(Math.random() * alphabet.length)];
    }
    return out;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setShowResult(false);
    setLoading(true);

    const endpoint = ENDPOINTS[predictTarget];

    // Simulate loading animation for 5 seconds
    setTimeout(async () => {
      try {
        // Use 5-char alphanumeric ID
        const id = genId();

        const payload = {
          id,
          patient_name: formData.patient_name,
          age: Number(formData.age),
          tumor_size: Number(formData.tumor_size),
          grade: Number(formData.grade),
          er: Number(formData.er),
          pr: Number(formData.pr),
          her2: Number(formData.her2),
        };

        const response = await axios.post(endpoint, payload);
        setPrediction(response.data);
      } catch (error) {
        setPrediction({ error: "Failed to get prediction" });
      } finally {
        setLoading(false);
        setShowResult(true);
      }
    }, 5000);
  };

  return (
    <Box sx={{ display: "flex", gap: 4 }}>
      <Paper sx={{ p: 3, maxWidth: 500, flex: 1 }}>
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{ display: "flex", flexDirection: "column", gap: 2 }}
        >
          <h1>Treatment Prediction</h1>

          {/* New: Prediction mode dropdown (left-aligned, compact) */}
          <TextField
            select
            label="Mode"
            value={predictTarget}
            onChange={(e) => setPredictTarget(e.target.value)}
            size="small"
            sx={{ maxWidth: 240 }}
          >
            <MenuItem value="auto">Auto (All)</MenuItem>
            <MenuItem value="chemotherapy">Chemotherapy</MenuItem>
            <MenuItem value="radiotherapy">Radiotherapy</MenuItem>
            <MenuItem value="hormone">Hormone Therapy</MenuItem>
          </TextField>

          <Typography variant="h6" gutterBottom>
            Enter New Patient Details
          </Typography>

          {/* New: Patient Name */}
          <TextField
            label="Patient Name"
            name="patient_name"
            value={formData.patient_name}
            onChange={handleChange}
            required
          />

          <TextField
            label="Age at Diagnosis"
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />

          <TextField
            label="Tumor Size (mm)"
            type="number"
            name="tumor_size"
            value={formData.tumor_size}
            onChange={handleChange}
            required
          />

          {/* Changed to dropdown: Histologic Grade */}
          <TextField
            select
            label="Histologic Grade"
            name="grade"
            value={formData.grade}
            onChange={handleChange}
            required
          >
            <MenuItem value="1">1</MenuItem>
            <MenuItem value="2">2</MenuItem>
            <MenuItem value="3">3</MenuItem>
          </TextField>

          {/* Changed to dropdown: ER Status */}
          <TextField
            select
            label="ER Status"
            name="er"
            value={formData.er}
            onChange={handleChange}
            required
          >
            <MenuItem value="1">Positive</MenuItem>
            <MenuItem value="0">Negative</MenuItem>
          </TextField>

          {/* Changed to dropdown: PR Status */}
          <TextField
            select
            label="PR Status"
            name="pr"
            value={formData.pr}
            onChange={handleChange}
            required
          >
            <MenuItem value="1">Positive</MenuItem>
            <MenuItem value="0">Negative</MenuItem>
          </TextField>

          {/* Changed to dropdown: HER2 Status */}
          <TextField
            select
            label="HER2 Status"
            name="her2"
            value={formData.her2}
            onChange={handleChange}
            required
          >
            <MenuItem value="1">Positive</MenuItem>
            <MenuItem value="0">Negative</MenuItem>
          </TextField>

          <Button
            type="submit"
            variant="contained"
            sx={{ backgroundColor: "#5A67D8" }}
            disabled={loading}
          >
            Predict
          </Button>
        </Box>
      </Paper>

      {/* Prediction Result Box */}
      <Box
        sx={{
          flex: 1,
          display: showResult || loading ? "block" : "none",
        }}
      >
        <Paper
          sx={{
            p: 3,
            minHeight: 200,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {loading ? (
            <>
              <CircularProgress sx={{ mb: 2 }} />
              <Typography variant="subtitle1">Predicting...</Typography>
            </>
          ) : (
            showResult && (
              <>
                <Typography variant="h6" gutterBottom>
                  Prediction Result
                </Typography>
                <Typography variant="body1" sx={{ fontWeight: "bold" }}>
                  {prediction?.result || prediction?.error}
                </Typography>
              </>
            )
          )}
        </Paper>
      </Box>
    </Box>
  );
}
