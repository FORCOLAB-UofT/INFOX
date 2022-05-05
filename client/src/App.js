import React, { useEffect, useCallback, useState } from "react";
import Box from "@mui/material/Box";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { Grid, Typography, Drawer, IconButton, Divider } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useRecoilValue, useSetRecoilState } from "recoil";
import isEmpty from "lodash/isEmpty";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { userState } from "./recoil/atoms";
import AppHeader from "./AppHeader";
import FollowedRespositories from "./FollowedRepositories";
import ImportRepositories from "./ImportRepositories";
import SearchGithub from "./SearchGithub";
import AboutUs from "./AboutUs";
import Home from "./Home";
import LoginModal from "./LoginModal";
import ForkCluster from "./ForkCluster";
import { getUserLogin } from "./repository";
import Forklist from "./Forklist";
import DrawerCard from "./DrawerCard";

const theme = createTheme({
  typography: {
    fontFamily: "Zilla Slab",
  },
});

const App = () => {
  const setUser = useSetRecoilState(userState);
  const currentUser = useRecoilValue(userState);
  const [isLoadingUser, setIsLoadingUser] = useState(true);
  const [openDrawer, setOpenDrawer] = useState(false);

  const fetchUser = useCallback(async () => {
    setIsLoadingUser(true);
    console.log("fetchUser");
    const access_token = localStorage.getItem("access_token");
    const username = localStorage.getItem("username");
    console.log(access_token, username);

    if (!access_token) {
      setUser(null);
    } else {
      const user = await getUserLogin();
      console.log("test", user);

      if (user?.data) {
        localStorage.setItem("username", user.data.username);
        setUser(user);
      } else {
        setUser(null);
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");
      }
    }
    setIsLoadingUser(false);
  }, [setUser]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const handleCloseDrawer = () => {
    setOpenDrawer(false);
  };

  const handleOpenDrawer = () => {
    setOpenDrawer(true);
  };

  return (
    <ThemeProvider theme={theme}>
      <Box>
        <Router>
          <AppHeader onOpenDrawer={handleOpenDrawer} />
          <Drawer anchor="left" open={openDrawer} onClose={handleCloseDrawer}>
            <Grid container padding={2}>
              <Grid item xs={11}>
                <Typography variant="h4">Fork Analysis</Typography>
              </Grid>
              <Grid item xs={1}>
                <IconButton onClick={handleCloseDrawer}>
                  <CloseIcon />
                </IconButton>
              </Grid>
            </Grid>
            <Divider />
            <DrawerCard
              title="Fork Clustering"
              description="Cluster forks of a respository according to keywords in their commit messages."
              link="/cluster"
              onCloseDrawer={handleCloseDrawer}
            />
            <DrawerCard
              title="Fork Comparison"
              description="Compare forks against each other in terms of code changes. Includes: files changed, number of commits, lines changes, etc."
              onCloseDrawer={handleCloseDrawer}
              link="/compare"
            />
            <DrawerCard
              title="Fork Conflict Detection"
              description="Check for possible conflicts for a fork"
              onCloseDrawer={handleCloseDrawer}
              link="/conflict"
            />
          </Drawer>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginModal />} />
            <Route
              path="/private"
              element={
                !isEmpty(currentUser) ? (
                  <div>private</div>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/followed"
              element={
                !isEmpty(currentUser) ? (
                  <FollowedRespositories />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/import"
              element={
                !isEmpty(currentUser) ? (
                  <ImportRepositories />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/search"
              element={
                !isEmpty(currentUser) ? (
                  <SearchGithub />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route path="/aboutus" element={<AboutUs />} />
            <Route
              path="/cluster"
              element={
                !isEmpty(currentUser) ? (
                  <ForkCluster />
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/forks/:repo1/:repo2"
              element={
                !isEmpty(currentUser) ? (
                  <Forklist />
                ) : (
                  <Navigate to="/followed" />
                )
              }
            />
          </Routes>
        </Router>
      </Box>
    </ThemeProvider>
  );
};

export default App;
