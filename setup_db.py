#!/usr/bin/env python3
import sqlite3
import bcrypt

# Crear base de datos de prueba
conn = sqlite3.connect('auth_api.db')
cursor = conn.cursor()

# Crear tablas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_types (
        id INTEGER PRIMARY KEY,
        type_name TEXT UNIQUE,
        type_hash TEXT UNIQUE,
        description TEXT,
        active BOOLEAN DEFAULT TRUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE,
        telefono TEXT UNIQUE,
        password TEXT NOT NULL,
        user_type_id INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        address TEXT,
        phone TEXT,
        email TEXT,
        description TEXT,
        rating REAL DEFAULT 0.0,
        visits_for_prize INTEGER DEFAULT 6,
        active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Limpiar datos existentes
cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM user_types")
cursor.execute("DELETE FROM businesses")

# Insertar tipos de usuario
cursor.execute('''
    INSERT INTO user_types (type_name, type_hash, description) VALUES 
    ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
    ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio')
''')

# Crear usuarios de prueba
password = "123456"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

cursor.execute('''
    INSERT INTO users (nombre, email, password, user_type_id) VALUES
    ('Admin Test', 'admin@test.com', ?, 1),
    ('Negocio Test', 'negocio@test.com', ?, 2),
    ('Cliente Test', 'cliente@test.com', ?, 1)
''', (hashed_password.decode('utf-8'), hashed_password.decode('utf-8'), hashed_password.decode('utf-8')))

# Crear negocios de prueba
cursor.execute('''
    INSERT INTO businesses (name, category, address, phone, email, description, rating) VALUES
    ('Restaurante El Totonaco', 'Restaurante', 'Calle Enriquez 123, Centro', '7841234567', 'contacto@eltotonaco.com', 'Comida tradicional veracruzana', 4.5),
    ('Cafe Vanilla', 'Cafeteria', 'Av. 20 de Noviembre 45', '7822345678', 'info@cafevanilla.com', 'Cafe de especialidad y vainilla', 4.2),
    ('Pizzeria Don Juan', 'Pizzeria', 'Plaza Principal 12', '7843333333', 'juan@pizzeria.com', 'Las mejores pizzas artesanales', 4.7)
''')

conn.commit()

# Verificar datos
print("=== USUARIOS CREADOS ===")
cursor.execute("SELECT id, nombre, email, user_type_id FROM users")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | {row[1]} | {row[2]} | Tipo: {row[3]}")

print("\n=== NEGOCIOS CREADOS ===")
cursor.execute("SELECT id, name, category FROM businesses")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | {row[1]} | {row[2]}")

print("\n=== CREDENCIALES DE PRUEBA ===")
print("admin@test.com / 123456")
print("negocio@test.com / 123456")
print("cliente@test.com / 123456")

conn.close()
print("\nBase de datos creada exitosamente!")