import socketio
from typing import Dict, List
from app.utils.logger import log_info, log_error

import json

class WebSocketService:
    def __init__(self):
        self.sio = socketio.AsyncServer(
            cors_allowed_origins="*",
            logger=True,
            engineio_logger=True
        )
        self.connected_users = {}  # {user_id: [session_ids]}
        self.connected_businesses = {}  # {business_id: [session_ids]}
        
        self._setup_events()
    
    def _setup_events(self):
        """Configura los eventos de WebSocket"""
        
        @self.sio.event
        async def connect(sid, environ, auth):
            """Maneja conexión de cliente"""
            try:
                # Verificar autenticación JWT desde query params
                import urllib.parse
                query_string = environ.get('QUERY_STRING', '')
                token = None
                
                log_info(f"WebSocket Query String: {query_string}")
                
                # Extraer token de query params
                if 'token=' in query_string:
                    # Encontrar el inicio del token
                    token_start = query_string.find('token=') + 6
                    # Buscar el siguiente parámetro (&user_id, &business_id, etc)
                    next_param = query_string.find('&', token_start)
                    if next_param == -1:
                        raw_token = query_string[token_start:]
                    else:
                        raw_token = query_string[token_start:next_param]
                    
                    # Decodificar HTML entities
                    token = urllib.parse.unquote(raw_token.replace('&amp;', '&'))
                    log_info(f"Token extraído: {token[:50]}...")
                
                if not token and auth:
                    token = auth.get('token')
                
                if not token:
                    log_error(f"WebSocket: Token no encontrado. Query: {query_string}")
                    await self.sio.disconnect(sid)
                    return False
                
                # Decodificar token manualmente para WebSocket
                try:
                    from jose import jwt
                    from app.config.settings import settings
                    import time
                    
                    log_info(f"Intentando decodificar token de longitud: {len(token)}")
                    
                    payload = jwt.decode(
                        token, 
                        settings.jwt_secret_key, 
                        algorithms=[settings.jwt_algorithm]
                    )
                    
                    log_info(f"Token decodificado exitosamente. Payload: {payload}")
                    
                    # Verificar expiración
                    exp = payload.get('exp')
                    current_time = time.time()
                    if exp and exp < current_time:
                        log_error(f"Token expirado. Exp: {exp}, Current: {current_time}")
                        await self.sio.disconnect(sid)
                        return False
                    
                    user_id = payload.get("sub")
                    if not user_id:
                        log_error("Token sin user_id en payload")
                        await self.sio.disconnect(sid)
                        return False
                    
                    user_data = {'id': int(user_id)}
                    log_info(f"Usuario autenticado: {user_data['id']}")
                    
                except jwt.ExpiredSignatureError as e:
                    log_error(f"JWT Token expirado: {e}")
                    await self.sio.disconnect(sid)
                    return False
                except jwt.JWTError as e:
                    log_error(f"Error decodificando JWT: {e}. Token: {token[:50]}...")
                    await self.sio.disconnect(sid)
                    return False
                except Exception as e:
                    log_error(f"Error procesando token: {e}. Token: {token[:50]}...")
                    await self.sio.disconnect(sid)
                    return False
                
                # Guardar datos del usuario en la sesión
                await self.sio.save_session(sid, {
                    'user_id': user_data['id'],
                    'user_type': user_data.get('user_type', 1),
                    'business_id': user_data.get('business_id')
                })
                
                log_info(f"Usuario {user_data['id']} conectado via WebSocket: {sid}")
                
            except Exception as e:
                log_error(f"Error en conexión WebSocket: {e}")
                await self.sio.disconnect(sid)
                return False
        
        @self.sio.event
        async def disconnect(sid):
            """Maneja desconexión de cliente"""
            try:
                session = await self.sio.get_session(sid)
                user_id = session.get('user_id')
                business_id = session.get('business_id')
                
                # Remover de listas de conectados
                if user_id and user_id in self.connected_users:
                    if sid in self.connected_users[user_id]:
                        self.connected_users[user_id].remove(sid)
                    if not self.connected_users[user_id]:
                        del self.connected_users[user_id]
                
                if business_id and business_id in self.connected_businesses:
                    if sid in self.connected_businesses[business_id]:
                        self.connected_businesses[business_id].remove(sid)
                    if not self.connected_businesses[business_id]:
                        del self.connected_businesses[business_id]
                
                log_info(f"Usuario desconectado: {sid}")
                
            except Exception as e:
                log_error(f"Error en desconexión: {e}")
        
        @self.sio.event
        async def connect_customer_app(sid, data):
            """Conecta cliente a la app de usuario"""
            try:
                session = await self.sio.get_session(sid)
                user_id = session.get('user_id')
                
                if user_id:
                    if user_id not in self.connected_users:
                        self.connected_users[user_id] = []
                    self.connected_users[user_id].append(sid)
                    
                    await self.sio.emit('connected', {
                        'type': 'customer_app',
                        'user_id': user_id
                    }, room=sid)
                
            except Exception as e:
                log_error(f"Error conectando customer app: {e}")
        
        @self.sio.event
        async def connect_business_dashboard(sid, data):
            """Conecta negocio al dashboard"""
            try:
                session = await self.sio.get_session(sid)
                user_id = session.get('user_id')
                business_id = data.get('business_id')
                
                if user_id and business_id:
                    if business_id not in self.connected_businesses:
                        self.connected_businesses[business_id] = []
                    self.connected_businesses[business_id].append(sid)
                    
                    await self.sio.emit('connected', {
                        'type': 'business_dashboard',
                        'business_id': business_id
                    }, room=sid)
                
            except Exception as e:
                log_error(f"Error conectando business dashboard: {e}")
    
    async def emit_to_user(self, user_id: int, event: str, data: Dict):
        """Envía evento a un usuario específico"""
        try:
            if user_id in self.connected_users:
                for sid in self.connected_users[user_id]:
                    await self.sio.emit(event, data, room=sid)
                return True
            return False
        except Exception as e:
            log_error(f"Error enviando evento a usuario {user_id}: {e}")
            return False
    
    async def emit_to_business(self, business_id: int, event: str, data: Dict):
        """Envía evento a un negocio específico"""
        try:
            if business_id in self.connected_businesses:
                for sid in self.connected_businesses[business_id]:
                    await self.sio.emit(event, data, room=sid)
                return True
            return False
        except Exception as e:
            log_error(f"Error enviando evento a negocio {business_id}: {e}")
            return False
    
    # Eventos específicos de Flevo
    async def notify_visit_registered(self, user_id: int, business_id: int, visit_data: Dict):
        """Notifica visita registrada en tiempo real"""
        # Al usuario
        await self.emit_to_user(user_id, 'event:visit_registered', {
            'type': 'visit_registered',
            'message': 'Visita registrada exitosamente',
            'data': visit_data
        })
        
        # Al dashboard del negocio
        await self.emit_to_business(business_id, 'event:visit_registered', {
            'type': 'visit_registered',
            'message': f'Nueva visita registrada',
            'data': visit_data,
            'user_id': user_id
        })
    
    async def notify_reward_redeemed(self, user_id: int, business_id: int, reward_data: Dict):
        """Notifica premio redimido"""
        # Al usuario
        await self.emit_to_user(user_id, 'event:reward_redeemed', {
            'type': 'reward_redeemed',
            'message': 'Premio redimido exitosamente',
            'data': reward_data
        })
        
        # Al dashboard del negocio
        await self.emit_to_business(business_id, 'event:reward_redeemed', {
            'type': 'reward_redeemed',
            'message': f'Premio redimido por cliente',
            'data': reward_data,
            'user_id': user_id
        })
    
    async def notify_new_round_started(self, user_id: int, business_id: int, round_data: Dict):
        """Notifica nueva ronda iniciada"""
        await self.emit_to_user(user_id, 'event:new_round_started', {
            'type': 'new_round_started',
            'message': 'Nueva ronda iniciada',
            'data': round_data
        })
    
    async def notify_system_notification(self, user_id: int, notification: Dict):
        """Notifica mensaje del sistema"""
        await self.emit_to_user(user_id, 'event:system_notification', {
            'type': 'system_notification',
            'message': notification.get('message', ''),
            'data': notification
        })
    
    def get_asgi_app(self):
        """Retorna la app ASGI para integrar con FastAPI"""
        return socketio.ASGIApp(self.sio)

# Instancia global del servicio WebSocket
websocket_service = WebSocketService()