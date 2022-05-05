import React from "react";
import Button from "@mui/material/Button";
import { useSetRecoilState } from "recoil";
import { useNavigate } from "react-router-dom";
import { userState } from "./recoil/atoms";

const Logout = () => {
  const setUser = useSetRecoilState(userState);
  const navigate = useNavigate();

  const onClickLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    setUser(null);
    navigate("/");
  };

  return (
    <Button color="inherit" onClick={onClickLogout}>
      Logout
    </Button>
  );
};

export default Logout;
