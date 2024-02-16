import Button from "@mui/material/Button";
import { useSetRecoilState } from "recoil";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { postUserLogin } from "./repository";
import { userState } from "./recoil/atoms";

const Login = () => {
  const setUser = useSetRecoilState(userState);
  const navigate = useNavigate();
  const [isLoggingIn, setIsLoggingIn] = useState(false);

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
    setIsLoggingIn(true);
    try {
      const res = await postUserLogin(values);
      console.log("res", res);

      if (!!res?.data?.access_token) {
        localStorage.setItem("access_token", res.data.access_token);
        localStorage.setItem("username", res.data.username);
        setUser({ username: res.data.username });
        navigate("/");
      }
    } catch (error) {
      console.log("unable to login");
      navigate("/");
    }
    setIsLoggingIn(false);
  };

  const onClickLogin = () => {
        let authURL = `https://github.com/login/oauth/authorize?scope=user:email&scope=repo&client_id=a23cbec4da1d5270a30d`;
        console.log(authURL);
        // console.log(chrome);
        chrome.identity.launchWebAuthFlow({
            url: authURL,
            interactive: true
        }, function(redirectURL) {
            console.log(redirectURL);
            fetch('https://github.com/login/oauth/access_token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    client_id: "a23cbec4da1d5270a30d",
                    client_secret: "secret",
                    code: redirectURL.slice(redirectURL.indexOf("?code=") + 6)
                })
            }).then(response => {
                response.json().then(result => {
                    console.log(result);
                    localStorage.setItem("access_token", result.access_token);
                    localStorage.setItem("username", result.username);
                    setUser({ username: result.username });
                    navigate("/");
                });
            });
        });
  };

  return (
    <>
      {!isLoggingIn ? (
        <Button color="inherit" onClick={onClickLogin}>
          Login
        </Button>
      ) : (
        <Button color="inherit" onClick={() => {}}>
          Logging In...
        </Button>
      )}
    </>
  );
};

export default Login;
