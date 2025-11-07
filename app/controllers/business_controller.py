from fastapi import HTTPException
from app.services.business_service import BusinessService

class BusinessController:
    @staticmethod
    def get_businesses():
        try:
            businesses = BusinessService.get_all_businesses()
            return {"data": businesses}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_business(business_id: int):
        try:
            business = BusinessService.get_business_by_id(business_id)
            if not business:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            return {"data": business}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")