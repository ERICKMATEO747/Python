#!/usr/bin/env python3
"""
Script para crear tablas faltantes
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def create_missing_tables():
    """Crea las tablas que faltan"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("Creando tabla business_menu...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_menu (
                    id BIGSERIAL PRIMARY KEY,
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    producto VARCHAR(200) NOT NULL,
                    descripcion TEXT,
                    precio DECIMAL(10,2) NOT NULL,
                    categoria VARCHAR(100),
                    disponible BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Creando tabla otp_codes...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS otp_codes (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) NOT NULL,
                    otp_code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Creando índices...")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_email_otp ON otp_codes(email, otp_code)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_expires ON otp_codes(expires_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_business_month ON user_visits(user_id, business_id, visit_month)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_rounds_user_business ON user_rounds(user_id, business_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_rounds_completed ON user_rounds(is_completed)")
            
            connection.commit()
            print("✅ Tablas faltantes creadas")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Creando tablas faltantes...")
    if create_missing_tables():
        print("✅ Tablas creadas exitosamente")
    else:
        print("❌ Error creando tablas")