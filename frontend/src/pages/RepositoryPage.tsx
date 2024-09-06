import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { faCodeFork, faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Context } from "../App";

// Define the shape of the data you expect from the API, adjust as needed.
type Node = {
  id: string;
  name: string;
  createdAt: string;
  isPublic?: boolean;
  stargazerCount: number;
  forkCount: number;
};

type Repository = {
  nodes: Node[];
};
type User = {
  repositories: Repository;
};
type ApiResponse = {
  user: User;
};

const RepositoryList: React.FC = () => {
  // const { username } = useParams<{ username: string }>();
  const { state } = useContext(Context);
  const username = state.searchedUser ? state.searchedUser : state.user;
  const [data, setData] = useState<ApiResponse | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `http://localhost:5000/api/graphql/user-repositories/${username}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      const result: ApiResponse = await response.json();
      setData(result);
    };

    fetchData();
  }, [username]);

  return (
    <div className="card repo_card p-3">
      {data &&
        data.user.repositories.nodes.map((repo: Node) => (
          <div key={repo.name} className="card-body">
            <div className="d-flex justify-content-between align-items-center">
              <span
                className="card-title"
                style={{
                  fontSize: 20,
                  textOverflow: "ellipsis",
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  color: "#4A90E2",
                }}
              >
                {repo.name}
              </span>
              <span style={{ color: "#7F8C8D" }}>
                {new Date(repo.createdAt).toLocaleDateString()}
              </span>
            </div>
            <div className="d-inline-flex align-items-center">
              <div
                className="d-flex align-items-center"
                style={{ marginRight: 15 }}
              >
                <FontAwesomeIcon
                  icon={faStar}
                  style={{ color: "#848d97", marginRight: 3 }}
                />
                <span style={{ color: "#7F8C8D" }}>{repo.stargazerCount}</span>
              </div>
              <div className="d-flex align-items-center">
                <FontAwesomeIcon
                  icon={faCodeFork}
                  style={{ color: "#848d97", marginRight: 3 }}
                />
                <span style={{ color: "#7F8C8D" }}>{repo.forkCount}</span>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
};

export default RepositoryList;
