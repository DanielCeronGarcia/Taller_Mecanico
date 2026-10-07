# Caso de uso: Registrar cliente

**Actores autorizados:** Administrador y Recepcionista.  
**Propósito:** crear el expediente mínimo de un cliente para futuras órdenes de servicio.

## Flujo principal

1. El actor inicia sesión con correo y contraseña.
2. El cliente web recupera su perfil y habilita la pantalla Clientes sólo si su rol está autorizado.
3. El actor captura nombre, correo y teléfono.
4. El frontend valida los datos antes de enviarlos y muestra el error en la misma pantalla si alguno es inválido.
5. La API valida de nuevo el contrato, el JWT y el rol.
6. La API verifica que correo y teléfono no existan y guarda el cliente de forma atómica.
7. La interfaz confirma el registro y actualiza el listado.
8. La solicitud queda en el historial auditable con actor, método, ruta, estado y fecha.

## Flujos alternos

- Sin sesión o sesión vencida: la API devuelve `401` y el cliente vuelve a Inicio de sesión.
- Rol no permitido: la API devuelve `403` y no crea ningún dato.
- Correo o teléfono duplicado: la API devuelve `409`; el formulario conserva los datos y explica el conflicto.
- Datos inválidos: el frontend impide el envío y la API responde `422` si se intenta evitar la interfaz.
