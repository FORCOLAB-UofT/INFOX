import axios from "axios";
import Button from "@mui/material/Button";
import { useSetRecoilState } from "recoil";
import React, { useEffect } from "react";
import { postUserLogin } from "./repository";
import { userState } from "./recoil/atoms";

const Login = () => {
  const setUser = useSetRecoilState(userState);

  useEffect(() => {
    const newUrl = window.location.href;
    const hasCode = newUrl.includes("?code=");

    console.log("hasCode", hasCode);

    if (hasCode) {
      const url = newUrl.split("?code=")[1];
      //const data = {
      //  code: url[0],
      //};

      console.log("url", url);

      submitGithub(url);
    }
  }, [postUserLogin]);

  const submitGithub = async (values) => {
    try {
      const res = await postUserLogin(values);
      console.log("res", res);

      if (!!res?.data?.access_token) {
        localStorage.setItem("access_token", res.data.access_token);
        localStorage.setItem("username", res.data.username);
        setUser({ username: res.data.username });
      }
    } catch (error) {
      console.log("unable to login");
    }
  };

  const onClickLogin = () => {
    window.location.href =
      "https://github.com/login/oauth/authorize?scope=user:email&client_id=2d8e058ac0d5cf153c9e";
  };

  return (
    <Button color="inherit" onClick={onClickLogin}>
      Login
    </Button>
  );
};

export default Login;
