import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useSetRecoilState, RecoilRoot } from "recoil";
import { userState } from "../recoil/atoms";
import AppHeader from "../AppHeader";

const AppHeaderWithRoutes = ({ login }) => {
  const setUser = useSetRecoilState(userState);
  if (login) {
    setUser({ username: "testUser", access_token: "testAccessToken" });
  }
  return (
    <Router>
      <AppHeader />
      <Routes>
        <Route path="/" element={<div>BasePage</div>} />
        <Route path="/login" element={<div>LoginPage</div>} />
        <Route path="/followed" element={<div>FollowedPage</div>} />
        <Route path="/import" element={<div>ImportPage</div>} />
        <Route path="/search" element={<div>SearchPage</div>} />
        <Route path="/aboutus" element={<div>AboutUs</div>} />
      </Routes>
    </Router>
  );
};

const AppHeaderWithRoutesAndRecoil = ({ login }) => {
  return (
    <RecoilRoot>
      <AppHeaderWithRoutes login={login} />
    </RecoilRoot>
  );
};

describe("<AppHeader />", () => {
  it("should contain content", () => {
    render(<AppHeaderWithRoutesAndRecoil login={false} />);
    expect(screen.getByText("Followed Repositories")).toBeInTheDocument();
    expect(screen.getByText("Import Repositories")).toBeInTheDocument();
    expect(screen.getByText("Search Github")).toBeInTheDocument();
    expect(screen.getByText("About Us")).toBeInTheDocument();
    expect(screen.getByText("INFOX - Forks Insight")).toBeInTheDocument();
  });

  it("should show login state", () => {
    render(<AppHeaderWithRoutesAndRecoil login={false} />);
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  it("should show logout state", async () => {
    render(<AppHeaderWithRoutesAndRecoil login />);
    await expect(screen.queryByText("Logout")).toBeInTheDocument();
  });
});
