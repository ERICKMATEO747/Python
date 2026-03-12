#!/usr/bin/env python3
"""
Script de verificación de configuración
Verifica que todas las variables de entorno estén configuradas correctamente
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_env_file():
    """Verifica que existe el archivo .env"""
    print_header("Verificando Archivo .env")
    
    if not os.path.exists(".env"):
        print("❌ Archivo .env NO encontrado\n")
        print("📋 Solución:")
        print("   1. Copia el archivo .env.example:")
        print("      Windows: copy .env.example .env")
        print("      Linux/Mac: cp .env.example .env")
        print("   2. Edita el archivo .env con tus configuraciones\n")
        return False
    
    print("✅ Archivo .env encontrado\n")
    return True

def check_required_vars():
    """Verifica variables requeridas"""
    print_header("Verificando Variables Requeridas")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        "DATABASE_URL": "Conexión a PostgreSQL",
        "JWT_SECRET_KEY": "Clave secreta para JWT tokens"
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value == "":
            print(f"❌ {var} - {description}")
            missing_vars.append(var)
        else:
            # Ocultar valor sensible
            masked_value = value[:10] + "..." if len(value) > 10 else "***"
            print(f"✅ {var} - {masked_value}")
    
    if missing_vars:
        print(f"\n❌ Faltan {len(missing_vars)} variable(s) requerida(s)\n")
        print("📋 Agrega estas variables a tu archivo .env:\n")
        for var in missing_vars:
            print(f"   {var}=tu_valor_aqui")
        print()
        return False
    
    print("\n✅ Todas las variables requeridas están configuradas\n")
    return True

def check_optional_vars():
    """Verifica variables opcionales"""
    print_header("Verificando Variables Opcionales")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    optional_vars = {
        "VAPID_PUBLIC_KEY": "Push Notifications (público)",
        "VAPID_PRIVATE_KEY": "Push Notifications (privado)",
        "VAPID_SUBJECT": "Email para VAPID",
        "SMTP_USERNAME": "Email SMTP",
        "SMTP_PASSWORD": "Contraseña SMTP"
    }
    
    configured = 0
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and value != "":
            masked_value = value[:10] + "..." if len(value) > 10 else "***"
            print(f"✅ {var} - {masked_value}")
            configured += 1
        else:
            print(f"⚠️  {var} - No configurado ({description})")
    
    print(f"\n📊 Variables opcionales configuradas: {configured}/{len(optional_vars)}\n")
    return True

def test_database_connection():
    """Prueba conexión a base de datos"""
    print_header("Probando Conexión a Base de Datos")
    
    try:
        from app.config.database import get_db_connection
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        connection.close()
        
        print("✅ Conexión a base de datos exitosa\n")
        return True
    except Exception as e:
        print(f"❌ Error conectando a base de datos:\n   {str(e)}\n")
        print("📋 Verifica tu DATABASE_URL en el archivo .env\n")
        return False

def generate_jwt_secret():
    """Genera una clave JWT segura"""
    import secrets
    return secrets.token_urlsafe(32)

def main():
    """Función principal"""
    print_header("Verificación de Configuración - Flevo Backend")
    
    all_ok = True
    
    # Verificar archivo .env
    if not check_env_file():
        all_ok = False
        print("\n❌ Configuración incompleta. Crea el archivo .env primero.\n")
        sys.exit(1)
    
    # Verificar variables requeridas
    if not check_required_vars():
        all_ok = False
        print("\n💡 Sugerencia: Genera una clave JWT segura con:")
        print(f"   JWT_SECRET_KEY={generate_jwt_secret()}\n")
    
    # Verificar variables opcionales
    check_optional_vars()
    
    # Probar conexión a BD
    if all_ok:
        test_database_connection()
    
    # Resumen final
    print_header("Resumen")
    
    if all_ok:
        print("✅ Configuración completa y válida")
        print("🚀 Puedes ejecutar el servidor con: python main.py\n")
        return 0
    else:
        print("❌ Configuración incompleta")
        print("📋 Completa las variables faltantes en el archivo .env\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}\n")
        sys.exit(1)
