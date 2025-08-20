import React, { useState } from "react";
import {
  Box,
  Button,
  Typography,
  Paper,
  CircularProgress,
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import axios from "axios";

export default function ModelConfidence() {
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [treatment, setTreatment] = useState("all"); // Added

  const getConfidenceColor = (value) => {
    if (value >= 75) return "#4caf50"; // Green
    if (value >= 50) return "#ff9800"; // Orange/Yellow
    if (value >= 40) return "#ff5722"; // Orange
    return "#f44336"; // Red
  };

  const getConfidenceLabel = (value) => {
    if (value >= 75) return "Excellent";
    if (value >= 50) return "Good";
    if (value >= 40) return "Fair";
    return "Poor";
  };

  const handleMeasureConfidence = async () => {
    setLoading(true);
    setShowResult(false);

    try {
      // Map selection to backend endpoint
      const endpoints = {
        all: "http://localhost:5000/measure_model_confidence_all",
        radio: "http://localhost:5000/measure_model_confidence_radio",
        chemo: "http://localhost:5000/measure_model_confidence_chemo",
        hormone: "http://localhost:5000/measure_model_confidence_hormone",
      };
      const url = endpoints[treatment] || endpoints.all;

      // 3s delay for animation while preserving try/catch
      await new Promise((r) => setTimeout(r, 3000));

      const response = await axios.get(url);
      const confidenceStr = response.data.confidence;
      const confidenceValue = parseFloat(
        typeof confidenceStr === "string" ? confidenceStr.replace("%", "") : confidenceStr
      );
      setConfidence(confidenceValue);
      setLoading(false);
      setShowResult(true);
    } catch (error) {
      console.error("Error measuring confidence:", error);
      setConfidence(null);
      setLoading(false);
      setShowResult(true);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: "auto" }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
        Model Performance Analytics
      </Typography>

      <Paper sx={{ p: 4, textAlign: "center" }}>
        <Typography variant="h6" gutterBottom align="left" sx={{ mb: 3 }}>
          Measure Model Accuracy
        </Typography>

        {/* Dropdown for treatment selection */}
        <Box sx={{ textAlign: "left", mb: 2 }}>
          <FormControl
            sx={{ width: { xs: "100%", sm: 260 } }}  // narrow and responsive
            disabled={loading}
          >
            <InputLabel id="treatment-label">Select Treatment</InputLabel>
            <Select
              labelId="treatment-label"
              value={treatment}
              label="Select Treatment"
              onChange={(e) => setTreatment(e.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="radio">Radio Therapy</MenuItem>
              <MenuItem value="chemo">Chemo Therapy</MenuItem>
              <MenuItem value="hormone">Hormone Therapy</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Button
          variant="contained"
          onClick={handleMeasureConfidence}
          disabled={loading}
          sx={{
            backgroundColor: "#5A67D8",
            px: 4,
            py: 1.5,
            fontSize: "1.1rem",
            mb: 4,
          }}
        >
          {loading ? "Measuring..." : "Predict Model Accuracy"}
        </Button>

        {loading && (
          <Box sx={{ mb: 4 }}>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography variant="subtitle1">Analyzing model performance...</Typography>
          </Box>
        )}

        {showResult && confidence !== null && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Model Accuracy
            </Typography>

            {/* Accuracy Meter */}
            <Box sx={{ position: "relative", mb: 3 }}>
              <LinearProgress
                variant="determinate"
                value={confidence}
                sx={{
                  height: 20,
                  borderRadius: 10,
                  backgroundColor: "#e0e0e0",
                  "& .MuiLinearProgress-bar": {
                    backgroundColor: getConfidenceColor(confidence),
                    borderRadius: 10,
                  },
                }}
              />
              <Typography
                variant="body2"
                sx={{
                  position: "absolute",
                  top: "50%",
                  left: "50%",
                  transform: "translate(-50%, -50%)",
                  fontWeight: "bold",
                  color: "white",
                  textShadow: "1px 1px 2px rgba(0,0,0,0.7)",
                }}
              >
                {confidence.toFixed(1)}%
              </Typography>
            </Box>

            <Typography
              variant="h6"
              sx={{
                color: getConfidenceColor(confidence),
                fontWeight: "bold",
                mb: 2,
              }}
            >
              {getConfidenceLabel(confidence)} Performance
            </Typography>

            <Typography variant="body1" color="text.secondary">
              The model shows {confidence.toFixed(1)}% accuracy on the validation dataset.
            </Typography>
          </Box>
        )}

        {showResult && confidence === null && (
          <Typography variant="body1" color="error" sx={{ mt: 4 }}>
            Failed to measure model confidence. Please try again.
          </Typography>
        )}
      </Paper>
    </Box>
  );
}