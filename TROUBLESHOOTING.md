# 🚨 Solución Rápida de Errores Comunes

## ❌ Error: "Field required [type=missing, input_value={}, input_type=dict]"

### Causa:
Faltan variables de entorno requeridas en el archivo `.env`

### Solución:

**1. Verifica que existe el archivo .env:**
```bash
# Windows
dir .env

# Linux/Mac
ls -la .env
```

**2. Si NO existe, créalo desde el ejemplo:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**3. Edita el archivo .env y agrega las variables REQUERIDAS:**

```env
# REQUERIDO: Conexión a PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/database

# REQUERIDO: Clave secreta para JWT
JWT_SECRET_KEY=tu-clave-secreta-muy-segura-cambiala
```

**4. Genera una clave JWT segura:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**5. Verifica la configuración:**
```bash
python verify_config.py
```

---

## ❌ Error: "error while attempting to bind on address (0.0.0.0, 8000)"

### Causa:
El puerto 8000 ya está en uso

### Solución:

**Windows:**
```bash
# Opción 1: Usar script
kill_port_8000.bat

# Opción 2: Manual
netstat -ano | findstr :8000
taskkill /PID [número_pid] /F
```

**Linux/Mac:**
```bash
# Opción 1: Usar script
./kill_port_8000.sh

# Opción 2: Manual
lsof -ti:8000 | xargs kill -9
```

---

## ❌ Error: "No module named 'app'"

### Causa:
No estás en el directorio correcto o el entorno virtual no está activado

### Solución:

```bash
# 1. Ve al directorio del proyecto
cd Python

# 2. Activa el entorno virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 3. Ejecuta el servidor
python main.py
```

---

## ❌ Error: "Connection refused" (Base de datos)

### Causa:
No se puede conectar a PostgreSQL

### Solución:

**1. Verifica tu DATABASE_URL en .env:**
```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

**2. Verifica que PostgreSQL esté corriendo**

**3. Prueba la conexión:**
```bash
python verify_config.py
```

**4. Si usas Supabase, verifica:**
- URL correcta
- Credenciales válidas
- Conexión a internet

---

## ❌ Error: "ModuleNotFoundError: No module named 'psycopg2'"

### Causa:
Dependencias no instaladas

### Solución:

```bash
# Activa el entorno virtual primero
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstala dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ❌ Error: "VAPID keys not configured"

### Causa:
Faltan claves VAPID para push notifications

### Solución:

**1. Genera claves VAPID:**
```bash
python -c "from pywebpush import webpush; import json; print(json.dumps(webpush.generate_vapid_keys(), indent=2))"
```

**2. Agrega las claves a .env:**
```env
VAPID_PRIVATE_KEY=tu_clave_privada_generada
VAPID_PUBLIC_KEY=tu_clave_publica_generada
VAPID_SUBJECT=mailto:tu-email@example.com
```

---

## 🔍 Verificación General

**Ejecuta el script de verificación:**
```bash
python verify_config.py
```

Este script verificará:
- ✅ Archivo .env existe
- ✅ Variables requeridas configuradas
- ✅ Conexión a base de datos
- ⚠️ Variables opcionales

---

## 📞 Checklist Antes de Ejecutar

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado (`venv/`)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` existe
- [ ] `DATABASE_URL` configurado
- [ ] `JWT_SECRET_KEY` configurado
- [ ] Puerto 8000 libre
- [ ] PostgreSQL accesible

---

## 🚀 Comando Completo de Inicio

```bash
# 1. Activar entorno virtual
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 2. Verificar configuración
python verify_config.py

# 3. Ejecutar servidor
python main.py
```

---

## 💡 Instalación Limpia

Si nada funciona, reinstala desde cero:

```bash
# 1. Eliminar entorno virtual
# Windows: rmdir /s /q venv
# Linux/Mac: rm -rf venv

# 2. Ejecutar instalador automático
# Windows: install.bat
# Linux/Mac: ./install.sh

# 3. Configurar .env
# Edita el archivo .env con tus valores

# 4. Verificar
python verify_config.py

# 5. Ejecutar
python main.py
```
