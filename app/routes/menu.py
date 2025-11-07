from fastapi import APIRouter, Depends
from app.controllers.menu_controller import MenuController
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/menu", tags=["menu"])

@router.get("/{business_id}")
async def get_business_menu(business_id: int, current_user: dict = Depends(get_current_user)):
    return MenuController.get_business_menu(business_id)