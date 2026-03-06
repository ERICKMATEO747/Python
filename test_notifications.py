#!/usr/bin/env python3
"""
Script de prueba para verificar notificaciones push y WebSockets
"""
import requests
import json

def test_vapid_key():
    """Prueba obtener clave pública VAPID"""
    try:
        response = requests.get("http://localhost:8000/api/notifications/vapid-public-key")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ VAPID Key: {data['public_key'][:20]}...")
            return True
        else:
            print(f"❌ Error obteniendo VAPID key: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_websocket_connection():
    """Prueba conexión WebSocket"""
    try:
        import socketio
        
        sio = socketio.Client()
        
        @sio.event
        def connect():
            print("✅ WebSocket conectado")
            sio.disconnect()
        
        @sio.event
        def connect_error(data):
            print(f"❌ Error WebSocket: {data}")
        
        sio.connect('http://localhost:8000/ws', auth={'token': 'test_token'})
        return True
    except Exception as e:
        print(f"❌ Error WebSocket: {e}")
        return False

def main():
    print("🧪 Probando sistema de notificaciones...")
    
    print("\n1. Probando VAPID Key...")
    test_vapid_key()
    
    print("\n2. Probando WebSocket...")
    test_websocket_connection()
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    main()