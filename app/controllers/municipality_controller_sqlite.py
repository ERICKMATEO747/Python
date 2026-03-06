from fastapi import HTTPException
from app.models.municipality_sqlite import Municipality

class MunicipalityController:
    @staticmethod
    def get_municipalities():
        try:
            municipalities = Municipality.get_all()
            return {"data": municipalities}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")