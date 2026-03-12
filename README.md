# 🚀 Flevo Backend - API REST

API REST para sistema de lealtad con autenticación, construida con FastAPI y PostgreSQL.

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar Automáticamente

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### 2️⃣ Configurar (Opcional)

El proyecto funciona sin configuración para desarrollo local. Para producción:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edita `.env` con tus valores reales.

### 3️⃣ Ejecutar

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**O manualmente:**
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Ejecutar
python main.py
```

## 🌐 Acceder a la API

- **API**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📋 Requisitos

- **Python 3.8+** ([Descargar](https://www.python.org/downloads/))
- **PostgreSQL** (Supabase recomendado) - Opcional para desarrollo
- **Git** (opcional)

---

## 🚨 Solución de Errores Comunes

### ❌ Error: "Field required [type=missing]"

**Causa:** Falta el archivo `.env`

**Solución Rápida:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Luego ejecuta: `python main.py`

### ❌ Error: "Port 8000 already in use"

**Solución:**
```bash
# Windows
kill_port_8000.bat

# Linux/Mac
./kill_port_8000.sh
```

### ❌ Error: "No module named 'app'"

**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd Python

# Activa el entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 📖 Más soluciones

Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para más errores comunes.

---

## 🎯 Características

### Autenticación y Usuarios
- ✅ Registro con validación de email/teléfono único
- ✅ Login con JWT tokens (24h expiración)
- ✅ Encriptación bcrypt (12 salt rounds)
- ✅ Middleware de autenticación
- ✅ Rate limiting

### Sistema de Lealtad
- ✅ Sistema de rondas por negocio
- ✅ Seguimiento automático de progreso
- ✅ Generación automática de cupones
- ✅ Códigos QR para registro de visitas
- ✅ Dashboard para negocios

### Notificaciones
- ✅ Push Notifications (VAPID)
- ✅ WebSockets en tiempo real
- ✅ Notificaciones por email

### Infraestructura
- ✅ PostgreSQL con Supabase
- ✅ Arquitectura modular (MVC)
- ✅ Documentación automática (Swagger)
- ✅ Logging y auditoría
- ✅ Manejo robusto de errores

---

## 📁 Estructura del Proyecto

```
Python/
├── app/
│   ├── config/              # Configuración
│   │   ├── settings.py      # Variables de entorno
│   │   └── database.py      # Conexión PostgreSQL
│   ├── models/              # Modelos de datos
│   ├── schemas/             # Validaciones Pydantic
│   ├── services/            # Lógica de negocio
│   ├── controllers/         # Controladores
│   ├── routes/              # Rutas de la API
│   └── utils/               # Utilidades
├── main.py                  # Punto de entrada
├── requirements.txt         # Dependencias
├── .env.example             # Ejemplo de configuración
├── install.bat/sh           # Instalador automático
├── start.bat/sh             # Iniciador rápido
└── README.md                # Esta documentación
```

---

## 🔗 Endpoints Principales

### Autenticación

**Registro:**
```http
POST /api/auth/register
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "telefono": "8091234567",
  "password": "mipassword123"
}
```

**Login:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "juan@ejemplo.com",
  "password": "mipassword123"
}
```

### Negocios

```http
GET /api/businesses
Authorization: Bearer <token>
```

### Visitas del Usuario

```http
GET /api/user/visits
Authorization: Bearer <token>
```

### Dashboard de Negocio

```http
GET /api/business/{business_id}/dashboard
Authorization: Bearer <token>
```

**Ver documentación completa en:** http://localhost:8000/docs

---

## ⚙️ Configuración Avanzada

### Variables de Entorno (.env)

```env
# Base de Datos (Requerido para producción)
DATABASE_URL=postgresql://user:password@host:5432/database

# JWT (Requerido para producción)
JWT_SECRET_KEY=tu-clave-secreta-muy-segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# VAPID para Push Notifications (Opcional)
VAPID_PUBLIC_KEY=tu_clave_publica
VAPID_PRIVATE_KEY=tu_clave_privada
VAPID_SUBJECT=mailto:tu-email@example.com

# Email SMTP (Opcional)
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
```

### Generar Claves Seguras

**JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**VAPID Keys:**
```bash
python -c "from pywebpush import webpush; import json; print(json.dumps(webpush.generate_vapid_keys(), indent=2))"
```

---

## 🔒 Seguridad

- 🔐 Contraseñas hasheadas con bcrypt
- 🎫 JWT tokens con expiración
- 🛡️ Validación de datos con Pydantic
- 🔒 SSL/TLS para PostgreSQL
- 🚫 Rate limiting en endpoints sensibles
- 📝 Logging de auditoría

---

## 🧪 Testing

### Con cURL

**Registro:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","email":"test@test.com","password":"test123"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### Con Swagger UI

Visita http://localhost:8000/docs para probar todos los endpoints interactivamente.

---

## 🛠️ Scripts Útiles

| Script | Descripción |
|--------|-------------|
| `install.bat/sh` | Instalación automática completa |
| `start.bat/sh` | Inicia el servidor con verificaciones |
| `kill_port_8000.bat/sh` | Libera el puerto 8000 |
| `verify_config.py` | Verifica configuración |
| `setup.py` | Setup interactivo |

---

## 📚 Documentación Adicional

- [INSTALL.md](INSTALL.md) - Guía de instalación detallada
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas
- [Swagger UI](http://localhost:8000/docs) - Documentación interactiva de API

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'feat: nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📞 Soporte

¿Problemas? Revisa:
1. [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Ejecuta: `python verify_config.py`
3. Revisa los logs del servidor

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 🎉 ¡Listo!

Tu servidor debería estar corriendo en http://localhost:8000

**Próximos pasos:**
1. ✅ Visita http://localhost:8000/docs
2. ✅ Prueba el endpoint de registro
3. ✅ Configura tu base de datos en `.env`
4. ✅ Despliega a producción
