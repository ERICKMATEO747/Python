# Usuarios de Ejemplo para Negocios - Auth API

## 🏪 Credenciales de Acceso para Negocios

### 1. Restaurante El Totonaco
- **Nombre:** Carlos Hernández
- **Email:** carlos@eltotonaco.com
- **Teléfono:** 7841234567
- **Contraseña:** negocio123
- **Tipo:** Propietario de Negocio
- **Negocio:** Restaurante El Totonaco

### 2. Café Vanilla
- **Nombre:** María González
- **Email:** maria@cafevanilla.com
- **Teléfono:** 7822345678
- **Contraseña:** negocio123
- **Tipo:** Propietario de Negocio
- **Negocio:** Café Vanilla

### 3. Usuario Administrador de Negocio
- **Nombre:** Admin Negocio
- **Email:** admin@negocio.com
- **Teléfono:** 7841111111
- **Contraseña:** negocio123
- **Tipo:** Propietario de Negocio
- **Negocio:** Sin asignar (puede gestionar cualquier negocio)

## 🔧 Cómo usar estos usuarios

### Para Login via API:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "carlos@eltotonaco.com",
       "password": "negocio123"
     }'
```

### Para Login via Teléfono:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "telefono": "7841234567",
       "password": "negocio123"
     }'
```

## 📋 Funcionalidades Disponibles

Con estos usuarios puedes:

1. **Acceder al Portal de Negocios**
   - Gestionar perfil del negocio
   - Actualizar información de contacto
   - Configurar horarios y días de trabajo

2. **Gestionar Menús y Productos**
   - Crear categorías de productos
   - Agregar/editar/eliminar productos
   - Configurar precios y descripciones

3. **Ver Estadísticas**
   - Número de visitas por mes
   - Usuarios más frecuentes
   - Cupones generados y reclamados

4. **Administrar Recompensas**
   - Configurar número de visitas para premio
   - Ver cupones pendientes
   - Gestionar reclamaciones

## 🚨 Problema Actual

**Error de Conexión a Base de Datos:**
```
FATAL: Tenant or user not found
```

### Soluciones:

1. **Verificar credenciales de Supabase:**
   - Revisa que la URL de Supabase sea correcta
   - Verifica que las claves API sean válidas
   - Confirma que el proyecto de Supabase esté activo

2. **Actualizar archivo .env:**
   ```env
   DATABASE_URL=postgresql://[usuario]:[password]@[host]:[puerto]/[database]
   SUPABASE_URL=https://[tu-proyecto].supabase.co
   SUPABASE_ANON_KEY=[tu-clave-anon]
   SUPABASE_SERVICE_ROLE_KEY=[tu-clave-service-role]
   ```

3. **Ejecutar migración:**
   ```bash
   python migrate_simple.py
   python create_business_users.py
   ```

## 🔄 Pasos para Solucionar

1. **Crear nuevo proyecto en Supabase** (si es necesario)
2. **Actualizar credenciales en .env**
3. **Ejecutar migración:** `python migrate_simple.py`
4. **Crear usuarios:** `python create_business_users.py`
5. **Iniciar servidor:** `python main.py`

## 📞 Usuarios de Prueba Adicionales

Si necesitas más usuarios, puedes crear con este patrón:

```python
# Ejemplo de usuario adicional
{
    'nombre': 'Juan Pérez',
    'email': 'juan@pizzeria.com',
    'telefono': '7843333333',
    'password': 'negocio123',  # Siempre usar bcrypt
    'user_type_id': 2,  # Tipo negocio
    'business_name': 'Pizzería Don Juan'
}
```

---

**Nota:** Una vez que soluciones la conexión a la base de datos, estos usuarios se crearán automáticamente y podrás usarlos para probar todas las funcionalidades del sistema.