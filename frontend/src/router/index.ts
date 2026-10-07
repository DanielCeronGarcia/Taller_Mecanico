import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore, type Role } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import CustomersView from '../views/CustomersView.vue'
import RolesView from '../views/RolesView.vue'
import UsersView from '../views/UsersView.vue'
import RegisterView from '../views/RegisterView.vue'

declare module 'vue-router' { interface RouteMeta { requiresAuth?: boolean; roles?: Role[] } }
const router = createRouter({ history: createWebHistory(), routes: [
  { path: '/', redirect: '/clientes' },
  { path: '/login', component: LoginView },
  { path: '/crear-cuenta', component: RegisterView },
  { path: '/clientes', component: CustomersView, meta: { requiresAuth: true, roles: ['ADMINISTRADOR', 'RECEPCIONISTA'] } },
  { path: '/roles', component: RolesView, meta: { requiresAuth: true, roles: ['ADMINISTRADOR'] } },
  { path: '/usuarios', component: UsersView, meta: { requiresAuth: true, roles: ['ADMINISTRADOR'] } }
] })
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.path === '/login' && auth.isAuthenticated) {
    try { if (!auth.user) await auth.loadUser(); return { path: '/clientes' } } catch { auth.logout() }
  }
  if (!to.meta.requiresAuth) return true
  if (!auth.isAuthenticated) return { path: '/login', query: { redirect: to.fullPath } }
  try { if (!auth.user) await auth.loadUser() } catch { auth.logout(); return { path: '/login' } }
  if (to.meta.roles && (!auth.user || !to.meta.roles.includes(auth.user.role))) return { path: '/clientes' }
  return true
})
export default router
