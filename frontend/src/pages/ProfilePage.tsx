import React, { useContext, useEffect, useState } from "react";
import "../styles/profile.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPeopleGroup } from "@fortawesome/free-solid-svg-icons";
import RepositoryCard from "../components/RepositoryCard";
import { axios } from "../utils/AxiosInstance";
import { Context } from "../App";

const ProfilePage: React.FC = () => {
  const [profile, setProfile]: any = useState(null);
  const [repos, setRepos]: any = useState([]);
  const { state } = useContext(Context);
  useEffect(() => {
    const user = state.searchedUser ? state.searchedUser : state.user;
    const userStatsUrl = `/api/graphql/user-stats/${user}`;
    const reposUrl = `/api/graphql/user-repositories/${user}`;
    axios
      .get(userStatsUrl)
      .then((res) => {
        setProfile(res.data);
      })
      .catch((err) => console.log(err.message));
    axios
      .get(reposUrl)
      .then((res) => {
        setRepos(res.data?.user?.repositories?.nodes?.slice(1, 7));
      })
      .catch((err) => console.log(err.message));
  }, [state]);

  return (
    <div className="row">
      {profile && (
        <div className="col-3">
          {profile.avatar_url && (
            <img
              src="https://avatars.githubusercontent.com/u/1024025?v=4"
              className="profile_pic"
            />
          )}
          {/* <h2 className="mt-4">Linus Torvalds</h2> */}
          <div
            className="github_username"
            style={{ marginTop: -10, color: "#848d97" }}
          >
            {profile?.github}
          </div>
          <div className="mt-3" style={{ fontSize: 20 }}>
            <div className="d-flex align-items-center">
              <FontAwesomeIcon
                icon={faPeopleGroup}
                style={{ marginRight: 5, color: "#848d97" }}
              />
              <span>
                <span style={{ fontWeight: "bold" }}>{profile.followers}</span>{" "}
                <span style={{ color: "#848d97" }}>followers</span> |{" "}
                <span style={{ fontWeight: "bold" }}>{profile.following}</span>{" "}
                <span style={{ color: "#848d97" }}>following</span>
              </span>
            </div>
            {/* <div className="mt-4">
            <FontAwesomeIcon icon={faBuilding} style={{ color: "#848d97" }} />{" "}
            <span>Linux Foundation</span>
          </div>
          <div>
            <FontAwesomeIcon
              icon={faLocationDot}
              style={{ color: "#848d97" }}
            />{" "}
            <span>Portland, OR</span>
          </div> */}
          </div>
        </div>
      )}
      <div className="col-9">
        <h4>Popular repositories</h4>
        <div className="row d-flex gx-4 gy-4 my-1">
          {repos.map((repo: any) => {
            return (
              <div className="col-6 md-col-12">
                <RepositoryCard repo={repo} />
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
