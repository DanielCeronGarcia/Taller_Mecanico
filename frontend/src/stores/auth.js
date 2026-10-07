import { defineStore } from 'pinia';
import { api } from '../services/api';
export const useAuthStore = defineStore('auth', {
    state: () => ({ user: null, loading: false }),
    getters: { isAuthenticated: () => Boolean(localStorage.getItem('access_token')) },
    actions: {
        async login(email, password) {
            try {
                const { data } = await api.post('/auth/login', { email, password });
                localStorage.setItem('access_token', data.access_token);
                await this.loadUser();
            }
            catch (error) {
                // Evita que un token incompleto deje la pantalla de acceso en un estado inválido.
                this.logout();
                throw error;
            }
        },
        async loadUser() { this.user = (await api.get('/auth/me')).data; },
        logout() { localStorage.removeItem('access_token'); this.user = null; }
    }
});
