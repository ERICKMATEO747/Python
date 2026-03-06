#!/usr/bin/env python3
"""
Script de migración simplificado para PostgreSQL
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def init_database_simple():
    """Inicializa la base de datos PostgreSQL de forma simple"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("Creando tabla users...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    telefono VARCHAR(20) UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    user_type_id INTEGER NOT NULL DEFAULT 1,
                    municipality_id BIGINT,
                    avatar VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_contact CHECK (email IS NOT NULL OR telefono IS NOT NULL)
                )
            """)
            
            print("Creando tabla user_types...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_types (
                    id SERIAL PRIMARY KEY,
                    type_name VARCHAR(50) NOT NULL UNIQUE,
                    type_hash VARCHAR(64) NOT NULL UNIQUE,
                    description VARCHAR(200),
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Insertando tipos de usuario...")
            cursor.execute("SELECT COUNT(*) as count FROM user_types")
            result = cursor.fetchone()
            user_types_count = result['count'] if result else 0
            
            if user_types_count == 0:
                cursor.execute("""
                    INSERT INTO user_types (type_name, type_hash, description) VALUES 
                    ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
                    ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio'),
                    ('admin', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1b2', 'Administrador del sistema')
                """)
                print("✅ Tipos de usuario insertados")
            
            print("Creando tabla municipalities...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS municipalities (
                    id BIGSERIAL PRIMARY KEY,
                    municipio VARCHAR(100) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Creando tabla businesses...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS businesses (
                    id BIGSERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL UNIQUE,
                    category VARCHAR(100) NOT NULL,
                    address TEXT,
                    municipality_id BIGINT REFERENCES municipalities(id),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    logo VARCHAR(500),
                    description TEXT,
                    rating DECIMAL(2,1) DEFAULT 0.0,
                    visits_for_prize INTEGER DEFAULT 6,
                    facebook VARCHAR(500),
                    instagram VARCHAR(500),
                    tiktok VARCHAR(500),
                    whatsapp VARCHAR(500),
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Creando tabla user_visits...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_visits (
                    id BIGSERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    visit_date TIMESTAMP NOT NULL,
                    visit_month VARCHAR(7) NOT NULL,
                    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'cancelled')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Creando tabla user_rounds...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_rounds (
                    id BIGSERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    business_id BIGINT NOT NULL REFERENCES businesses(id),
                    round_number INTEGER NOT NULL DEFAULT 1,
                    progress_in_round INTEGER NOT NULL DEFAULT 0,
                    round_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
                    is_reward_claimed BOOLEAN NOT NULL DEFAULT FALSE,
                    last_visit_id BIGINT NULL
                )
            """)
            
            print("Agregando foreign keys...")
            # Agregar foreign keys con manejo de errores
            try:
                cursor.execute("ALTER TABLE users ADD CONSTRAINT fk_user_type FOREIGN KEY (user_type_id) REFERENCES user_types(id)")
            except psycopg2.errors.DuplicateObject:
                pass  # Ya existe
            
            try:
                cursor.execute("ALTER TABLE users ADD CONSTRAINT fk_municipality FOREIGN KEY (municipality_id) REFERENCES municipalities(id)")
            except psycopg2.errors.DuplicateObject:
                pass  # Ya existe
            
            print("Insertando datos de prueba...")
            cursor.execute("SELECT COUNT(*) as count FROM municipalities")
            result = cursor.fetchone()
            municipality_count = result['count'] if result else 0
            
            if municipality_count == 0:
                cursor.execute("""
                    INSERT INTO municipalities (municipio, state) VALUES
                    ('Papantla', 'Veracruz'),
                    ('Coatzintla', 'Veracruz'),
                    ('Poza Rica', 'Veracruz'),
                    ('Tuxpan', 'Veracruz')
                """)
                print("✅ Municipios insertados")
            
            cursor.execute("SELECT COUNT(*) as count FROM businesses")
            result = cursor.fetchone()
            business_count = result['count'] if result else 0
            
            if business_count == 0:
                cursor.execute("""
                    INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating) VALUES
                    ('Restaurante El Totonaco', 'Restaurante', 'Calle Enríquez 123, Centro', 1, '7841234567', 'contacto@eltotonaco.com', 'Comida tradicional veracruzana', 4.5),
                    ('Café Vanilla', 'Cafetería', 'Av. 20 de Noviembre 45', 2, '7822345678', 'info@cafevanilla.com', 'Café de especialidad y vainilla', 4.2)
                """)
                print("✅ Businesses insertados")
            
            connection.commit()
            print("🎉 ¡Base de datos inicializada correctamente!")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando migración a PostgreSQL...")
    if init_database_simple():
        print("✅ Migración completada exitosamente")
        print("Puedes ejecutar: python main.py")
    else:
        print("❌ Error en la migración")