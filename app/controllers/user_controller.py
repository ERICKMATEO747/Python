from fastapi import HTTPException
from app.services.user_service import UserService
from app.schemas.user import UserProfileUpdate, VisitCreate
from app.services.push_notification_service import PushNotificationService
from app.services.websocket_service import websocket_service
import asyncio

class UserController:
    @staticmethod
    def get_profile(user_id: int):
        try:
            profile = UserService.get_user_profile(user_id)
            if not profile:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"data": profile}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_profile(user_id: int, data: UserProfileUpdate):
        try:
            update_data = data.dict(exclude_unset=True)
            success = UserService.update_user_profile(user_id, update_data)
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el perfil")
            
            updated_profile = UserService.get_user_profile(user_id)
            return {
                "success": True,
                "message": "Perfil actualizado exitosamente",
                "data": updated_profile
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_visits(user_id: int):
        try:
            visits = UserService.get_user_visits(user_id)
            return visits
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def generate_qr(visit_data: VisitCreate):
        try:
            success, qr_code = UserService.generate_qr_code(
                visit_data.user_id, 
                visit_data.business_id, 
                visit_data.visit_date
            )
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo generar el código QR")
            
            return {
                "success": True,
                "message": "Código QR generado exitosamente",
                "qr_code": qr_code
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def validate_qr_visit(qr_token: str, business_id: int, current_user: dict):
        """Valida QR y registra visita efectiva con notificaciones"""
        from app.models.audit_log import AuditLog
        
        try:
            result = UserService.validate_qr_visit(qr_token, current_user['id'], business_id)
            
            if result["valid"]:
                # Registrar en audit trail
                AuditLog.log_action(
                    user_id=current_user['id'],
                    action_type='VISIT_REGISTER',
                    description=f"Visita registrada en negocio {business_id}",
                    business_id=business_id,
                    new_values=result.get("visit_data")
                )
                
                # Enviar notificaciones
                push_service = PushNotificationService()
                business_name = result.get("business_name", "Negocio")
                
                # Preparar datos para notificación
                visit_notification_data = {
                    **result.get("visit_data", {}),
                    'progress_in_round': result.get("progress_in_round", 0),
                    'max_visits_per_round': result.get("max_visits_per_round", 6)
                }
                
                # Notificación push de visita registrada
                push_service.notify_visit_registered(
                    current_user['id'], 
                    business_name, 
                    visit_notification_data
                )
                
                # WebSocket de visita registrada
                asyncio.create_task(
                    websocket_service.notify_visit_registered(
                        current_user['id'],
                        business_id,
                        result.get("visit_data", {})
                    )
                )
                
                # Si se generó premio
                if result.get("reward_earned"):
                    AuditLog.log_action(
                        user_id=current_user['id'],
                        action_type='REWARD_CREATE',
                        description=f"Premio generado automáticamente",
                        business_id=business_id,
                        new_values=result.get("reward_data")
                    )
                    
                    # Notificación push de premio ganado
                    push_service.notify_reward_earned(
                        current_user['id'],
                        business_name,
                        result.get("reward_data", {})
                    )
                
                return {
                    "success": True,
                    "message": "Visita registrada exitosamente",
                    "data": {
                        "visit_registered": result["visit_registered"],
                        "visit_data": result.get("visit_data"),
                        "current_round": result.get("current_round", 1),
                        "progress_in_round": result.get("progress_in_round", 0),
                        "max_visits_per_round": result.get("max_visits_per_round", 6),
                        "reward_earned": result.get("reward_earned", False),
                        "reward_data": result.get("reward_data")
                    }
                }
            else:
                raise HTTPException(status_code=400, detail=result["error"])
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
