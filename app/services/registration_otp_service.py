from app.models.otp import OTP
from app.utils.email_service import EmailService
from app.utils.logger import log_info, log_error
from typing import Dict

class RegistrationOTPService:
    """Servicio para OTP de registro"""
    
    @staticmethod
    def send_registration_otp(email: str) -> Dict:
        """Envía código OTP para verificación de registro"""
        try:
            # Generar código OTP
            otp_code = OTP.generate_code()
            
            # Guardar OTP en base de datos con prefijo para diferenciarlo
            registration_email = f"reg_{email}"
            if not OTP.create(registration_email, otp_code):
                raise Exception("Error creando OTP de registro")
            
            # Enviar email
            if not EmailService.send_registration_otp_email(email, otp_code):
                raise Exception("Error enviando email de registro")
            
            log_info("OTP de registro enviado", email=email)
            
            return {
                "success": True,
                "message": "Código de verificación enviado al email"
            }
            
        except Exception as e:
            log_error("Error enviando OTP de registro", error=e)
            raise Exception("Error enviando código de verificación")
    
    @staticmethod
    def verify_registration_otp(email: str, otp_code: str) -> Dict:
        """Verifica código OTP de registro"""
        try:
            # Verificar OTP con prefijo de registro
            registration_email = f"reg_{email}"
            if not OTP.verify(registration_email, otp_code):
                return {
                    "success": False,
                    "message": "Código inválido o expirado"
                }
            
            # Eliminar OTP después de verificación exitosa
            OTP.delete(registration_email)
            
            log_info("OTP de registro verificado exitosamente", email=email)
            
            return {
                "success": True,
                "message": "Código verificado correctamente"
            }
            
        except Exception as e:
            log_error("Error verificando OTP de registro", error=e)
            return {
                "success": False,
                "message": "Código inválido o expirado"
            }