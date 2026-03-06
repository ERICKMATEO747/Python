#!/usr/bin/env python3
"""
Script de migración de MySQL a PostgreSQL (Supabase)
Ejecutar después de actualizar las dependencias
"""

import subprocess
import sys
import os
from app.config.database import init_database
from app.utils.logger import log_info, log_error

def install_dependencies():
    """Instala las nuevas dependencias de PostgreSQL"""
    try:
        log_info("Instalando dependencias de PostgreSQL...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        log_info("Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        log_error("Error instalando dependencias", error=e)
        return False

def test_connection():
    """Prueba la conexión a PostgreSQL"""
    try:
        log_info("Probando conexión a PostgreSQL...")
        from app.config.database import get_db_connection
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            log_info(f"Conexión exitosa a PostgreSQL: {version}")
        connection.close()
        return True
    except Exception as e:
        log_error("Error conectando a PostgreSQL", error=e)
        return False

def migrate_database():
    """Inicializa la base de datos PostgreSQL"""
    try:
        log_info("Inicializando base de datos PostgreSQL...")
        init_database()
        log_info("Base de datos inicializada correctamente")
        return True
    except Exception as e:
        log_error(f"Error inicializando base de datos: {str(e)}")
        print(f"❌ Error detallado: {str(e)}")
        return False

def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración de MySQL a PostgreSQL (Supabase)")
    print("=" * 60)
    
    # Paso 1: Instalar dependencias
    print("\n📦 Paso 1: Instalando dependencias...")
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        return False
    print("✅ Dependencias instaladas")
    
    # Paso 2: Probar conexión
    print("\n🔗 Paso 2: Probando conexión...")
    if not test_connection():
        print("❌ Error conectando a PostgreSQL")
        print("Verifica tu archivo .env y las credenciales de Supabase")
        return False
    print("✅ Conexión exitosa")
    
    # Paso 3: Migrar base de datos
    print("\n🗄️ Paso 3: Inicializando base de datos...")
    if not migrate_database():
        print("❌ Error inicializando base de datos")
        return False
    print("✅ Base de datos inicializada")
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("=" * 60)
    print("Tu aplicación ahora usa PostgreSQL con Supabase")
    print("Puedes ejecutar: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)