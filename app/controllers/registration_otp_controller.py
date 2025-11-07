from fastapi import HTTPException, status, Request
from app.schemas.registration_otp import RegistrationOTPRequest
from app.services.registration_otp_service import RegistrationOTPService
from app.utils.logger import log_info, log_error, log_warning
from app.utils.security import rate_limiter
from typing import Dict

class RegistrationOTPController:
    """Controlador para OTP de registro"""
    
    @staticmethod
    def send_otp(otp_data: RegistrationOTPRequest, request: Request) -> Dict:
        """Maneja envío de OTP para registro"""
        client_ip = request.client.host
        
        # Rate limiting
        if not rate_limiter.is_allowed(client_ip):
            log_warning("Rate limit excedido", ip=client_ip, endpoint="registration_otp")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiados intentos. Intente más tarde"
            )
        
        try:
            log_info("Solicitud de OTP de registro", email=otp_data.email, ip=client_ip)
            
            result = RegistrationOTPService.send_registration_otp(otp_data.email)
            
            log_info("OTP de registro enviado exitosamente", email=otp_data.email, ip=client_ip)
            
            return result
            
        except Exception as e:
            log_error("Error enviando OTP de registro", error=e, ip=client_ip)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )