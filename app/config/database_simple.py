import psycopg2
import psycopg2.extras
from app.config.settings import settings
from app.utils.logger import log_info, log_error

def get_db_connection():
    """Obtiene conexión a la base de datos PostgreSQL"""
    try:
        connection = psycopg2.connect(
            settings.database_url,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        return connection
    except Exception as e:
        raise Exception(f"Error conectando a la base de datos: {str(e)}")

def init_database():
    """Inicializa la base de datos - versión simplificada"""
    try:
        log_info("Base de datos ya inicializada con migrate_simple.py")
        return True
    except Exception as e:
        log_error(f"Error: {str(e)}")
        return False