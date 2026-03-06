## ✅ MENÚS Y IMÁGENES COMPLETADOS

### 🍽️ **Menús cargados en todos los negocios:**

**1. Restaurante El Totonaco (ID: 1)**
- Platillos Principales: Mole Poblano, Chiles en Nogada, Pescado a la Veracruzana
- Bebidas: Agua de Jamaica, Cerveza Nacional

**2. Café Vanilla (ID: 2)**
- Cafés Especiales: Café Vanilla Latte, Cappuccino, Americano
- Postres: Cheesecake de Vainilla, Brownie

**3. Pizzería Don Juan (ID: 3)**
- Pizzas Artesanales: Margherita, Pepperoni, Hawaiana
- Bebidas: Refresco

**4. Tacos El Buen Sabor (ID: 4)**
- Tacos: Pastor, Carnitas, Pollo
- Quesadillas: Queso, Pastor

**5. Heladería Tropical (ID: 5)**
- Helados Artesanales: Mango, Coco, Fresa
- Paletas: Limón, Tamarindo

**6. Panadería La Espiga (ID: 6)**
- Pan Dulce: Conchas, Cuernitos, Orejas
- Pasteles: Tres Leches, Chocolate

### 🖼️ **Imágenes principales actualizadas:**

Cada negocio ahora tiene:
- ✅ **logo:** URL de imagen para logo (400px)
- ✅ **image_url:** URL de imagen principal (200px)

**URLs de imágenes por negocio:**
- **Restaurante:** https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=200
- **Café:** https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=200
- **Pizzería:** https://images.unsplash.com/photo-1513104890138-7c749659a591?w=200
- **Tacos:** https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=200
- **Heladería:** https://images.unsplash.com/photo-1488900128323-21503983a07e?w=200
- **Panadería:** https://images.unsplash.com/photo-1509440159596-0249088772ff?w=200

### 🧪 **Para probar menús completos:**
```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "juan@cliente.com", "password": "password"}'

# Ver menú completo de cualquier negocio (1-6)
curl -X GET "http://localhost:8000/api/menu/1" \
     -H "Authorization: Bearer <token>"

# Ver negocios con imágenes
curl -X GET "http://localhost:8000/api/businesses" \
     -H "Authorization: Bearer <token>"
```

### 📊 **Respuesta de negocio con imagen:**
```json
{
  "id": 2,
  "name": "Café Vanilla",
  "logo": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400",
  "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=200",
  "description": "Café de especialidad y vainilla de la región"
}
```

**¡Todos los negocios tienen menús completos e imágenes profesionales desde URLs!**