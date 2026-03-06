from fastapi import APIRouter, Depends
from app.controllers.reward_controller import RewardController
from app.schemas.reward import RewardCreate, RewardUpdate, CouponGenerate, CouponClaim, CouponRedeem, CouponQRValidation
from app.utils.auth_middleware import get_current_user

router = APIRouter(prefix="/api/rewards", tags=["rewards"])

@router.post("")
async def create_reward(reward_data: RewardCreate, current_user: dict = Depends(get_current_user)):
    """
    Crear premio para un negocio
    
    - **business_id**: ID del negocio
    - **title**: Título del premio
    - **description**: Descripción del premio
    - **terms_conditions**: Términos y condiciones
    - **validity_days**: Días de vigencia del cupón (default: 30)
    """
    return RewardController.create_reward(reward_data)

@router.get("/item/{reward_id}")
async def get_reward_item(reward_id: int, current_user: dict = Depends(get_current_user)):
    """
    Obtener un premio específico por ID
    
    - **reward_id**: ID del premio
    """
    return RewardController.get_reward_by_id(reward_id)

@router.get("/{business_id}")
async def get_business_rewards(business_id: int, current_user: dict = Depends(get_current_user)):
    """
    Obtener todos los premios activos del negocio
    
    - **business_id**: ID del negocio
    """
    return RewardController.get_business_rewards(business_id)

@router.put("/{reward_id}")
async def update_reward(reward_id: int, reward_data: RewardUpdate, current_user: dict = Depends(get_current_user)):
    """
    Actualizar un premio
    
    - **reward_id**: ID del premio a actualizar
    """
    return RewardController.update_reward(reward_id, reward_data)

@router.post("/generate")
async def generate_coupon(coupon_data: CouponGenerate, current_user: dict = Depends(get_current_user)):
    """
    Generar cupón de premio para usuario
    
    - **user_id**: ID del usuario
    - **business_id**: ID del negocio
    
    Verifica si el usuario ha completado las visitas necesarias y genera un cupón.
    """
    return RewardController.generate_coupon(coupon_data)

@router.get("/user/{user_id}")
async def get_user_rewards(user_id: int, current_user: dict = Depends(get_current_user)):
    """
    Obtener todos los cupones del usuario
    
    - **user_id**: ID del usuario
    
    Retorna cupones organizados por estado: vigentes, usados, expirados
    """
    return RewardController.get_user_rewards(user_id)

@router.patch("/{coupon_id}/claim")
async def claim_coupon(coupon_id: int, current_user: dict = Depends(get_current_user)):
    """
    Reclamar un cupón (usuario lo acepta)
    
    - **coupon_id**: ID del cupón a reclamar
    
    Cambia el estado de 'vigente' a 'reclamado'. El usuario acepta el premio.
    """
    coupon_data = CouponClaim(coupon_id=coupon_id)
    return RewardController.claim_coupon(coupon_data, current_user["id"])

@router.patch("/{coupon_id}/redeem")
async def redeem_coupon(coupon_id: int, current_user: dict = Depends(get_current_user)):
    """
    Redimir un cupón (usado en el negocio)
    
    - **coupon_id**: ID del cupón a redimir
    
    Cambia el estado de 'reclamado' a 'usado'. Se usa físicamente en el negocio.
    """
    coupon_data = CouponRedeem(coupon_id=coupon_id)
    return RewardController.redeem_coupon(coupon_data, current_user["id"])

@router.post("/validate-qr")
async def validate_coupon_qr(qr_data: CouponQRValidation, current_user: dict = Depends(get_current_user)):
    """
    Validar código QR de cupón
    
    - **qr_token**: Token JWT del código QR
    - **business_id**: ID del negocio donde se valida
    
    Verifica que el cupón sea válido y esté vigente para el negocio.
    """
    return RewardController.validate_coupon_qr(qr_data)