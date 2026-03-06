import sqlite3
import bcrypt
from app.utils.logger import log_info, log_error

def get_db_connection():
    """Obtiene conexión a SQLite"""
    try:
        connection = sqlite3.connect('auth_api.db', check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA encoding = "UTF-8"')
        return connection
    except Exception as e:
        raise Exception(f"Error conectando a SQLite: {str(e)}")

def init_database():
    """Inicializa SQLite con datos de prueba"""
    try:
        conn = sqlite3.connect('auth_api.db', check_same_thread=False)
        conn.execute('PRAGMA encoding = "UTF-8"')
        cursor = conn.cursor()
        
        # Crear tablas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_types (
                id INTEGER PRIMARY KEY,
                type_name TEXT UNIQUE,
                type_hash TEXT UNIQUE,
                description TEXT,
                active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT UNIQUE,
                password TEXT NOT NULL,
                user_type_id INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT,
                description TEXT,
                rating REAL DEFAULT 0.0,
                visits_for_prize INTEGER DEFAULT 6,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar tipos de usuario
        cursor.execute("SELECT COUNT(*) FROM user_types")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO user_types (type_name, type_hash, description) VALUES 
                ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
                ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio')
            ''')
        
        # Crear usuarios de prueba
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            password = "123456"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
            
            cursor.execute('''
                INSERT INTO users (nombre, email, password, user_type_id) VALUES
                ('Admin Test', 'admin@test.com', ?, 1),
                ('Negocio Test', 'negocio@test.com', ?, 2),
                ('Cliente Test', 'cliente@test.com', ?, 1)
            ''', (hashed_password.decode('utf-8'), hashed_password.decode('utf-8'), hashed_password.decode('utf-8')))
        
        # Crear negocios de prueba
        cursor.execute("SELECT COUNT(*) FROM businesses")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO businesses (name, category, address, phone, email, description, rating) VALUES
                ('Restaurante El Totonaco', 'Restaurante', 'Calle Enriquez 123, Centro', '7841234567', 'contacto@eltotonaco.com', 'Comida tradicional veracruzana', 4.5),
                ('Cafe Vanilla', 'Cafeteria', 'Av. 20 de Noviembre 45', '7822345678', 'info@cafevanilla.com', 'Cafe de especialidad y vainilla', 4.2),
                ('Pizzeria Don Juan', 'Pizzeria', 'Plaza Principal 12', '7843333333', 'juan@pizzeria.com', 'Las mejores pizzas artesanales', 4.7)
            ''')
        
        conn.commit()
        conn.close()
        log_info("SQLite inicializado con usuarios y negocios de prueba")
        return True
    except Exception as e:
        log_error(f"Error inicializando SQLite: {str(e)}")
        return False