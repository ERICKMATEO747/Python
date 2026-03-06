## 🍽️ MENÚS COMPLETOS PARA DEMO

### 📋 **Menús por Negocio:**

**1. Restaurante El Totonaco (ID: 1)**
- **Platillos Principales:** Mole Poblano ($180), Chiles en Nogada ($220), Pescado a la Veracruzana ($250)
- **Bebidas:** Agua de Jamaica ($35), Cerveza Nacional ($45)

**2. Café Vanilla (ID: 2)**
- **Cafés Especiales:** Café Vanilla Latte ($65), Cappuccino ($55), Americano ($40)
- **Postres:** Cheesecake de Vainilla ($85), Brownie ($70)

**3. Pizzería Don Juan (ID: 3)**
- **Pizzas Artesanales:** Pizza Margherita ($180), Pizza Pepperoni ($220), Pizza Hawaiana ($200)
- **Bebidas:** Refresco ($35)

**4. Tacos El Buen Sabor (ID: 4)**
- **Tacos:** Pastor ($15), Carnitas ($18), Pollo ($16)
- **Quesadillas:** Queso ($45), Pastor ($55)

**5. Heladería Tropical (ID: 5)**
- **Helados Artesanales:** Mango ($35), Coco ($40), Fresa ($38)
- **Paletas:** Limón ($25), Tamarindo ($28)

**6. Panadería La Espiga (ID: 6)**
- **Pan Dulce:** Conchas ($12), Cuernitos ($15), Orejas ($18)
- **Pasteles:** Tres Leches ($85), Chocolate ($90)

### 🖼️ **Imágenes Actualizadas:**
- Todas las imágenes son de Unsplash (libres de derechos)
- Imágenes específicas para cada tipo de comida
- URLs optimizadas para web (300px)

### 🧪 **Para probar todos los menús:**
```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "juan@cliente.com", "password": "password"}'

# Menú Restaurante
curl -X GET "http://localhost:8000/api/menu/1" \
     -H "Authorization: Bearer <token>"

# Menú Café
curl -X GET "http://localhost:8000/api/menu/2" \
     -H "Authorization: Bearer <token>"

# Menú Pizzería
curl -X GET "http://localhost:8000/api/menu/3" \
     -H "Authorization: Bearer <token>"

# Menú Tacos
curl -X GET "http://localhost:8000/api/menu/4" \
     -H "Authorization: Bearer <token>"

# Menú Heladería
curl -X GET "http://localhost:8000/api/menu/5" \
     -H "Authorization: Bearer <token>"

# Menú Panadería
curl -X GET "http://localhost:8000/api/menu/6" \
     -H "Authorization: Bearer <token>"
```

### 🎯 **Características de la Demo:**
- ✅ 6 negocios con menús únicos
- ✅ 2-3 categorías por negocio
- ✅ 3-5 productos por categoría
- ✅ Precios realistas mexicanos
- ✅ Descripciones atractivas
- ✅ Imágenes profesionales variadas

**¡Demo completa con menús detallados para presentar al cliente!**