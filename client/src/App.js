import React, { useEffect, useCallback, useState } from "react";
import Box from "@mui/material/Box";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { useRecoilValue, useSetRecoilState } from "recoil";
import isEmpty from "lodash/isEmpty";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { userState } from "./recoil/atoms";
import AppHeader from "./AppHeader";
import FollowedRespositories from "./FollowedRepositories";
import ImportRepositories from "./ImportRepositories";
import SearchGithub from "./SearchGithub";
import Home from "./Home";
import LoginModal from "./LoginModal";
import { getUserLogin } from "./repository";

const theme = createTheme({
  typography: {
    fontFamily: "Roboto",
  },
});

const App = () => {
  const setUser = useSetRecoilState(userState);
  const currentUser = useRecoilValue(userState);
  const [isLoadingUser, setIsLoadingUser] = useState(true);

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

  return (
    <ThemeProvider theme={theme}>
      <Box>
        <Router>
          <AppHeader />
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
          </Routes>
        </Router>
      </Box>
    </ThemeProvider>
  );
};

export default App;
