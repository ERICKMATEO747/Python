# -*- coding: utf-8 -*-
"""
Script para mostrar usuarios de negocio
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.database_sqlite import get_db_connection

def show_business_users():
    print("=== USUARIOS DE NEGOCIO ===")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtener usuarios de tipo negocio (user_type_id = 2)
    cursor.execute("""
        SELECT u.id, u.nombre, u.email, u.telefono, u.user_type_id, m.municipio
        FROM users u
        LEFT JOIN municipalities m ON u.municipality_id = m.id
        WHERE u.user_type_id = 2
        ORDER BY u.id
    """)
    
    business_users = cursor.fetchall()
    
    if business_users:
        print(f"Total usuarios de negocio: {len(business_users)}")
        print()
        
        for user in business_users:
            print(f"ID: {user['id']}")
            print(f"Nombre: {user['nombre']}")
            print(f"Email: {user['email']}")
            print(f"Telefono: {user['telefono']}")
            print(f"Municipio: {user['municipio'] or 'No especificado'}")
            print(f"Password: password")
            print("-" * 40)
    else:
        print("No se encontraron usuarios de negocio")
    
    # Mostrar también todos los tipos de usuario
    print("\n=== TIPOS DE USUARIO ===")
    cursor.execute("SELECT id, type_name, description FROM user_types")
    user_types = cursor.fetchall()
    
    for user_type in user_types:
        print(f"ID {user_type['id']}: {user_type['type_name']} - {user_type['description']}")
    
    conn.close()

if __name__ == "__main__":
    show_business_users()