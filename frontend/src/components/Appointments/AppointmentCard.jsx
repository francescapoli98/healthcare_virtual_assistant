export default function AppointmentCard({ appointment }) {
    return (
      <div style={styles.card}>
        <div>📅 {appointment.data_ora}</div>
        <div>👨‍⚕️ Medico: {appointment.medico_id}</div>
        <div>⏱ {appointment.durata} min</div>
        <div>📌 {appointment.stato}</div>
      </div>
    );
  }
  
  const styles = {
    card: {
      padding: 10,
      margin: 5,
      background: "#fff",
      border: "1px solid #ddd",
      borderRadius: 8,
    },
  };