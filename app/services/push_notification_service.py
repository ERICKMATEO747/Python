from pywebpush import webpush, WebPushException
from app.models.push_subscription import PushSubscription
from app.config.settings import get_settings
from app.utils.logger import log_error, log_info
import json
import asyncio
from typing import Dict, List

class PushNotificationService:
    def __init__(self):
        self.settings = get_settings()
        self.vapid_claims = {
            "sub": self.settings.vapid_subject
        }
    
    def send_push_notification(self, user_id: int, payload: Dict) -> bool:
        """Envía notificación push a un usuario específico"""
        try:
            subscriptions = PushSubscription.get_user_subscriptions(user_id)
            if not subscriptions:
                log_info(f"No hay suscripciones para usuario {user_id}")
                return False
            
            # Sanitizar payload
            sanitized_payload = self._sanitize_payload(payload)
            payload_json = json.dumps(sanitized_payload)
            
            success_count = 0
            for subscription in subscriptions:
                try:
                    webpush(
                        subscription_info=subscription,
                        data=payload_json,
                        vapid_private_key=self.settings.vapid_private_key,
                        vapid_claims=self.vapid_claims
                    )
                    success_count += 1
                except WebPushException as e:
                    if e.response.status_code in [410, 404]:
                        # Suscripción inválida, eliminar
                        PushSubscription.remove_invalid_subscription(subscription['endpoint'])
                        log_info(f"Suscripción inválida eliminada: {subscription['endpoint']}")
                    else:
                        log_error(f"Error enviando push: {e}")
                except Exception as e:
                    log_error(f"Error inesperado enviando push: {e}")
            
            return success_count > 0
        except Exception as e:
            log_error("Error en send_push_notification", error=e)
            return False
    
    async def send_push_notification_async(self, user_id: int, payload: Dict) -> bool:
        """Versión asíncrona para no bloquear el event loop"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.send_push_notification, user_id, payload)
    
    def _sanitize_payload(self, payload: Dict) -> Dict:
        """Sanitiza el payload antes de enviarlo"""
        sanitized = {
            'title': str(payload.get('title', ''))[:100],
            'body': str(payload.get('body', ''))[:300],
            'icon': str(payload.get('icon', '/icon-192x192.png')),
            'url_action': str(payload.get('url_action', '/')),
            'data': payload.get('data', {})
        }
        
        # Remover campos sensibles del data
        if 'data' in sanitized and isinstance(sanitized['data'], dict):
            sensitive_keys = ['password', 'token', 'key', 'secret']
            for key in sensitive_keys:
                sanitized['data'].pop(key, None)
        
        return sanitized
    
    # Métodos específicos para eventos de Flevo
    def notify_visit_registered(self, user_id: int, business_name: str, visit_data: Dict) -> bool:
        """Notifica visita registrada"""
        progress = visit_data.get('progress_in_round', 0)
        max_visits = visit_data.get('max_visits_per_round', 6)
        visits_left = max_visits - progress
        
        if visits_left > 0:
            body_message = f'¡Genial! Tu visita a {business_name} fue registrada. Te faltan {visits_left} visitas para tu próximo premio 🎉'
        else:
            body_message = f'¡Felicidades! Completaste tu ronda en {business_name}. ¡Ya puedes reclamar tu premio! 🎆'
        
        payload = {
            'title': '🎉 ¡Visita registrada!',
            'body': body_message,
            'icon': '/icons/visit-success.png',
            'url_action': '/visits',
            'data': {
                'type': 'visit_registered',
                'business_name': business_name,
                'visit_id': visit_data.get('id'),
                'progress': progress,
                'visits_left': visits_left
            }
        }
        return self.send_push_notification(user_id, payload)
    
    def notify_reward_earned(self, user_id: int, business_name: str, reward_data: Dict) -> bool:
        """Notifica premio ganado"""
        reward_name = reward_data.get('name', 'premio especial')
        
        payload = {
            'title': '🎆 ¡Felicidades! Premio desbloqueado',
            'body': f'¡Increible! Has ganado "{reward_name}" en {business_name}. Muéstralo al personal para reclamarlo 🎉',
            'icon': '/icons/trophy.png',
            'url_action': '/rewards',
            'data': {
                'type': 'reward_earned',
                'business_name': business_name,
                'reward_id': reward_data.get('id'),
                'reward_name': reward_name
            }
        }
        return self.send_push_notification(user_id, payload)
    
    def notify_new_round_started(self, user_id: int, business_name: str, round_data: Dict) -> bool:
        """Notifica nueva ronda iniciada"""
        payload = {
            'title': '🔄 Nueva ronda iniciada',
            'body': f'Has comenzado una nueva ronda en {business_name}',
            'icon': '/icons/round-icon.png',
            'url_action': '/visits',
            'data': {
                'type': 'new_round_started',
                'business_name': business_name,
                'round_number': round_data.get('round_number')
            }
        }
        return self.send_push_notification(user_id, payload)
    
    def notify_loyalty_reminder(self, user_id: int, business_name: str, progress: Dict) -> bool:
        """Notifica recordatorio del programa de lealtad"""
        visits_left = progress.get('visits_left', 0)
        payload = {
            'title': f'📍 {business_name}',
            'body': f'Te faltan {visits_left} visitas para tu próximo premio',
            'icon': '/icons/loyalty-icon.png',
            'url_action': '/businesses',
            'data': {
                'type': 'loyalty_reminder',
                'business_name': business_name,
                'visits_left': visits_left
            }
        }
        return self.send_push_notification(user_id, payload)