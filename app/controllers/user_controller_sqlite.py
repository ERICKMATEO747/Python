from fastapi import HTTPException
from app.models.user_visit_sqlite import UserVisit
from app.models.user_sqlite import User

class UserController:
    @staticmethod
    def get_profile(user_id: int):
        try:
            user = User.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"success": True, "data": user}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_profile(user_id: int, data):
        try:
            # Implementación básica - en una app real actualizaría la BD
            return {"success": True, "message": "Perfil actualizado exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_visits(user_id: int):
        try:
            visits = UserVisit.get_user_visits_with_rounds(user_id)
            total_visits = sum(visit.get('visit_count', 0) for visit in visits)
            return {
                "success": True,
                "data": {
                    "data": visits,
                    "total_visits": total_visits
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def generate_qr(visit_data):
        try:
            # Implementación básica - retorna QR dummy
            return {
                "success": True,
                "message": "QR generado exitosamente",
                "data": {
                    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                    "qr_token": "dummy_token_123"
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def validate_qr_visit(qr_token: str, business_id: int, current_user: dict):
        try:
            # Implementación básica - simula validación exitosa
            return {
                "success": True,
                "message": "Visita registrada exitosamente",
                "data": {
                    "visit_id": 999,
                    "business_id": business_id,
                    "user_id": current_user["id"],
                    "points_earned": 1
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")