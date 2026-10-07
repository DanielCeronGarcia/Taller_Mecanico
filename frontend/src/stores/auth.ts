import { defineStore } from 'pinia'
import { api } from '../services/api'

export type Role = 'ADMINISTRADOR' | 'RECEPCIONISTA' | 'ASESOR' | 'TECNICO' | 'CLIENTE'
export interface User { id: number; email: string; full_name: string; role: Role }

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null as User | null, loading: false }),
  getters: { isAuthenticated: () => Boolean(localStorage.getItem('access_token')) },
  actions: {
    async login(email: string, password: string) {
      try {
        const { data } = await api.post('/auth/login', { email, password })
        localStorage.setItem('access_token', data.access_token)
        await this.loadUser()
      } catch (error) {
        // Evita que un token incompleto deje la pantalla de acceso en un estado inválido.
        this.logout()
        throw error
      }
    },
    async loadUser() { this.user = (await api.get<User>('/auth/me')).data },
    logout() { localStorage.removeItem('access_token'); this.user = null }
  }
})
