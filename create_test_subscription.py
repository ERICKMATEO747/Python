#!/usr/bin/env python3
"""
Script para crear una suscripción push de prueba
"""
from app.models.push_subscription import PushSubscription

def create_test_subscription():
    """Crea una suscripción push de prueba para el usuario 1"""
    
    # Datos de suscripción de prueba
    user_id = 1
    subscription_data = {
        'endpoint': 'https://fcm.googleapis.com/fcm/send/test-endpoint-123',
        'keys': {
            'p256dh': 'test-p256dh-key-123',
            'auth': 'test-auth-key-123'
        }
    }
    
    print(f"Creando suscripción de prueba para usuario {user_id}...")
    
    success = PushSubscription.subscribe(
        user_id=user_id,
        subscription_data=subscription_data,
        business_id=2
    )
    
    if success:
        print("Suscripción de prueba creada exitosamente")
        
        # Verificar que se creó
        subscriptions = PushSubscription.get_user_subscriptions(user_id)
        print(f"Suscripciones activas para usuario {user_id}: {len(subscriptions)}")
        
        for i, sub in enumerate(subscriptions):
            print(f"   {i+1}. Endpoint: {sub['endpoint'][:50]}...")
    else:
        print("Error creando suscripción de prueba")

if __name__ == "__main__":
    create_test_subscription()