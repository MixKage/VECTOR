import { useState } from "react";
import RoleModal from "../components/RoleModal";
import {
  login,
  chooseRole,
  storeToken,
  clearToken,
  roleLabel,
} from "../api";

export default function LoginPage() {
  const [form, setForm] = useState({ login: "", password: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [multiRoles, setMultiRoles] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [pendingCredentials, setPendingCredentials] = useState(null);
  const [currentToken, setCurrentToken] = useState(() => {
    const token = sessionStorage.getItem("auth_token");
    const role = sessionStorage.getItem("auth_role");
    return token ? { access_token: token, role: Number(role ?? 0) } : null;
  });

  const handleChange = (field) => (event) => {
    setForm((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const resetAlerts = () => {
    setMessage("");
    setError("");
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    resetAlerts();
    setMultiRoles([]);
    setPendingCredentials(null);

    try {
      const { status, data } = await login(form);
      const roles = Array.isArray(data?.roles) ? data.roles : [];
      if (status === 204 || roles.length > 1) {
        setMultiRoles(roles);
        setPendingCredentials({ ...form });
        setModalOpen(true);
        setMessage("Выберите одну из доступных ролей");
      } else if (data?.access_token) {
        storeToken(data);
        setCurrentToken({ access_token: data.access_token, role: data.role });
        setMessage(`Авторизация успешна. Выбрана роль: ${roleLabel(data.role)}.`);
      } else {
        setError("Неизвестный ответ сервера");
      }
    } catch (err) {
      setError(err.message || "Ошибка авторизации");
    }
  };

  const handleRoleSubmit = async (codes) => {
    const chosen = codes[0];
    if (!pendingCredentials) return;
    try {
      const { data } = await chooseRole({
        ...pendingCredentials,
        role: Number(chosen),
      });
      if (data?.access_token) {
        storeToken(data);
        setCurrentToken({ access_token: data.access_token, role: data.role });
        setMessage(`Роль ${roleLabel(data.role)} успешно активирована.`);
      } else {
        setError("Не удалось получить токен для выбранной роли");
      }
    } catch (err) {
      setError(err.message || "Ошибка выбора роли");
    } finally {
      setModalOpen(false);
      setMultiRoles([]);
      setPendingCredentials(null);
    }
  };

  const handleLogout = () => {
    clearToken();
    setCurrentToken(null);
    setMessage("Токен удалён из памяти браузера");
  };

  return (
    <div className="card">
      <h2>Авторизация</h2>
      <form className="form vertical" onSubmit={handleLogin}>
        <label>
          Логин
          <input
            type="text"
            value={form.login}
            onChange={handleChange("login")}
            required
            autoComplete="username"
          />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={form.password}
            onChange={handleChange("password")}
            required
            minLength={6}
            autoComplete="current-password"
          />
        </label>
        <button type="submit" className="btn-primary">
          Войти
        </button>
      </form>

      {currentToken && (
        <div className="token-block">
          <p>
            <strong>Текущая роль:</strong> {roleLabel(Number(currentToken.role))}
          </p>
          <p className="token">{currentToken.access_token}</p>
          <button className="btn-secondary" onClick={handleLogout}>
            Очистить токен
          </button>
        </div>
      )}

      {message && <div className="success">{message}</div>}
      {error && <div className="error">{error}</div>}

      <RoleModal
        visible={modalOpen}
        multiple={false}
        initialSelected={multiRoles.slice(0, 1)}
        title="Выберите доступную роль"
        description="У этой учётной записи несколько ролей."
        onCancel={() => {
          setModalOpen(false);
          setMultiRoles([]);
        }}
        onSubmit={handleRoleSubmit}
      />
    </div>
  );
}
