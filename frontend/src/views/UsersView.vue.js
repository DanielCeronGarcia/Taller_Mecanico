import { onMounted, ref } from 'vue';
import { api } from '../services/api';
const roles = [
    { value: 'ADMINISTRADOR', label: 'Administrador' }, { value: 'RECEPCIONISTA', label: 'Recepcionista' }, { value: 'ASESOR', label: 'Asesor' }, { value: 'TECNICO', label: 'Técnico' }, { value: 'CLIENTE', label: 'Cliente' }
];
const users = ref([]);
const error = ref('');
const success = ref('');
const saving = ref(false);
const form = ref({ full_name: '', email: '', password: '', role: 'RECEPCIONISTA' });
async function load() { try {
    users.value = (await api.get('/users')).data;
}
catch (e) {
    error.value = e.response?.data?.detail ?? 'No se pudieron cargar los usuarios.';
} }
async function createUser() {
    error.value = '';
    success.value = '';
    if (form.value.full_name.trim().length < 3 || !/^\S+@\S+\.\S+$/.test(form.value.email) || form.value.password.length < 8) {
        error.value = 'Complete nombre, correo válido y una contraseña de al menos 8 caracteres.';
        return;
    }
    saving.value = true;
    try {
        await api.post('/users', form.value);
        success.value = 'Usuario creado correctamente.';
        form.value = { full_name: '', email: '', password: '', role: 'RECEPCIONISTA' };
        await load();
    }
    catch (e) {
        error.value = e.response?.data?.detail ?? 'No se pudo crear el usuario.';
    }
    finally {
        saving.value = false;
    }
}
async function updateRole(user) { try {
    await api.patch(`/users/${user.id}/role`, { role: user.role });
    success.value = `Rol de ${user.full_name} actualizado.`;
}
catch (e) {
    error.value = e.response?.data?.detail ?? 'No se pudo actualizar el rol.';
    await load();
} }
onMounted(load);
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "eyebrow" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
    ...{ onSubmit: (__VLS_ctx.createUser) },
    ...{ class: "card" },
    novalidate: true,
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    required: true,
});
(__VLS_ctx.form.full_name);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    type: "email",
    required: true,
});
(__VLS_ctx.form.email);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    type: "password",
    minlength: "8",
    required: true,
});
(__VLS_ctx.form.password);
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
    value: (__VLS_ctx.form.role),
});
for (const [role] of __VLS_getVForSourceType((__VLS_ctx.roles))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
        key: (role.value),
        value: (role.value),
    });
    (role.label);
}
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error" },
        role: "alert",
    });
    (__VLS_ctx.error);
}
if (__VLS_ctx.success) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "success" },
    });
    (__VLS_ctx.success);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    disabled: (__VLS_ctx.saving),
});
(__VLS_ctx.saving ? 'Guardando…' : 'Crear usuario');
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
if (!__VLS_ctx.users.length) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
}
for (const [user] of __VLS_getVForSourceType((__VLS_ctx.users))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (user.id),
        ...{ class: "user-row" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
    (user.full_name);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.br, __VLS_intrinsicElements.br)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.small, __VLS_intrinsicElements.small)({});
    (user.email);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
        ...{ onChange: (...[$event]) => {
                __VLS_ctx.updateRole(user);
            } },
        value: (user.role),
        'aria-label': (`Rol de ${user.full_name}`),
    });
    for (const [role] of __VLS_getVForSourceType((__VLS_ctx.roles))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
            key: (role.value),
            value: (role.value),
        });
        (role.label);
    }
}
/** @type {__VLS_StyleScopedClasses['eyebrow']} */ ;
/** @type {__VLS_StyleScopedClasses['grid']} */ ;
/** @type {__VLS_StyleScopedClasses['card']} */ ;
/** @type {__VLS_StyleScopedClasses['error']} */ ;
/** @type {__VLS_StyleScopedClasses['success']} */ ;
/** @type {__VLS_StyleScopedClasses['card']} */ ;
/** @type {__VLS_StyleScopedClasses['user-row']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            roles: roles,
            users: users,
            error: error,
            success: success,
            saving: saving,
            form: form,
            createUser: createUser,
            updateRole: updateRole,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
