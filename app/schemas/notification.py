from pydantic import BaseModel, Field
from typing import Optional, Dict

class PushSubscriptionKeys(BaseModel):
    p256dh: str = Field(..., description="Clave P256DH del navegador")
    auth: str = Field(..., description="Clave de autenticación del navegador")

class PushSubscriptionCreate(BaseModel):
    endpoint: str = Field(..., description="Endpoint de la suscripción push")
    keys: PushSubscriptionKeys = Field(..., description="Claves de encriptación")
    business_id: Optional[int] = Field(None, description="ID del negocio (opcional)")

class NotificationPayload(BaseModel):
    title: str = Field(..., max_length=100, description="Título de la notificación")
    body: str = Field(..., max_length=300, description="Cuerpo de la notificación")
    icon: Optional[str] = Field("/icon-192x192.png", description="URL del icono")
    url_action: Optional[str] = Field("/", description="URL de acción al hacer clic")
    data: Optional[Dict] = Field({}, description="Datos adicionales")