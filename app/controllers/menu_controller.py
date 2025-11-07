from fastapi import HTTPException
from app.services.menu_service import MenuService

class MenuController:
    @staticmethod
    def get_business_menu(business_id: int):
        try:
            menu = MenuService.get_business_menu(business_id)
            if not menu:
                return {"data": [], "message": "No hay menú disponible para este negocio"}
            return {"data": menu}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")