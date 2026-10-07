<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../services/api'
import type { Role, User } from '../stores/auth'

const roles: { value: Role; label: string }[] = [
  { value: 'ADMINISTRADOR', label: 'Administrador' }, { value: 'RECEPCIONISTA', label: 'Recepcionista' }, { value: 'ASESOR', label: 'Asesor' }, { value: 'TECNICO', label: 'Técnico' }, { value: 'CLIENTE', label: 'Cliente' }
]
const users = ref<User[]>([]); const error = ref(''); const success = ref(''); const saving = ref(false)
const form = ref({ full_name: '', email: '', password: '', role: 'RECEPCIONISTA' as Role })
async function load() { try { users.value = (await api.get<User[]>('/users')).data } catch (e: any) { error.value = e.response?.data?.detail ?? 'No se pudieron cargar los usuarios.' } }
async function createUser() {
  error.value = ''; success.value = ''
  if (form.value.full_name.trim().length < 3 || !/^\S+@\S+\.\S+$/.test(form.value.email) || form.value.password.length < 8) { error.value = 'Complete nombre, correo válido y una contraseña de al menos 8 caracteres.'; return }
  saving.value = true
  try { await api.post('/users', form.value); success.value = 'Usuario creado correctamente.'; form.value = { full_name: '', email: '', password: '', role: 'RECEPCIONISTA' }; await load() }
  catch (e: any) { error.value = e.response?.data?.detail ?? 'No se pudo crear el usuario.' } finally { saving.value = false }
}
async function updateRole(user: User) { try { await api.patch(`/users/${user.id}/role`, { role: user.role }); success.value = `Rol de ${user.full_name} actualizado.` } catch (e: any) { error.value = e.response?.data?.detail ?? 'No se pudo actualizar el rol.'; await load() } }
onMounted(load)
</script>
<template><section><p class="eyebrow">ADMINISTRACIÓN</p><h1>Usuarios</h1><p>Registra usuarios y asigna uno de los roles autorizados.</p><div class="grid"><form class="card" @submit.prevent="createUser" novalidate><h2>Crear usuario</h2><label>Nombre completo<input v-model.trim="form.full_name" required /></label><label>Correo<input v-model.trim="form.email" type="email" required /></label><label>Contraseña<input v-model="form.password" type="password" minlength="8" required /></label><label>Rol<select v-model="form.role"><option v-for="role in roles" :key="role.value" :value="role.value">{{ role.label }}</option></select></label><p v-if="error" class="error" role="alert">{{ error }}</p><p v-if="success" class="success">{{ success }}</p><button :disabled="saving">{{ saving ? 'Guardando…' : 'Crear usuario' }}</button></form><article class="card"><h2>Usuarios registrados</h2><p v-if="!users.length">No hay usuarios registrados.</p><div v-for="user in users" :key="user.id" class="user-row"><span><strong>{{ user.full_name }}</strong><br><small>{{ user.email }}</small></span><select v-model="user.role" @change="updateRole(user)" :aria-label="`Rol de ${user.full_name}`"><option v-for="role in roles" :key="role.value" :value="role.value">{{ role.label }}</option></select></div></article></div></section></template>
