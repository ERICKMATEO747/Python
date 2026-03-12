from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import sys
import os

class Settings(BaseSettings):
    """Configuración de la aplicación usando variables de entorno"""
    
    # Configuración de Base de Datos (con valor por defecto para desarrollo)
    database_url: str = "postgresql://postgres:postgres@localhost:5432/flevo_db"
    
    # Configuración JWT (con valor por defecto INSEGURO para desarrollo)
    jwt_secret_key: str = "CHANGE-THIS-SECRET-KEY-IN-PRODUCTION-USE-ENV-FILE"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    
    # Configuración Supabase (Opcional)
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    
    # Configuración SMTP (Opcional)
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "Flevo App"
    
    # Configuración VAPID (Opcional)
    vapid_public_key: str = ""
    vapid_private_key: str = ""
    vapid_subject: str = "mailto:flevoapp@gmail.com"
    
    # Configuración del Servidor
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True
    )

def get_settings():
    """Obtiene configuración con validación mejorada"""
    return Settings()

# Inicializar settings
try:
    settings = Settings()
    
    # Verificar si existe .env
    if not os.path.exists(".env"):
        print("\n" + "="*60)
        print("  MODO DESARROLLO: Usando valores por defecto")
        print("="*60)
        print("\nEl archivo .env no fue encontrado")
        print("Usando configuracion por defecto (SOLO DESARROLLO)")
        print("\nIMPORTANTE: NO usar en produccion")
        print("\nPara configurar correctamente:")
        print("   1. Copia: copy .env.example .env")
        print("   2. Edita .env con tus valores")
        print("\n" + "="*60 + "\n")
    elif settings.jwt_secret_key == "CHANGE-THIS-SECRET-KEY-IN-PRODUCTION-USE-ENV-FILE":
        print("\n" + "="*60)
        print("  ADVERTENCIA: JWT_SECRET_KEY por defecto")
        print("="*60)
        print("\nGenera una clave segura:")
        print("   python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
        print("\n" + "="*60 + "\n")
        
except Exception as e:
    print("\n" + "="*60)
    print("  ERROR DE CONFIGURACION")
    print("="*60)
    print(f"\nError: {e}\n")
    print("Solucion:")
    print("   1. Crea el archivo .env: copy .env.example .env")
    print("   2. Verifica el formato de las variables")
    print("   3. Ejecuta: python verify_config.py")
    print("\n" + "="*60 + "\n")
    sys.exit(1)