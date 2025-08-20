import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Box, CssBaseline } from "@mui/material";
import Sidebar from "./components/Sidebar";
import PredictionForm from "./components/PredictionForm";
import ModelConfidence from "./components/ModelConfidence";
import DataViewer from "./components/DataViewer";

function App() {
  return (
    <Router>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Sidebar />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            backgroundColor: "#f7f8fa",
            minHeight: "100vh",
          }}
        >
          <Routes>
            <Route path="/" element={<PredictionForm />} />
            <Route path="/prediction" element={<PredictionForm />} />
            <Route path="/ModelConfidence" element={<ModelConfidence />} />
            <Route path="/data" element={<div>{<DataViewer />}</div>} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
