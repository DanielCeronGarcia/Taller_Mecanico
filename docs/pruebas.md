# Pruebas incluidas

Ejecute desde `backend`:

```powershell
pytest tests -q
```

- Unitarias de esquema: normalización de nombres, teléfono inválido y rechazo de roles fuera del catálogo.
- Integración: rutas privadas sin sesión, alta correcta de cliente, duplicidad de cliente, autorización de Recepcionista, denegación a Técnico y duplicidad de usuario.
