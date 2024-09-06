import { faGithub } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "../styles/navbar.css";
import {
  faBookOpen,
  faList,
  faRightFromBracket,
  faTimeline,
} from "@fortawesome/free-solid-svg-icons";
import { removeToken } from "../utils/AxiosInstance";
import { redirect, useNavigate } from "react-router-dom";
import { isLoggedIn } from "../utils";
import { useContext, useState } from "react";
import { Context } from "../App";
import { Link } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const handleLogout = () => {
    removeToken();
    localStorage.clear();
    navigate("/");
  };
  const [text, setText] = useState("");
  const { state, setState } = useContext(Context);
  const handleSearch = (e: any) => {
    e.preventDefault();
    localStorage.setItem("searchedUser", text);
    setState({ ...state, searchedUser: text });
  };
  return (
    <div>
      <nav
        className="navbar navbar-expand-lg bg-body-tertiary p-4"
        style={{ color: "inherit", backgroundColor: "#010409" }}
      >
        <div className="container-fluid">
          <a
            className="navbar-brand d-flex align-items-center"
            href="/profile"
            style={{ color: "inherit" }}
          >
            <FontAwesomeIcon
              icon={faGithub}
              style={{ marginRight: 10 }}
              size="2x"
            />
            <span>GitHub Miner</span>
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          {
            isLoggedIn() && (
              <div
                className="collapse navbar-collapse"
                id="navbarSupportedContent"
              >
                <ul
                  className="navbar-nav me-auto mb-2 mb-lg-0"
                  style={{ marginLeft: 30, fontSize: 18 }}
                >
                  <li className="nav-item navbar_item">
                    <Link
                      className="nav-link active "
                      aria-current="page"
                      to="/profile"
                    >
                      <FontAwesomeIcon
                        icon={faBookOpen}
                        style={{ marginRight: 5 }}
                      />{" "}
                      Overview
                    </Link>
                  </li>
                  <li className="nav-item navbar_item">
                    <Link
                      className="nav-link"
                      to={`/${localStorage.getItem("username")}/repositories`}
                    >
                      <FontAwesomeIcon
                        icon={faList}
                        style={{ marginRight: 5 }}
                      />{" "}
                      Repositories
                    </Link>
                  </li>
                  <li className="nav-item navbar_item">
                    <Link
                      className="nav-link"
                      to={`/${localStorage.getItem("username")}/contributions`}
                    >
                      <FontAwesomeIcon
                        icon={faTimeline}
                        style={{ marginRight: 5 }}
                      />{" "}
                      Time-range contributions
                    </Link>
                  </li>
                </ul>
                <div
                  className="d-flex align-items-center"
                  style={{ marginRight: 30 }}
                >
                  <input
                    type="text"
                    value={text}
                    placeholder="Search"
                    className="searchbox"
                    onChange={(e: any) => {
                      setText(e.target.value);
                    }}
                  />
                  <button
                    className="btn btn-light search_btn"
                    onClick={handleSearch}
                  >
                    Search
                  </button>
                </div>
                <div className="btn btn-danger" onClick={handleLogout}>
                  <FontAwesomeIcon icon={faRightFromBracket} /> Sign Out
                </div>
              </div>
            )
            // : (
            //   <div
            //     className="collapse navbar-collapse d-flex"
            //     id="navbarSupportedContent"
            //   >
            //     <div
            //       className="btn btn-success align-self-end"
            //       onClick={redirectToGitHub}
            //     >
            //       <FontAwesomeIcon icon={faRightFromBracket} /> Sign In
            //     </div>
            //   </div>
            // )
          }
        </div>
      </nav>
    </div>
  );
};

export default Navbar;
