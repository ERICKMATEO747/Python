from fastapi import APIRouter, Depends
from app.controllers.business_controller import BusinessController
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/businesses", tags=["businesses"])

@router.get("")
async def get_businesses(current_user: dict = Depends(get_current_user)):
    return BusinessController.get_businesses()

@router.get("/{business_id}")
async def get_business(business_id: int, current_user: dict = Depends(get_current_user)):
    return BusinessController.get_business(business_id)