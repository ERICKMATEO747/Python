from fastapi import APIRouter, Request, Depends
from app.schemas.auth import UserRegister, UserLogin
from app.schemas.password_reset import PasswordResetRequest, VerifyOTPRequest, ResetPasswordRequest
from app.schemas.registration_otp import RegistrationOTPRequest
from app.controllers.auth_controller import AuthController
from app.controllers.password_reset_controller import PasswordResetController
from app.controllers.registration_otp_controller import RegistrationOTPController
from app.utils.auth_middleware import get_current_user
from app.utils.logger import log_info
from typing import Dict

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Rutas públicas (no requieren autenticación)

@router.post("/register")
async def register(user_data: UserRegister, request: Request):
    """
    Endpoint PÚBLICO para registro de usuarios
    
    - **nombre**: Nombre del usuario (mínimo 2 caracteres)
    - **email**: Email válido del usuario (opcional si se proporciona teléfono)
    - **telefono**: Número de teléfono (opcional si se proporciona email)
    - **password**: Contraseña (mínimo 8 caracteres, debe incluir mayúscula, minúscula y número)
    - **user_type_hash**: Código hash del tipo de usuario (64 caracteres)
    
    Nota: Debe proporcionar al menos email o teléfono
    """
    return AuthController.register(user_data, request)

@router.post("/login")
async def login(login_data: UserLogin, request: Request):
    """
    Endpoint PÚBLICO para login de usuarios
    
    - **email**: Email del usuario registrado
    - **password**: Contraseña del usuario
    
    Retorna JWT token válido por 24 horas que debe usarse en endpoints protegidos
    """
    return AuthController.login(login_data, request)

@router.post("/send-registration-otp")
async def send_registration_otp(otp_data: RegistrationOTPRequest, request: Request):
    """
    Endpoint PÚBLICO para enviar código OTP de registro
    
    - **email**: Email para el cual se generará el código OTP
    
    Envía un código OTP de 6 dígitos al email (válido por 10 minutos)
    Este código es para verificar el email durante el proceso de registro
    """
    return RegistrationOTPController.send_otp(otp_data, request)

@router.post("/forgot-password")
async def forgot_password(reset_data: PasswordResetRequest, request: Request):
    """
    Endpoint PÚBLICO para solicitar recuperación de contraseña
    
    - **email**: Email del usuario registrado
    
    Envía un código OTP de 6 dígitos al email (válido por 10 minutos)
    """
    return PasswordResetController.request_reset(reset_data, request)

@router.post("/verify-otp")
async def verify_otp(verify_data: VerifyOTPRequest, request: Request):
    """
    Endpoint PÚBLICO para verificar código OTP (registro o recuperación)
    
    - **email**: Email del usuario
    - **otp_code**: Código de 6 dígitos recibido por email
    
    Verifica códigos OTP tanto de:
    - Registro de nuevos usuarios
    - Recuperación de contraseña
    
    Retorna el tipo de OTP verificado en el campo 'type'
    """
    return PasswordResetController.verify_otp(verify_data, request)

@router.post("/reset-password")
async def reset_password(reset_data: ResetPasswordRequest, request: Request):
    """
    Endpoint PÚBLICO para actualizar contraseña
    
    - **email**: Email del usuario
    - **otp_code**: Código de 6 dígitos válido
    - **new_password**: Nueva contraseña (mínimo 8 caracteres, mayúscula, minúscula, número)
    
    Actualiza la contraseña si el código es válido
    """
    return PasswordResetController.reset_password(reset_data, request)

# Rutas protegidas (requieren autenticación JWT)

@router.get("/me")
async def get_user_info(current_user: Dict = Depends(get_current_user)):
    """
    Endpoint PROTEGIDO - Obtiene información del usuario autenticado
    
    Requiere JWT token válido en el header: Authorization: Bearer <token>
    
    Retorna la información completa del usuario logueado
    """
    return AuthController.get_user_info(current_user)