from fastapi import HTTPException, status, Request
from app.schemas.password_reset import PasswordResetRequest, VerifyOTPRequest, ResetPasswordRequest
from app.services.password_reset_service import PasswordResetService
from app.utils.logger import log_info, log_error, log_warning
from app.utils.security import rate_limiter
from typing import Dict

class PasswordResetController:
    """Controlador para recuperación de contraseñas"""
    
    @staticmethod
    def request_reset(reset_data: PasswordResetRequest, request: Request) -> Dict:
        """Maneja solicitud de recuperación de contraseña"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="password_reset")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Solicitud de recuperación de contraseña", email=reset_data.email, ip=client_ip)
            
            result = PasswordResetService.request_password_reset(reset_data.email)
            
            return result
            
        except Exception as e:
            log_error("Error en solicitud de recuperación", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def verify_otp(verify_data: VerifyOTPRequest, request: Request) -> Dict:
        """Maneja verificación de código OTP (recuperación y registro)"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="verify_otp")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("=== INICIO VERIFICACIÓN OTP ===", email=verify_data.email, otp_code=verify_data.otp_code, ip=client_ip)
            
            # Intentar verificar OTP de recuperación de contraseña primero
            log_info("Intentando verificar como OTP de recuperación", email=verify_data.email)
            result = PasswordResetService.verify_otp_code(verify_data.email, verify_data.otp_code)
            log_info("Resultado OTP recuperación", email=verify_data.email, result=result)
            
            if result["success"]:
                log_info("OTP de recuperación verificado exitosamente", email=verify_data.email, ip=client_ip)
                return {
                    "success": True,
                    "message": "Código verificado correctamente",
                    "type": "password_reset"
                }
            
            # Si no es de recuperación, intentar verificar OTP de registro
            log_info("Intentando verificar como OTP de registro", email=verify_data.email)
            from app.services.registration_otp_service import RegistrationOTPService
            result = RegistrationOTPService.verify_registration_otp(verify_data.email, verify_data.otp_code)
            log_info("Resultado OTP registro", email=verify_data.email, result=result)
            
            if result["success"]:
                log_info("OTP de registro verificado exitosamente", email=verify_data.email, ip=client_ip)
                return {
                    "success": True,
                    "message": "Código verificado correctamente",
                    "type": "registration"
                }
            
            # Si ninguno funciona
            log_warning("=== Código OTP inválido para ambos tipos ===", email=verify_data.email, otp_code=verify_data.otp_code, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código inválido o expirado"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            log_error("Error verificando OTP", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def reset_password(reset_data: ResetPasswordRequest, request: Request) -> Dict:
        """Maneja actualización de contraseña"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="reset_password")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Actualización de contraseña", email=reset_data.email, ip=client_ip)
            
            result = PasswordResetService.reset_password(
                reset_data.email, 
                reset_data.otp_code, 
                reset_data.new_password
            )
            
            if not result["success"]:
                log_warning("Error actualizando contraseña", email=reset_data.email, ip=client_ip)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )
            
            log_info("Contraseña actualizada exitosamente", email=reset_data.email, ip=client_ip)
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            log_error("Error reseteando contraseña", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )