from app.config.database_sqlite import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict, Optional

class Business:
    @staticmethod
    def get_all(user_id: int = None) -> List[Dict]:
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT b.*, m.municipio, 0 as unclaimed_coupons
                FROM businesses b 
                LEFT JOIN municipalities m ON b.municipality_id = m.id 
                WHERE b.active = 1 
                ORDER BY b.name
            """)
            
            businesses = cursor.fetchall()
            return [dict(business) for business in businesses]
        except Exception as e:
            log_error("Error obteniendo negocios", error=e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(business_id: int, user_id: int = None) -> Optional[Dict]:
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT b.*, m.municipio, 0 as unclaimed_coupons
                FROM businesses b 
                LEFT JOIN municipalities m ON b.municipality_id = m.id 
                WHERE b.id = ? AND b.active = 1
            """, (business_id,))
            
            business = cursor.fetchone()
            return dict(business) if business else None
        except Exception as e:
            log_error("Error obteniendo negocio", error=e)
            return None
        finally:
            connection.close()