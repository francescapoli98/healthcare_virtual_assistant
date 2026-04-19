import { useState } from "react";
import { sendMessage, createAppointment } from "../../services/api";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import AppointmentForm from "../Appointments/AppointmentForm";

export default function ChatWindow({ pazienteId = 1 }) {
  const [messages,      setMessages]      = useState([]);
  const [bookingMode,   setBookingMode]   = useState(false);
  const [mediciSuggeriti, setMediciSuggeriti] = useState([]);
  const [sessioneId,    setSessioneId]    = useState(null);

  const addMessage = (role, text) =>
    setMessages(prev => [...prev, { role, text }]);

  const handleSend = async (text) => {
    addMessage("user", text);

    try {
      const res = await sendMessage(text, sessioneId, pazienteId);
      const data = res.data;

      // Aggiorna sessione_id se è la prima risposta
      if (data.sessione_id && !sessioneId) {
        setSessioneId(data.sessione_id);
      }

      addMessage("bot", data.response);

      // Gestione intent
      if (data.intent === "prenotazione") {
        setBookingMode(true);
        setMediciSuggeriti([]);
      } else if (data.intent === "raccomandazione") {
        setMediciSuggeriti(data.medici || []);
        setBookingMode(false);
      } else {
        // intent "medica" o altro: resetta UI extra
        setMediciSuggeriti([]);
        setBookingMode(false);
      }
    } catch {
      addMessage("bot", "Errore di connessione. Riprova tra qualche istante.");
    }
  };

  const handleAppointmentSubmit = async (data) => {
    try {
      await createAppointment(data);
      addMessage("bot", "Appuntamento creato con successo!");
      setBookingMode(false);
      setMediciSuggeriti([]);
    } catch {
      addMessage("bot", "Errore durante la prenotazione. Riprova.");
    }
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />

      {/* Lista medici suggeriti dopo raccomandazione */}
      {mediciSuggeriti.length > 0 && (
        <div className="medici-suggeriti">
          <p className="medici-label">Medici disponibili:</p>
          {mediciSuggeriti.map(m => (
            <div key={m.id} className="medico-card">
              <span className="medico-nome">{m.nome}</span>
              <span className="medico-spec">{m.specializzazione}</span>
              <button
                className="medico-prenota-btn"
                onClick={() => {
                  setBookingMode(true);
                  setMediciSuggeriti([]);
                }}
              >
                Prenota
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Form prenotazione — aperto da intent o da pulsante manuale */}
      {bookingMode && (
        <AppointmentForm
          pazienteId={pazienteId}
          onSuccess={handleAppointmentSubmit}
        />
      )}

      <div className="input-box-row">
        {!bookingMode && (
          <button
            className="prenota-btn"
            onClick={() => {
              setBookingMode(true);
              setMediciSuggeriti([]);
            }}
          >
            Prenota appuntamento
          </button>
        )}
        {bookingMode && (
          <button
            className="annulla-btn"
            onClick={() => setBookingMode(false)}
          >
            Annulla
          </button>
        )}
      </div>

      <MessageInput onSend={handleSend} />
    </div>
  );
}