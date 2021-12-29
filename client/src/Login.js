import axios from "axios";
import React, { useEffect } from "react";
import { postUserLogin } from "./repository";

const Login = () => {
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
        localStorage.setItem("name", res.data.username);
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
    <>
      <button onClick={onClickLogin}>Login</button>
      <button
        onClick={async () => {
          const res = await axios({
            method: "GET",
            url: "http://localhost:5000/flask/auth",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("access_token"),
            },
          });
          console.log("res", res);
        }}
      >
        test get
      </button>
    </>
  );
};

export default Login;
