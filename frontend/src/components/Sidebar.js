import { useNavigate, useLocation } from "react-router-dom";
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Box,
} from "@mui/material";

import AnalyticsIcon from "@mui/icons-material/Analytics";
import PredictionsIcon from "@mui/icons-material/Psychology";

import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import StorageIcon from "@mui/icons-material/Storage"; // Data icon

const drawerWidth = 240;

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { text: "Live Prediction", icon: <PredictionsIcon />, path: "/prediction" },
    { text: "Model Confidence", icon: <AnalyticsIcon />, path: "/ModelConfidence" },
    { text: "Data Model", icon: <StorageIcon />, path: "/data" }, // renamed + icon changed
  ];

  const getActiveItem = () => {
    const currentPath = location.pathname;
    const activeItem = menuItems.find((item) => item.path === currentPath);
    return activeItem ? activeItem.text : "Live Prediction";
  };

  const handleItemClick = (item) => {
    navigate(item.path);
  };

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          backgroundColor: "#fff",
          borderRight: "1px solid #e0e0e0",
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <Toolbar>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <LocalHospitalIcon sx={{ color: "#5A67D8", fontSize: 28 }} />
          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
              color: "#2d3748",
              letterSpacing: "-0.5px",
            }}
          >
            Cancer Care
          </Typography>
        </Box>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => handleItemClick(item)}
            sx={{
              backgroundColor:
                getActiveItem() === item.text ? "#f0f4ff" : "transparent",
              borderRight:
                getActiveItem() === item.text ? "3px solid #5A67D8" : "none",
              "&:hover": {
                backgroundColor: "#f8faff",
              },
              transition: "all 0.2s ease-in-out",
            }}
          >
            <ListItemIcon
              sx={{
                color: getActiveItem() === item.text ? "#5A67D8" : "#718096",
                transition: "color 0.2s ease-in-out",
              }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText
              primary={item.text}
              sx={{
                "& .MuiListItemText-primary": {
                  color: getActiveItem() === item.text ? "#5A67D8" : "#4a5568",
                  fontWeight: getActiveItem() === item.text ? 600 : 400,
                  transition: "all 0.2s ease-in-out",
                },
              }}
            />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}
