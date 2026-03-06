#!/usr/bin/env python3
"""
Script de prueba rápida para login con SQLite
"""

import sqlite3
import bcrypt
import json

def setup_test_db():
    """Crea base de datos SQLite de prueba"""
    conn = sqlite3.connect('test.db')
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
    
    # Insertar tipos de usuario
    cursor.execute("DELETE FROM user_types")
    cursor.execute('''
        INSERT INTO user_types (type_name, type_hash, description) VALUES 
        ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
        ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio')
    ''')
    
    # Crear usuarios de prueba
    password = "negocio123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    
    cursor.execute("DELETE FROM users")
    
    # Usuario cliente
    cursor.execute('''
        INSERT INTO users (nombre, email, password, user_type_id) 
        VALUES (?, ?, ?, ?)
    ''', ('Test Cliente', 'cliente@test.com', hashed_password.decode('utf-8'), 1))
    
    # Usuario negocio
    cursor.execute('''
        INSERT INTO users (nombre, email, password, user_type_id) 
        VALUES (?, ?, ?, ?)
    ''', ('Carlos Hernandez', 'carlos@eltotonaco.com', hashed_password.decode('utf-8'), 2))
    
    conn.commit()
    conn.close()
    
    print("Base de datos SQLite creada con usuarios:")
    print("- cliente@test.com / negocio123")
    print("- carlos@eltotonaco.com / negocio123")

def test_login():
    """Prueba el login con los usuarios creados"""
    import requests
    
    users = [
        {"email": "cliente@test.com", "password": "negocio123"},
        {"email": "carlos@eltotonaco.com", "password": "negocio123"}
    ]
    
    for user in users:
        try:
            response = requests.post(
                "http://localhost:8000/api/auth/login",
                json=user,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\nLogin {user['email']}:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Configurando base de datos de prueba...")
    setup_test_db()
    print("\nProbando login...")
    test_login()