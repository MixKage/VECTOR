import { useState } from "react";
import { registerAccount } from "../api";

export default function RegisterPage() {
  const [form, setForm] = useState({ login: "", password: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (event) => {
    setForm((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await registerAccount({
        login: form.login,
        password: form.password,
      });
      setMessage("Регистрация прошла успешно");
      setForm({ login: "", password: "" });
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
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Отправка..." : "Создать аккаунт"}
        </button>
      </form>
      {message && <div className="success">{message}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}
