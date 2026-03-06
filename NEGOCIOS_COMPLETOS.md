## ✅ INFORMACIÓN COMPLETA AGREGADA A NEGOCIOS

### 📱 **Redes Sociales y Contacto:**

**1. Restaurante El Totonaco**
- Facebook: https://facebook.com/eltotonaco
- Instagram: https://instagram.com/eltotonaco
- WhatsApp: 7841234567

**2. Café Vanilla**
- Facebook: https://facebook.com/cafevanilla
- Instagram: https://instagram.com/cafevanilla
- WhatsApp: 7822345678

**3. Pizzería Don Juan**
- Facebook: https://facebook.com/pizzeriadonjuan
- Instagram: https://instagram.com/pizzeriadonjuan
- WhatsApp: 7843333333

**4. Tacos El Buen Sabor**
- Facebook: https://facebook.com/tacosbuensabor
- Instagram: https://instagram.com/tacosbuensabor
- WhatsApp: 7844444444

**5. Heladería Tropical**
- Facebook: https://facebook.com/heladeria.tropical
- Instagram: https://instagram.com/heladeria.tropical
- WhatsApp: 7845555555

**6. Panadería La Espiga**
- Facebook: https://facebook.com/panaderiaespiga
- Instagram: https://instagram.com/panaderiaespiga
- WhatsApp: 7846666666

### 📊 **Información Completa por Negocio:**

Cada negocio ahora incluye:
- ✅ **Nombre y categoría**
- ✅ **Dirección completa**
- ✅ **Municipio (Veracruz)**
- ✅ **Teléfono y email**
- ✅ **Logo profesional (Unsplash)**
- ✅ **Descripción atractiva**
- ✅ **Rating realista (4.2-4.7)**
- ✅ **Visitas para premio (5-12)**
- ✅ **Facebook, Instagram, WhatsApp**
- ✅ **Estado activo**
- ✅ **Fecha de creación**

### 🧪 **Para probar información completa:**
```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "juan@cliente.com", "password": "password"}'

# Ver todos los negocios con información completa
curl -X GET "http://localhost:8000/api/businesses" \
     -H "Authorization: Bearer <token>"

# Ver negocio específico
curl -X GET "http://localhost:8000/api/businesses/2" \
     -H "Authorization: Bearer <token>"
```

### 📋 **Respuesta esperada (ejemplo Café Vanilla):**
```json
{
  "id": 2,
  "name": "Café Vanilla",
  "category": "Cafetería",
  "address": "Av. 20 de Noviembre 45",
  "municipality_id": 2,
  "municipio": "Coatzintla",
  "phone": "7822345678",
  "email": "info@cafevanilla.com",
  "logo": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400",
  "description": "Café de especialidad y vainilla de la región",
  "rating": 4.2,
  "visits_for_prize": 8,
  "facebook": "https://facebook.com/cafevanilla",
  "instagram": "https://instagram.com/cafevanilla",
  "whatsapp": "7822345678",
  "active": 1,
  "created_at": "2026-03-06 19:27:25",
  "unclaimed_coupons": 0
}
```

**¡Negocios con información completa y profesional para demo!**