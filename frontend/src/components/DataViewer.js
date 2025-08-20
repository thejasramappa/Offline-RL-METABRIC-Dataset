import React, { useEffect, useState, useCallback } from "react";
import {
  Box,
  Paper,
  Tabs,
  Tab,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  CircularProgress,
  Button,
  Stack,
} from "@mui/material";
import axios from "axios";

const COLUMNS = [
  "ID",
  "Patient Name",
  "Age",
  "Tumor Size",
  "Grade",
  "ER",
  "PR",
  "HER2",
  "Predicted Action",
];

export default function DataViewer() {
  const [tab, setTab] = useState("all");
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchData = useCallback(async (t) => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.get(`http://localhost:5000/logs/${t}`);
      setRows(res.data?.rows ?? []);
    } catch (e) {
      setError("Failed to load data");
      setRows([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(tab);
  }, [tab, fetchData]);

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 2 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Tabs
            value={tab}
            onChange={(_, v) => setTab(v)}
            aria-label="log type tabs"
            sx={{ mb: 2 }}
          >
            <Tab value="all" label="All Treatments - M1" />
            <Tab value="chemo" label="Chemotherapy - M2" />
            <Tab value="radio" label="Radiotherapy - M3" />
            <Tab value="hormone" label="Hormonetherapy - M4" />
          </Tabs>
          <Button variant="outlined" onClick={() => fetchData(tab)}>
            Refresh
          </Button>
        </Stack>

        {loading ? (
          <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Typography color="error">{error}</Typography>
        ) : rows.length === 0 ? (
          <Typography>No records found.</Typography>
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                {COLUMNS.map((col) => (
                  <TableCell key={col} sx={{ fontWeight: 600 }}>
                    {col}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((r, idx) => (
                <TableRow key={idx}>
                  {COLUMNS.map((col) => (
                    <TableCell key={col}>{r[col]}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Paper>
    </Box>
  );
}