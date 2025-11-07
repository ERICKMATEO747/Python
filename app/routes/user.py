from fastapi import APIRouter, Depends
from app.controllers.user_controller import UserController
from app.schemas.user import UserProfileUpdate, VisitCreate, QRValidation
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/user", tags=["user"])

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return UserController.get_profile(current_user["id"])

@router.put("/profile")
async def update_profile(data: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    return UserController.update_profile(current_user["id"], data)

@router.get("/visits")
async def get_visits(current_user: dict = Depends(get_current_user)):
    return UserController.get_visits(current_user["id"])

@router.post("/generate-qr")
async def generate_qr(
    visit_data: VisitCreate, 
    current_user: dict = Depends(get_current_user)
):
    """
    Genera código QR para visita
    
    - **user_id**: ID del usuario
    - **business_id**: ID del negocio
    - **visit_date**: Fecha y hora de la visita
    
    Retorna el código QR en formato Base64 sin guardarlo en la base de datos.
    El QR debe ser validado posteriormente con el endpoint validate-qr.
    """
    return UserController.generate_qr(visit_data)

@router.post("/validate-qr")
async def validate_qr_visit(
    qr_data: QRValidation, 
    current_user: dict = Depends(get_current_user)
):
    """
    Valida código QR y registra visita efectiva
    
    - **qr_token**: Token JWT del código QR generado
    - **business_id**: ID del negocio donde se valida
    
    Este endpoint valida el QR y registra la visita en la base de datos.
    Solo aquí se crea el registro efectivo de la visita.
    """
    return UserController.validate_qr_visit(qr_data.qr_token, qr_data.business_id, current_user)