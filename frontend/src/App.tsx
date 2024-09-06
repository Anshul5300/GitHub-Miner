import React, { Dispatch, SetStateAction, useEffect, useState } from "react";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import RepositoryPage from "./pages/RepositoryPage";
import UserContributions from "./pages/UserContributions";
import { isLoggedIn } from "./utils";

interface PrivateRouteProps {
  children: React.ReactNode;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate("/login");
    }
  }, [navigate]);

  return isLoggedIn() ? <>{children}</> : null;
};

type StateType = {
  searchedUser: string | null;
  user: string | null;
};

type SetStateType = Dispatch<SetStateAction<StateType>>;

export const Context = React.createContext<{
  state: StateType;
  setState: SetStateType;
}>({
  state: { searchedUser: null, user: null },
  setState: () => {},
});

const App: React.FC = () => {
  const [state, setState] = useState<StateType>({
    searchedUser: null,
    user: localStorage.getItem("username")
      ? localStorage.getItem("username")
      : null,
  });

  return (
    <BrowserRouter>
      <Context.Provider value={{ state, setState }}>
        <Navbar />
        <div className="mx-5 py-5 px-5">
          <Routes>
            <Route path="/login" Component={LoginPage} />
            <Route
              path="/:username/repositories"
              element={
                <PrivateRoute>
                  <RepositoryPage />
                </PrivateRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <ProfilePage />
                </PrivateRoute>
              }
            />
            <Route
              path="/:username/contributions"
              element={
                <PrivateRoute>
                  <UserContributions />
                </PrivateRoute>
              }
            />

            <Route path="*" Component={LoginPage} />
          </Routes>
        </div>
      </Context.Provider>
    </BrowserRouter>
  );
};

export default App;
