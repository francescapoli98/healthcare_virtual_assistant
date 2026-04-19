import { useState, useEffect } from "react";
import ChatWindow from "./components/Chat/ChatWindow";
import AuthForm   from "./components/Auth/AuthForm";
import SidePanel  from "./components/Sidebar/SidePanel";
import { getMe, logout } from "./services/api";
import "./App.css";

export default function App() {
  const [paziente, setPaziente] = useState(null);   // null = non autenticato
  const [checking, setChecking] = useState(true);   // controlla sessione al mount

  // Al caricamento verifica se esiste già una sessione attiva
  useEffect(() => {
    getMe()
      .then(res => setPaziente(res.data))
      .catch(() => setPaziente(null))
      .finally(() => setChecking(false));
  }, []);

  const handleLogout = async () => {
    await logout();
    setPaziente(null);
  };

  if (checking) {
    return <div className="app-loading">Caricamento...</div>;
  }

  if (!paziente) {
    return <AuthForm onAuth={setPaziente} />;
  }

  return (
    <div className="app-layout">
      <SidePanel paziente={paziente} onLogout={handleLogout} />
      <div className="app-main">
        <ChatWindow pazienteId={paziente.id} />
      </div>
    </div>
  );
}