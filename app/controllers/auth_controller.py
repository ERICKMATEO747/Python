from fastapi import HTTPException, status, Request
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.utils.email_service import EmailService
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
                password=user_data.password,
                user_type_hash=user_data.user_type_hash
            )
            
            # Enviar email de bienvenida si hay email
            if user_data.email:
                try:
                    EmailService.send_welcome_email(user_data.email, user_data.nombre)
                    log_info("Email de bienvenida enviado", user_id=user['id'], email=user_data.email)
                except Exception as e:
                    log_error("Error enviando email de bienvenida", error=e, user_id=user['id'])
                    # No fallar el registro por error de email
            
            log_info("Usuario registrado exitosamente", user_id=user['id'], ip=client_ip)
            
            return {
                "success": True,
                "message": "Usuario creado exitosamente. ¡Revisa tu email de bienvenida!",
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
    def get_user_info(current_user: Dict) -> Dict:
        """Obtiene información del usuario autenticado"""
        log_info("Consulta de información de usuario", user_id=current_user['id'])
        
        return {
            "success": True,
            "message": "Información del usuario obtenida exitosamente",
            "data": {
                "id": current_user['id'],
                "nombre": current_user['nombre'],
                "email": current_user['email'],
                "telefono": current_user['telefono'],
                "user_type": current_user['user_type']
            }
        }
    
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