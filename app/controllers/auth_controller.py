from fastapi import HTTPException, status, Request
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.utils.logger import log_info, log_error, log_warning
from app.utils.security import rate_limiter
from typing import Dict

class AuthController:
    """Controlador para manejar la lógica de autenticación"""
    
    @staticmethod
    def register(user_data: UserRegister, request: Request) -> Dict:
        """Maneja el registro de usuarios"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="register")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Iniciando registro de usuario", 
                    email=user_data.email, 
                    telefono=user_data.telefono[:4] + "****" if user_data.telefono else None,
                    ip=client_ip)
            
            user = AuthService.register_user(
                nombre=user_data.nombre,
                email=user_data.email,
                telefono=user_data.telefono,
                password=user_data.password
            )
            
            log_info("Usuario registrado exitosamente", user_id=user['id'], ip=client_ip)
            
            return {
                "success": True,
                "message": "Usuario creado exitosamente",
                "data": user
            }
        except ValueError as e:
            log_warning("Error de validación en registro", error=str(e), ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            log_error("Error interno en registro", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def login(login_data: UserLogin, request: Request) -> Dict:
        """Maneja el login de usuarios"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="login")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Intento de login", email=login_data.email, ip=client_ip)
            
            user = AuthService.authenticate_user(
                email=login_data.email,
                password=login_data.password
            )
            
            if not user:
                log_warning("Credenciales inválidas", email=login_data.email, ip=client_ip)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            
            # Generar token JWT
            access_token = AuthService.create_access_token(user['id'])
            
            log_info("Login exitoso", user_id=user['id'], ip=client_ip)
            
            return {
                "success": True,
                "message": "Login exitoso",
                "data": {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": user
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            log_error("Error interno en login", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )