import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { Context } from "../App";
import { saveAs } from "file-saver";
import * as XLSX from "xlsx";

const UserContributions = () => {
  const [contributions, setContributions] = useState(null);
  // const { username } = useParams<{ username: string }>();
  const { state } = useContext(Context);
  const username = state.searchedUser ? state.searchedUser : state.user;
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (start && end) {
      const fetchData = async () => {
        try {
          const headers = {
            Authorization: `Bearer ${token}`,
          };

          console.log("Headers:", headers);

          const response = await axios.get(
            `http://localhost:5000/api/graphql/user-contributions/${username}/${start}/${end}`,
            { headers }
          );
          console.log(response.data);
          setContributions(response.data);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };

      fetchData();
    }
  }, [username, start, end]);

  const [userNames, setUserNames]: any = useState([]);
  const [userData, setUserData]: any = useState([]);
  const [loading, setLoading]: any = useState(false);

  const handleFileUpload = (event: any) => {
    const file = event.target.files && event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target) {
          const content = e.target.result as string;
          const usernamesArray = content.split("\n").map((line, index) => {
            const [username, startTime, endTime] = line.trim().split(",");
            return { username, startTime, endTime };
          });
          setUserNames(usernamesArray);
        }
      };
      reader.readAsText(file);
    } else {
      setUserNames([]);
      setUserData([]);
    }
  };

  const handleFetch = async () => {
    try {
      setLoading(true);
      const promises = userNames.map(async (user: any) => {
        const response = await axios.get(
          `http://localhost:5000/api/graphql/user-contributions/${user.username}/${user.startTime}/${user.endTime}`
        );
        return response.data;
      });
      let userDataArray = await Promise.all(promises);
      userDataArray = userDataArray.map((user: any, index: any) => {
        return { username: userNames[index].username, ...user };
      });
      setUserData(userDataArray);
      generateExcel(userDataArray);
      console.log(userDataArray);
    } catch (error) {
      console.error("Error fetching GitHub data:", error);
      setLoading(false);
    } finally {
    }
  };

  const generateExcel = (userData: any[]) => {
    // Create a new workbook
    const wb = XLSX.utils.book_new();

    // Convert fetched data to worksheet format
    const wsData = userData.map((user: any) => {
      return [
        user.username,
        user.commit,
        user.issue,
        user.pr,
        user.pr_review,
        user.repository,
        user.res_con,
      ]; // Add more fields as needed
    });

    console.log(wsData);

    // Add the data to a worksheet
    const ws = XLSX.utils.aoa_to_sheet([
      [
        "Username",
        "Commits",
        "Issues",
        "Pull Requests",
        "Pull Request Reviews",
        "Repositories",
        "Restricted Contributions",
      ],
      ...wsData,
    ]);

    // Add the worksheet to the workbook
    XLSX.utils.book_append_sheet(wb, ws, "GitHub Data");

    // Write the workbook to a file
    const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });

    // Convert array buffer to Blob
    const blob = new Blob([excelBuffer], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    setLoading(false);
    // Save the file using file-saver library
    saveAs(blob, "github_data.xlsx");
  };

  const renderContributions = () => {
    if (!contributions) {
      return <p>Loading...</p>;
    }

    return (
      <div className="card repo_card p-3">
        {Object.entries(contributions).map(([key, value]) => (
          <div key={key} className="card-body">
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
                {key}
              </span>
              <span style={{ color: "#7F8C8D" }}>
                {(value as string).toString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="card repo_card p-3">
      <h1 style={{ textAlign: "center" }}>User Contributions</h1>
      <div>
        <h4>Multiple users</h4>
        <input
          type="file"
          accept=".txt"
          onChange={handleFileUpload}
          className="p-3"
          style={{ cursor: "pointer" }}
        />
        <button
          className="btn btn-success"
          disabled={userNames && userNames.length === 0}
          onClick={handleFetch}
        >
          {loading ? (
            <>
              <span
                className="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              <span style={{ marginLeft: 10 }}>Loading...</span>
            </>
          ) : (
            "Download"
          )}
        </button>
      </div>
      <hr className="my-5"></hr>
      <form
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: "20px",
        }}
      >
        <label style={{ marginRight: "10px" }}>
          Start Time:
          <input
            type="datetime-local"
            value={start}
            onChange={(e) => setStart(e.target.value)}
          />
        </label>
        <label>
          End Time:
          <input
            type="datetime-local"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
          />
        </label>
      </form>
      {renderContributions()}
    </div>
  );
};

export default UserContributions;
