#!/usr/bin/env python3
"""
Test unitario para validar la actualización del perfil del negocio
"""
import json
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.business import Business

def test_business_profile_update():
    """Test para validar la actualización del perfil del negocio"""
    
    # Payload de prueba (el mismo que está causando problemas)
    test_payload = {
        "phone": "3109876543",
        "email": "info@cafevanilla.com",
        "website": "",
        "facebook": "https://facebook.com/cafecentral",
        "instagram": "https://instagram.com/cafecentral",
        "whatsapp": "3109876543",
        "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=500",
        "logo": "",
        "payment_methods": ["efectivo", "transferencia", "tarjeta", "nequi"],
        "delivery_options": ["pickup", "local"],
        "working_days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
        "opening_hours": {
            "friday": "06:00-20:00",
            "monday": "06:00-18:00",
            "sunday": "08:00-16:00",
            "tuesday": "06:00-18:00",
            "saturday": "07:00-20:00",
            "thursday": "06:00-18:00",
            "wednesday": "06:00-18:00"
        }
    }
    
    print("Iniciando test de actualización del perfil del negocio...")
    
    # Test 1: Verificar conversión de datos
    print("\nTest 1: Validando conversión de datos")
    
    # Simular la conversión que hace el modelo
    payment_methods = test_payload.get('payment_methods')
    if isinstance(payment_methods, list):
        payment_methods = json.dumps(payment_methods)
    print(f"OK payment_methods convertido: {payment_methods}")
    
    delivery_options = test_payload.get('delivery_options')
    if isinstance(delivery_options, list):
        delivery_options = json.dumps(delivery_options)
    print(f"OK delivery_options convertido: {delivery_options}")
    
    working_days = test_payload.get('working_days')
    if isinstance(working_days, list):
        working_days = json.dumps(working_days)
    print(f"OK working_days convertido: {working_days}")
    
    opening_hours = test_payload.get('opening_hours')
    if isinstance(opening_hours, dict):
        opening_hours = json.dumps(opening_hours)
    print(f"OK opening_hours convertido: {opening_hours}")
    
    # Test 2: Validar JSON
    print("\nTest 2: Validando JSON generado")
    try:
        json.loads(payment_methods)
        print("OK payment_methods es JSON válido")
    except:
        print("ERROR payment_methods NO es JSON válido")
        
    try:
        json.loads(delivery_options)
        print("OK delivery_options es JSON válido")
    except:
        print("ERROR delivery_options NO es JSON válido")
        
    try:
        json.loads(working_days)
        print("OK working_days es JSON válido")
    except:
        print("ERROR working_days NO es JSON válido")
        
    try:
        json.loads(opening_hours)
        print("OK opening_hours es JSON válido")
    except:
        print("ERROR opening_hours NO es JSON válido")
    
    # Test 3: Probar actualización real
    print("\nTest 3: Probando actualización real en BD")
    business_id = 2  # ID del negocio de prueba
    
    try:
        result = Business.update_profile(business_id, test_payload)
        if result:
            print("OK Actualización exitosa")
        else:
            print("ERROR Actualización falló")
    except Exception as e:
        print(f"ERROR en actualización: {e}")
    
    # Test 4: Verificar datos guardados
    print("\nTest 4: Verificando datos guardados")
    try:
        profile = Business.get_profile(business_id)
        if profile:
            print("OK Perfil recuperado exitosamente")
            print(f"Phone: {profile.get('phone')}")
            print(f"Email: {profile.get('email')}")
            print(f"Payment methods: {profile.get('payment_methods')}")
            print(f"Delivery options: {profile.get('delivery_options')}")
        else:
            print("ERROR No se pudo recuperar el perfil")
    except Exception as e:
        print(f"ERROR recuperando perfil: {e}")
    
    print("\nTest completado")

if __name__ == "__main__":
    test_business_profile_update()