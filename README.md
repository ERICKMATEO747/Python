# Auth API - Backend Python

API REST para autenticación de usuarios con registro y login, construida con FastAPI y MySQL.

## 🚀 Características

- ✅ Registro de usuarios con validación de email único
- ✅ Login con JWT tokens (24h de expiración)
- ✅ Encriptación de contraseñas con bcrypt (12 salt rounds)
- ✅ Validaciones robustas con Pydantic
- ✅ Arquitectura modular (controllers, services, models)
- ✅ Manejo de errores con códigos HTTP apropiados
- ✅ Documentación automática con Swagger
- ✅ Sistema de rondas para programa de lealtad
- ✅ Seguimiento automático de progreso por ronda
- ✅ Migración automática de datos existentes

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL (Supabase recomendado)
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Python
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos PostgreSQL (Supabase)

La aplicación ahora usa PostgreSQL con Supabase. Las tablas se crean automáticamente.

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo:
```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:
```env
# PostgreSQL Supabase Configuration
DATABASE_URL=postgresql://postgres.rfqmpodqjmqniuvdmmzd:okr4CL7LXgu3Ip5Q@aws-1-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require
SUPABASE_URL=https://rfqmpodqjmqniuvdmmzd.supabase.co
SUPABASE_ANON_KEY=tu_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=tu_supabase_service_role_key
JWT_SECRET_KEY=tu-clave-secreta-jwt-muy-segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
```

## 🚀 Ejecutar la aplicación

### Migración automática (recomendado)
```bash
python migrate_to_postgresql.py
```

### Ejecución manual
```bash
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Endpoints

### Registro de Usuario
```http
POST /api/auth/register
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "password": "mipassword123"
}
```

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com"
  }
}
```

### Login de Usuario
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "juan@ejemplo.com",
  "password": "mipassword123"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "nombre": "Juan Pérez",
      "email": "juan@ejemplo.com"
    }
  }
}
```

### Obtener Visitas del Usuario (con Sistema de Rondas)
```http
GET /api/user/visits
Authorization: Bearer <token>
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": {
    "data": [
      {
        "business_id": 2,
        "visit_month": "2024-11",
        "business_name": "Café Vanilla",
        "visit_count": 6,
        "round_number": 1,
        "progress_in_round": 6,
        "max_visits_per_round": 6,
        "is_reward_claimed": false,
        "last_visit_date": "2024-11-29T13:33:00",
        "latest_visit_id": 27
      }
    ],
    "total_visits": 6
  }
}
```

### Reclamar Premio (Completa Ronda)
```http
POST /api/rewards/{coupon_id}/claim
Authorization: Bearer <token>
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Premio reclamado exitosamente. Nueva ronda iniciada.",
  "data": {
    "round_completed": 1,
    "new_round_started": 2
  }
}
```

## 🏗️ Arquitectura del Proyecto

```
Python/
├── app/
│   ├── config/          # Configuración y base de datos
│   │   ├── settings.py  # Variables de entorno
│   │   └── database.py  # Conexión MySQL
│   ├── models/          # Modelos de datos
│   │   ├── user.py      # Modelo Usuario
│   │   ├── business.py  # Modelo Negocio
│   │   ├── user_visit.py # Modelo Visitas
│   │   ├── user_round.py # Modelo Rondas (NUEVO)
│   │   └── user_reward.py # Modelo Premios
│   ├── schemas/         # Validaciones Pydantic
│   │   ├── auth.py      # Schemas de autenticación
│   │   ├── user.py      # Schemas de usuario
│   │   └── reward.py    # Schemas de premios
│   ├── services/        # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── reward_service.py
│   ├── controllers/     # Controladores
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   └── reward_controller.py
│   ├── routes/          # Rutas de la API
│   │   ├── auth.py      # Rutas de autenticación
│   │   ├── user.py      # Rutas de usuario
│   │   └── rewards.py   # Rutas de premios
│   └── utils/           # Utilidades
│       ├── auth_middleware.py
│       └── logger.py
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
├── .env.example         # Ejemplo de variables de entorno
└── README.md           # Documentación
```

## 🎯 Sistema de Rondas

El sistema de lealtad ahora soporta **rondas** para un mejor seguimiento:

### Características:
- **Rondas automáticas**: Cada negocio define un máximo de visitas por ronda
- **Progreso en tiempo real**: Seguimiento del progreso actual en la ronda
- **Completado automático**: Al reclamar un premio, se completa la ronda y se inicia una nueva
- **Migración suave**: Los usuarios existentes se migran automáticamente
- **Concurrencia segura**: Previene reclamaciones duplicadas

### Flujo de Rondas:
1. Usuario visita negocio → `progress_in_round++`
2. Alcanza meta → Se genera cupón automáticamente
3. Usuario reclama premio → Ronda se marca como completada
4. Sistema inicia nueva ronda automáticamente (`round_number++`, `progress_in_round = 0`)

### Base de Datos:
```sql
CREATE TABLE user_rounds (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    business_id BIGINT NOT NULL REFERENCES businesses(id),
    round_number INTEGER NOT NULL DEFAULT 1,
    progress_in_round INTEGER NOT NULL DEFAULT 0,
    round_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    is_reward_claimed BOOLEAN NOT NULL DEFAULT FALSE,
    last_visit_id BIGINT NULL
);
```

## 🔒 Seguridad

- Contraseñas encriptadas con bcrypt (12 salt rounds)
- JWT tokens con expiración de 24 horas
- Validación de email único en registro
- Variables sensibles en archivo .env
- Conexión segura SSL con PostgreSQL/Supabase
- Nunca se expone la contraseña en respuestas

## ⚠️ Códigos de Error

- **400**: Datos inválidos o email ya registrado
- **401**: Credenciales incorrectas
- **422**: Error de validación de campos
- **500**: Error interno del servidor

## 🧪 Pruebas con cURL

### Registro:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Test User",
       "email": "test@ejemplo.com",
       "password": "password123"
     }'
```

### Login:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@ejemplo.com",
       "password": "password123"
     }'
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.