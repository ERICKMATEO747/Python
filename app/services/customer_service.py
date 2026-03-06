from app.config.database import get_db_connection
from app.utils.logger import log_error
from app.models.user_round import UserRound
from typing import Dict

class CustomerService:
    """Servicio para gestión de clientes desde el portal de negocios"""
    
    @staticmethod
    def get_customer_progress(user_id: int, business_id: int) -> Dict:
        """Obtiene el progreso actual de un cliente en el negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar que el usuario existe
                cursor.execute("SELECT nombre FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                if not user:
                    return {"success": False, "error": "Usuario no encontrado"}
                
                # Obtener configuración del negocio
                cursor.execute("""
                    SELECT visits_for_prize FROM businesses WHERE id = %s
                """, (business_id,))
                business = cursor.fetchone()
                max_visits = business['visits_for_prize'] if business else 6
                
                # Obtener ronda actual
                current_round = UserRound.get_current_round_only(user_id, business_id)
                
                if not current_round:
                    # Crear ronda inicial si no existe
                    current_round = UserRound.get_or_create_current_round(user_id, business_id)
                
                # Obtener cupones disponibles
                cursor.execute("""
                    SELECT id, coupon_code, status, expires_at, created_at
                    FROM user_rewards
                    WHERE user_id = %s AND business_id = %s AND status IN ('vigente', 'reclamado')
                    ORDER BY created_at DESC
                """, (user_id, business_id))
                
                available_coupons = cursor.fetchall()
                
                # Determinar si puede reclamar premio
                can_claim_reward = (
                    current_round and 
                    current_round['progress_in_round'] >= max_visits and 
                    not current_round['is_reward_claimed']
                )
                
                return {
                    "success": True,
                    "data": {
                        "user_id": user_id,
                        "user_name": user['nombre'],
                        "business_id": business_id,
                        "round_number": current_round['round_number'] if current_round else 1,
                        "progress_in_round": current_round['progress_in_round'] if current_round else 0,
                        "max_visits_per_round": max_visits,
                        "can_claim_reward": can_claim_reward,
                        "available_coupons": [
                            {
                                "id": coupon['id'],
                                "coupon_code": coupon['coupon_code'],
                                "status": coupon['status'],
                                "expires_at": coupon['expires_at'].isoformat() if coupon['expires_at'] else None,
                                "created_at": coupon['created_at'].isoformat() if coupon['created_at'] else None
                            }
                            for coupon in available_coupons
                        ]
                    }
                }
        except Exception as e:
            log_error("Error obteniendo progreso del cliente", error=e)
            return {"success": False, "error": "Error interno del servidor"}
        finally:
            connection.close()