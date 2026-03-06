from fastapi import APIRouter, Depends
from app.controllers.business_controller import BusinessController
from app.utils.auth_simple import get_current_user

router = APIRouter(prefix="/api/businesses", tags=["businesses"])

@router.get("")
async def get_businesses(current_user: dict = Depends(get_current_user)):
    """Lista todos los negocios disponibles"""
    return BusinessController.get_businesses(current_user)

@router.get("/{business_id}")
async def get_business(business_id: int, current_user: dict = Depends(get_current_user)):
    """Obtiene información detallada del negocio"""
    return BusinessController.get_business(business_id, current_user)