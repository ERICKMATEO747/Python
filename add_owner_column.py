#!/usr/bin/env python3
"""
Script para agregar la columna owner_user_id a la tabla businesses
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def add_owner_column():
    """Agrega la columna owner_user_id a la tabla businesses"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("Agregando columna owner_user_id...")
            
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='businesses' AND column_name='owner_user_id'
            """)
            
            if cursor.fetchone():
                print("La columna owner_user_id ya existe")
            else:
                # Agregar la columna
                cursor.execute("ALTER TABLE businesses ADD COLUMN owner_user_id INTEGER REFERENCES users(id)")
                print("Columna owner_user_id agregada")
            
            # Crear usuario admin si no existe
            cursor.execute("SELECT id FROM users WHERE email = 'admin@flevoapp.com'")
            admin_user = cursor.fetchone()
            
            if not admin_user:
                print("Creando usuario administrador...")
                cursor.execute("""
                    INSERT INTO users (nombre, email, password, user_type_id) VALUES
                    ('Administrador', 'admin@flevoapp.com', '$2b$12$LQv3c1yqBWVHxkd0LQ4YCOdHrCkUAI6H0O/8VfzCr5FqSQqIBfxSm', 3)
                """)
                cursor.execute("SELECT id FROM users WHERE email = 'admin@flevoapp.com'")
                admin_user = cursor.fetchone()
                print("Usuario administrador creado")
            
            # Actualizar negocios existentes para asignar el admin como propietario
            cursor.execute("UPDATE businesses SET owner_user_id = %s WHERE owner_user_id IS NULL", (admin_user['id'],))
            updated_count = cursor.rowcount
            
            connection.commit()
            print(f"{updated_count} negocios actualizados con propietario")
            print("Migracion completada exitosamente!")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Agregando columna owner_user_id...")
    if add_owner_column():
        print("Migracion completada")
    else:
        print("Error en la migracion")