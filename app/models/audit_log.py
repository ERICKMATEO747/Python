from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import Dict, List, Optional
from datetime import datetime
import json

class AuditLog:
    """Modelo para registro de auditoría"""
    
    ACTION_TYPES = {
        'USER_LOGIN': 'Inicio de sesión',
        'VISIT_REGISTER': 'Registro de visita',
        'REWARD_CREATE': 'Creación de premio',
        'REWARD_CLAIM': 'Reclamación de cupón',
        'REWARD_REDEEM': 'Redención de cupón',
        'MENU_UPDATE': 'Actualización de menú',
        'PROGRAM_TOGGLE': 'Activar/pausar programa',
        'SETTINGS_CHANGE': 'Cambio de configuración',
        'CONFIG_UPDATE': 'Actualización de configuración'
    }
    
    @staticmethod
    def log_action(
        user_id: int,
        action_type: str,
        description: str,
        business_id: Optional[int] = None,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> bool:
        """Registra una acción en el audit trail"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO audit_logs (
                        user_id, business_id, action_type, action_description,
                        old_values, new_values, ip_address, user_agent, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """, (
                    user_id,
                    business_id,
                    action_type,
                    description,
                    json.dumps(old_values) if old_values else None,
                    json.dumps(new_values) if new_values else None,
                    ip_address,
                    user_agent
                ))
                
                connection.commit()
                return True
        except Exception as e:
            log_error("Error registrando audit log", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def get_business_logs(
        business_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        action_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict:
        """Obtiene logs de auditoría de un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                where_conditions = ["business_id = %s"]
                params = [business_id]
                
                if start_date:
                    where_conditions.append("created_at >= %s")
                    params.append(start_date)
                
                if end_date:
                    where_conditions.append("created_at <= %s")
                    params.append(end_date)
                
                if action_type:
                    where_conditions.append("action_type = %s")
                    params.append(action_type)
                
                where_clause = " AND ".join(where_conditions)
                
                # Obtener logs
                cursor.execute(f"""
                    SELECT al.*, u.nombre as user_name
                    FROM audit_logs al
                    LEFT JOIN users u ON al.user_id = u.id
                    WHERE {where_clause}
                    ORDER BY al.created_at DESC
                    LIMIT %s OFFSET %s
                """, params + [limit, offset])
                
                logs = cursor.fetchall()
                
                # Contar total
                cursor.execute(f"""
                    SELECT COUNT(*) as total
                    FROM audit_logs
                    WHERE {where_clause}
                """, params)
                
                total = cursor.fetchone()['total']
                
                # Procesar logs
                processed_logs = []
                for log in logs:
                    processed_log = dict(log)
                    if processed_log['old_values']:
                        processed_log['old_values'] = json.loads(processed_log['old_values'])
                    if processed_log['new_values']:
                        processed_log['new_values'] = json.loads(processed_log['new_values'])
                    processed_logs.append(processed_log)
                
                return {
                    "audit_logs": processed_logs,
                    "total_records": total,
                    "page": (offset // limit) + 1,
                    "has_more": (offset + limit) < total
                }
        except Exception as e:
            log_error("Error obteniendo audit logs", error=e)
            return {"audit_logs": [], "total_records": 0, "page": 1, "has_more": False}
        finally:
            connection.close()
    
    @staticmethod
    def get_user_logs(user_id: int, limit: int = 50) -> Dict:
        """Obtiene logs de auditoría de un usuario"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT al.*, b.name as business_name
                    FROM audit_logs al
                    LEFT JOIN businesses b ON al.business_id = b.id
                    WHERE al.user_id = %s
                    ORDER BY al.created_at DESC
                    LIMIT %s
                """, (user_id, limit))
                
                logs = cursor.fetchall()
                
                cursor.execute("""
                    SELECT COUNT(*) as total
                    FROM audit_logs
                    WHERE user_id = %s
                """, (user_id,))
                
                total = cursor.fetchone()['total']
                
                return {
                    "user_id": user_id,
                    "actions": logs,
                    "total_actions": total
                }
        except Exception as e:
            log_error("Error obteniendo user logs", error=e)
            return {"user_id": user_id, "actions": [], "total_actions": 0}
        finally:
            connection.close()