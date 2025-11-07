from app.models.user import User
from app.models.otp import OTP
from app.utils.email_service import EmailService
from app.services.auth_service import AuthService
from app.utils.logger import log_info, log_error
from typing import Dict, Optional

class PasswordResetService:
    """Servicio para recuperación de contraseñas"""
    
    @staticmethod
    def request_password_reset(email: str) -> Dict:
        """Solicita recuperación de contraseña"""
        try:
            # Verificar que el usuario existe
            user = User.get_by_email(email)
            if not user:
                # Por seguridad, no revelamos si el email existe o no
                log_info("Intento de recuperación con email inexistente", email=email)
                return {
                    "success": True,
                    "message": "Si el email existe, recibirás un código de verificación"
                }
            
            # Generar código OTP
            otp_code = OTP.generate_code()
            
            # Guardar OTP en base de datos
            if not OTP.create(email, otp_code):
                raise Exception("Error creando OTP")
            
            # Enviar email
            if not EmailService.send_password_reset_email(email, user['nombre'], otp_code):
                raise Exception("Error enviando email")
            
            log_info("Solicitud de recuperación procesada", email=email)
            
            return {
                "success": True,
                "message": "Si el email existe, recibirás un código de verificación"
            }
            
        except Exception as e:
            log_error("Error en solicitud de recuperación", error=e)
            raise Exception("Error procesando solicitud")
    
    @staticmethod
    def verify_otp_code(email: str, otp_code: str) -> Dict:
        """Verifica código OTP"""
        try:
            log_info("Iniciando verificación OTP recuperación", email=email, otp_code=otp_code)
            
            # Verificar que el usuario existe
            user = User.get_by_email(email)
            if not user:
                log_warning("Usuario no encontrado para recuperación", email=email)
                return {
                    "success": False,
                    "message": "Código inválido o expirado"
                }
            
            log_info("Usuario encontrado para recuperación", email=email, user_id=user['id'])
            
            # Verificar OTP
            otp_result = OTP.verify(email, otp_code)
            log_info("Resultado verificación OTP recuperación", email=email, otp_code=otp_code, result=otp_result)
            
            if not otp_result:
                log_warning("OTP de recuperación inválido o expirado", email=email, otp_code=otp_code)
                return {
                    "success": False,
                    "message": "Código inválido o expirado"
                }
            
            log_info("Código OTP de recuperación verificado exitosamente", email=email)
            
            return {
                "success": True,
                "message": "Código verificado correctamente"
            }
            
        except Exception as e:
            log_error("Error verificando OTP de recuperación", error=e, email=email, otp_code=otp_code)
            return {
                "success": False,
                "message": "Código inválido o expirado"
            }
    
    @staticmethod
    def reset_password(email: str, otp_code: str, new_password: str) -> Dict:
        """Resetea la contraseña del usuario"""
        try:
            # Verificar que el usuario existe
            user = User.get_by_email(email)
            if not user:
                return {
                    "success": False,
                    "message": "Código inválido o expirado"
                }
            
            # Verificar OTP nuevamente
            if not OTP.verify(email, otp_code):
                return {
                    "success": False,
                    "message": "Código inválido o expirado"
                }
            
            # Encriptar nueva contraseña
            hashed_password = AuthService.hash_password(new_password)
            
            # Actualizar contraseña en base de datos
            if not User.update_password(user['id'], hashed_password):
                raise Exception("Error actualizando contraseña")
            
            # Eliminar OTP usado
            OTP.delete(email)
            
            log_info("Contraseña actualizada exitosamente", email=email, user_id=user['id'])
            
            return {
                "success": True,
                "message": "Contraseña actualizada exitosamente"
            }
            
        except Exception as e:
            log_error("Error reseteando contraseña", error=e)
            raise Exception("Error actualizando contraseña")