# 🚀 Guía de Instalación - Flevo Backend

Esta guía te ayudará a configurar el proyecto en cualquier equipo de forma rápida y sencilla.

## 📋 Requisitos Previos

- **Python 3.8+** ([Descargar](https://www.python.org/downloads/))
- **PostgreSQL** (Supabase recomendado)
- **Git** (opcional)

## 🛠️ Instalación Automática (Recomendado)

### Windows
```bash
# Ejecutar instalador automático
install.bat
```

### Linux/Mac
```bash
# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar instalador
./install.sh
```

## 🔧 Instalación Manual

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Python
```

### 2. Crear entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
```

### 5. Configurar Base de Datos

Edita el archivo `.env` con tu conexión a PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

**Ejemplo con Supabase:**
```env
DATABASE_URL=postgresql://postgres.xxx:password@aws-1-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require
```

### 6. Generar claves VAPID (Push Notifications)

```bash
# Activar entorno virtual primero
python -c "from pywebpush import webpush; import json; print(json.dumps(webpush.generate_vapid_keys(), indent=2))"
```

Copia las claves generadas a tu archivo `.env`:
```env
VAPID_PRIVATE_KEY=tu_clave_privada
VAPID_PUBLIC_KEY=tu_clave_publica
VAPID_SUBJECT=mailto:tu-email@example.com
```

### 7. Configurar JWT Secret

Genera una clave secreta segura:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Agrégala al `.env`:
```env
JWT_SECRET_KEY=tu_clave_secreta_generada
```

## 🚀 Ejecutar el Servidor

### Desarrollo
```bash
# Activar entorno virtual
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Ejecutar servidor
python main.py
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Verificar Instalación

1. **Servidor corriendo:**
   ```
   http://localhost:8000
   ```

2. **Documentación API:**
   ```
   http://localhost:8000/docs
   ```

3. **Health Check:**
   ```bash
   curl http://localhost:8000/
   ```

## 🔍 Solución de Problemas

### Error: "No module named 'app'"
```bash
# Asegúrate de estar en el directorio correcto
cd Python

# Verifica que el entorno virtual esté activado
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

### Error: "Connection refused" (Base de datos)
```bash
# Verifica tu DATABASE_URL en .env
# Asegúrate de que PostgreSQL esté corriendo
# Verifica credenciales y permisos
```

### Error: "ModuleNotFoundError: No module named 'psycopg2'"
```bash
# Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### Error: "VAPID keys not configured"
```bash
# Genera claves VAPID
python -c "from pywebpush import webpush; import json; print(json.dumps(webpush.generate_vapid_keys(), indent=2))"

# Agrégalas a .env
```

## 📦 Dependencias Principales

- **FastAPI**: Framework web
- **Uvicorn**: Servidor ASGI
- **psycopg2-binary**: Driver PostgreSQL
- **python-jose**: JWT tokens
- **bcrypt**: Encriptación de contraseñas
- **pywebpush**: Push notifications
- **python-socketio**: WebSockets en tiempo real
- **qrcode**: Generación de códigos QR

## 🔐 Variables de Entorno Requeridas

```env
# Base de datos
DATABASE_URL=postgresql://...

# JWT
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# VAPID (Push Notifications)
VAPID_PRIVATE_KEY=...
VAPID_PUBLIC_KEY=...
VAPID_SUBJECT=mailto:...

# Servidor
HOST=0.0.0.0
PORT=8000
```

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. Verifica que Python 3.8+ esté instalado
2. Asegúrate de que todas las dependencias estén instaladas
3. Verifica que el archivo `.env` esté configurado correctamente
4. Revisa los logs del servidor para errores específicos

## 🎯 Próximos Pasos

1. ✅ Instalar dependencias
2. ✅ Configurar variables de entorno
3. ✅ Ejecutar servidor
4. 📱 Configurar frontend
5. 🧪 Probar endpoints en `/docs`
6. 🚀 Desplegar a producción

---

**¡Listo para desarrollar! 🎉**
