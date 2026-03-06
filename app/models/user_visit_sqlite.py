from app.config.database_sqlite import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict

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