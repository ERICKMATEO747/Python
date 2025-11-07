from fastapi import HTTPException
from app.services.municipality_service import MunicipalityService

class MunicipalityController:
    @staticmethod
    def get_municipalities():
        try:
            municipalities = MunicipalityService.get_all_municipalities()
            return {"data": municipalities}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")