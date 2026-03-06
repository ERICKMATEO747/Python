## 🎯 DEMO COMPLETA - AUTH API

### 👥 USUARIOS PARA DEMO

| Email | Contraseña | Tipo | Descripción |
|-------|------------|------|-------------|
| **juan@cliente.com** | **password** | Cliente | Cliente activo con 12 visitas |
| **maria@cliente.com** | **password** | Cliente | Cliente moderado con 6 visitas |
| **carlos@negocio.com** | **password** | Negocio | Propietario de negocio |
| **ana@negocio.com** | **password** | Negocio | Propietario de negocio |
| **admin@sistema.com** | **password** | Admin | Administrador del sistema |
| **pedro@cliente.com** | **password** | Cliente | Cliente nuevo con 3 visitas |
| **sofia@cliente.com** | **password** | Cliente | Cliente sin visitas |

### 🏪 NEGOCIOS EN LA DEMO

1. **Restaurante El Totonaco** - Comida tradicional veracruzana (6 visitas para premio)
2. **Café Vanilla** - Café de especialidad (8 visitas para premio)
3. **Pizzería Don Juan** - Pizzas artesanales (5 visitas para premio)
4. **Tacos El Buen Sabor** - Comida rápida (10 visitas para premio)
5. **Heladería Tropical** - Helados artesanales (7 visitas para premio)
6. **Panadería La Espiga** - Pan y repostería (12 visitas para premio)

### 🌍 MUNICIPIOS

- Papantla, Veracruz
- Coatzintla, Veracruz
- Poza Rica, Veracruz
- Tuxpan, Veracruz
- Xalapa, Veracruz

### 🧪 COMANDOS DE PRUEBA

**1. Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "juan@cliente.com", "password": "password"}'
```

**2. Ver negocios:**
```bash
curl -X GET "http://localhost:8000/api/businesses" \
     -H "Authorization: Bearer <token>"
```

**3. Ver municipios:**
```bash
curl -X GET "http://localhost:8000/api/municipalities" \
     -H "Authorization: Bearer <token>"
```

**4. Ver visitas del usuario:**
```bash
curl -X GET "http://localhost:8000/api/user/visits" \
     -H "Authorization: Bearer <token>"
```

**5. Ver perfil del usuario:**
```bash
curl -X GET "http://localhost:8000/api/user/profile" \
     -H "Authorization: Bearer <token>"
```

### 📊 DATOS DE DEMO INCLUIDOS

- ✅ **21 visitas** distribuidas entre usuarios
- ✅ **7 rondas de lealtad** en progreso
- ✅ **3 cupones/recompensas** generados
- ✅ **Historial de 3 meses** de actividad
- ✅ **Diferentes niveles** de actividad por usuario

### 🎯 ESCENARIOS DE DEMO

**Cliente Activo (Juan):**
- 6 visitas completadas en Restaurante El Totonaco (1 ronda completa + premio reclamado)
- 3 visitas en Café Vanilla (progreso en ronda actual)
- 2 visitas en Pizzería Don Juan (progreso en ronda actual)

**Cliente Moderado (María):**
- 3 visitas en Café Vanilla
- 2 visitas en Tacos El Buen Sabor
- 1 visita en Heladería Tropical

**Cliente Nuevo (Pedro):**
- 2 visitas en Restaurante El Totonaco
- 1 visita en Pizzería Don Juan

### 🚀 PARA INICIAR DEMO

1. **Ejecutar servidor:**
   ```bash
   python main.py
   ```

2. **Acceder a documentación:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Hacer login con cualquier usuario**

4. **Probar endpoints con token JWT**

**¡La demo está lista para presentar al cliente!**