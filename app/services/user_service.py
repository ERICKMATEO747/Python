from app.config.database import get_db_connection
from app.models.user_visit import UserVisit
from app.utils.logger import log_info, log_error
from datetime import datetime
from typing import Dict, Optional

class UserService:
    @staticmethod
    def get_user_profile(user_id: int) -> Optional[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT u.*, m.municipio 
                    FROM users u 
                    LEFT JOIN municipalities m ON u.municipality_id = m.id 
                    WHERE u.id = %s
                """, (user_id,))
                return cursor.fetchone()
        except Exception as e:
            log_error("Error obteniendo perfil de usuario", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def update_user_profile(user_id: int, data: Dict) -> bool:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                fields = []
                values = []
                
                for field, value in data.items():
                    if value is not None:
                        fields.append(f"{field} = %s")
                        values.append(value)
                
                if fields:
                    values.append(user_id)
                    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
                    cursor.execute(query, values)
                    connection.commit()
                    return True
                return False
        except Exception as e:
            log_error("Error actualizando perfil", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def get_user_visits(user_id: int):
        log_info(f"Obteniendo visitas del usuario: {user_id}")
        return UserVisit.get_user_visits(user_id)
    
    @staticmethod
    def generate_qr_code(user_id: int, business_id: int, visit_date: datetime):
        """Genera código QR sin registrar visita"""
        log_info(f"Generando QR para usuario {user_id} en negocio {business_id}")
        qr_code = UserVisit.generate_qr_code(user_id, business_id, visit_date)
        return qr_code is not None, qr_code
    
    @staticmethod
    def validate_qr_visit(qr_token: str, expected_user_id: int, expected_business_id: int) -> Dict:
        """Valida QR y registra visita efectiva"""
        from datetime import datetime
        
        qr_data = UserVisit.verify_qr_code(qr_token)
        if not qr_data:
            return {"valid": False, "error": "Código QR inválido o corrupto"}
        
        if qr_data["user_id"] != expected_user_id:
            return {"valid": False, "error": "El código QR no pertenece a este usuario"}
        
        if qr_data["business_id"] != expected_business_id:
            return {"valid": False, "error": "El código QR no es válido para este negocio"}
        
        visit_date = datetime.fromtimestamp(qr_data["visit_timestamp"])
        current_date = datetime.now()
        
        if visit_date.year != current_date.year or visit_date.month != current_date.month:
            return {"valid": False, "error": "El código QR no corresponde al mes actual"}
        
        # Verificar si ya existe la visita
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM user_visits 
                    WHERE user_id = %s AND business_id = %s 
                    AND DATE(visit_date) = DATE(%s)
                """, (expected_user_id, expected_business_id, visit_date))
                
                if cursor.fetchone()["count"] > 0:
                    return {"valid": False, "error": "Esta visita ya fue registrada anteriormente"}
        except Exception as e:
            log_error("Error verificando visita existente", error=e)
            return {"valid": False, "error": "Error interno validando la visita"}
        finally:
            connection.close()
        
        # Registrar visita efectiva
        if UserVisit.register_visit(expected_user_id, expected_business_id, visit_date):
            return {
                "valid": True,
                "visit_registered": True,
                "visit_data": {
                    "user_id": qr_data["user_id"],
                    "business_id": qr_data["business_id"],
                    "visit_date": visit_date.isoformat()
                }
            }
        else:
            return {"valid": False, "error": "Error registrando la visita"}