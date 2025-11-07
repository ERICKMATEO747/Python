# 🔄 Guía de Migración - Sistema de Roles de Usuario

## 📋 Para Desarrolladores Nuevos

### 1. **Instalación Limpia**
```bash
# 1. Clonar repositorio
git clone <url-repositorio>
cd Python

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tus credenciales de MySQL

# 5. Crear base de datos
# En MySQL: CREATE DATABASE auth_db;

# 6. Ejecutar aplicación
python main.py
```

La aplicación creará automáticamente todas las tablas necesarias.

## 🔧 Para Desarrolladores Existentes

### 1. **Actualizar Código**
```bash
git pull origin main
pip install -r requirements.txt
```

### 2. **Migración Automática**
Al ejecutar `python main.py`, la aplicación:
- ✅ Detectará si la columna `user_type_id` existe
- ✅ La creará automáticamente si no existe
- ✅ Agregará la foreign key correspondiente
- ✅ Insertará los tipos de usuario por defecto

### 3. **Sin Intervención Manual**
No necesitas ejecutar scripts SQL manualmente. Todo es automático.

## 📊 Tipos de Usuario Disponibles

| Tipo | Hash | Descripción |
|------|------|-------------|
| cliente | `a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456` | Usuario final |
| negocio | `b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1` | Propietario de negocio |
| admin | `c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1b2` | Administrador |

## 🎯 Nuevo Formato de Registro

```json
{
  "nombre": "Juan Perez",
  "email": "juan@test.com",
  "password": "Password123",
  "user_type_hash": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"
}
```

## ⚠️ Compatibilidad

- ✅ **BD Nuevas**: Funciona perfectamente
- ✅ **BD Existentes**: Migración automática
- ✅ **Usuarios Existentes**: Se asignan como "cliente" por defecto
- ✅ **APIs Existentes**: Mantienen compatibilidad

## 🚨 Posibles Problemas

### Error: "Unknown column 'user_type_id'"
**Solución**: Reinicia la aplicación, la migración se ejecutará automáticamente.

### Error: "Tipo de usuario no válido"
**Solución**: Usa uno de los hashes válidos de la tabla anterior.

### Error de Foreign Key
**Solución**: La aplicación maneja esto automáticamente con verificaciones.

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que MySQL esté ejecutándose
2. Confirma que la base de datos `auth_db` existe
3. Revisa los logs en consola para más detalles
4. Reinicia la aplicación para forzar la migración