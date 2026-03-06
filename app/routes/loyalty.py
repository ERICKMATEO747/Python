from fastapi import APIRouter, Depends
from app.services.loyalty_service import LoyaltyService
from app.schemas.business import LoyaltyConfigUpdate
from app.utils.auth_middleware import get_current_user

router = APIRouter(prefix="/api/loyalty", tags=["Loyalty"])

@router.get("/config/{business_id}")
async def get_loyalty_config(
    business_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Obtiene configuración del programa de lealtad"""
    return LoyaltyService.get_config(business_id)

@router.put("/config/{business_id}")
async def update_loyalty_config(
    business_id: int,
    config_data: LoyaltyConfigUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Actualiza configuración del programa de lealtad"""
    return LoyaltyService.update_config(business_id, config_data, current_user)