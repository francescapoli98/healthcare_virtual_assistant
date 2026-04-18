import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000",
});


// CHAT
export const sendMessage = (message) =>
  api.post("/chat/messaggio", {
    message,
  });


// APPUNTAMENTI - CREAZIONE
export const createAppointment = (data) =>
  api.post("/appuntamenti", data);


// APPUNTAMENTI - LISTA PAZIENTE
export const getAppointments = (patientId) =>
  api.get(`/pazienti/${patientId}/appuntamenti`);


// CANCELLA APPUNTAMENTO
export const cancelAppointment = (id) =>
  api.delete(`/appuntamenti/${id}`);

export default api;