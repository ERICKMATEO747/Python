from app.models.reward import Reward
from app.models.user_reward import UserReward
from app.utils.logger import log_info, log_error
from typing import Dict, Optional, List

class RewardService:
    @staticmethod
    def create_reward(business_id: int, title: str, description: str, terms_conditions: str, validity_days: int = 30) -> Optional[int]:
        """Crea un nuevo premio para un negocio"""
        return Reward.create(business_id, title, description, terms_conditions, validity_days)
    
    @staticmethod
    def get_reward_by_id(reward_id: int) -> Optional[Dict]:
        """Obtiene un premio específico por ID"""
        return Reward.get_by_id(reward_id)
    
    @staticmethod
    def get_business_rewards(business_id: int) -> List[Dict]:
        """Obtiene todos los premios activos de un negocio"""
        return Reward.get_by_business_id(business_id)
    
    @staticmethod
    def update_reward(reward_id: int, **kwargs) -> bool:
        """Actualiza un premio"""
        return Reward.update(reward_id, **kwargs)
    
    @staticmethod
    def check_and_generate_reward(user_id: int, business_id: int) -> Optional[Dict]:
        """Verifica si el usuario merece un premio basado en rondas y lo genera"""
        from app.config.database import get_db_connection
        from app.models.user_round import UserRound
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener información del negocio
                cursor.execute("""
                    SELECT visits_for_prize, reward_id FROM businesses 
                    WHERE id = %s AND active = 1
                """, (business_id,))
                
                business = cursor.fetchone()
                if not business:
                    return None
                
                visits_needed = business['visits_for_prize'] or 6
                reward_id = business['reward_id']
                
                # Obtener estadísticas de ronda
                round_stats = UserRound.get_user_round_stats(user_id, business_id)
                current_round = round_stats['current_round']
                
                if not current_round:
                    return None
                
                # Verificar si alcanzó las visitas necesarias en la ronda actual
                if current_round['progress_in_round'] >= visits_needed:
                    # Verificar si ya tiene un cupón vigente para esta ronda
                    cursor.execute("""
                        SELECT COUNT(*) as count FROM user_rewards 
                        WHERE user_id = %s AND business_id = %s AND status = 'vigente'
                    """, (user_id, business_id))
                    
                    if cursor.fetchone()['count'] > 0:
                        log_info(f"Usuario {user_id} ya tiene cupón vigente para negocio {business_id}")
                        return None
                    
                    # Verificar si ya reclamó premio de esta ronda
                    if current_round['is_reward_claimed']:
                        log_info(f"Usuario {user_id} ya reclamó premio de ronda {current_round['round_number']}")
                        return None
                    
                    # Marcar que hay premio pendiente (is_reward_claimed = 0 por defecto)
                    # No cambiar el estado hasta que se reclame
                    
                    # Obtener premio del negocio
                    if reward_id:
                        cursor.execute("SELECT * FROM rewards WHERE id = %s AND is_active = 1", (reward_id,))
                    else:
                        cursor.execute("""
                            SELECT * FROM rewards 
                            WHERE business_id = %s AND is_active = 1 
                            ORDER BY created_at DESC LIMIT 1
                        """, (business_id,))
                    
                    reward = cursor.fetchone()
                    if not reward:
                        log_error(f"No hay premio configurado para negocio {business_id}")
                        return None
                    
                    # Generar cupón
                    coupon = UserReward.create_reward(
                        user_id, 
                        business_id, 
                        reward['id'], 
                        reward['validity_days']
                    )
                    
                    if coupon:
                        log_info(f"Premio generado para usuario {user_id} en ronda {current_round['round_number']}")
                        return {
                            **coupon,
                            "reward_title": reward['title'],
                            "reward_description": reward['description'],
                            "round_number": current_round['round_number']
                        }
                
                return None
        except Exception as e:
            log_error("Error verificando y generando premio con rondas", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def _reset_visit_counter(user_id: int, business_id: int):
        """Reinicia el contador de visitas del usuario para el negocio (opcional)"""
        # Esta función se puede implementar si se desea reiniciar el contador
        # Por ahora se mantiene comentada para preservar el historial
        pass
    
    @staticmethod
    def get_user_rewards(user_id: int) -> Dict:
        """Obtiene todos los cupones del usuario"""
        return UserReward.get_user_rewards(user_id)
    
    @staticmethod
    def claim_coupon(coupon_id: int, user_id: int) -> Dict:
        """Reclama un cupón y completa la ronda"""
        from app.models.user_round import UserRound
        from app.config.database import get_db_connection
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener información del cupón
                cursor.execute("""
                    SELECT ur.*, b.visits_for_prize 
                    FROM user_rewards ur
                    JOIN businesses b ON ur.business_id = b.id
                    WHERE ur.id = %s AND ur.user_id = %s AND ur.status = 'vigente'
                """, (coupon_id, user_id))
                
                coupon = cursor.fetchone()
                if not coupon:
                    return {"success": False, "error": "Cupón no válido o ya reclamado"}
                
                business_id = coupon['business_id']
                max_visits = coupon['visits_for_prize'] or 6
                
                # Si el cupón existe y está vigente, significa que ya alcanzó la meta cuando se generó
                # No necesitamos verificar el progreso actual de la ronda
                
                # Obtener la ronda donde se generó este cupón
                cursor.execute("""
                    SELECT * FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s 
                    AND progress_in_round >= %s
                    ORDER BY round_number DESC LIMIT 1
                """, (user_id, business_id, max_visits))
                
                completed_round = cursor.fetchone()
                
                # Si no hay ronda completada, verificar ronda actual
                if not completed_round:
                    round_stats = UserRound.get_user_round_stats(user_id, business_id)
                    current_round = round_stats['current_round']
                    
                    if not current_round or current_round['progress_in_round'] < max_visits:
                        return {
                            "success": False, 
                            "error": f"Necesitas {max_visits} visitas para reclamar el premio. Tienes {current_round['progress_in_round'] if current_round else 0}"
                        }
                    completed_round = current_round
                
                # Verificar que no haya reclamado ya esta ronda
                if completed_round['is_reward_claimed']:
                    return {"success": False, "error": "Ya reclamaste el premio de esta ronda"}
                
                # Reclamar cupón
                success = UserReward.claim_coupon(coupon_id, user_id)
                if not success:
                    return {"success": False, "error": "Error reclamando cupón"}
                
                # Completar ronda, reclamar premio e iniciar nueva
                UserRound.complete_round_and_claim_reward(user_id, business_id)
                
                log_info(f"Cupón {coupon_id} reclamado y ronda completada para usuario {user_id}")
                
                return {
                    "success": True,
                    "message": "Premio reclamado exitosamente. Nueva ronda iniciada.",
                    "round_completed": completed_round['round_number'],
                    "new_round_started": completed_round['round_number'] + 1
                }
                
        except Exception as e:
            log_error("Error reclamando cupón con rondas", error=e)
            return {"success": False, "error": "Error interno del servidor"}
        finally:
            connection.close()
    
    @staticmethod
    def redeem_coupon(coupon_id: int, user_id: int) -> bool:
        """Redime un cupón (usado en el negocio)"""
        return UserReward.redeem_coupon(coupon_id, user_id)
    
    @staticmethod
    def delete_reward(reward_id: int) -> bool:
        """Elimina un premio"""
        from app.config.database import get_db_connection
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM rewards WHERE id = %s", (reward_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            log_error("Error eliminando premio", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def validate_coupon_qr(qr_token: str, business_id: int) -> Dict:
        """Valida un código QR de cupón"""
        qr_data = UserReward.verify_coupon_qr(qr_token)
        
        if not qr_data:
            return {"valid": False, "error": "Código QR inválido"}
        
        if qr_data["business_id"] != business_id:
            return {"valid": False, "error": "El cupón no es válido para este negocio"}
        
        # Verificar que el cupón existe y está vigente
        coupon = UserReward.get_coupon_by_code(qr_data["coupon_code"])
        
        if not coupon:
            return {"valid": False, "error": "Cupón no encontrado"}
        
        if coupon["status"] != "vigente":
            return {"valid": False, "error": f"Cupón {coupon['status']}"}
        
        return {
            "valid": True,
            "coupon": coupon,
            "message": "Cupón válido para redención"
        }