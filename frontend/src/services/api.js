import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000",
  withCredentials: true,
});

// AUTHENTICATION (login system)
export const register  = (data) => api.post("/auth/register", data);
export const login     = (data) => api.post("/auth/login", data);
export const logout    = ()     => api.post("/auth/logout");
export const getMe     = ()     => api.get("/auth/me");


// CHAT
export const sendMessage = (message, sessione_id = null, paziente_id = 1) =>
  api.post("/chat/messaggio", { message, sessione_id, paziente_id });

// APPUNTAMENTI
export const createAppointment  = (data) => api.post("/appuntamenti", data);
export const getAppointments = (pid) => api.get(`/appuntamenti/paziente/${pid}`);
export const cancelAppointment  = (id)   => api.delete(`/appuntamenti/${id}`);

// STORICO CHAT
export const getStorico = (pid) => api.get(`/chat/sessione/${pid}`);

export default api;