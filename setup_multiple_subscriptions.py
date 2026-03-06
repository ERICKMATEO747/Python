#!/usr/bin/env python3
"""
Script para crear suscripciones push para múltiples usuarios
"""
from app.models.push_subscription import PushSubscription

def create_subscriptions_for_users():
    """Crea suscripciones push para usuarios 1, 2, 3, 4, 5"""
    
    users = [1, 2, 3, 4, 5]
    
    for user_id in users:
        subscription_data = {
            'endpoint': f'https://fcm.googleapis.com/fcm/send/test-endpoint-user-{user_id}',
            'keys': {
                'p256dh': f'test-p256dh-key-user-{user_id}',
                'auth': f'test-auth-key-user-{user_id}'
            }
        }
        
        print(f"Creando suscripcion para usuario {user_id}...")
        
        success = PushSubscription.subscribe(
            user_id=user_id,
            subscription_data=subscription_data,
            business_id=2
        )
        
        if success:
            print(f"  OK - Usuario {user_id} suscrito")
        else:
            print(f"  ERROR - Usuario {user_id} fallo")
    
    print(f"\nVerificando suscripciones creadas:")
    for user_id in users:
        subscriptions = PushSubscription.get_user_subscriptions(user_id)
        print(f"  Usuario {user_id}: {len(subscriptions)} suscripciones")

def show_notification_flow():
    """Muestra cómo funciona el flujo de notificaciones"""
    
    print("\n" + "="*60)
    print("FLUJO DE NOTIFICACIONES PUSH")
    print("="*60)
    
    print("\n1. REGISTRO DE VISITA:")
    print("   - Usuario X escanea QR en negocio Y")
    print("   - Sistema valida QR y registra visita")
    print("   - Sistema obtiene suscripciones del Usuario X")
    print("   - Sistema envia notificacion SOLO al Usuario X")
    
    print("\n2. NOTIFICACIONES AUTOMATICAS:")
    print("   - Visita registrada: 'Genial! Tu visita fue registrada...'")
    print("   - Premio ganado: 'Felicidades! Has ganado un premio...'")
    print("   - Nueva ronda: 'Nueva ronda iniciada...'")
    
    print("\n3. USUARIOS SOPORTADOS:")
    print("   - Cualquier usuario puede recibir notificaciones")
    print("   - Solo necesita tener suscripcion push registrada")
    print("   - Cada usuario recibe SUS propias notificaciones")
    
    print("\n4. PARA PROBAR:")
    print("   - Crea QR para usuario 2: /api/user/generate-qr")
    print("   - Valida QR usuario 2: /api/business/validate-qr")
    print("   - Usuario 2 recibira su notificacion")

if __name__ == "__main__":
    print("CONFIGURACION DE NOTIFICACIONES PUSH PARA MULTIPLES USUARIOS")
    print("=" * 70)
    
    create_subscriptions_for_users()
    show_notification_flow()
    
    print(f"\nLISTO! Ahora cualquier usuario (1-5) puede recibir notificaciones")
    print("Cada usuario recibira notificaciones cuando ELLOS registren visitas")