import { useState } from "react";
import { login, register } from "../../services/api";
import "../../App.css";

export default function AuthForm({ onAuth }) {
  const [mode,    setMode]    = useState("login"); // "login" | "register"
  const [form,    setForm]    = useState({ nome: "", cognome: "", email: "", password: "" });
  const [error,   setError]   = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async () => {
    setError(null);
    setLoading(true);
    try {
      const fn  = mode === "login" ? login : register;
      const res = await fn(form);
      onAuth(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Errore, riprova.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-overlay">
      <div className="auth-card">
        <div className="auth-logo">Assistente Sanitario</div>
        <div className="auth-tabs">
          <button
            className={`auth-tab ${mode === "login" ? "auth-tab-active" : ""}`}
            onClick={() => { setMode("login"); setError(null); }}
          >
            Accedi
          </button>
          <button
            className={`auth-tab ${mode === "register" ? "auth-tab-active" : ""}`}
            onClick={() => { setMode("register"); setError(null); }}
          >
            Registrati
          </button>
        </div>

        {mode === "register" && (
          <div className="auth-row">
            <input
              className="auth-input"
              name="nome"
              placeholder="Nome"
              value={form.nome}
              onChange={handleChange}
            />
            <input
              className="auth-input"
              name="cognome"
              placeholder="Cognome"
              value={form.cognome}
              onChange={handleChange}
            />
          </div>
        )}

        <input
          className="auth-input"
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />
        <input
          className="auth-input"
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
        />

        {error && <div className="error-box">{error}</div>}

        <button
          className="confirm-btn"
          style={{ opacity: loading ? 0.5 : 1 }}
          disabled={loading}
          onClick={handleSubmit}
        >
          {loading ? "..." : mode === "login" ? "Accedi" : "Registrati"}
        </button>
      </div>
    </div>
  );
}
