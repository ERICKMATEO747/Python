#!/usr/bin/env python3
"""
Script para crear usuarios de ejemplo para negocios
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import bcrypt

# Cargar variables de entorno
load_dotenv()

def create_business_users():
    """Crea usuarios de ejemplo para los negocios"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("Creando usuarios de negocios...")
            
            # Verificar si ya existen usuarios de negocio
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE user_type_id = 2")
            result = cursor.fetchone()
            business_users_count = result['count'] if result else 0
            
            if business_users_count > 0:
                print(f"Ya existen {business_users_count} usuarios de negocio")
                # Mostrar usuarios existentes
                cursor.execute("""
                    SELECT u.id, u.nombre, u.email, u.telefono, b.name as business_name
                    FROM users u
                    LEFT JOIN businesses b ON u.id = b.owner_user_id
                    WHERE u.user_type_id = 2
                    ORDER BY u.id
                """)
                existing_users = cursor.fetchall()
                
                print("\nUsuarios de negocio existentes:")
                for user in existing_users:
                    print(f"  - ID: {user['id']} | {user['nombre']} | {user['email'] or user['telefono']} | Negocio: {user['business_name'] or 'Sin asignar'}")
                
                return True
            
            # Obtener negocios existentes
            cursor.execute("SELECT id, name FROM businesses ORDER BY id")
            businesses = cursor.fetchall()
            
            if not businesses:
                print("ERROR: No hay negocios en la base de datos. Ejecuta primero migrate_simple.py")
                return False
            
            # Crear contraseña encriptada
            password = "negocio123"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
            
            # Usuarios de ejemplo para negocios
            business_users = [
                {
                    'nombre': 'Carlos Hernández',
                    'email': 'carlos@eltotonaco.com',
                    'telefono': '7841234567',
                    'business_name': 'Restaurante El Totonaco'
                },
                {
                    'nombre': 'María González',
                    'email': 'maria@cafevanilla.com', 
                    'telefono': '7822345678',
                    'business_name': 'Café Vanilla'
                },
                {
                    'nombre': 'Admin Negocio',
                    'email': 'admin@negocio.com',
                    'telefono': '7841111111',
                    'business_name': None  # Usuario genérico
                }
            ]
            
            created_users = []
            
            for user_data in business_users:
                try:
                    # Insertar usuario
                    cursor.execute("""
                        INSERT INTO users (nombre, email, telefono, password, user_type_id, municipality_id)
                        VALUES (%s, %s, %s, %s, 2, 1)
                        RETURNING id
                    """, (
                        user_data['nombre'],
                        user_data['email'],
                        user_data['telefono'],
                        hashed_password.decode('utf-8')
                    ))
                    
                    user_id = cursor.fetchone()['id']
                    created_users.append({
                        'id': user_id,
                        'nombre': user_data['nombre'],
                        'email': user_data['email'],
                        'telefono': user_data['telefono'],
                        'business_name': user_data['business_name']
                    })
                    
                    print(f"Usuario creado: {user_data['nombre']} (ID: {user_id})")
                    
                except psycopg2.IntegrityError as e:
                    if "email" in str(e):
                        print(f"AVISO: Email {user_data['email']} ya existe")
                    elif "telefono" in str(e):
                        print(f"AVISO: Telefono {user_data['telefono']} ya existe")
                    else:
                        print(f"AVISO: Error de integridad: {e}")
                    connection.rollback()
                    continue
            
            # Agregar columna owner_user_id a businesses si no existe
            try:
                cursor.execute("ALTER TABLE businesses ADD COLUMN owner_user_id INTEGER REFERENCES users(id)")
                print("Columna owner_user_id agregada a businesses")
            except psycopg2.errors.DuplicateColumn:
                print("INFO: Columna owner_user_id ya existe en businesses")
            
            # Asignar usuarios a negocios
            for user in created_users:
                if user['business_name']:
                    cursor.execute("""
                        UPDATE businesses 
                        SET owner_user_id = %s 
                        WHERE name = %s
                    """, (user['id'], user['business_name']))
                    print(f"Usuario {user['nombre']} asignado a {user['business_name']}")
            
            connection.commit()
            
            print("\nUsuarios de negocio creados exitosamente!")
            print("\nCredenciales de acceso:")
            print("=" * 50)
            for user in created_users:
                print(f"USUARIO: {user['nombre']}")
                print(f"   Email: {user['email']}")
                print(f"   Telefono: {user['telefono']}")
                print(f"   Password: {password}")
                print(f"   Negocio: {user['business_name'] or 'Sin asignar'}")
                print("-" * 30)
            
            print("\nPuedes usar estos usuarios para:")
            print("  - Acceder al portal de negocios")
            print("  - Gestionar menus y productos")
            print("  - Ver estadisticas de visitas")
            print("  - Administrar cupones y recompensas")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Creando usuarios de ejemplo para negocios...")
    if create_business_users():
        print("Proceso completado exitosamente")
    else:
        print("Error en el proceso")