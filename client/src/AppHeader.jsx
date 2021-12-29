import React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import SignalCellularAltIcon from "@mui/icons-material/SignalCellularAlt";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import SearchIcon from "@mui/icons-material/Search";
import { useRecoilValue } from "recoil";
import ButtonLink from "./common/ButtonLink";
import { PRIMARY } from "./common/constants";
import Login from "./Login";
import Logout from "./Logout";
import { userState } from "./recoil/atoms";

const AppHeader = () => {
  const currentUser = useRecoilValue(userState);
  console.log("appheader current", currentUser);
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" style={{ background: PRIMARY }}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            INFOX - Forks Insight
          </Typography>
          <ButtonLink
            to="/followed"
            linkText="Followed Repositories"
            color="inherit"
            startIcon={<SignalCellularAltIcon />}
          />
          <ButtonLink
            to="/import"
            linkText="Import Repositories"
            color="inherit"
            startIcon={<CloudUploadIcon />}
          />
          <ButtonLink
            to="/search"
            linkText="Search Github"
            color="inherit"
            startIcon={<SearchIcon />}
          />
          {!currentUser ? <Login /> : <Logout />}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default AppHeader;
