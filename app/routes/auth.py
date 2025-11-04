from fastapi import APIRouter, Request
from app.schemas.auth import UserRegister, UserLogin
from app.controllers.auth_controller import AuthController

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register")
async def register(user_data: UserRegister, request: Request):
    """
    Endpoint para registro de usuarios
    
    - **nombre**: Nombre del usuario (mínimo 2 caracteres)
    - **email**: Email válido del usuario (opcional si se proporciona teléfono)
    - **telefono**: Número de teléfono (opcional si se proporciona email)
    - **password**: Contraseña (mínimo 6 caracteres)
    
    Nota: Debe proporcionar al menos email o teléfono
    """
    return AuthController.register(user_data, request)

@router.post("/login")
async def login(login_data: UserLogin, request: Request):
    """
    Endpoint para login de usuarios
    
    - **email**: Email del usuario registrado
    - **password**: Contraseña del usuario
    
    Retorna JWT token válido por 24 horas
    """
    return AuthController.login(login_data, request)