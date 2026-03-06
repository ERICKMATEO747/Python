# 📱 Guía de Notificaciones - Flevo Backend

## 🔐 Push Notifications (VAPID)

### Configuración
Las claves VAPID están configuradas en `.env`:
```env
VAPID_PUBLIC_KEY=BI--cuzH-KaiFo97BbTSui-A-i6mM-gX-vw63DS1LFogi-wgFFX5fbvKupbLeu7R18Di00HMSVm5bKDVulJkSCw
VAPID_PRIVATE_KEY=LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0t...
VAPID_SUBJECT=mailto:flevoapp@gmail.com
```

### Endpoints Disponibles

#### 1. Obtener Clave Pública VAPID
```http
GET /api/notifications/vapid-public-key
```
**Respuesta:**
```json
{
  "success": true,
  "public_key": "BI--cuzH-KaiFo97BbTSui-A-i6mM-gX-vw63DS1LFogi-wgFFX5fbvKupbLeu7R18Di00HMSVm5bKDVulJkSCw"
}
```

#### 2. Registrar Suscripción Push
```http
POST /api/notifications/subscribe
Authorization: Bearer <token>
Content-Type: application/json

{
  "endpoint": "https://fcm.googleapis.com/fcm/send/...",
  "keys": {
    "p256dh": "BKd...",
    "auth": "abc..."
  },
  "business_id": 2
}
```

#### 3. Notificación de Prueba
```http
POST /api/notifications/test
Authorization: Bearer <token>
```

### Notificaciones Automáticas
El sistema envía automáticamente:
- ✅ **Visita registrada**: Al escanear QR exitosamente
- 🎉 **Premio ganado**: Al completar ronda
- 🔄 **Nueva ronda**: Al reclamar premio
- 📍 **Recordatorios**: Programados

## 🔌 WebSockets

### Conexión
```javascript
const socket = io('ws://localhost:8000/ws', {
  auth: {
    token: 'jwt_token_here'
  }
});
```

### Eventos del Cliente

#### Conectar App de Usuario
```javascript
socket.emit('connect_customer_app', {});
```

#### Conectar Dashboard de Negocio
```javascript
socket.emit('connect_business_dashboard', {
  business_id: 2
});
```

### Eventos del Servidor

#### Visita Registrada
```javascript
socket.on('event:visit_registered', (data) => {
  console.log('Visita registrada:', data);
  // data.type = 'visit_registered'
  // data.message = 'Visita registrada exitosamente'
  // data.data = { visit info }
});
```

#### Premio Redimido
```javascript
socket.on('event:reward_redeemed', (data) => {
  console.log('Premio redimido:', data);
});
```

#### Nueva Ronda
```javascript
socket.on('event:new_round_started', (data) => {
  console.log('Nueva ronda:', data);
});
```

#### Notificación del Sistema
```javascript
socket.on('event:system_notification', (data) => {
  console.log('Notificación:', data);
});
```

## 🛡️ Seguridad

### Autenticación
- **Push**: JWT token en headers
- **WebSocket**: JWT token en auth object
- **Validación**: Automática en cada conexión

### Datos Sanitizados
- Títulos: máx 100 caracteres
- Cuerpos: máx 300 caracteres
- Campos sensibles removidos automáticamente

### Manejo de Errores
- **410/404**: Suscripciones inválidas eliminadas automáticamente
- **Logs**: Errores registrados sin exponer datos sensibles
- **Desconexión**: Automática si falla autenticación

## 🚀 Integración Frontend

### Service Worker (Push)
```javascript
// Registrar service worker
navigator.serviceWorker.register('/sw.js');

// Solicitar permisos
const permission = await Notification.requestPermission();

// Obtener suscripción
const registration = await navigator.serviceWorker.ready;
const subscription = await registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: vapidPublicKey
});

// Enviar al backend
await fetch('/api/notifications/subscribe', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(subscription)
});
```

### WebSocket Cliente
```javascript
import io from 'socket.io-client';

const socket = io('ws://localhost:8000/ws', {
  auth: { token: localStorage.getItem('token') }
});

// Para app de usuario
socket.emit('connect_customer_app', {});

// Para dashboard de negocio
socket.emit('connect_business_dashboard', { business_id: 2 });

// Escuchar eventos
socket.on('event:visit_registered', handleVisitRegistered);
socket.on('event:reward_redeemed', handleRewardRedeemed);
```

## 📊 Base de Datos

### Tabla: push_subscriptions
```sql
CREATE TABLE push_subscriptions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  business_id BIGINT NULL,
  endpoint TEXT NOT NULL,
  p256dh_key TEXT NOT NULL,
  auth_key TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔧 Desarrollo

### Generar Nuevas Claves VAPID
```bash
python generate_vapid_keys.py
```

### Crear Tabla Push
```bash
python create_push_table.py
```

### Probar Notificaciones
```bash
curl -X POST "http://localhost:8000/api/notifications/test" \
  -H "Authorization: Bearer <token>"
```

## 📈 Monitoreo

### Logs Importantes
- Conexiones WebSocket
- Suscripciones push registradas
- Notificaciones enviadas
- Errores de entrega

### Métricas
- Usuarios conectados via WebSocket
- Suscripciones activas
- Tasa de entrega de notificaciones
- Errores 410/404 (suscripciones inválidas)