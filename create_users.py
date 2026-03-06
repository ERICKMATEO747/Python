#!/usr/bin/env python3
"""
Script para crear usuarios con contraseña correcta
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import bcrypt

# Cargar variables de entorno
load_dotenv()

def create_test_users():
    """Crea usuarios de prueba con contraseña correcta"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("=== VERIFICANDO USUARIOS EXISTENTES ===")
            cursor.execute("SELECT id, nombre, email FROM users ORDER BY id")
            existing_users = cursor.fetchall()
            
            if existing_users:
                print(f"Usuarios existentes ({len(existing_users)}):")
                for user in existing_users:
                    print(f"  ID {user['id']}: {user['nombre']} ({user['email']})")
                
                # Eliminar usuarios existentes para recrearlos
                print("\nEliminando usuarios existentes...")
                cursor.execute("DELETE FROM user_rounds")
                cursor.execute("DELETE FROM user_visits") 
                cursor.execute("DELETE FROM users")
                connection.commit()
                print("✅ Usuarios eliminados")
            
            print("\n=== CREANDO NUEVOS USUARIOS ===")
            
            # Generar hash correcto para "password123"
            password = "password123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
            hashed_str = hashed.decode('utf-8')
            
            print(f"Hash generado: {hashed_str}")
            
            # Crear usuarios
            users_data = [
                ('Juan Pérez', 'juan@test.com', hashed_str, 1),
                ('María García', 'maria@test.com', hashed_str, 1),
                ('Carlos López', 'carlos@test.com', hashed_str, 1),
                ('Ana Martínez', 'ana@test.com', hashed_str, 1),
                ('Luis Rodríguez', 'luis@test.com', hashed_str, 1)
            ]
            
            cursor.executemany("""
                INSERT INTO users (nombre, email, password, user_type_id)
                VALUES (%s, %s, %s, %s)
            """, users_data)
            
            connection.commit()
            
            # Verificar usuarios creados
            cursor.execute("SELECT id, nombre, email FROM users ORDER BY id")
            new_users = cursor.fetchall()
            
            print(f"\n✅ Usuarios creados ({len(new_users)}):")
            for user in new_users:
                print(f"  ID {user['id']}: {user['nombre']} ({user['email']})")
            
            print(f"\n🔑 CREDENCIALES DE ACCESO:")
            print(f"Contraseña para todos: {password}")
            print(f"Emails disponibles:")
            for user in new_users:
                print(f"  - {user['email']}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_login():
    """Prueba el login con bcrypt"""
    try:
        password = "password123"
        
        # Generar hash
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        print(f"Hash generado: {hashed.decode('utf-8')}")
        
        # Verificar hash
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
        print(f"Verificación: {is_valid}")
        
        return True
    except Exception as e:
        print(f"Error en test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Creando usuarios de prueba...")
    
    print("\n=== TEST DE BCRYPT ===")
    test_login()
    
    print("\n=== CREACIÓN DE USUARIOS ===")
    if create_test_users():
        print("\n✅ Usuarios creados exitosamente")
        print("\n📝 Para probar el login:")
        print("POST http://localhost:8000/api/auth/login")
        print('{"email": "juan@test.com", "password": "password123"}')
    else:
        print("❌ Error creando usuarios")