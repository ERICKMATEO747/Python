from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import Dict, List, Optional
import json

class PushSubscription:
    @staticmethod
    def create_table():
        """Crea la tabla de suscripciones push si no existe"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS push_subscriptions (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        business_id BIGINT NULL,
                        endpoint TEXT NOT NULL,
                        p256dh_key TEXT NOT NULL,
                        auth_key TEXT NOT NULL,
                        user_agent TEXT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        UNIQUE KEY unique_user_endpoint (user_id, endpoint(255)),
                        INDEX idx_user_id (user_id),
                        INDEX idx_business_id (business_id),
                        INDEX idx_active (is_active)
                    )
                """)
                connection.commit()
        except Exception as e:
            log_error("Error creando tabla push_subscriptions", error=e)
        finally:
            connection.close()
    
    @staticmethod
    def subscribe(user_id: int, subscription_data: Dict, business_id: int = None) -> bool:
        """Registra una nueva suscripción push"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar si ya existe
                cursor.execute("""
                    SELECT id FROM push_subscriptions 
                    WHERE user_id = %s AND endpoint = %s
                """, (user_id, subscription_data['endpoint']))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar existente
                    cursor.execute("""
                        UPDATE push_subscriptions SET 
                            p256dh_key = %s, auth_key = %s, business_id = %s,
                            is_active = TRUE, updated_at = NOW()
                        WHERE id = %s
                    """, (
                        subscription_data['keys']['p256dh'],
                        subscription_data['keys']['auth'],
                        business_id,
                        existing['id']
                    ))
                else:
                    # Crear nueva
                    cursor.execute("""
                        INSERT INTO push_subscriptions 
                        (user_id, business_id, endpoint, p256dh_key, auth_key)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        business_id,
                        subscription_data['endpoint'],
                        subscription_data['keys']['p256dh'],
                        subscription_data['keys']['auth']
                    ))
                
                connection.commit()
                return True
        except Exception as e:
            log_error("Error registrando suscripción push", error=e)
            connection.rollback()
            return False
        finally:
            connection.close()
    
    @staticmethod
    def get_user_subscriptions(user_id: int) -> List[Dict]:
        """Obtiene todas las suscripciones activas de un usuario"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT endpoint, p256dh_key, auth_key 
                    FROM push_subscriptions 
                    WHERE user_id = %s AND is_active = TRUE
                """, (user_id,))
                
                subscriptions = []
                for row in cursor.fetchall():
                    subscriptions.append({
                        'endpoint': row['endpoint'],
                        'keys': {
                            'p256dh': row['p256dh_key'],
                            'auth': row['auth_key']
                        }
                    })
                return subscriptions
        except Exception as e:
            log_error("Error obteniendo suscripciones", error=e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def remove_invalid_subscription(endpoint: str) -> bool:
        """Elimina suscripción inválida (410, 404)"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE push_subscriptions 
                    SET is_active = FALSE 
                    WHERE endpoint = %s
                """, (endpoint,))
                connection.commit()
                return True
        except Exception as e:
            log_error("Error eliminando suscripción inválida", error=e)
            return False
        finally:
            connection.close()