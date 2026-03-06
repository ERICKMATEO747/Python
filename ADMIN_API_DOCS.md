# API de Administrador - Documentación Frontend

## 🔐 Autenticación

**Todas las rutas requieren autenticación JWT con permisos de administrador (user_type = 3)**

```bash
Authorization: Bearer <jwt_token>
```

### Login de Administrador
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@flevoapp.com",
  "password": "Admin123!"
}
```

---

## 📊 Dashboard

### GET /api/admin/dashboard
Obtiene estadísticas generales del sistema con filtros opcionales.

**Query Parameters:**
- `start_date` (opcional): Fecha inicio (YYYY-MM-DD)
- `end_date` (opcional): Fecha fin (YYYY-MM-DD)
- `municipality_id` (opcional): ID del municipio
- `category` (opcional): Categoría de negocio

**Request:**
```bash
GET /api/admin/dashboard?start_date=2024-01-01&end_date=2024-12-31
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_users": 150,
    "total_businesses": 25,
    "total_coupons": 300,
    "coupons_by_status": {
      "vigente": 120,
      "reclamado": 80,
      "usado": 90,
      "expirado": 10
    },
    "businesses_by_category": [
      {"category": "Restaurante", "count": 8},
      {"category": "Cafetería", "count": 5}
    ],
    "users_by_type": [
      {"type_name": "cliente", "count": 140},
      {"type_name": "negocio", "count": 8},
      {"type_name": "admin", "count": 2}
    ],
    "recent_user_registrations": [
      {"date": "2024-01-15", "count": 5},
      {"date": "2024-01-16", "count": 3}
    ],
    "payment_metrics": {
      "total_revenue_this_month": 12450.00,
      "pending_payments": 8,
      "active_subscriptions": 35,
      "trial_subscriptions": 5,
      "expired_subscriptions": 2,
      "payments_today": 3,
      "revenue_today": 897.00
    },
    "businesses_with_payment_status": [
      {
        "business_id": 2,
        "business_name": "Café Vanilla",
        "subscription_status": "active",
        "monthly_revenue": 299.00,
        "last_payment_date": "2024-02-15",
        "next_payment_due": "2024-03-15",
        "days_until_due": 28
      },
      {
        "business_id": 5,
        "business_name": "Café Central",
        "subscription_status": "pending_payment",
        "amount_due": 299.00,
        "days_overdue": 3,
        "grace_period_ends": "2024-02-22"
      }
    ]
  }
}
```

### GET /api/admin/stats
Obtiene estadísticas básicas del sistema.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_users": 150,
    "total_businesses": 25,
    "total_rewards": 300,
    "total_visits": 1200,
    "new_users_last_month": 45,
    "visits_last_month": 350
  }
}
```

---

## 🏢 Gestión de Negocios

### GET /api/admin/businesses
Obtiene todos los negocios con paginación y búsqueda.

**Query Parameters:**
- `page` (default: 1): Número de página
- `limit` (default: 20, max: 100): Elementos por página
- `search` (opcional): Búsqueda por nombre, categoría o dirección

**Request:**
```bash
GET /api/admin/businesses?page=1&limit=20&search=café
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "businesses": [
      {
        "id": 1,
        "name": "Café Central",
        "category": "Cafetería",
        "address": "Calle Principal 123",
        "municipality_id": 1,
        "municipio": "Papantla",
        "phone": "2281234567",
        "email": "info@cafecentral.com",
        "owner_name": "Juan Pérez",
        "owner_email": "juan@ejemplo.com",
        "active": true,
        "created_at": "2024-01-15T10:30:00",
        "visits_for_prize": 6
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 25,
      "pages": 2
    }
  }
}
```

### POST /api/admin/businesses
Crea un nuevo negocio.

**Request:**
```bash
POST /api/admin/businesses
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "Restaurante Nuevo",
  "category": "Restaurante",
  "address": "Av. Principal 456",
  "municipality_id": 1,
  "phone": "2281234567",
  "email": "info@restaurante.com",
  "description": "Comida tradicional mexicana",
  "owner_email": "propietario@ejemplo.com",
  "visits_for_prize": 8,
  "opening_hours": {
    "monday": "09:00-22:00",
    "tuesday": "09:00-22:00"
  },
  "working_days": ["monday", "tuesday", "wednesday"],
  "payment_methods": ["efectivo", "tarjeta"],
  "delivery_available": true,
  "facebook": "https://facebook.com/restaurante",
  "instagram": "https://instagram.com/restaurante",
  "whatsapp": "2281234567"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Negocio creado exitosamente",
  "data": {
    "id": 26,
    "name": "Restaurante Nuevo"
  }
}
```

**Errores:**
- `400`: Email del propietario no existe
- `403`: Sin permisos de administrador

### PUT /api/admin/businesses/{business_id}
Actualiza un negocio existente.

**Request:**
```bash
PUT /api/admin/businesses/1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "Café Central Renovado",
  "phone": "2289876543",
  "active": true
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Negocio actualizado exitosamente",
  "data": {
    "id": 1,
    "name": "Café Central Renovado"
  }
}
```

### DELETE /api/admin/businesses/{business_id}
Elimina (desactiva) un negocio.

**Request:**
```bash
DELETE /api/admin/businesses/1
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Negocio eliminado exitosamente"
}
```

---

## 👥 Gestión de Usuarios

### GET /api/admin/users
Obtiene todos los usuarios con paginación y filtros.

**Query Parameters:**
- `page` (default: 1): Número de página
- `limit` (default: 20, max: 100): Elementos por página
- `search` (opcional): Búsqueda por nombre o email
- `user_type` (opcional): Filtro por tipo (1=cliente, 2=negocio, 3=admin)

**Request:**
```bash
GET /api/admin/users?page=1&limit=20&user_type=1&search=juan
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@ejemplo.com",
        "telefono": "2281234567",
        "user_type_id": 1,
        "user_type_name": "cliente",
        "created_at": "2024-01-15T10:30:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "pages": 8
    }
  }
}
```

### POST /api/admin/users
Crea un nuevo usuario.

**Request:**
```bash
POST /api/admin/users
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "nombre": "María González",
  "email": "maria@ejemplo.com",
  "telefono": "2289876543",
  "password": "Password123!",
  "user_type": 2
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "id": 151,
    "nombre": "María González",
    "email": "maria@ejemplo.com",
    "user_type": 2
  }
}
```

**Errores:**
- `400`: Email o teléfono ya existe
- `400`: user_type inválido (debe ser 1, 2 o 3)

### PUT /api/admin/users/{user_id}
Actualiza un usuario existente.

**Request:**
```bash
PUT /api/admin/users/1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "nombre": "Juan Pérez Actualizado",
  "user_type": 2,
  "active": true
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Usuario actualizado exitosamente",
  "data": {
    "id": 1,
    "nombre": "Juan Pérez Actualizado"
  }
}
```

---

## 🔧 Tipos de Usuario

- **1**: Cliente (usuario final)
- **2**: Negocio (propietario de establecimiento)
- **3**: Administrador (acceso completo)

---

## 📝 Campos Requeridos

### BusinessCreate
- `name` ✅
- `category` ✅
- `address` ✅
- `municipality_id` ✅
- `phone` ✅
- `owner_email` ✅ (debe existir en la tabla users)

### UserCreate
- `nombre` ✅
- `password` ✅
- Al menos uno: `email` o `telefono`

---

## ⚠️ Códigos de Error

- **400**: Datos inválidos o duplicados
- **401**: No autenticado
- **403**: Sin permisos de administrador
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

---

## 🚀 Ejemplo de Flujo Completo

```javascript
// 1. Login como admin
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'admin@flevoapp.com',
    password: 'Admin123!'
  })
});

const { data } = await loginResponse.json();
const token = data.access_token;

// 2. Obtener dashboard
const dashboardResponse = await fetch('/api/admin/dashboard', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// 3. Crear negocio
const businessResponse = await fetch('/api/admin/businesses', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Mi Nuevo Negocio',
    category: 'Restaurante',
    address: 'Calle Principal 123',
    municipality_id: 1,
    phone: '2281234567',
    owner_email: 'propietario@ejemplo.com',
    visits_for_prize: 6
  })
});
```

---

## 📋 Credenciales de Administrador

**Email**: `admin@flevoapp.com`  
**Password**: `Admin123!`

¡La API de administrador está lista para ser implementada en el frontend!

---

## 💳 Gestión de Suscripciones y Pagos

### Estados de Suscripción
- **trial**: Periodo de prueba gratuito
- **active**: Suscripción activa y al día
- **pending_payment**: Pago pendiente (en periodo de gracia)
- **expired**: Suscripción vencida (sin acceso)

### Tipos de Plan
- **monthly**: Plan mensual (30 días)
- **bimonthly**: Plan bimestral (60 días)
- **semiannual**: Plan semestral (180 días)
- **annual**: Plan anual (365 días)

### Métodos de Pago
- **stripe**: Pasarela Stripe
- **mercadopago**: Pasarela MercadoPago
- **cash**: Efectivo (registro manual)
- **transfer**: Transferencia bancaria
- **deposit**: Depósito bancario

---

## 📋 Suscripciones

### GET /api/admin/subscriptions
Obtiene todas las suscripciones con filtros y paginación.

**Query Parameters:**
- `page` (default: 1): Número de página
- `limit` (default: 20, max: 100): Elementos por página
- `status` (opcional): Filtro por estado (trial, active, pending_payment, expired)
- `plan_type` (opcional): Filtro por tipo de plan
- `expires_soon` (opcional): true para suscripciones que vencen en 7 días
- `search` (opcional): Búsqueda por nombre de negocio

**Request:**
```bash
GET /api/admin/subscriptions?status=pending_payment&expires_soon=true
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "subscriptions": [
      {
        "id": 1,
        "business_id": 5,
        "business_name": "Café Central",
        "plan_type": "monthly",
        "status": "pending_payment",
        "start_date": "2024-01-15",
        "end_date": "2024-02-15",
        "grace_period_days": 7,
        "grace_period_end": "2024-02-22",
        "trial_days": 0,
        "monthly_price": 299.00,
        "currency": "MXN",
        "auto_renew": true,
        "payment_method": "stripe",
        "last_payment_date": "2024-01-15",
        "next_payment_due": "2024-02-15",
        "days_until_expiry": 3,
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-02-12T15:45:00"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "pages": 3
    },
    "summary": {
      "total_active": 35,
      "total_pending": 8,
      "total_expired": 2,
      "total_trial": 5,
      "revenue_this_month": 12450.00
    }
  }
}
```

### POST /api/admin/subscriptions
Crea una nueva suscripción para un negocio.

**Request:**
```bash
POST /api/admin/subscriptions
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "business_id": 5,
  "plan_type": "monthly",
  "trial_days": 15,
  "grace_period_days": 7,
  "monthly_price": 299.00,
  "currency": "MXN",
  "auto_renew": true,
  "payment_method": "stripe",
  "start_immediately": true
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Suscripción creada exitosamente",
  "data": {
    "id": 15,
    "business_id": 5,
    "status": "trial",
    "start_date": "2024-02-20",
    "end_date": "2024-03-06",
    "trial_end_date": "2024-03-06"
  }
}
```

### POST /api/admin/payments
Registra un pago manual (efectivo, transferencia, depósito).

**Request:**
```bash
POST /api/admin/payments
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "subscription_id": 1,
  "amount": 299.00,
  "currency": "MXN",
  "payment_method": "cash",
  "reference": "Efectivo recibido en oficina",
  "payment_date": "2024-02-15T10:00:00",
  "notes": "Pago realizado por el propietario Juan Pérez",
  "receipt_number": "REC-2024-0215-001"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Pago registrado exitosamente",
  "data": {
    "id": 124,
    "subscription_id": 1,
    "amount": 299.00,
    "status": "completed",
    "payment_date": "2024-02-15T10:00:00",
    "subscription_extended_until": "2024-03-17"
  }
}
```

### GET /api/admin/payments
Obtiene historial de pagos con filtros.

**Query Parameters:**
- `page` (default: 1): Número de página
- `business_id` (opcional): Filtro por negocio específico
- `payment_method` (opcional): Filtro por método de pago
- `status` (opcional): Filtro por estado (pending, completed, failed)
- `start_date` (opcional): Fecha inicio (YYYY-MM-DD)
- `end_date` (opcional): Fecha fin (YYYY-MM-DD)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "payments": [
      {
        "id": 123,
        "subscription_id": 1,
        "business_name": "Café Central",
        "amount": 299.00,
        "currency": "MXN",
        "payment_method": "stripe",
        "status": "completed",
        "transaction_id": "pi_1234567890",
        "reference": "Pago mensual Febrero 2024",
        "payment_date": "2024-02-15T14:30:00",
        "processed_by_admin_name": "Admin Sistema",
        "gateway_fee": 12.45,
        "net_amount": 286.55
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 156,
      "pages": 8
    },
    "summary": {
      "total_amount": 45670.00,
      "completed_payments": 145,
      "pending_payments": 8,
      "failed_payments": 3
    }
  }
}
```

### POST /api/admin/payment-links
Genera un link de pago para una suscripción.

**Request:**
```bash
POST /api/admin/payment-links
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "subscription_id": 1,
  "gateway": "stripe",
  "amount": 299.00,
  "currency": "MXN",
  "description": "Pago mensual - Café Central",
  "expires_in_hours": 72
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Link de pago generado exitosamente",
  "data": {
    "payment_link_id": "plink_1234567890",
    "url": "https://checkout.stripe.com/pay/cs_test_1234567890",
    "amount": 299.00,
    "currency": "MXN",
    "expires_at": "2024-02-23T14:30:00",
    "status": "active"
  }
}
```

### GET /api/admin/billing/alerts
Obtiene alertas de facturación pendientes.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "alerts": [
      {
        "id": 1,
        "type": "expiring_soon",
        "priority": "high",
        "business_name": "Café Central",
        "message": "Suscripción vence en 2 días",
        "expires_at": "2024-02-17T23:59:59",
        "action_required": "Generar recordatorio de pago",
        "created_at": "2024-02-15T08:00:00",
        "is_read": false
      }
    ],
    "summary": {
      "total_alerts": 15,
      "high_priority": 8,
      "unread": 12
    }
  }
}
```

---

## 🔧 Modelos de Base de Datos Sugeridos

### Tabla: business_subscriptions
```sql
CREATE TABLE business_subscriptions (
    id BIGSERIAL PRIMARY KEY,
    business_id BIGINT NOT NULL REFERENCES businesses(id),
    plan_type VARCHAR(20) NOT NULL, -- monthly, bimonthly, semiannual, annual
    status VARCHAR(20) NOT NULL DEFAULT 'trial', -- trial, active, pending_payment, expired
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    trial_days INTEGER DEFAULT 0,
    grace_period_days INTEGER DEFAULT 7,
    monthly_price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'MXN',
    auto_renew BOOLEAN DEFAULT true,
    payment_method VARCHAR(20), -- stripe, mercadopago, cash, transfer
    last_payment_date TIMESTAMP,
    next_payment_due DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: subscription_payments
```sql
CREATE TABLE subscription_payments (
    id BIGSERIAL PRIMARY KEY,
    subscription_id BIGINT NOT NULL REFERENCES business_subscriptions(id),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'MXN',
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed, refunded
    transaction_id VARCHAR(100),
    reference TEXT,
    payment_date TIMESTAMP,
    processed_by_admin_id BIGINT REFERENCES users(id),
    gateway_fee DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚡ Buenas Prácticas

### Para Frontend:
- **Estados Visuales**: Indicadores claros para cada estado de suscripción
- **Alertas Proactivas**: Notificaciones para vencimientos próximos
- **Confirmaciones**: Solicitar confirmación para acciones críticas
- **Validación**: Validar montos y fechas antes de enviar

### Para Backend:
- **Transacciones**: Usar transacciones de BD para operaciones críticas
- **Webhooks**: Implementar webhooks para pasarelas de pago
- **Logs**: Registrar todas las acciones administrativas
- **Seguridad**: Nunca almacenar datos de tarjetas, usar tokens

### Extensibilidad:
- **Descuentos**: Estructura preparada para códigos promocionales
- **Multi-moneda**: Soporte para múltiples monedas
- **Facturación**: Integración con sistemas de facturación
- **Analytics**: Métricas de retención y churn