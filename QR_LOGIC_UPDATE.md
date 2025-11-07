# Actualización de Lógica de Códigos QR y Registro de Visitas

## Cambios Implementados

### 1. Separación de Generación QR y Registro de Visitas

**ANTES:**
- El endpoint `/api/user/visits` generaba QR y guardaba la visita en BD
- El código QR se almacenaba en la columna `qr_code` de la tabla `user_visits`
- La validación solo verificaba el QR sin registrar nueva visita

**AHORA:**
- **`/api/user/generate-qr`**: Genera código QR sin guardar nada en BD
- **`/api/user/validate-qr`**: Valida QR y registra la visita efectiva en BD

### 2. Flujo de Negocio Actualizado

1. **Generar QR** (`POST /api/user/generate-qr`):
   - Crea código QR encriptado con JWT
   - Retorna imagen QR en Base64
   - **NO guarda nada en la base de datos**

2. **Validar QR** (`POST /api/user/validate-qr`):
   - Decodifica y valida el token JWT del QR
   - Verifica usuario, negocio y mes actual
   - Comprueba que no exista visita duplicada
   - **Registra la visita efectiva en la BD**

### 3. Cambios en Base de Datos

- **Eliminada** la columna `qr_code` de la tabla `user_visits`
- Los registros de visita solo se crean cuando se valida el QR
- Cada registro representa una visita efectiva confirmada

### 4. Archivos Modificados

#### Modelos (`app/models/user_visit.py`):
- `generate_qr_code()`: Genera QR sin guardar en BD
- `register_visit()`: Registra visita efectiva
- Eliminado: `create_visit()` que guardaba QR en BD

#### Servicios (`app/services/user_service.py`):
- `generate_qr_code()`: Servicio para generar QR
- `validate_qr_visit()`: Valida QR y registra visita

#### Controladores (`app/controllers/user_controller.py`):
- `generate_qr()`: Controlador para generar QR
- `validate_qr_visit()`: Actualizado para registrar visita

#### Rutas (`app/routes/user.py`):
- `POST /api/user/generate-qr`: Nuevo endpoint para generar QR
- `POST /api/user/validate-qr`: Actualizado para registrar visita

### 5. Esquemas de Request/Response

#### Generar QR:
```json
POST /api/user/generate-qr
{
  "user_id": 1,
  "business_id": 5,
  "visit_date": "2024-01-15T10:30:00"
}

Response:
{
  "success": true,
  "message": "Código QR generado exitosamente",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

#### Validar QR:
```json
POST /api/user/validate-qr
{
  "qr_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "business_id": 5
}

Response:
{
  "success": true,
  "message": "Visita registrada exitosamente",
  "data": {
    "user_id": 1,
    "business_id": 5,
    "visit_date": "2024-01-15T10:30:00"
  }
}
```

### 6. Beneficios de los Cambios

1. **Eficiencia de BD**: No se almacenan códigos QR innecesarios
2. **Registro Preciso**: Solo se registran visitas efectivamente validadas
3. **Separación de Responsabilidades**: Generación y validación son procesos independientes
4. **Mejor Control**: Evita registros de visitas no confirmadas

### 7. Migración Realizada

- Ejecutado script `remove_qr_code_column.py` para eliminar columna `qr_code`
- Tabla `user_visits` ahora solo contiene datos de visitas efectivas
- No se requieren cambios adicionales en BD

## Uso de los Nuevos Endpoints

1. **Para generar QR**: Llamar a `/api/user/generate-qr` con datos de la visita
2. **Para registrar visita**: Escanear QR y llamar a `/api/user/validate-qr`
3. **El registro en BD solo ocurre en el paso 2**