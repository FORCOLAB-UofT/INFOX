import Box from "@mui/material/Box";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { useRecoilValue } from "recoil";
import isEmpty from "lodash/isEmpty";
import { userState } from "./recoil/atoms";
import AppHeader from "./AppHeader";
import FollowedRespositories from "./FollowedRepositories";
import ImportRepositories from "./ImportRepositories";
import SearchGithub from "./SearchGithub";

const App = () => {
  const currentUser = useRecoilValue(userState);

  return (
    <Box>
      <Router>
        <AppHeader />
        <Routes>
          <Route path="/" element={<div>home</div>} />
          <Route path="/login" element={<div>please login </div>} />
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
  );
};

export default App;
