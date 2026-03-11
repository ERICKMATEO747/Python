#!/usr/bin/env python3
"""
Script de Setup Automatizado para Flevo Backend
Facilita la instalación y configuración en diferentes equipos
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(command, description):
    """Ejecuta comando y maneja errores"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Verifica versión de Python"""
    print_header("Verificando Python")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def create_virtual_environment():
    """Crea entorno virtual"""
    print_header("Creando Entorno Virtual")
    
    if os.path.exists("venv"):
        print("⚠️  Entorno virtual ya existe")
        response = input("¿Deseas recrearlo? (s/n): ").lower()
        if response == 's':
            print("🗑️  Eliminando entorno virtual existente...")
            if platform.system() == "Windows":
                run_command("rmdir /s /q venv", "Eliminando venv")
            else:
                run_command("rm -rf venv", "Eliminando venv")
        else:
            return True
    
    return run_command("python -m venv venv", "Creando entorno virtual")

def install_dependencies():
    """Instala dependencias"""
    print_header("Instalando Dependencias")
    
    # Determinar comando pip según OS
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Actualizar pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Actualizando pip"):
        return False
    
    # Instalar dependencias
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias"):
        return False
    
    return True

def setup_environment_file():
    """Configura archivo .env"""
    print_header("Configurando Variables de Entorno")
    
    if os.path.exists(".env"):
        print("⚠️  Archivo .env ya existe")
        response = input("¿Deseas mantenerlo? (s/n): ").lower()
        if response == 's':
            print("✅ Manteniendo .env existente")
            return True
    
    if not os.path.exists(".env.example"):
        print("❌ No se encontró .env.example")
        return False
    
    # Copiar .env.example a .env
    try:
        with open(".env.example", "r") as source:
            content = source.read()
        
        with open(".env", "w") as dest:
            dest.write(content)
        
        print("✅ Archivo .env creado desde .env.example")
        print("\n⚠️  IMPORTANTE: Edita el archivo .env con tus configuraciones:")
        print("   - DATABASE_URL")
        print("   - JWT_SECRET_KEY")
        print("   - VAPID_PRIVATE_KEY y VAPID_PUBLIC_KEY")
        print("   - Configuración de email (opcional)")
        
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def generate_vapid_keys():
    """Genera claves VAPID para push notifications"""
    print_header("Generando Claves VAPID")
    
    response = input("¿Deseas generar nuevas claves VAPID? (s/n): ").lower()
    if response != 's':
        print("⏭️  Saltando generación de claves VAPID")
        return True
    
    try:
        from pywebpush import webpush
        import json
        
        # Generar claves
        vapid_key = webpush.generate_vapid_keys()
        
        print("\n📋 Claves VAPID generadas:")
        print(f"\nVAPID_PRIVATE_KEY={vapid_key['private_key']}")
        print(f"VAPID_PUBLIC_KEY={vapid_key['public_key']}")
        
        print("\n✅ Copia estas claves a tu archivo .env")
        
        return True
    except ImportError:
        print("⚠️  pywebpush no instalado. Instala dependencias primero.")
        return False
    except Exception as e:
        print(f"❌ Error generando claves VAPID: {e}")
        return False

def verify_database_connection():
    """Verifica conexión a base de datos"""
    print_header("Verificando Conexión a Base de Datos")
    
    response = input("¿Deseas verificar la conexión a la base de datos? (s/n): ").lower()
    if response != 's':
        print("⏭️  Saltando verificación de base de datos")
        return True
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from app.config.database import get_db_connection
        
        connection = get_db_connection()
        connection.close()
        
        print("✅ Conexión a base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando a base de datos: {e}")
        print("\n⚠️  Verifica tu DATABASE_URL en el archivo .env")
        return False

def print_next_steps():
    """Muestra pasos siguientes"""
    print_header("Setup Completado")
    
    print("🎉 ¡Instalación completada exitosamente!\n")
    print("📋 Próximos pasos:\n")
    print("1. Edita el archivo .env con tus configuraciones")
    print("2. Verifica la conexión a la base de datos")
    print("3. Ejecuta el servidor:\n")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("   python main.py")
    print("\n4. Accede a la documentación:")
    print("   http://localhost:8000/docs")
    print("\n" + "=" * 60)

def main():
    """Función principal"""
    print_header("Setup Automatizado - Flevo Backend")
    print("Este script configurará el entorno de desarrollo\n")
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_virtual_environment():
        print("\n❌ Error creando entorno virtual")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        sys.exit(1)
    
    # Configurar .env
    if not setup_environment_file():
        print("\n❌ Error configurando variables de entorno")
        sys.exit(1)
    
    # Generar claves VAPID (opcional)
    generate_vapid_keys()
    
    # Verificar base de datos (opcional)
    verify_database_connection()
    
    # Mostrar próximos pasos
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
