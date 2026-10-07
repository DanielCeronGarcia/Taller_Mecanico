<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter(); const name = ref(''); const email = ref(''); const password = ref(''); const confirmation = ref(''); const error = ref(''); const pending = ref(false)
async function submit() {
  error.value = ''
  if (name.value.trim().length < 3 || !/^\S+@\S+\.\S+$/.test(email.value) || password.value.length < 8) { error.value = 'Complete nombre, correo válido y una contraseña de al menos 8 caracteres.'; return }
  if (password.value !== confirmation.value) { error.value = 'Las contraseñas no coinciden.'; return }
  pending.value = true
  try { await api.post('/auth/register', { full_name: name.value, email: email.value, password: password.value }); await router.replace('/login') }
  catch (e: any) { error.value = e.response?.data?.detail ?? 'No fue posible crear la cuenta.' } finally { pending.value = false }
}
</script>
<template><section class="auth-card"><p class="eyebrow">TALLER SERENO</p><h1>Crear cuenta</h1><p>La nueva cuenta tendrá acceso de Administrador.</p><form @submit.prevent="submit" novalidate><label>Nombre completo<input v-model.trim="name" required /></label><label>Correo<input v-model.trim="email" type="email" required /></label><label>Contraseña<input v-model="password" type="password" minlength="8" required /></label><label>Confirmar contraseña<input v-model="confirmation" type="password" minlength="8" required /></label><p v-if="error" class="error" role="alert">{{ error }}</p><button :disabled="pending">{{ pending ? 'Creando…' : 'Crear cuenta' }}</button></form><p class="account-link"><RouterLink to="/login">Volver a iniciar sesión</RouterLink></p></section></template>
