import { useState } from "react";
import RoleModal from "../components/RoleModal";
import { registerAccount, ROLE_OPTIONS } from "../api";

const DEFAULT_ROLES = [0];

export default function RegisterPage() {
  const [form, setForm] = useState({ login: "", password: "" });
  const [selectedRoles, setSelectedRoles] = useState(DEFAULT_ROLES);
  const [modalOpen, setModalOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (event) => {
    setForm((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const rolesSummary = selectedRoles
    .map((code) => ROLE_OPTIONS.find((item) => item.code === code)?.label || code)
    .join(", " );

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      const codes = selectedRoles.length ? selectedRoles : DEFAULT_ROLES;
      await registerAccount({
        login: form.login,
        password: form.password,
        roles: codes.join(" "),
      });
      setMessage("Регистрация прошла успешно");
      setForm({ login: "", password: "" });
      setSelectedRoles(DEFAULT_ROLES);
    } catch (err) {
      setError(err.message || "Не удалось зарегистрировать пользователя");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Регистрация</h2>
      <form className="form vertical" onSubmit={handleSubmit}>
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
            autoComplete="new-password"
          />
        </label>
        <div className="inline-field">
          <div>
            <span className="field-label">Выбранные роли:</span>
            <span className="chip-list">{rolesSummary || "Нет ролей"}</span>
          </div>
          <button type="button" className="btn-secondary" onClick={() => setModalOpen(true)}>
            Выбрать роли
          </button>
        </div>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Отправка..." : "Создать аккаунт"}
        </button>
      </form>
      {message && <div className="success">{message}</div>}
      {error && <div className="error">{error}</div>}

      <RoleModal
        visible={modalOpen}
        multiple
        initialSelected={selectedRoles}
        title="Выберите роли"
        description="Можно выбрать одну или несколько ролей."
        onCancel={() => setModalOpen(false)}
        onSubmit={(codes) => {
          setSelectedRoles(codes.length ? codes : DEFAULT_ROLES);
          setModalOpen(false);
        }}
      />
    </div>
  );
}
