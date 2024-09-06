import axios from "axios";

const url = "http://localhost:5000";

axios.defaults.baseURL = url;

const setToken = (token: string) => {
  axios.defaults.headers["Authorization"] = `Bearer ${token}`;
};

const removeToken = () => {
  delete axios.defaults.headers["Authorization"];
};

export { axios, setToken, removeToken };
