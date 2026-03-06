from fastapi import APIRouter, Depends
from app.controllers.municipality_controller_sqlite import MunicipalityController
from app.utils.auth_simple import get_current_user

router = APIRouter(prefix="/api/municipalities", tags=["municipalities"])

@router.get("")
async def get_municipalities(current_user: dict = Depends(get_current_user)):
    return MunicipalityController.get_municipalities()