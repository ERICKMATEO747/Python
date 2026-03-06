from fastapi import HTTPException
from app.services.business_service_sqlite import BusinessService
from app.schemas.business import BusinessProfileUpdate

class BusinessController:
    @staticmethod
    def get_businesses(current_user: dict = None):
        try:
            user_id = current_user["id"] if current_user else None
            businesses = BusinessService.get_all_businesses(user_id)
            return {"data": businesses}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_business(business_id: int, current_user: dict = None):
        try:
            user_id = current_user["id"] if current_user else None
            business = BusinessService.get_business_by_id(business_id, user_id)
            if not business:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            return {"data": business}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_business_profile(business_id: int, current_user: dict):
        try:
            profile = BusinessService.get_business_profile(business_id)
            if not profile:
                raise HTTPException(status_code=404, detail="Perfil del negocio no encontrado")
            return {"success": True, "data": profile}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_business_profile(business_id: int, profile_data: BusinessProfileUpdate, current_user: dict):
        try:
            success = BusinessService.update_business_profile(business_id, profile_data.dict(exclude_unset=True))
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el perfil del negocio")
            return {"success": True, "message": "Perfil actualizado exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")