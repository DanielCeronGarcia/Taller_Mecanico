<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../services/api'
const records = ref<any[]>([]); const path = ref(''); const error = ref('')
async function load() { try { records.value = (await api.get('/consultas', { params: path.value ? { path: path.value } : {} })).data } catch (e: any) { error.value = e.response?.data?.detail ?? 'No se pudo cargar la auditoría.' } }
onMounted(load)
</script>
<template><section><p class="eyebrow">ADMINISTRACIÓN</p><h1>Consultas auditadas</h1><div class="card"><form class="inline" @submit.prevent="load"><label>Filtrar por ruta<input v-model="path" placeholder="customers" /></label><button>Filtrar</button></form><p v-if="error" class="error">{{ error }}</p><table><thead><tr><th>Fecha</th><th>Actor</th><th>Método</th><th>Ruta</th><th>Estado</th></tr></thead><tbody><tr v-for="item in records" :key="item.id"><td>{{ new Date(item.created_at).toLocaleString() }}</td><td>{{ item.actor_role }}</td><td>{{ item.method }}</td><td>{{ item.path }}</td><td>{{ item.status_code }}</td></tr></tbody></table></div></section></template>
