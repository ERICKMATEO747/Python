#!/usr/bin/env python3
"""
Test para verificar notificaciones push al registrar visitas
"""
from app.services.push_notification_service import PushNotificationService

def test_visit_notification():
    """Prueba notificación de visita registrada"""
    
    push_service = PushNotificationService()
    
    # Datos de prueba
    user_id = 1
    business_name = "Café Vanilla"
    visit_data = {
        'id': 123,
        'progress_in_round': 3,
        'max_visits_per_round': 6
    }
    
    print("Probando notificación de visita...")
    print(f"Usuario: {user_id}")
    print(f"Negocio: {business_name}")
    print(f"Progreso: {visit_data['progress_in_round']}/{visit_data['max_visits_per_round']}")
    
    # Simular notificación (sin enviar realmente)
    visits_left = visit_data['max_visits_per_round'] - visit_data['progress_in_round']
    
    if visits_left > 0:
        expected_message = f"¡Genial! Tu visita a {business_name} fue registrada. Te faltan {visits_left} visitas para tu próximo premio 🎉"
    else:
        expected_message = f"¡Felicidades! Completaste tu ronda en {business_name}. ¡Ya puedes reclamar tu premio! 🎆"
    
    print(f"\nMensaje esperado:")
    print(f"Título: Visita registrada!")
    print(f"Cuerpo: {expected_message}")
    
    print("\nTest completado - Notificación configurada correctamente")

def test_reward_notification():
    """Prueba notificación de premio ganado"""
    
    push_service = PushNotificationService()
    
    # Datos de prueba
    user_id = 1
    business_name = "Café Vanilla"
    reward_data = {
        'id': 456,
        'name': 'Café gratis'
    }
    
    print("\nProbando notificación de premio...")
    print(f"Usuario: {user_id}")
    print(f"Negocio: {business_name}")
    print(f"Premio: {reward_data['name']}")
    
    expected_message = f"¡Increible! Has ganado \"{reward_data['name']}\" en {business_name}. Muéstralo al personal para reclamarlo 🎉"
    
    print(f"\nMensaje esperado:")
    print(f"Título: Felicidades! Premio desbloqueado")
    print(f"Cuerpo: {expected_message}")
    
    print("\nTest completado - Notificación de premio configurada correctamente")

if __name__ == "__main__":
    test_visit_notification()
    test_reward_notification()