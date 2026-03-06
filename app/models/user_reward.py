from app.config.database import get_db_connection
from app.utils.logger import log_error, log_info
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid
import qrcode
import io
import base64
from jose import jwt
from app.config.settings import settings

class UserReward:
    @staticmethod
    def generate_coupon_code() -> str:
        """Genera un código único de cupón"""
        return f"CPN-{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def generate_qr_code(coupon_code: str, user_id: int, business_id: int, expires_at: datetime) -> str:
        """Genera código QR para el cupón"""
        try:
            qr_payload = {
                "coupon_code": coupon_code,
                "user_id": user_id,
                "business_id": business_id,
                "expires_at": expires_at.isoformat(),
                "type": "reward_coupon"
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
            log_error("Error generando QR del cupón", error=e)
            return None
    
    @staticmethod
    def create_reward(user_id: int, business_id: int, reward_id: int, validity_days: int = 30) -> Optional[Dict]:
        """Crea un nuevo cupón de premio para el usuario"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar si ya tiene un cupón vigente para este negocio
                cursor.execute("""
                    SELECT COUNT(*) as count FROM user_rewards 
                    WHERE user_id = %s AND business_id = %s AND status = 'vigente'
                """, (user_id, business_id))
                
                if cursor.fetchone()['count'] > 0:
                    log_info(f"Usuario {user_id} ya tiene cupón vigente para negocio {business_id}")
                    return None
                
                # Generar datos del cupón
                coupon_code = UserReward.generate_coupon_code()
                expires_at = datetime.now() + timedelta(days=validity_days)
                qr_code = UserReward.generate_qr_code(coupon_code, user_id, business_id, expires_at)
                
                # Insertar cupón
                cursor.execute("""
                    INSERT INTO user_rewards (user_id, business_id, reward_id, coupon_code, qr_code, expires_at, reclamado, redimido)
                    VALUES (%s, %s, %s, %s, %s, %s, FALSE, FALSE)
                    RETURNING id
                """, (user_id, business_id, reward_id, coupon_code, qr_code, expires_at))
                
                reward_id = cursor.fetchone()['id']
                connection.commit()
                
                log_info(f"Cupón creado: {coupon_code} para usuario {user_id}")
                
                return {
                    "id": reward_id,
                    "coupon_code": coupon_code,
                    "qr_code": qr_code,
                    "expires_at": expires_at,
                    "status": "vigente"
                }
        except Exception as e:
            log_error("Error creando cupón de premio", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def get_user_rewards(user_id: int) -> Dict:
        """Obtiene todos los cupones del usuario organizados por estado"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Actualizar estados expirados
                cursor.execute("""
                    UPDATE user_rewards 
                    SET status = 'expirado' 
                    WHERE user_id = %s AND status IN ('vigente', 'reclamado') AND expires_at < NOW()
                """, (user_id,))
                
                # Obtener cupones con información del negocio y premio
                cursor.execute("""
                    SELECT ur.*, b.name as business_name, r.title as reward_title, r.description as reward_description
                    FROM user_rewards ur
                    JOIN businesses b ON ur.business_id = b.id
                    JOIN rewards r ON ur.reward_id = r.id
                    WHERE ur.user_id = %s
                    ORDER BY ur.created_at DESC
                """, (user_id,))
                
                all_rewards = cursor.fetchall()
                
                # Organizar por estado - vigentes incluye reclamados y no reclamados
                result = {
                    "vigentes": [],
                    "historicos": [],
                    "total": 0
                }
                
                for reward in all_rewards:
                    # Vigentes: cupones activos (reclamados y no reclamados)
                    if reward['status'] in ('vigente', 'reclamado'):
                        result['vigentes'].append(reward)
                        result['total'] += 1  # Solo contar cupones no redimidos
                    # Históricos: cupones usados o expirados del mes actual
                    elif reward['status'] in ('usado', 'expirado'):
                        # Solo incluir los del mes actual
                        created_month = reward['created_at'].strftime('%Y-%m')
                        current_month = datetime.now().strftime('%Y-%m')
                        if created_month == current_month:
                            result['historicos'].append(reward)
                
                connection.commit()
                return result
        except Exception as e:
            log_error("Error obteniendo cupones del usuario", error=e)
            return {"vigentes": [], "historicos": [], "total": 0}
        finally:
            connection.close()
    
    @staticmethod
    def claim_coupon(coupon_id: int, user_id: int) -> bool:
        """Marca un cupón como reclamado (usuario lo acepta)"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE user_rewards 
                    SET status = 'reclamado', claimed_at = NOW(), reclamado = TRUE
                    WHERE id = %s AND user_id = %s AND status = 'vigente'
                """, (coupon_id, user_id))
                
                connection.commit()
                
                if cursor.rowcount > 0:
                    log_info(f"Cupón {coupon_id} reclamado por usuario {user_id}")
                    return True
                return False
        except Exception as e:
            log_error("Error reclamando cupón", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def redeem_coupon(coupon_id: int, user_id: int) -> bool:
        """Marca un cupón como usado (redimido en el negocio)"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE user_rewards 
                    SET status = 'usado', redeemed_at = NOW(), redimido = TRUE
                    WHERE id = %s AND user_id = %s AND status = 'reclamado'
                """, (coupon_id, user_id))
                
                connection.commit()
                
                if cursor.rowcount > 0:
                    log_info(f"Cupón {coupon_id} redimido por usuario {user_id}")
                    return True
                return False
        except Exception as e:
            log_error("Error redimiendo cupón", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def verify_coupon_qr(qr_token: str) -> Optional[Dict]:
        """Verifica y decodifica un código QR de cupón"""
        try:
            payload = jwt.decode(qr_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            
            if payload.get("type") != "reward_coupon":
                return None
            
            return {
                "coupon_code": payload.get("coupon_code"),
                "user_id": payload.get("user_id"),
                "business_id": payload.get("business_id"),
                "expires_at": payload.get("expires_at")
            }
        except Exception as e:
            log_error("Error verificando QR de cupón", error=e)
            return None
    
    @staticmethod
    def get_coupon_by_code(coupon_code: str) -> Optional[Dict]:
        """Obtiene un cupón por su código"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT ur.*, b.name as business_name, r.title as reward_title
                    FROM user_rewards ur
                    JOIN businesses b ON ur.business_id = b.id
                    JOIN rewards r ON ur.reward_id = r.id
                    WHERE ur.coupon_code = %s
                """, (coupon_code,))
                return cursor.fetchone()
        except Exception as e:
            log_error("Error obteniendo cupón por código", error=e)
            return None
        finally:
            connection.close()