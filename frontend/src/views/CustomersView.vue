<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../services/api'
interface Customer { id: number; name: string; email: string; phone: string }
const customers = ref<Customer[]>([]); const error = ref(''); const success = ref(''); const saving = ref(false)
const form = ref({ name: '', email: '', phone: '' })
async function load() { try { customers.value = (await api.get('/customers')).data } catch (e: any) { error.value = e.response?.data?.detail ?? 'No se pudieron cargar los clientes.' } }
async function submit() {
  error.value = ''; success.value = ''
  if (form.value.name.trim().length < 3 || !/^\S+@\S+\.\S+$/.test(form.value.email) || !/^\+?\d{10,15}$/.test(form.value.phone)) { error.value = 'Revise nombre, correo y teléfono (10 a 15 dígitos).'; return }
  saving.value = true
  try { await api.post('/customers', form.value); success.value = 'Cliente registrado correctamente.'; form.value = { name: '', email: '', phone: '' }; await load() }
  catch (e: any) { error.value = e.response?.data?.detail ?? 'No se pudo registrar el cliente.' }
  finally { saving.value = false }
}
onMounted(load)
</script>

<template>
  <section><p class="eyebrow">ATENCIÓN AL CLIENTE</p><h1>Clientes</h1><div class="grid"><form class="card" @submit.prevent="submit" novalidate><h2>Registrar cliente</h2><label>Nombre completo<input v-model.trim="form.name" required minlength="3" /></label><label>Correo<input v-model.trim="form.email" type="email" required /></label><label>Teléfono<input v-model.trim="form.phone" inputmode="numeric" placeholder="5512345678" required /></label><p v-if="error" class="error" role="alert">{{ error }}</p><p v-if="success" class="success">{{ success }}</p><button :disabled="saving">{{ saving ? 'Guardando…' : 'Guardar cliente' }}</button></form><article class="card"><h2>Clientes registrados</h2><p v-if="!customers.length">Aún no hay clientes registrados.</p><ul><li v-for="customer in customers" :key="customer.id"><strong>{{ customer.name }}</strong><br><small>{{ customer.email }} · {{ customer.phone }}</small></li></ul></article></div></section>
</template>
