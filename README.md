# Sistema de Gestión — Taller Mecánico

Monorepo con API FastAPI y cliente Vue 3 + TypeScript.

## Puesta en marcha

1. Cree la base `taller_mecanico` en MySQL y copie `backend/.env.example` a `backend/.env`.
2. Backend: `cd backend`, cree un entorno virtual, instale `pip install -r requirements.txt` y ejecute `uvicorn app.main:app --reload`.
3. Frontend: `cd frontend`, instale `npm install` y ejecute `npm run dev`.

El usuario administrador inicial se configura con `FIRST_ADMIN_EMAIL` y `FIRST_ADMIN_PASSWORD`.

## Estructura

```text
Taller_Mecanico/
├── backend/       # API, reglas de negocio, persistencia y pruebas
├── frontend/      # Vistas Vue, seguridad de rutas y servicios
└── docker-compose.yml
```

| Actor | Acceso inicial |
|---|---|
| Administrador | Administración, altas de clientes y auditoría |
| Recepcionista | Altas y consulta de clientes |
| Asesor | Consulta operativa |
| Técnico | Consulta operativa limitada |
| Cliente | Portal propio |

La API es la fuente de verdad de permisos: toda ruta privada exige JWT. Los roles asignables son estrictamente los cinco de la tabla. El historial `/api/v1/consultas` permite al Administrador filtrar las solicitudes por actor, ruta y fecha.
