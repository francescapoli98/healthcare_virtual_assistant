import AppointmentCard from "./AppointmentCard";

export default function AppointmentList({ appointments }) {
  return (
    <div>
      <h3>📅 I tuoi appuntamenti</h3>

      {appointments.map((a) => (
        <AppointmentCard key={a.id} appointment={a} />
      ))}
    </div>
  );
}