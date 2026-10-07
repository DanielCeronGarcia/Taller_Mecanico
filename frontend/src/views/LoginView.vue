<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
const email = ref(''); const password = ref(''); const error = ref(''); const pending = ref(false)
const auth = useAuthStore()
async function submit() {
  error.value = ''
  if (!email.value.includes('@') || password.value.length < 8) { error.value = 'Ingrese un correo válido y una contraseña de al menos 8 caracteres.'; return }
  pending.value = true
  try {
    await auth.login(email.value, password.value)
    // Recarga la aplicación ya autenticada y evita que una navegación interna
    // pendiente mantenga visible la vista de Login.
    window.location.assign('/clientes')
  }
  catch (e: any) { error.value = e.response?.data?.detail ?? 'No fue posible iniciar sesión. Intente de nuevo.' }
  finally { pending.value = false }
}
</script>

<template>
  <section class="auth-card"><p class="eyebrow">TALLER SERENO</p><h1>Bienvenido</h1><p>Inicie sesión para continuar de forma segura.</p>
    <form @submit.prevent="submit" novalidate><label>Correo<input v-model.trim="email" type="email" autocomplete="email" required /></label><label>Contraseña<input v-model="password" type="password" autocomplete="current-password" minlength="8" required /></label><p v-if="error" class="error" role="alert">{{ error }}</p><button :disabled="pending">{{ pending ? 'Ingresando…' : 'Ingresar' }}</button></form>
    <p class="account-link">¿Aún no tiene cuenta? <RouterLink to="/crear-cuenta">Crear cuenta</RouterLink></p>
  </section>
</template>
