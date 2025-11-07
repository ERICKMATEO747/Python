from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict

class BusinessMenu:
    @staticmethod
    def get_by_business_id(business_id: int) -> List[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM business_menu 
                    WHERE business_id = %s AND disponible = 1 
                    ORDER BY categoria, producto
                """, (business_id,))
                return cursor.fetchall()
        except Exception as e:
            log_error("Error obteniendo menú del negocio", error=e)
            return []
        finally:
            connection.close()