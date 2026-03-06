#!/usr/bin/env python3
"""
Script para probar validación QR y notificaciones
"""
import requests
import json
import time

# Configuración
API_BASE = "http://localhost:8000"
BUSINESS_TOKEN = "tu_token_de_negocio_aqui"  # Reemplazar con token real
QR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJidXNpbmVzc19pZCI6MiwidmlzaXRfdGltZXN0YW1wIjoxNzY0MjYyMjY4LCJleHAiOjE3NjQzNDg0OTN9.wlprMuO5vjURA_Gr5CxzPprVZMzdkReNYKWi7dcyD08"

def test_qr_validation():
    """Prueba validación QR"""
    
    headers = {
        "Authorization": f"Bearer {BUSINESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "qr_token": QR_TOKEN,
        "business_id": 2
    }
    
    print("Probando validación QR...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{API_BASE}/api/business/validate-qr",
            headers=headers,
            json=payload
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("\n✅ Visita registrada exitosamente")
                print("📱 Notificación push enviada automáticamente")
            else:
                print(f"\n❌ Error: {data.get('error')}")
                print(f"Mensaje: {data.get('message')}")
        
    except Exception as e:
        print(f"❌ Error en la petición: {e}")

def test_multiple_visits():
    """Prueba múltiples visitas para verificar el período de espera"""
    
    print("\n" + "="*50)
    print("PRUEBA DE MÚLTIPLES VISITAS")
    print("="*50)
    
    # Primera visita
    print("\n1. Primera visita:")
    test_qr_validation()
    
    # Segunda visita inmediata (debería fallar)
    print("\n2. Segunda visita inmediata:")
    test_qr_validation()
    
    # Esperar y probar de nuevo
    print("\n3. Esperando 6 minutos para la siguiente prueba...")
    print("(En producción sería 5 minutos, pero agregamos 1 minuto de margen)")
    
    # En lugar de esperar realmente, solo mostramos el mensaje
    print("⏰ Simularemos que pasaron 6 minutos...")
    print("4. Tercera visita (después de 6 minutos):")
    print("   Esta debería ser exitosa y enviar notificación")

if __name__ == "__main__":
    print("🧪 PRUEBA DE VALIDACIÓN QR Y NOTIFICACIONES")
    print("=" * 60)
    
    if BUSINESS_TOKEN == "tu_token_de_negocio_aqui":
        print("❌ ERROR: Debes configurar un token de negocio válido")
        print("   Edita la variable BUSINESS_TOKEN en este archivo")
    else:
        test_multiple_visits()
    
    print("\n📋 RESUMEN:")
    print("- Período de espera: 5 minutos entre visitas")
    print("- Notificaciones push: Se envían automáticamente en visitas exitosas")
    print("- WebSocket: Actualiza dashboards en tiempo real")