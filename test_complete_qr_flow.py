# -*- coding: utf-8 -*-
"""
Script para probar generación y validación completa de códigos QR
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.controllers.user_controller_sqlite import UserController
from app.schemas.user import VisitCreate
from datetime import datetime

def test_complete_qr_flow():
    print("=== PRUEBA COMPLETA DE FLUJO QR ===")
    
    # Datos de prueba
    user_id = 1
    business_id = 1
    current_user = {"id": user_id, "email": "test@example.com"}
    
    print(f"Usuario: {user_id}, Negocio: {business_id}")
    
    # 1. Generar QR
    print("\n1. GENERANDO CODIGO QR...")
    visit_data = VisitCreate(
        user_id=user_id,
        business_id=business_id,
        visit_date=datetime.now()
    )
    
    try:
        qr_result = UserController.generate_qr(visit_data)
        
        if qr_result["success"]:
            print("[OK] QR generado exitosamente")
            qr_token = qr_result['data']['qr_token']
            print(f"Token generado: {qr_token[:50]}...")
        else:
            print("[ERROR] Error generando QR:", qr_result)
            return
            
    except Exception as e:
        print(f"[ERROR] Error generando QR: {str(e)}")
        return
    
    # 2. Validar QR
    print("\n2. VALIDANDO CODIGO QR...")
    try:
        validation_result = UserController.validate_qr_visit(
            qr_token, business_id, current_user
        )
        
        if validation_result["success"]:
            print("[OK] QR validado exitosamente")
            print(f"Visita registrada con ID: {validation_result['data']['visit_id']}")
            print(f"Puntos ganados: {validation_result['data']['points_earned']}")
        else:
            print("[ERROR] Error validando QR:", validation_result)
            
    except Exception as e:
        print(f"[ERROR] Error validando QR: {str(e)}")
    
    # 3. Verificar visitas del usuario
    print("\n3. VERIFICANDO VISITAS DEL USUARIO...")
    try:
        visits_result = UserController.get_visits(user_id)
        
        if visits_result["success"]:
            visits = visits_result['data']['data']
            total_visits = visits_result['data']['total_visits']
            print(f"[OK] Total de visitas: {total_visits}")
            
            if visits:
                latest_visit = visits[0]
                print(f"Ultima visita: Negocio {latest_visit['business_name']}")
                print(f"Progreso en ronda: {latest_visit['progress_in_round']}/{latest_visit['max_visits_per_round']}")
        else:
            print("[ERROR] Error obteniendo visitas:", visits_result)
            
    except Exception as e:
        print(f"[ERROR] Error obteniendo visitas: {str(e)}")

if __name__ == "__main__":
    test_complete_qr_flow()