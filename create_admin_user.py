#!/usr/bin/env python3
"""
Script para crear usuario administrador
"""

from app.config.database import get_db_connection
import bcrypt

def create_admin_user():
    """Crea un usuario administrador"""
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Datos del admin
            email = "admin@flevoapp.com"
            password = "Admin123!"
            nombre = "Administrador Sistema"
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                print(f"Usuario admin {email} ya existe")
                return
            
            # Hash de la contraseña
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
            
            # Insertar usuario admin (user_type_id = 3)
            cursor.execute("""
                INSERT INTO users (nombre, email, password, user_type_id) 
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (nombre, email, hashed_password, 3))
            
            user_id = cursor.fetchone()['id']
            connection.commit()
            
            print(f"""
USUARIO ADMINISTRADOR CREADO:
- ID: {user_id}
- Nombre: {nombre}
- Email: {email}
- Password: {password}
- Tipo: Administrador (3)

CREDENCIALES PARA LOGIN:
Email: {email}
Password: {password}
            """)
                
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    create_admin_user()