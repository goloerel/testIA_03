# Specification: Vehicle Inventory API

## 1. Feature Overview
La API de Inventario de Vehículos tiene como objetivo centralizar la gestión de la flota de una empresa de transporte de carga en México. Permitirá el registro, actualización, consulta y baja de unidades (tractocamiones, remolques, etc.), asegurando que cada vehículo cumpla con las validaciones de normativa mexicana y mantenga su estatus operativo actualizado.

## 2. User Stories

### Historia 1: Registro de Unidades
*   **Como:** Administrador de Flota.
*   **Quiero:** Registrar un nuevo vehículo en el sistema con su placa, número económico y datos técnicos.
*   **Criterio de Aceptación:** El sistema debe validar que la placa siga el formato mexicano y que el número económico sea único.

### Historia 2: Consulta de Inventario
*   **Como:** Coordinador de Operaciones.
*   **Quiero:** Listar todos los vehículos registrados de forma paginada.
*   **Criterio de Aceptación:** La respuesta debe incluir el total de registros y permitir navegar por páginas para no saturar la red.

### Historia 3: Control de Mantenimiento
*   **Como:** Jefe de Taller.
*   **Quiero:** Cambiar el estado de un vehículo a `IN_MAINTENANCE`.
*   **Criterio de Aceptación:** El sistema debe permitir actualizar solo el campo de estado y registrar la última fecha de verificación.

### Historia 4: Verificación de Seguros
*   **Como:** Gestor de Cumplimiento.
*   **Quiero:** Consultar los detalles de un vehículo por su ID para revisar la vigencia de la póliza de seguro.
*   **Criterio de Aceptación:** Si el ID no existe, el sistema debe devolver un error 404 claro.

### Historia 5: Depuración de Flota
*   **Como:** Director de Logística.
*   **Quiero:** Eliminar del sistema vehículos que han sido vendidos o dados de baja definitiva.
*   **Criterio de Aceptación:** Al eliminar un vehículo, este ya no debe aparecer en las búsquedas generales.

## 3. Functional Requirements

### 3.1 CRUD Completo
*   Implementar endpoints para Crear, Leer (individual y lista), Actualizar y Borrar vehículos.

### 3.2 Paginación
*   El endpoint `GET /api/v1/vehicles` debe soportar parámetros de `limit` y `offset`.

### 3.3 Validaciones Obligatorias
*   **Placa**: Validación de formato string.
*   **Año**: Solo valores entre 1990 y el año en curso.
*   **Enums**: El tipo de vehículo debe ser estrictamente:
    *   `TRACTOR_TRUCK`
    *   `RIGID_TRUCK`
    *   `TRAILER`
    *   `DOLLY`

### 3.4 Salud del Sistema
*   Endpoint `/health` que verifique la conexión activa con MongoDB.

## 4. Edge Cases (Casos de Borde)
*   Intento de registrar una placa o número económico que ya existe en la base de datos.
*   Búsqueda de un vehículo con un ID de MongoDB mal formado o inexistente.
*   Envío de tipos de datos incorrectos (ej. una cadena en el campo `capacidad_carga_kg`).

## 5. Success Metrics
*   El 100% de los endpoints definidos en el contrato OpenAPI funcionan correctamente.
*   Todas las validaciones de datos impiden la entrada de información basura a la base de datos.
*   El tiempo de respuesta del endpoint de salud es inferior a 200ms.
