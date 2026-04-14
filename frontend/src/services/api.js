// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
});

export const sendMessage = (message, sessionId) =>
  api.post('/api/chat', { message, session_id: sessionId });

export const getHistory = (sessionId) =>
  api.get(`/api/chat/history/${sessionId}`);

export const getAppointments = (patientId) =>
  api.get(`/api/appointments/${patientId}`);

export const createAppointment = (data) =>
  api.post('/api/appointments', data);

export default api;