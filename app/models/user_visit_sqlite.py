from app.config.database_sqlite import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict
from datetime import datetime

class UserVisit:
    @staticmethod
    def get_user_visits_with_rounds(user_id: int) -> List[Dict]:
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    b.id as business_id,
                    b.name as business_name,
                    COUNT(v.id) as visit_count,
                    MAX(v.visit_date) as last_visit_date,
                    MAX(v.id) as latest_visit_id,
                    COALESCE(r.round_number, 1) as round_number,
                    COALESCE(r.progress_in_round, 0) as progress_in_round,
                    b.visits_for_prize as max_visits_per_round,
                    COALESCE(r.is_reward_claimed, 0) as is_reward_claimed,
                    v.visit_month
                FROM user_visits v
                JOIN businesses b ON v.business_id = b.id
                LEFT JOIN user_rounds r ON r.user_id = v.user_id AND r.business_id = v.business_id
                WHERE v.user_id = ?
                GROUP BY b.id, b.name, v.visit_month, r.round_number, r.progress_in_round, r.is_reward_claimed
                ORDER BY last_visit_date DESC
            """, (user_id,))
            
            visits = cursor.fetchall()
            return [dict(visit) for visit in visits]
        except Exception as e:
            log_error("Error obteniendo visitas del usuario", error=e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def register_visit(user_id: int, business_id: int, visit_date: datetime) -> int:
        """Registra una nueva visita en la base de datos"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            
            # Verificar si ya existe una visita para este usuario, negocio y fecha
            visit_month = visit_date.strftime('%Y-%m')
            cursor.execute("""
                SELECT id FROM user_visits 
                WHERE user_id = ? AND business_id = ? AND visit_month = ?
                AND DATE(visit_date) = DATE(?)
            """, (user_id, business_id, visit_month, visit_date.isoformat()))
            
            existing_visit = cursor.fetchone()
            if existing_visit:
                return existing_visit['id']
            
            # Insertar nueva visita
            cursor.execute("""
                INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                VALUES (?, ?, ?, ?)
            """, (user_id, business_id, visit_date.isoformat(), visit_month))
            
            visit_id = cursor.lastrowid
            connection.commit()
            
            # Actualizar progreso en rondas
            UserVisit._update_user_round(user_id, business_id, visit_id, connection)
            
            return visit_id
        except Exception as e:
            connection.rollback()
            log_error("Error registrando visita", error=e)
            raise e
        finally:
            connection.close()
    
    @staticmethod
    def _update_user_round(user_id: int, business_id: int, visit_id: int, connection):
        """Actualiza el progreso del usuario en la ronda actual"""
        try:
            cursor = connection.cursor()
            
            # Obtener o crear ronda actual
            cursor.execute("""
                SELECT id, progress_in_round FROM user_rounds
                WHERE user_id = ? AND business_id = ? AND is_completed = 0
                ORDER BY round_number DESC LIMIT 1
            """, (user_id, business_id))
            
            current_round = cursor.fetchone()
            
            if current_round:
                # Actualizar progreso en ronda existente
                new_progress = current_round['progress_in_round'] + 1
                cursor.execute("""
                    UPDATE user_rounds 
                    SET progress_in_round = ?, last_visit_id = ?
                    WHERE id = ?
                """, (new_progress, visit_id, current_round['id']))
            else:
                # Crear nueva ronda
                cursor.execute("""
                    INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, last_visit_id)
                    VALUES (?, ?, 1, 1, ?)
                """, (user_id, business_id, visit_id))
            
            connection.commit()
        except Exception as e:
            log_error("Error actualizando ronda de usuario", error=e)
            raise e