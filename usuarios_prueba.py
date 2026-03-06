#!/usr/bin/env python3

# Usuarios de prueba para login
usuarios = [
    {
        "email": "admin@test.com",
        "password": "admin123",
        "tipo": "Administrador"
    },
    {
        "email": "negocio@test.com", 
        "password": "negocio123",
        "tipo": "Negocio"
    },
    {
        "email": "cliente@test.com",
        "password": "cliente123", 
        "tipo": "Cliente"
    }
]

print("=== USUARIOS DE PRUEBA PARA LOGIN ===")
print()
for user in usuarios:
    print(f"Tipo: {user['tipo']}")
    print(f"Email: {user['email']}")
    print(f"Password: {user['password']}")
    print("-" * 30)

print("\nComando cURL para login:")
print('curl -X POST "http://localhost:8000/api/auth/login" \\')
print('     -H "Content-Type: application/json" \\')
print('     -d \'{"email": "admin@test.com", "password": "admin123"}\'')

print("\nComando cURL para registro:")
print('curl -X POST "http://localhost:8000/api/auth/register" \\')
print('     -H "Content-Type: application/json" \\')
print('     -d \'{"nombre": "Test User", "email": "test@nuevo.com", "password": "password123", "user_type_hash": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"}\'')