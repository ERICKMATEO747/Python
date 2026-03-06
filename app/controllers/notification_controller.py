from fastapi import HTTPException
from app.models.push_subscription import PushSubscription
from app.services.push_notification_service import PushNotificationService
from app.schemas.notification import PushSubscriptionCreate
from app.utils.logger import log_info
import time

class NotificationController:
    def __init__(self):
        self.push_service = PushNotificationService()
    
    def subscribe_push(self, subscription_data: PushSubscriptionCreate, current_user: dict):
        """Registra suscripción push del usuario"""
        try:
            success = PushSubscription.subscribe(
                user_id=current_user['id'],
                subscription_data=subscription_data.dict(),
                business_id=subscription_data.business_id
            )
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo registrar la suscripción")
            
            log_info(f"Suscripción push registrada para usuario {current_user['id']}")
            
            return {
                "success": True,
                "message": "Suscripción registrada exitosamente"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    def get_vapid_public_key(self):
        """Obtiene la clave pública VAPID para el cliente"""
        from app.config.settings import get_settings
        settings = get_settings()
        
        return {
            "success": True,
            "public_key": settings.VAPID_PUBLIC_KEY
        }
    
    def test_notification(self, current_user: dict):
        """Envía notificación de prueba (solo para desarrollo)"""
        try:
            payload = {
                'title': '🧪 Notificación de prueba',
                'body': 'Esta es una notificación de prueba de Flevo',
                'icon': '/icons/test-icon.png',
                'url_action': '/',
                'data': {
                    'type': 'test',
                    'timestamp': str(int(time.time()))
                }
            }
            
            success = self.push_service.send_push_notification(current_user['id'], payload)
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo enviar la notificación")
            
            return {
                "success": True,
                "message": "Notificación de prueba enviada"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")