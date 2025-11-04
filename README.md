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

## 📋 Requisitos Previos

- Python 3.8+
- MySQL 5.7+ o MariaDB
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

### 4. Configurar base de datos MySQL

Crear base de datos:
```sql
CREATE DATABASE auth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo:
```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:
```env
DATABASE_URL=mysql+pymysql://root:tu_password@localhost:3306/auth_db
JWT_SECRET_KEY=tu-clave-secreta-jwt-muy-segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
```

## 🚀 Ejecutar la aplicación

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

## 🏗️ Arquitectura del Proyecto

```
Python/
├── app/
│   ├── config/          # Configuración y base de datos
│   │   ├── settings.py  # Variables de entorno
│   │   └── database.py  # Conexión MySQL
│   ├── models/          # Modelos de datos
│   │   └── user.py      # Modelo Usuario
│   ├── schemas/         # Validaciones Pydantic
│   │   └── auth.py      # Schemas de autenticación
│   ├── services/        # Lógica de negocio
│   │   └── auth_service.py
│   ├── controllers/     # Controladores
│   │   └── auth_controller.py
│   └── routes/          # Rutas de la API
│       └── auth.py      # Rutas de autenticación
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
├── .env.example         # Ejemplo de variables de entorno
└── README.md           # Documentación
```

## 🔒 Seguridad

- Contraseñas encriptadas con bcrypt (12 salt rounds)
- JWT tokens con expiración de 24 horas
- Validación de email único en registro
- Variables sensibles en archivo .env
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