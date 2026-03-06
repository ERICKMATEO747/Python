#!/usr/bin/env python3
import sqlite3
import bcrypt

# Conectar a la base de datos
conn = sqlite3.connect('auth_api.db')
cursor = conn.cursor()

# Verificar usuarios
cursor.execute("SELECT id, nombre, email, password FROM users")
users = cursor.fetchall()

print("=== VERIFICACIÓN DE USUARIOS ===")
for user in users:
    print(f"ID: {user[0]} | {user[1]} | {user[2]}")
    
    # Probar contraseña
    stored_hash = user[3]
    test_password = "123456"
    
    try:
        is_valid = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f"  Contraseña '123456': {'✅ VÁLIDA' if is_valid else '❌ INVÁLIDA'}")
    except Exception as e:
        print(f"  Error verificando contraseña: {e}")
    
    print("-" * 50)

# Crear nuevo usuario con contraseña simple
print("\n=== CREANDO USUARIO DE PRUEBA ===")
simple_password = "123456"
simple_hash = bcrypt.hashpw(simple_password.encode('utf-8'), bcrypt.gensalt(rounds=4))

cursor.execute("DELETE FROM users WHERE email = 'test@simple.com'")
cursor.execute(
    "INSERT INTO users (nombre, email, password, user_type_id) VALUES (?, ?, ?, ?)",
    ('Test Simple', 'test@simple.com', simple_hash.decode('utf-8'), 1)
)

conn.commit()
print("Usuario creado: test@simple.com / 123456")

# Verificar el nuevo usuario
cursor.execute("SELECT password FROM users WHERE email = 'test@simple.com'")
new_hash = cursor.fetchone()[0]
is_valid = bcrypt.checkpw(simple_password.encode('utf-8'), new_hash.encode('utf-8'))
print(f"Verificación: {'✅ VÁLIDA' if is_valid else '❌ INVÁLIDA'}")

conn.close()