from app.config.database import get_db_connection
from app.utils.logger import log_error
from app.models.audit_log import AuditLog
from app.schemas.business import LoyaltyConfigUpdate
from typing import Dict

class LoyaltyService:
    """Servicio para configuración del programa de lealtad"""
    
    @staticmethod
    def get_config(business_id: int) -> Dict:
        """Obtiene configuración del programa de lealtad"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT visits_for_prize, active as program_active, 
                           reward_id, updated_at
                    FROM businesses
                    WHERE id = %s
                """, (business_id,))
                
                config = cursor.fetchone()
                if not config:
                    return {"success": False, "error": "Negocio no encontrado"}
                
                return {
                    "success": True,
                    "data": {
                        "business_id": business_id,
                        "visits_per_round": config['visits_for_prize'] or 6,
                        "daily_reward_limit": 5,  # Default value
                        "program_active": bool(config['program_active']),
                        "auto_generate_rewards": True,  # Default value
                        "reward_expiry_days": 30,  # Default value
                        "updated_at": config['updated_at'].isoformat() if config['updated_at'] else None
                    }
                }
        except Exception as e:
            log_error("Error obteniendo configuración de lealtad", error=e)
            return {"success": False, "error": "Error interno del servidor"}
        finally:
            connection.close()
    
    @staticmethod
    def update_config(business_id: int, config_data: LoyaltyConfigUpdate, current_user: dict) -> Dict:
        """Actualiza configuración del programa de lealtad"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener configuración actual
                cursor.execute("""
                    SELECT visits_for_prize, active FROM businesses WHERE id = %s
                """, (business_id,))
                
                current_config = cursor.fetchone()
                if not current_config:
                    return {"success": False, "error": "Negocio no encontrado"}
                
                old_values = {
                    "visits_per_round": current_config['visits_for_prize'],
                    "program_active": bool(current_config['active'])
                }
                
                # Preparar datos para actualizar
                update_data = config_data.dict(exclude_unset=True)
                fields = []
                values = []
                new_values = {}
                
                if 'visits_per_round' in update_data:
                    fields.append("visits_for_prize = %s")
                    values.append(update_data['visits_per_round'])
                    new_values['visits_per_round'] = update_data['visits_per_round']
                
                if 'program_active' in update_data:
                    fields.append("active = %s")
                    values.append(update_data['program_active'])
                    new_values['program_active'] = update_data['program_active']
                
                if fields:
                    fields.append("updated_at = NOW()")
                    values.append(business_id)
                    
                    query = f"UPDATE businesses SET {', '.join(fields)} WHERE id = %s"
                    cursor.execute(query, values)
                    connection.commit()
                    
                    changes_applied = cursor.rowcount
                    
                    # Registrar en audit trail
                    AuditLog.log_action(
                        user_id=current_user['id'],
                        action_type='CONFIG_UPDATE',
                        description="Configuración del programa de lealtad actualizada",
                        business_id=business_id,
                        old_values=old_values,
                        new_values=new_values
                    )
                    
                    return {
                        "success": True,
                        "message": "Configuración actualizada exitosamente",
                        "data": {
                            "changes_applied": changes_applied,
                            "updated_fields": list(new_values.keys())
                        }
                    }
                else:
                    return {
                        "success": True,
                        "message": "No hay cambios para aplicar",
                        "data": {"changes_applied": 0, "updated_fields": []}
                    }
                    
        except Exception as e:
            log_error("Error actualizando configuración de lealtad", error=e)
            return {"success": False, "error": "Error interno del servidor"}
        finally:
            connection.close()