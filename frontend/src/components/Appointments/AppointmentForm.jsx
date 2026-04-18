import { useState } from "react";

export default function AppointmentForm({ onSubmit }) {
  const [form, setForm] = useState({
    medico_id: "",
    paziente_id: 1, // per ora fisso
    data_ora: "",
    durata_minuti: 30,
    note: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    onSubmit(form);
  };

  return (
    <div style={styles.container}>
      <h4>📅 Prenota appuntamento</h4>

      <input
        name="medico_id"
        placeholder="ID medico"
        onChange={handleChange}
      />

      <input
        name="data_ora"
        type="datetime-local"
        onChange={handleChange}
      />

      <input
        name="durata_minuti"
        placeholder="Durata (min)"
        onChange={handleChange}
      />

      <input
        name="note"
        placeholder="Note"
        onChange={handleChange}
      />

      <button onClick={handleSubmit}>
        Conferma appuntamento
      </button>
    </div>
  );
}

const styles = {
  container: {
    padding: 15,
    margin: 10,
    background: "#fff",
    borderRadius: 10,
    border: "1px solid #ddd",
    display: "flex",
    flexDirection: "column",
    gap: 8,
  },
};