import { faCodeFork, faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const RepositoryCard = ({ repo }: any) => (
  <div className="card repo_card p-3">
    <div className="card-body">
      <div className="d-flex justify-content-between align-items-center">
        <span
          className="card-title"
          style={{
            fontSize: 20,
            textOverflow: "ellipsis",
            overflow: "hidden",
            whiteSpace: "nowrap",
          }}
        >
          {console.log(repo.name)}
          {repo.name}
        </span>
        <span
          className="badge rounded-pill text-bg-primary access_pill"
          style={{ fontSize: 15 }}
        >
          Public
        </span>
      </div>
      <div
        className="card-text my-3"
        style={{
          textOverflow: "ellipsis",
          overflow: "hidden",
          whiteSpace: "nowrap",
        }}
      >
        {repo.bio ? repo.bio : "This is a public repository"}
      </div>
      <div className="d-inline-flex align-items-center">
        <div className="d-flex align-items-center" style={{ marginRight: 15 }}>
          <FontAwesomeIcon
            icon={faStar}
            style={{ color: "#848d97", marginRight: 3 }}
          />
          <span>{repo.stargazerCount}</span>
        </div>
        <div className="d-flex align-items-center">
          <FontAwesomeIcon
            icon={faCodeFork}
            style={{ color: "#848d97", marginRight: 3 }}
          />
          <span>{repo.forkCount}</span>
        </div>
      </div>
    </div>
  </div>
);

export default RepositoryCard;
