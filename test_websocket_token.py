#!/usr/bin/env python3
"""
Test WebSocket Token Parsing
"""

import urllib.parse

# Token del log con HTML entities
raw_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY0MzEwMTQ1LCJpYXQiOjE3NjQyMjM3NDV9.Lq9jK3FWWoJbZ2aCtwSoq6t71XASt5t7F54qHusA6DQ&amp;user_id=1"

print("🔍 ANÁLISIS DEL TOKEN")
print("=" * 50)
print(f"Token raw: {raw_token}")

# Simular query string del log
query_string = f"token={raw_token}"
print(f"Query string: {query_string}")

# Extraer token como lo hace el código actual
token = None
if 'token=' in query_string:
    for param in query_string.split('&'):
        if param.startswith('token='):
            raw_extracted = param.split('=', 1)[1]
            token = urllib.parse.unquote(raw_extracted)
            break

print(f"Token extraído: {token}")

# Verificar si el token es válido
try:
    from jose import jwt
    import time
    
    # Configuración JWT (simulada)
    SECRET_KEY = "tu-clave-secreta-jwt-muy-segura"  # Debe coincidir con settings
    ALGORITHM = "HS256"
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    print("✅ Token decodificado exitosamente:")
    print(f"   - User ID: {payload.get('sub')}")
    print(f"   - Issued at: {payload.get('iat')}")
    print(f"   - Expires at: {payload.get('exp')}")
    
    # Verificar expiración
    exp = payload.get('exp')
    current_time = time.time()
    
    if exp and exp < current_time:
        print("❌ Token EXPIRADO")
    else:
        print("✅ Token VÁLIDO")
        
except Exception as e:
    print(f"❌ Error decodificando token: {e}")

print("\n🔧 SOLUCIÓN:")
print("El problema está en el parsing del query string.")
print("El token contiene '&user_id=1' que se interpreta como parámetro separado.")