import psycopg2
import psycopg2.extras
from app.utils.logger import log_info, log_error

def get_db_connection():
    """Obtiene conexión a PostgreSQL local"""
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="auth_api",
            user="postgres",
            password="postgres",
            port="5432",
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        return connection
    except Exception as e:
        raise Exception(f"Error conectando a PostgreSQL local: {str(e)}")

def init_database():
    """Inicializa la base de datos local"""
    try:
        log_info("Conectando a PostgreSQL local")
        return True
    except Exception as e:
        log_error(f"Error: {str(e)}")
        return False