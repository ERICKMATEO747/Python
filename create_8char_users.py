#!/usr/bin/env python3
import sqlite3
import bcrypt

conn = sqlite3.connect('auth_api.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM users")

# Contraseñas de 8 caracteres
password = "password"  # 8 caracteres
hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))

cursor.execute('''
    INSERT INTO users (nombre, email, password, user_type_id) VALUES
    ('Admin Test', 'admin@test.com', ?, 1),
    ('Negocio Test', 'negocio@test.com', ?, 2),
    ('Cliente Test', 'cliente@test.com', ?, 1)
''', (hash1.decode('utf-8'), hash1.decode('utf-8'), hash1.decode('utf-8')))

conn.commit()

# Verificar
cursor.execute("SELECT email FROM users")
for row in cursor.fetchall():
    print(f"{row[0]}: password")

conn.close()
print("Usuarios creados con contraseña de 8 caracteres: 'password'")