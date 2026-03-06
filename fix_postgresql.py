#!/usr/bin/env python3
"""
Script para arreglar errores de PostgreSQL
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def fix_postgresql_errors():
    """Arregla los errores de PostgreSQL"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("=== ARREGLANDO ERRORES DE POSTGRESQL ===")
            
            # 1. Crear tabla user_rewards si no existe
            print("1. Creando tabla user_rewards...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_rewards (
                    id BIGSERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    reward_id INTEGER,
                    coupon_code VARCHAR(50) UNIQUE,
                    qr_code TEXT,
                    status VARCHAR(20) DEFAULT 'vigente' CHECK (status IN ('vigente', 'reclamado', 'usado', 'expirado')),
                    expires_at TIMESTAMP,
                    claimed_at TIMESTAMP,
                    redeemed_at TIMESTAMP,
                    reclamado BOOLEAN DEFAULT FALSE,
                    redimido BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("✅ Tabla user_rewards creada")
            
            # 2. Crear tabla rewards si no existe (referenciada por user_rewards)
            print("2. Creando tabla rewards...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rewards (
                    id SERIAL PRIMARY KEY,
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    reward_type VARCHAR(50) DEFAULT 'discount',
                    value DECIMAL(10,2),
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("✅ Tabla rewards creada")
            
            # 3. Agregar algunos rewards de ejemplo
            cursor.execute("SELECT COUNT(*) as count FROM rewards")
            rewards_count = cursor.fetchone()['count']
            
            if rewards_count == 0:
                print("3. Agregando rewards de ejemplo...")
                cursor.execute("SELECT id, name FROM businesses ORDER BY id LIMIT 5")
                businesses = cursor.fetchall()
                
                rewards_data = []
                for business in businesses:
                    rewards_data.extend([
                        (business['id'], f'10% de descuento en {business["name"]}', 'Descuento del 10% en tu próxima compra', 'discount', 10.00, True),
                        (business['id'], f'Producto gratis en {business["name"]}', 'Obtén un producto gratis', 'free_item', 0.00, True)
                    ])
                
                cursor.executemany("""
                    INSERT INTO rewards (business_id, title, description, reward_type, value, active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, rewards_data)
                connection.commit()
                print(f"✅ {len(rewards_data)} rewards agregados")
            
            print("\n=== VERIFICACIÓN FINAL ===")
            
            # Verificar tablas creadas
            tables = ['user_rewards', 'rewards']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"{table}: {count} registros")
        
        connection.close()
        print("\n🎉 ¡Errores de PostgreSQL arreglados!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Arreglando errores de PostgreSQL...")
    if fix_postgresql_errors():
        print("\n✅ Errores arreglados")
        print("Ahora los endpoints deberían funcionar correctamente")
    else:
        print("❌ Error en el proceso")