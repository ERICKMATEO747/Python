from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict, Optional

class Reward:
    @staticmethod
    def create(business_id: int, title: str, description: str, terms_conditions: str, validity_days: int = 30) -> Optional[int]:
        """Crea un nuevo premio para un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO rewards (business_id, title, description, terms_conditions, validity_days)
                    VALUES (%s, %s, %s, %s, %s)
                """, (business_id, title, description, terms_conditions, validity_days))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            log_error("Error creando premio", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def get_by_business_id(business_id: int) -> List[Dict]:
        """Obtiene todos los premios activos de un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM rewards 
                    WHERE business_id = %s AND is_active = 1
                    ORDER BY created_at DESC
                """, (business_id,))
                return cursor.fetchall()
        except Exception as e:
            log_error("Error obteniendo premios del negocio", error=e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(reward_id: int) -> Optional[Dict]:
        """Obtiene un premio por ID"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM rewards WHERE id = %s AND is_active = 1", (reward_id,))
                return cursor.fetchone()
        except Exception as e:
            log_error("Error obteniendo premio", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def update(reward_id: int, **kwargs) -> bool:
        """Actualiza un premio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                fields = []
                values = []
                
                for field, value in kwargs.items():
                    if value is not None:
                        fields.append(f"{field} = %s")
                        values.append(value)
                
                if fields:
                    values.append(reward_id)
                    query = f"UPDATE rewards SET {', '.join(fields)} WHERE id = %s"
                    cursor.execute(query, values)
                    connection.commit()
                    return True
                return False
        except Exception as e:
            log_error("Error actualizando premio", error=e)
            return False
        finally:
            connection.close()