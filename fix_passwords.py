#!/usr/bin/env python3
import sqlite3
import bcrypt

conn = sqlite3.connect('auth_api.db')
cursor = conn.cursor()

# Limpiar y crear usuarios con contraseñas simples
cursor.execute("DELETE FROM users")

# Crear usuarios con contraseña simple
password = "123456"
hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))

cursor.execute('''
    INSERT INTO users (nombre, email, password, user_type_id) VALUES
    ('Admin Test', 'admin@test.com', ?, 1),
    ('Negocio Test', 'negocio@test.com', ?, 2),
    ('Cliente Test', 'cliente@test.com', ?, 1)
''', (hash1.decode('utf-8'), hash1.decode('utf-8'), hash1.decode('utf-8')))

conn.commit()

# Verificar
cursor.execute("SELECT email, password FROM users")
for email, stored_hash in cursor.fetchall():
    is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    print(f"{email}: {'VALIDA' if is_valid else 'INVALIDA'}")

conn.close()
print("Usuarios recreados con contraseña: 123456")