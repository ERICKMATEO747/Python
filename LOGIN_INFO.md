## USUARIOS DE PRUEBA - AUTH API

### ✅ PostgreSQL NO está instalado localmente
**Solución:** Usar SQLite (base de datos local simple)

### 👥 Usuarios Creados Automáticamente

**Credenciales de Login:**
- **admin@test.com** / **123456**
- **negocio@test.com** / **123456** 
- **cliente@test.com** / **123456**

### 🧪 Comandos de Prueba

**1. Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@test.com", "password": "123456"}'
```

**2. Registro:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Nuevo Usuario", "email": "nuevo@test.com", "password": "123456", "user_type_hash": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"}'
```

### 📋 Hashes de Tipo de Usuario
- **Cliente:** `a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456`
- **Negocio:** `b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1`

### 🔧 Estado Actual
- ✅ Servidor corriendo en puerto 8000
- ✅ SQLite configurado como base de datos
- ✅ Usuarios de prueba creados automáticamente
- ⚠️ Si hay errores, reiniciar el servidor: `python main.py`