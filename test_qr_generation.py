#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la generación de códigos QR
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.controllers.user_controller_sqlite import UserController
from app.schemas.user import VisitCreate
from datetime import datetime

def test_qr_generation():
    print("Probando generacion de codigo QR...")
    
    # Crear datos de visita de prueba
    visit_data = VisitCreate(
        user_id=1,
        business_id=1,
        visit_date=datetime.now()
    )
    
    try:
        # Generar QR
        result = UserController.generate_qr(visit_data)
        
        if result["success"]:
            print("Codigo QR generado exitosamente")
            print(f"Token: {result['data']['qr_token'][:50]}...")
            print(f"Expira: {result['data']['expires_at']}")
            print(f"QR Base64: {result['data']['qr_code'][:100]}...")
            
            # Verificar que el QR contiene datos válidos
            qr_data = result['data']['qr_code']
            if qr_data.startswith('data:image/png;base64,'):
                print("Formato de imagen QR correcto")
            else:
                print("Formato de imagen QR incorrecto")
                
        else:
            print("Error generando QR:", result)
            
    except Exception as e:
        print(f"Error en la prueba: {str(e)}")

if __name__ == "__main__":
    test_qr_generation()