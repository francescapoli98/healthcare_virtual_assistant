import { useState } from "react";

export default function MessageInput({ onSend }) {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    onSend(text);
    setText("");
  };

  return (
    <div className="input-box">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Scrivi un messaggio..."
      />
      <button onClick={handleSubmit}>Invia</button>
    </div>
  );
}