import { Route, Routes } from "react-router-dom";

import IndexPage from "@/pages/index";
import ModeratorPage from "./pages/moderator";
import HRPage from "./pages/hr";
import UniversityPage from "./pages/university";
import CandidatePage from "./pages/candidate";

function App() {
  return (
    <Routes>
      <Route element={<IndexPage />} path="/" />
      <Route element={<ModeratorPage />} path="/moderator" />
      <Route element={<HRPage />} path="/hr" />
      <Route element={<UniversityPage />} path="/university" />
      <Route element={<CandidatePage />} path="/candidate" />
    </Routes>
  );
}

export default App;
