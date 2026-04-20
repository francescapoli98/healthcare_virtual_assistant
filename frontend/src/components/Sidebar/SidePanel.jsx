import { useState, useEffect } from "react";
import { getStorico, getAppointments, cancelAppointment } from "../../services/api";
import "../../App.css";

export default function SidePanel({ paziente, onLogout }) {
  const [isOpen, setIsOpen] = useState(true);
  const [tab, setTab] = useState("appuntamenti");
  const [appuntamenti, setAppuntamenti] = useState([]);
  const [storico, setStorico] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (tab === "appuntamenti") loadAppuntamenti();
    else loadStorico();
  }, [tab]);

  async function loadAppuntamenti() {
    setLoading(true);
    try {
      const res = await getAppointments(paziente.id);
      setAppuntamenti(res.data);
    } catch {
      setAppuntamenti([]);
    } finally {
      setLoading(false);
    }
  }

  async function loadStorico() {
    setLoading(true);
    try {
      const res = await getStorico(paziente.id);
      setStorico(res.data);
    } catch {
      setStorico([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleCancel(id) {
    await cancelAppointment(id);
    loadAppuntamenti();
  }

  function formatData(dataOra) {
    if (!dataOra) return "—";
    const d = new Date(dataOra);
    return (
      d.toLocaleDateString("it-IT", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      }) +
      " " +
      d.toLocaleTimeString("it-IT", {
        hour: "2-digit",
        minute: "2-digit",
      })
    );
  }

  return (
    <div className={`side-panel ${!isOpen ? "closed" : ""}`}>
      
      {/* Header */}
      <div className="side-header">
        <div className="side-avatar">
          {paziente.nome[0]}{paziente.cognome[0]}
        </div>

        {isOpen && (
          <div className="side-user-info">
            <div className="side-user-name">
              {paziente.nome} {paziente.cognome}
            </div>
          </div>
        )}

        {isOpen && (
          <button className="side-logout-btn" onClick={onLogout}>
            Esci
          </button>
        )}

        {/* Toggle button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          style={{
            marginLeft: "auto",
            border: "none",
            background: "none",
            cursor: "pointer",
            fontSize: "16px"
          }}
        >
          {isOpen ? "⮜" : "⮞"}
        </button>
      </div>

      {/* Mostra resto solo se aperta */}
      {isOpen && (
        <>
          <div className="side-tabs">
            <button
              className={`side-tab ${tab === "appuntamenti" ? "side-tab-active" : ""}`}
              onClick={() => setTab("appuntamenti")}
            >
              Appuntamenti
            </button>

            <button
              className={`side-tab ${tab === "storico" ? "side-tab-active" : ""}`}
              onClick={() => setTab("storico")}
            >
              Chat
            </button>
          </div>

          <div className="side-content">
            {loading && <div className="side-empty">Caricamento...</div>}

            {!loading && tab === "appuntamenti" && (
              appuntamenti.length === 0
                ? <div className="side-empty">Nessun appuntamento</div>
                : appuntamenti.map(a => (
                    <div key={a.id} className={`appt-card appt-${a.stato}`}>
                      <div className="appt-data">{formatData(a.data_ora)}</div>
                      <div className="appt-medico">Medico ID: {a.medico_id}</div>
                      <div className="appt-stato">{a.stato}</div>
                      {a.stato === "programmato" && (
                        <button
                          className="appt-cancel-btn"
                          onClick={() => handleCancel(a.id)}
                        >
                          Annulla
                        </button>
                      )}
                    </div>
                  ))
            )}

            {!loading && tab === "storico" && (
              storico.length === 0
                ? <div className="side-empty">Nessun messaggio in storico</div>
                : storico.map((m, i) => (
                    <div key={i} className={`storico-msg storico-${m.ruolo}`}>
                      <span className="storico-ruolo">
                        {m.ruolo === "utente" ? "Tu" : "Assistente"}
                      </span>
                      <span className="storico-testo">{m.contenuto}</span>
                    </div>
                  ))
            )}
          </div>
        </>
      )}
    </div>
  );
}