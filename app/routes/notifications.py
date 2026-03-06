from fastapi import APIRouter, Depends
from app.controllers.notification_controller import NotificationController
from app.schemas.notification import PushSubscriptionCreate
from app.utils.auth_middleware import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])
notification_controller = NotificationController()

@router.post("/subscribe")
async def subscribe_push_notifications(
    subscription_data: PushSubscriptionCreate,
    current_user: dict = Depends(get_current_user)
):
    """Registra suscripción para notificaciones push"""
    return notification_controller.subscribe_push(subscription_data, current_user)

@router.get("/vapid-public-key")
async def get_vapid_public_key():
    """Obtiene la clave pública VAPID para configurar el cliente"""
    return notification_controller.get_vapid_public_key()

@router.post("/test")
async def send_test_notification(
    current_user: dict = Depends(get_current_user)
):
    """Envía notificación de prueba (solo desarrollo)"""
    return notification_controller.test_notification(current_user)