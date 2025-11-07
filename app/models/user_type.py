from app.config.database import get_db_connection
from app.utils.logger import log_info, log_error
from typing import Optional, Dict

class UserType:
    """Modelo para tipos de usuario"""
    
    @staticmethod
    def get_by_hash(type_hash: str) -> Optional[Dict]:
        """Obtiene tipo de usuario por hash"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM user_types WHERE type_hash = %s AND active = 1", (type_hash,))
                return cursor.fetchone()
        except Exception as e:
            log_error("Error obteniendo tipo de usuario", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def get_all_active() -> list:
        """Obtiene todos los tipos de usuario activos"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM user_types WHERE active = 1 ORDER BY id")
                return cursor.fetchall()
        except Exception as e:
            log_error("Error obteniendo tipos de usuario", error=e)
            return []
        finally:
            connection.close()