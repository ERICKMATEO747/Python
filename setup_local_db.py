#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import bcrypt

def setup_local_db():
    """Configura base de datos PostgreSQL local"""
    try:
        # Conectar a PostgreSQL
        connection = psycopg2.connect(
            host="localhost",
            database="auth_api",
            user="postgres", 
            password="postgres",
            port="5432",
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("Creando tablas...")
            
            # Tabla user_types
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_types (
                    id SERIAL PRIMARY KEY,
                    type_name VARCHAR(50) NOT NULL UNIQUE,
                    type_hash VARCHAR(64) NOT NULL UNIQUE,
                    description VARCHAR(200),
                    active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Tabla users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    telefono VARCHAR(20) UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    user_type_id INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_contact CHECK (email IS NOT NULL OR telefono IS NOT NULL)
                )
            """)
            
            # Insertar tipos de usuario
            cursor.execute("SELECT COUNT(*) FROM user_types")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO user_types (type_name, type_hash, description) VALUES 
                    ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
                    ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio')
                """)
                print("Tipos de usuario creados")
            
            # Crear usuarios de prueba
            password = "negocio123"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
            
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO users (nombre, email, password, user_type_id) VALUES
                    ('Test Cliente', 'cliente@test.com', %s, 1),
                    ('Carlos Hernandez', 'carlos@eltotonaco.com', %s, 2)
                """, (hashed_password.decode('utf-8'), hashed_password.decode('utf-8')))
                print("Usuarios de prueba creados")
            
            connection.commit()
            print("Base de datos configurada exitosamente")
            print("Usuarios disponibles:")
            print("- cliente@test.com / negocio123")
            print("- carlos@eltotonaco.com / negocio123")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    setup_local_db()