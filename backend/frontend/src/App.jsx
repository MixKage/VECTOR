import { BrowserRouter, NavLink, Route, Routes, Navigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";

export default function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        <header className="topbar">
          <div className="brand">Auth Portal</div>
          <nav className="nav">
            <NavLink to="/login" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
              Авторизация
            </NavLink>
            <NavLink to="/register" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
              Регистрация
            </NavLink>
          </nav>
        </header>
        <main className="content">
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
