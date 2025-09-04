import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function askGemini(prompt) {
  try {
    const response = await api.post("/ai/gemini/", { prompt });
    return response.data.response;
  } catch (error) {
    console.error("Erreur Gemini :", error);
    return "Erreur lors de la communication avec l'IA";
  }
}

export default api;
