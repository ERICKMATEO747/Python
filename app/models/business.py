from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict, Optional

class Business:
    @staticmethod
    def get_all() -> List[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT b.*, m.municipio 
                    FROM businesses b 
                    LEFT JOIN municipalities m ON b.municipality_id = m.id 
                    WHERE b.active = 1 
                    ORDER BY b.name
                """)
                return cursor.fetchall()
        except Exception as e:
            log_error("Error obteniendo negocios", error=e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(business_id: int) -> Optional[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT b.*, m.municipio 
                    FROM businesses b 
                    LEFT JOIN municipalities m ON b.municipality_id = m.id 
                    WHERE b.id = %s AND b.active = 1
                """, (business_id,))
                return cursor.fetchone()
        except Exception as e:
            log_error("Error obteniendo negocio", error=e)
            return None
        finally:
            connection.close()