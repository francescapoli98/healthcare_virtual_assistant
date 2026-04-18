import { useState } from "react";
import { sendMessage, createAppointment } from "../../services/api";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import AppointmentForm from "../Appointments/AppointmentForm";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [bookingMode, setBookingMode] = useState(false);

  const handleSend = async (text) => {
    setMessages((prev) => [
      ...prev,
      { role: "user", text }
    ]);
  
    const res = await sendMessage(text);
  
    console.log("RISPOSTA BACKEND:", res);
  
    setMessages((prev) => [
      ...prev,
      { role: "bot", text: res.data.response }
    ]);
  };

  const handleAppointmentSubmit = async (data) => {
    await createAppointment(data);

    setMessages((prev) => [
      ...prev,
      { role: "bot", text: "✅ Appuntamento creato con successo!" },
    ]);

    setBookingMode(false);
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />

      {/* 👉 FORM DINAMICO NELLA CHAT */}
      {bookingMode && (
        <AppointmentForm onSubmit={handleAppointmentSubmit} />
      )}

      <MessageInput onSend={handleSend} />
    </div>
  );
}