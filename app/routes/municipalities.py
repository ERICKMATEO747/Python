from fastapi import APIRouter, Depends
from app.controllers.municipality_controller import MunicipalityController
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/municipalities", tags=["municipalities"])

@router.get("")
async def get_municipalities(current_user: dict = Depends(get_current_user)):
    return MunicipalityController.get_municipalities()