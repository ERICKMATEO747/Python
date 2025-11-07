import pymysql
from app.config.settings import settings
from app.utils.logger import log_info

def get_db_connection():
    """Obtiene conexión a la base de datos MySQL"""
    try:
        # Parsear URL de conexión
        url_parts = settings.database_url.replace("mysql+pymysql://", "").split("/")
        auth_db = url_parts[1]
        host_port_user = url_parts[0].split("@")
        host_port = host_port_user[1].split(":")
        user_pass = host_port_user[0].split(":")
        
        connection = pymysql.connect(
            host=host_port[0],
            port=int(host_port[1]),
            user=user_pass[0],
            password=user_pass[1],
            database=auth_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        raise Exception(f"Error conectando a la base de datos: {str(e)}")

def init_database():
    """Inicializa la base de datos y crea las tablas si no existen"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Tabla users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NULL,
                    telefono VARCHAR(20) UNIQUE NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_contact CHECK (email IS NOT NULL OR telefono IS NOT NULL)
                )
            """)
            
            # Tabla otp_codes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS otp_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(100) NOT NULL,
                    otp_code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_email_otp (email, otp_code),
                    INDEX idx_expires (expires_at)
                )
            """)
            
            # Tabla user_types
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type_name VARCHAR(50) NOT NULL UNIQUE,
                    type_hash VARCHAR(64) NOT NULL UNIQUE,
                    description VARCHAR(200),
                    active TINYINT(1) DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insertar tipos de usuario por defecto
            cursor.execute("""
                INSERT IGNORE INTO user_types (type_name, type_hash, description) VALUES 
                ('cliente', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'Usuario cliente final'),
                ('negocio', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1', 'Usuario propietario de negocio'),
                ('admin', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456a1b2', 'Administrador del sistema')
            """)
            
            # Verificar y agregar columna user_type_id si no existe
            cursor.execute("""
                SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'user_type_id'
            """)
            column_exists = cursor.fetchone()['count'] > 0
            
            if not column_exists:
                log_info("Agregando columna user_type_id a tabla users")
                cursor.execute("ALTER TABLE users ADD COLUMN user_type_id INT NOT NULL DEFAULT 1")
                
                # Verificar si la foreign key ya existe
                cursor.execute("""
                    SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'users' 
                    AND COLUMN_NAME = 'user_type_id' 
                    AND REFERENCED_TABLE_NAME = 'user_types'
                """)
                fk_exists = cursor.fetchone()['count'] > 0
                
                if not fk_exists:
                    cursor.execute("ALTER TABLE users ADD FOREIGN KEY (user_type_id) REFERENCES user_types(id)")
                    log_info("Foreign key user_type_id agregada exitosamente")
            else:
                log_info("Columna user_type_id ya existe en tabla users")
            
        connection.commit()
    finally:
        connection.close()