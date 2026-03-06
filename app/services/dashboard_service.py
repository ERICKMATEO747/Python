from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import Dict
from datetime import datetime, timedelta

class DashboardService:
    """Servicio para dashboard de negocios"""
    
    @staticmethod
    def get_business_dashboard(business_id: int) -> Dict:
        """Obtiene datos completos del dashboard del negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                today = datetime.now().date()
                month_start = today.replace(day=1)
                
                # Visitas de hoy
                cursor.execute("""
                    SELECT COUNT(*) as visits_today
                    FROM user_visits
                    WHERE business_id = %s AND DATE(visit_date) = %s
                """, (business_id, today))
                visits_today = cursor.fetchone()['visits_today']
                
                # Visitas del mes
                cursor.execute("""
                    SELECT COUNT(*) as visits_month
                    FROM user_visits
                    WHERE business_id = %s AND DATE(visit_date) >= %s
                """, (business_id, month_start))
                visits_month = cursor.fetchone()['visits_month']
                
                # Premios redimidos hoy
                cursor.execute("""
                    SELECT COUNT(*) as rewards_today
                    FROM user_rewards
                    WHERE business_id = %s AND DATE(redeemed_at) = %s
                """, (business_id, today))
                rewards_today = cursor.fetchone()['rewards_today']
                
                # Premios redimidos del mes
                cursor.execute("""
                    SELECT COUNT(*) as rewards_month
                    FROM user_rewards
                    WHERE business_id = %s AND DATE(redeemed_at) >= %s
                """, (business_id, month_start))
                rewards_month = cursor.fetchone()['rewards_month']
                
                # Rondas activas
                cursor.execute("""
                    SELECT ur.user_id, ur.round_number, ur.progress_in_round, 
                           b.visits_for_prize as goal, u.nombre as user_name
                    FROM user_rounds ur
                    JOIN users u ON ur.user_id = u.id
                    JOIN businesses b ON ur.business_id = b.id
                    WHERE ur.business_id = %s AND ur.is_completed = 0
                    ORDER BY ur.progress_in_round DESC
                    LIMIT 10
                """, (business_id,))
                active_rounds = cursor.fetchall()
                
                # Visitas por día (últimos 7 días)
                cursor.execute("""
                    SELECT DATE(visit_date) as visit_date, COUNT(*) as visits
                    FROM user_visits
                    WHERE business_id = %s AND visit_date >= %s
                    GROUP BY DATE(visit_date)
                    ORDER BY visit_date DESC
                """, (business_id, today - timedelta(days=7)))
                visits_breakdown = {str(row['visit_date']): row['visits'] for row in cursor.fetchall()}
                
                # Últimos clientes del mes actual con municipio
                cursor.execute("""
                    SELECT DISTINCT u.id, u.nombre, m.municipio, MAX(uv.visit_date) as last_visit
                    FROM user_visits uv
                    JOIN users u ON uv.user_id = u.id
                    LEFT JOIN municipalities m ON u.municipality_id = m.id
                    WHERE uv.business_id = %s AND DATE(uv.visit_date) >= %s
                    GROUP BY u.id, u.nombre, m.municipio
                    ORDER BY last_visit DESC
                    LIMIT 5
                """, (business_id, month_start))
                recent_customers = cursor.fetchall()
                
                # Nuevos clientes del negocio (primera visita en el mes actual)
                cursor.execute("""
                    SELECT u.id, u.nombre, m.municipio, MIN(uv.visit_date) as first_visit
                    FROM user_visits uv
                    JOIN users u ON uv.user_id = u.id
                    LEFT JOIN municipalities m ON u.municipality_id = m.id
                    WHERE uv.business_id = %s AND DATE(uv.visit_date) >= %s
                    GROUP BY u.id, u.nombre, m.municipio
                    HAVING MIN(uv.visit_date) >= %s
                    ORDER BY first_visit DESC
                    LIMIT 10
                """, (business_id, month_start, month_start))
                new_customers = cursor.fetchall()
                
                # Estado del programa y datos del negocio
                cursor.execute("""
                    SELECT b.name, b.address, m.municipio, b.visits_for_prize, b.active as program_active
                    FROM businesses b
                    LEFT JOIN municipalities m ON b.municipality_id = m.id
                    WHERE b.id = %s
                """, (business_id,))
                business_info = cursor.fetchone()
                
                return {
                    "business_id": business_id,
                    "business_name": business_info['name'],
                    "business_address": business_info['address'],
                    "business_municipio": business_info['municipio'] or "No especificado",
                    "visits_today": visits_today,
                    "visits_month": visits_month,
                    "rewards_redeemed_today": rewards_today,
                    "rewards_redeemed_month": rewards_month,
                    "active_rounds": [
                        {
                            "user_id": round_data['user_id'],
                            "user_name": round_data['user_name'],
                            "current_round": round_data['round_number'],
                            "progress": round_data['progress_in_round'],
                            "goal": round_data['goal']
                        }
                        for round_data in active_rounds
                    ],
                    "visits_breakdown": visits_breakdown,
                    "recent_customers": [
                        {
                            "user_id": customer['id'],
                            "name": customer['nombre'],
                            "municipio": customer['municipio'] or "No especificado",
                            "last_visit": customer['last_visit'].isoformat() if customer['last_visit'] else None
                        }
                        for customer in recent_customers
                    ],
                    "new_customers_month": [
                        {
                            "user_id": customer['id'],
                            "name": customer['nombre'],
                            "municipio": customer['municipio'] or "No especificado",
                            "first_visit_date": customer['first_visit'].isoformat() if customer['first_visit'] else None
                        }
                        for customer in new_customers
                    ],
                    "program_status": {
                        "active": bool(business_info['program_active']),
                        "visits_per_round": business_info['visits_for_prize']
                    }
                }
        except Exception as e:
            log_error("Error obteniendo dashboard", error=e)
            return {}
        finally:
            connection.close()