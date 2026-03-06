from app.config.database import get_db_connection
from app.utils.logger import log_error, log_info
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from jose import jwt
from app.config.settings import settings
import qrcode
import io
import base64

class UserVisit:
    @staticmethod
    def get_user_visits(user_id: int) -> List[Dict]:
        from app.models.user_round import UserRound
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener negocios donde el usuario tiene visitas
                cursor.execute("""
                    SELECT DISTINCT uv.business_id, b.name as business_name,
                           b.visits_for_prize as max_visits_per_round,
                           MAX(uv.visit_date) as last_visit_date,
                           MAX(uv.id) as latest_visit_id
                    FROM user_visits uv
                    JOIN businesses b ON uv.business_id = b.id
                    WHERE uv.user_id = %s
                    GROUP BY uv.business_id, b.name, b.visits_for_prize
                    ORDER BY last_visit_date DESC
                """, (user_id,))
                businesses = cursor.fetchall()
                
                # Para cada negocio, obtener SOLO la ronda actual
                current_rounds = []
                for business in businesses:
                    business_id = business['business_id']
                    
                    # Migrar visitas existentes si es necesario
                    UserRound.migrate_existing_visits(user_id, business_id)
                    
                    # Obtener SOLO la ronda actual
                    current_round = UserRound.get_current_round_only(user_id, business_id)
                    
                    if not current_round:
                        # Si no hay ronda actual, crear una
                        current_round = UserRound.get_or_create_current_round(user_id, business_id)
                    
                    if current_round:
                        # Contar visitas del mes actual para esta ronda
                        cursor.execute("""
                            SELECT COUNT(*) as visit_count FROM user_visits 
                            WHERE user_id = %s AND business_id = %s 
                            AND visit_month = TO_CHAR(NOW(), 'YYYY-MM')
                        """, (user_id, business_id))
                        
                        visit_count = cursor.fetchone()['visit_count']
                        
                        round_data = {
                            'business_id': business_id,
                            'visit_month': datetime.now().strftime('%Y-%m'),
                            'business_name': business['business_name'],
                            'visit_count': visit_count,
                            'round_number': current_round['round_number'],
                            'progress_in_round': current_round['progress_in_round'],
                            'max_visits_per_round': business['max_visits_per_round'] or 6,
                            'is_reward_claimed': current_round['is_reward_claimed'],
                            'last_visit_date': business['last_visit_date'],
                            'latest_visit_id': business['latest_visit_id']
                        }
                        current_rounds.append(round_data)
                
                cursor.execute("SELECT COUNT(*) as total FROM user_visits WHERE user_id = %s", (user_id,))
                total = cursor.fetchone()['total']
                
                return {"data": current_rounds, "total_visits": total}
        except Exception as e:
            log_error("Error obteniendo visitas", error=e)
            return {"data": [], "total_visits": 0}
        finally:
            connection.close()
    
    @staticmethod
    def generate_qr_code(user_id: int, business_id: int, visit_date: datetime) -> Optional[str]:
        """Genera código QR sin guardarlo en BD"""
        try:
            qr_payload = {
                "user_id": user_id,
                "business_id": business_id,
                "visit_timestamp": int(visit_date.timestamp()),
                "exp": datetime.utcnow() + timedelta(hours=24)
            }
            qr_data = jwt.encode(qr_payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        except Exception as e:
            log_error("Error generando QR code", error=e)
            return None
    
    @staticmethod
    def register_visit(user_id: int, business_id: int, visit_date: datetime) -> bool:
        """Registra visita efectiva en BD y actualiza progreso de ronda"""
        from app.models.user_round import UserRound
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                visit_month = visit_date.strftime("%Y-%m")
                cursor.execute("""
                    INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (user_id, business_id, visit_date, visit_month))
                
                visit_id = cursor.fetchone()['id']
                connection.commit()
                
                # Actualizar progreso de ronda
                UserRound.update_round_progress(user_id, business_id, visit_id)
                
                log_info(f"Visita registrada: usuario {user_id}, negocio {business_id}")
                return True
        except Exception as e:
            log_error("Error registrando visita", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def verify_qr_code(qr_token: str) -> Optional[Dict]:
        """Verifica y decodifica un código QR encriptado"""
        try:
            payload = jwt.decode(qr_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return {
                "user_id": payload.get("user_id"),
                "business_id": payload.get("business_id"),
                "visit_timestamp": payload.get("visit_timestamp")
            }
        except Exception as e:
            log_error("Error verificando QR code", error=e)
            return None