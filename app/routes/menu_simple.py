from fastapi import APIRouter, Depends
from app.controllers.menu_controller_sqlite import MenuController
from app.utils.auth_simple import get_current_user

router = APIRouter(prefix="/api/menu", tags=["menu"])

@router.get("/{business_id}")
async def get_business_menu(business_id: int, current_user: dict = Depends(get_current_user)):
    """Obtiene el menú completo de un negocio específico desde la base de datos"""
    return MenuController.get_business_menu(business_id)

@router.get("/")
async def get_all_menus(current_user: dict = Depends(get_current_user)):
    """Obtiene todos los menús de todos los negocios"""
    return MenuController.get_all_menus()