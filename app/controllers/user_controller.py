from fastapi import HTTPException
from app.services.user_service import UserService
from app.schemas.user import UserProfileUpdate, VisitCreate

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
        """Valida QR y registra visita efectiva"""
        try:
            result = UserService.validate_qr_visit(qr_token, current_user['id'], business_id)
            
            if result["valid"]:
                return {
                    "success": True,
                    "message": "Visita registrada exitosamente",
                    "data": result["visit_data"]
                }
            else:
                raise HTTPException(status_code=400, detail=result["error"])
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")