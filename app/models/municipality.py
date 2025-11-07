from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict

class Municipality:
    @staticmethod
    def get_all() -> List[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM municipalities WHERE active = 1 ORDER BY municipio")
                return cursor.fetchall()
        except Exception as e:
            log_error("Error obteniendo municipios", error=e)
            return []
        finally:
            connection.close()