#!/usr/bin/env python3
import sqlite3
import bcrypt
from datetime import datetime, timedelta
import random

def create_demo_database():
    conn = sqlite3.connect('auth_api.db')
    cursor = conn.cursor()
    
    # Limpiar tablas existentes
    cursor.execute("DROP TABLE IF EXISTS user_visits")
    cursor.execute("DROP TABLE IF EXISTS user_rounds")
    cursor.execute("DROP TABLE IF EXISTS user_rewards")
    cursor.execute("DROP TABLE IF EXISTS businesses")
    cursor.execute("DROP TABLE IF EXISTS municipalities")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS user_types")
    
    # Crear tablas
    cursor.execute('''
        CREATE TABLE user_types (
            id INTEGER PRIMARY KEY,
            type_name TEXT UNIQUE,
            type_hash TEXT UNIQUE,
            description TEXT,
            active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE municipalities (
            id INTEGER PRIMARY KEY,
            municipio TEXT NOT NULL,
            state TEXT NOT NULL,
            active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE,
            telefono TEXT UNIQUE,
            password TEXT NOT NULL,
            user_type_id INTEGER DEFAULT 1,
            municipality_id INTEGER,
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE businesses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            address TEXT,
            municipality_id INTEGER,
            phone TEXT,
            email TEXT,
            logo TEXT,
            image_url TEXT,
            description TEXT,
            rating REAL DEFAULT 0.0,
            visits_for_prize INTEGER DEFAULT 6,
            facebook TEXT,
            instagram TEXT,
            whatsapp TEXT,
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE user_visits (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            business_id INTEGER NOT NULL,
            visit_date TIMESTAMP NOT NULL,
            visit_month TEXT NOT NULL,
            status TEXT DEFAULT 'completed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE user_rounds (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            business_id INTEGER NOT NULL,
            round_number INTEGER NOT NULL DEFAULT 1,
            progress_in_round INTEGER NOT NULL DEFAULT 0,
            round_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL,
            is_completed BOOLEAN NOT NULL DEFAULT FALSE,
            is_reward_claimed BOOLEAN NOT NULL DEFAULT FALSE,
            last_visit_id INTEGER NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE user_rewards (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            business_id INTEGER NOT NULL,
            reward_type TEXT DEFAULT 'coupon',
            status TEXT DEFAULT 'vigente',
            reclamado BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
    ''')
    
    # Insertar tipos de usuario
    cursor.execute('''
        INSERT INTO user_types (type_name, type_hash, description) VALUES 
        ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
        ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio'),
        ('admin', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1b2', 'Administrador del sistema')
    ''')
    
    # Insertar municipios
    cursor.execute('''
        INSERT INTO municipalities (municipio, state) VALUES
        ('Papantla', 'Veracruz'),
        ('Coatzintla', 'Veracruz'),
        ('Poza Rica', 'Veracruz'),
        ('Tuxpan', 'Veracruz'),
        ('Xalapa', 'Veracruz')
    ''')
    
    # Crear usuarios
    password = "password"
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))
    
    usuarios = [
        ('Juan Pérez', 'juan@cliente.com', '7841234567', 1, 1, 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150'),
        ('María González', 'maria@cliente.com', '7842345678', 1, 2, 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150'),
        ('Carlos Hernández', 'carlos@negocio.com', '7843456789', 2, 1, 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150'),
        ('Ana López', 'ana@negocio.com', '7844567890', 2, 3, 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150'),
        ('Admin Sistema', 'admin@sistema.com', '7845678901', 3, 1, 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150'),
        ('Pedro Martínez', 'pedro@cliente.com', '7846789012', 1, 4, 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150'),
        ('Sofía Rodríguez', 'sofia@cliente.com', '7847890123', 1, 5, 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150')
    ]
    
    for nombre, email, telefono, tipo, municipio, avatar in usuarios:
        cursor.execute('''
            INSERT INTO users (nombre, email, telefono, password, user_type_id, municipality_id, avatar) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, email, telefono, hash_pass.decode('utf-8'), tipo, municipio, avatar))
    
    # Crear negocios
    negocios = [
        ('Restaurante El Totonaco', 'Restaurante', 'Calle Enríquez 123, Centro', 1, '7841234567', 'contacto@eltotonaco.com', 'Comida tradicional veracruzana con sabores auténticos', 4.5, 6, 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400', 'https://facebook.com/eltotonaco', 'https://instagram.com/eltotonaco', '7841234567', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=200'),
        ('Café Vanilla', 'Cafetería', 'Av. 20 de Noviembre 45', 2, '7822345678', 'info@cafevanilla.com', 'Café de especialidad y vainilla de la región', 4.2, 8, 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400', 'https://facebook.com/cafevanilla', 'https://instagram.com/cafevanilla', '7822345678', 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=200'),
        ('Pizzería Don Juan', 'Pizzería', 'Plaza Principal 12', 1, '7843333333', 'juan@pizzeria.com', 'Las mejores pizzas artesanales de la ciudad', 4.7, 5, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400', 'https://facebook.com/pizzeriadonjuan', 'https://instagram.com/pizzeriadonjuan', '7843333333', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=200'),
        ('Tacos El Buen Sabor', 'Comida Rápida', 'Calle Hidalgo 89', 3, '7844444444', 'tacos@buensabor.com', 'Tacos tradicionales con ingredientes frescos', 4.3, 10, 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400', 'https://facebook.com/tacosbuensabor', 'https://instagram.com/tacosbuensabor', '7844444444', 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=200'),
        ('Heladería Tropical', 'Heladería', 'Av. Juárez 156', 2, '7845555555', 'helados@tropical.com', 'Helados artesanales con frutas tropicales', 4.6, 7, 'https://images.unsplash.com/photo-1488900128323-21503983a07e?w=400', 'https://facebook.com/heladeria.tropical', 'https://instagram.com/heladeria.tropical', '7845555555', 'https://images.unsplash.com/photo-1488900128323-21503983a07e?w=200'),
        ('Panadería La Espiga', 'Panadería', 'Calle Morelos 234', 4, '7846666666', 'pan@laespiga.com', 'Pan fresco y repostería tradicional', 4.4, 12, 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400', 'https://facebook.com/panaderiaespiga', 'https://instagram.com/panaderiaespiga', '7846666666', 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=200')
    ]
    
    for nombre, categoria, direccion, municipio, telefono, email, descripcion, rating, visitas, logo, facebook, instagram, whatsapp, image_url in negocios:
        cursor.execute('''
            INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating, visits_for_prize, logo, facebook, instagram, whatsapp, image_url) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, categoria, direccion, municipio, telefono, email, descripcion, rating, visitas, logo, facebook, instagram, whatsapp, image_url))
    
    # Crear visitas de ejemplo
    base_date = datetime.now() - timedelta(days=90)
    
    # Usuario 1 (Juan) - Cliente activo
    visitas_juan = [
        (1, 1, base_date + timedelta(days=5), '2024-11'),
        (1, 1, base_date + timedelta(days=12), '2024-11'),
        (1, 1, base_date + timedelta(days=18), '2024-11'),
        (1, 1, base_date + timedelta(days=25), '2024-11'),
        (1, 1, base_date + timedelta(days=32), '2024-12'),
        (1, 1, base_date + timedelta(days=45), '2024-12'),
        (1, 2, base_date + timedelta(days=10), '2024-11'),
        (1, 2, base_date + timedelta(days=20), '2024-11'),
        (1, 2, base_date + timedelta(days=35), '2024-12'),
        (1, 3, base_date + timedelta(days=15), '2024-11'),
        (1, 3, base_date + timedelta(days=28), '2024-11'),
        (1, 3, base_date + timedelta(days=40), '2024-12')
    ]
    
    # Usuario 2 (María) - Cliente moderado
    visitas_maria = [
        (2, 2, base_date + timedelta(days=8), '2024-11'),
        (2, 2, base_date + timedelta(days=22), '2024-11'),
        (2, 2, base_date + timedelta(days=38), '2024-12'),
        (2, 4, base_date + timedelta(days=14), '2024-11'),
        (2, 4, base_date + timedelta(days=30), '2024-12'),
        (2, 5, base_date + timedelta(days=42), '2024-12')
    ]
    
    # Usuario 6 (Pedro) - Cliente nuevo
    visitas_pedro = [
        (6, 1, base_date + timedelta(days=60), '2024-12'),
        (6, 1, base_date + timedelta(days=70), '2024-12'),
        (6, 3, base_date + timedelta(days=65), '2024-12')
    ]
    
    todas_visitas = visitas_juan + visitas_maria + visitas_pedro
    
    for user_id, business_id, fecha, mes in todas_visitas:
        cursor.execute('''
            INSERT INTO user_visits (user_id, business_id, visit_date, visit_month) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, business_id, fecha.isoformat(), mes))
    
    # Crear rondas de usuario
    rondas = [
        (1, 1, 1, 6, datetime.now() - timedelta(days=85), datetime.now() - timedelta(days=45), True, True, 6),
        (1, 1, 2, 0, datetime.now() - timedelta(days=45), None, False, False, None),
        (1, 2, 1, 3, datetime.now() - timedelta(days=80), None, False, False, None),
        (1, 3, 1, 2, datetime.now() - timedelta(days=75), None, False, False, None),
        (2, 2, 1, 3, datetime.now() - timedelta(days=82), None, False, False, None),
        (2, 4, 1, 2, datetime.now() - timedelta(days=76), None, False, False, None),
        (6, 1, 1, 2, datetime.now() - timedelta(days=30), None, False, False, None)
    ]
    
    for user_id, business_id, round_num, progress, start_date, completed_date, is_completed, is_claimed, last_visit in rondas:
        cursor.execute('''
            INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, round_start_date, completed_at, is_completed, is_reward_claimed, last_visit_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, business_id, round_num, progress, start_date.isoformat(), 
              completed_date.isoformat() if completed_date else None, is_completed, is_claimed, last_visit))
    
    # Crear recompensas
    recompensas = [
        (1, 1, 'coupon', 'reclamado', True, datetime.now() - timedelta(days=40), datetime.now() + timedelta(days=30)),
        (1, 2, 'coupon', 'vigente', False, datetime.now() - timedelta(days=10), datetime.now() + timedelta(days=60)),
        (2, 2, 'coupon', 'vigente', False, datetime.now() - timedelta(days=5), datetime.now() + timedelta(days=65))
    ]
    
    for user_id, business_id, reward_type, status, reclamado, created, expires in recompensas:
        cursor.execute('''
            INSERT INTO user_rewards (user_id, business_id, reward_type, status, reclamado, created_at, expires_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, business_id, reward_type, status, reclamado, created.isoformat(), expires.isoformat()))
    
    conn.commit()
    conn.close()
    
    print("=== BASE DE DATOS DEMO CREADA ===")
    print("OK 7 usuarios (3 clientes, 2 negocios, 1 admin, 1 cliente nuevo)")
    print("OK 6 negocios con datos completos")
    print("OK 5 municipios")
    print("OK 21 visitas distribuidas")
    print("OK 7 rondas de lealtad")
    print("OK 3 cupones/recompensas")
    print("\n=== CREDENCIALES ===")
    print("Todos los usuarios: password")
    print("- juan@cliente.com (Cliente activo)")
    print("- maria@cliente.com (Cliente moderado)")
    print("- carlos@negocio.com (Propietario)")
    print("- ana@negocio.com (Propietario)")
    print("- admin@sistema.com (Administrador)")
    print("- pedro@cliente.com (Cliente nuevo)")
    print("- sofia@cliente.com (Cliente)")

if __name__ == "__main__":
    create_demo_database()