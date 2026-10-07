<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
const auth = useAuthStore(); const router = useRouter()
function logout() { auth.logout(); router.push('/login') }
</script>

<template>
  <header v-if="auth.user" class="topbar">
    <strong>🔧 Taller Sereno</strong><span>{{ auth.user.full_name }} · {{ auth.user.role }}</span>
    <nav class="main-nav">
      <RouterLink to="/clientes">Clientes</RouterLink>
      <RouterLink v-if="auth.user.role === 'ADMINISTRADOR'" to="/usuarios">Usuarios</RouterLink>
      <RouterLink v-if="auth.user.role === 'ADMINISTRADOR'" to="/roles">Roles</RouterLink>
      <button @click="logout">Salir</button>
    </nav>
  </header>
  <main><RouterView /></main>
</template>
