import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { axiosInstance, isLoggedIn } from "../utils";
import { Context } from "../App";

const LoginPage: React.FC = () => {
  const fetchData = async () => {
    const response = await axiosInstance.get(
      `/auth/login/client${window.location.search}`
    );
    return response.data;
  };
  const navigate = useNavigate();
  useEffect(() => {
    //get code from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const codeParam = urlParams.get("code");

    if (codeParam && !isLoggedIn()) {
      fetchData()
        .then((data) => {
          localStorage.setItem("token", data.token);
          fetchUserData();
        })
        .catch((error) => {
          console.error(error);
        });
    }
    if (isLoggedIn()) navigate("/");
  }, []);
  const { state, setState } = useContext(Context);
  const fetchUserData = () => {
    axiosInstance
      .get("http://localhost:5000/api/graphql/current-user-login", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      .then((response: any) => {
        localStorage.setItem("username", response.data.viewer.login);
        setState({ ...state, user: response.data.viewer.login });
        navigate("/profile");
      })
      .catch((error: Error) => {
        console.error(error);
      });
  };

  const redirectToGitHub = () => {
    // Redirect the user to GitHub's OAuth authorization endpoint
    window.location.assign(
      `https://github.com/login/oauth/authorize?client_id=38c2bd50b945f3adbd41&scope=user repo gist admin:org project read:user read:org read:project`
    );
  };

  return (
    <div className="text-center mt-5">
      <h3
        style={{
          fontSize: 30,
          fontWeight: "lighter",
          marginBottom: 20,
        }}
      >
        WELCOME TO
      </h3>
      <h1 style={{ fontSize: 60, fontFamily: "cursive", fontWeight: "bold" }}>
        GITHUB MINER
      </h1>
      <button className="btn btn-primary mt-5" onClick={redirectToGitHub}>
        Login with Github
      </button>
    </div>
  );
};

export default LoginPage;
