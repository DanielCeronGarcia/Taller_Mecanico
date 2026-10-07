import axios from 'axios';
// En desarrollo la API se inicia en 127.0.0.1; usar el mismo host evita fallos
// de resolución de localhost y de origen al crear la sesión.
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000/api/v1' });
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token)
        config.headers.Authorization = `Bearer ${token}`;
    return config;
});
