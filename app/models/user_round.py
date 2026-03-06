from app.config.database import get_db_connection
from app.utils.logger import log_error, log_info
from typing import Dict, Optional, List
from datetime import datetime

class UserRound:
    @staticmethod
    def get_or_create_current_round(user_id: int, business_id: int) -> Dict:
        """Obtiene la ronda actual del usuario para un negocio o crea una nueva"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Buscar ronda actual (no completada)
                cursor.execute("""
                    SELECT * FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s AND is_completed = FALSE
                    ORDER BY round_number DESC LIMIT 1
                """, (user_id, business_id))
                
                current_round = cursor.fetchone()
                
                if current_round:
                    return dict(current_round)
                
                # No hay ronda actual, crear nueva
                # Obtener el número de la siguiente ronda
                cursor.execute("""
                    SELECT COALESCE(MAX(round_number), 0) + 1 as next_round
                    FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s
                """, (user_id, business_id))
                
                result = cursor.fetchone()
                next_round_number = result['next_round'] if result else 1
                
                # Crear nueva ronda
                cursor.execute("""
                    INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, 
                                           round_start_date, is_completed, is_reward_claimed)
                    VALUES (%s, %s, %s, 0, NOW(), FALSE, FALSE)
                    RETURNING id
                """, (user_id, business_id, next_round_number))
                
                round_id = cursor.fetchone()['id']
                connection.commit()
                
                # Retornar la nueva ronda
                cursor.execute("SELECT * FROM user_rounds WHERE id = %s", (round_id,))
                new_round = cursor.fetchone()
                
                log_info(f"Nueva ronda {next_round_number} creada para usuario {user_id} en negocio {business_id}")
                return dict(new_round)
                
        except Exception as e:
            log_error("Error obteniendo/creando ronda actual", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def update_round_progress(user_id: int, business_id: int, visit_id: int) -> bool:
        """Actualiza el progreso de la ronda actual al registrar una visita"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener ronda actual (no completada)
                current_round = UserRound.get_or_create_current_round(user_id, business_id)
                if not current_round:
                    return False
                
                # Solo incrementar si la ronda no está completada
                if not current_round['is_completed']:
                    new_progress = current_round['progress_in_round'] + 1
                    
                    cursor.execute("""
                        UPDATE user_rounds 
                        SET progress_in_round = %s, last_visit_id = %s
                        WHERE id = %s
                    """, (new_progress, visit_id, current_round['id']))
                    
                    connection.commit()
                    log_info(f"Progreso actualizado a {new_progress} para ronda {current_round['round_number']}")
                
                return True
                
        except Exception as e:
            log_error("Error actualizando progreso de ronda", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def complete_round_and_claim_reward(user_id: int, business_id: int) -> bool:
        """Marca la ronda como completada, premio reclamado y crea nueva ronda"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener ronda actual
                cursor.execute("""
                    SELECT * FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s AND is_completed = FALSE
                    ORDER BY round_number DESC LIMIT 1
                """, (user_id, business_id))
                
                current_round = cursor.fetchone()
                if not current_round:
                    return False
                
                # Marcar como completada y premio reclamado
                cursor.execute("""
                    UPDATE user_rounds 
                    SET is_completed = TRUE, is_reward_claimed = TRUE, completed_at = NOW()
                    WHERE id = %s
                """, (current_round['id'],))
                
                # Crear nueva ronda con progreso 0
                next_round_number = current_round['round_number'] + 1
                cursor.execute("""
                    INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round,
                                           round_start_date, is_completed, is_reward_claimed)
                    VALUES (%s, %s, %s, 0, NOW(), FALSE, FALSE)
                """, (user_id, business_id, next_round_number))
                
                connection.commit()
                
                log_info(f"Ronda {current_round['round_number']} completada, iniciada ronda {next_round_number}")
                return True
                
        except Exception as e:
            log_error("Error completando ronda", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def get_current_round_only(user_id: int, business_id: int) -> Optional[Dict]:
        """Obtiene SOLO la ronda actual (no completada) para el endpoint /visits"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Buscar ronda actual (no completada)
                cursor.execute("""
                    SELECT * FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s AND is_completed = FALSE
                    ORDER BY round_number DESC LIMIT 1
                """, (user_id, business_id))
                
                result = cursor.fetchone()
                return dict(result) if result else None
                
        except Exception as e:
            log_error("Error obteniendo ronda actual", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def get_user_round_stats(user_id: int, business_id: int) -> Dict:
        """Obtiene estadísticas de rondas del usuario para un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener ronda actual
                current_round = UserRound.get_or_create_current_round(user_id, business_id)
                
                # Contar rondas completadas
                cursor.execute("""
                    SELECT COUNT(*) as completed_rounds
                    FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s AND is_completed = TRUE
                """, (user_id, business_id))
                
                result = cursor.fetchone()
                completed_rounds = result['completed_rounds'] if result else 0
                
                return {
                    "current_round": current_round,
                    "completed_rounds": completed_rounds
                }
                
        except Exception as e:
            log_error("Error obteniendo estadísticas de rondas", error=e)
            return {"current_round": None, "completed_rounds": 0}
        finally:
            connection.close()
    
    @staticmethod
    def migrate_existing_visits(user_id: int, business_id: int) -> bool:
        """Migra visitas existentes al sistema de rondas"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar si ya tiene rondas
                cursor.execute("""
                    SELECT COUNT(*) as count FROM user_rounds 
                    WHERE user_id = %s AND business_id = %s
                """, (user_id, business_id))
                
                result = cursor.fetchone()
                if result['count'] > 0:
                    return True  # Ya migrado
                
                # Contar visitas existentes del mes actual
                cursor.execute("""
                    SELECT COUNT(*) as visits FROM user_visits 
                    WHERE user_id = %s AND business_id = %s 
                    AND visit_month = TO_CHAR(NOW(), 'YYYY-MM')
                """, (user_id, business_id))
                
                result = cursor.fetchone()
                existing_visits = result['visits'] if result else 0
                
                if existing_visits > 0:
                    # Obtener max_visits_per_round del negocio (asumiendo 6 por defecto)
                    max_visits = 6
                    
                    # Crear ronda inicial con el progreso actual
                    progress = min(existing_visits, max_visits)
                    
                    cursor.execute("""
                        INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round,
                                               round_start_date, is_completed, is_reward_claimed)
                        VALUES (%s, %s, 1, %s, NOW(), FALSE, FALSE)
                    """, (user_id, business_id, progress))
                    
                    connection.commit()
                    log_info(f"Migración completada: {existing_visits} visitas -> ronda 1 con progreso {progress}")
                
                return True
                
        except Exception as e:
            log_error("Error en migración de visitas", error=e)
            return False
        finally:
            connection.close()