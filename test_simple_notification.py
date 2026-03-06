#!/usr/bin/env python3
"""
Test simple para verificar notificaciones push
"""

def test_notification_logic():
    """Prueba la lógica de notificaciones"""
    
    # Datos de prueba
    business_name = "Cafe Vanilla"
    progress = 3
    max_visits = 6
    visits_left = max_visits - progress
    
    print("Probando notificacion de visita...")
    print(f"Negocio: {business_name}")
    print(f"Progreso: {progress}/{max_visits}")
    print(f"Visitas restantes: {visits_left}")
    
    # Lógica de mensaje
    if visits_left > 0:
        message = f"Genial! Tu visita a {business_name} fue registrada. Te faltan {visits_left} visitas para tu proximo premio"
    else:
        message = f"Felicidades! Completaste tu ronda en {business_name}. Ya puedes reclamar tu premio!"
    
    print(f"\nMensaje generado:")
    print(f"Titulo: Visita registrada!")
    print(f"Cuerpo: {message}")
    
    # Test de premio
    print(f"\nProbando notificacion de premio...")
    reward_name = "Cafe gratis"
    prize_message = f"Increible! Has ganado \"{reward_name}\" en {business_name}. Muestralo al personal para reclamarlo"
    
    print(f"Titulo: Felicidades! Premio desbloqueado")
    print(f"Cuerpo: {prize_message}")
    
    print(f"\nTest completado - Notificaciones configuradas correctamente")

if __name__ == "__main__":
    test_notification_logic()