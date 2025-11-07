from app.config.database import get_db_connection
from app.utils.logger import log_error
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
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT uv.business_id, uv.visit_month, b.name as business_name,
                           COUNT(*) as visit_count,
                           MAX(uv.visit_date) as last_visit_date,
                           MAX(uv.id) as latest_visit_id
                    FROM user_visits uv
                    JOIN businesses b ON uv.business_id = b.id
                    WHERE uv.user_id = %s
                    GROUP BY uv.business_id, uv.visit_month, b.name
                    ORDER BY last_visit_date DESC
                """, (user_id,))
                visits = cursor.fetchall()
                
                cursor.execute("SELECT COUNT(*) as total FROM user_visits WHERE user_id = %s", (user_id,))
                total = cursor.fetchone()['total']
                
                return {"data": visits, "total_visits": total}
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
        """Registra visita efectiva en BD"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                visit_month = visit_date.strftime("%Y-%m")
                cursor.execute("""
                    INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, business_id, visit_date, visit_month))
                connection.commit()
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