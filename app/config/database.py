import pymysql
from app.config.settings import settings

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
    """Inicializa la base de datos y crea la tabla users si no existe"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
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
        connection.commit()
    finally:
        connection.close()