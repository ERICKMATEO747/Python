import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.logger import log_info, log_error
from typing import Optional

class EmailService:
    """Servicio para envío de emails"""
    
    @staticmethod
    def get_registration_otp_template(nombre: str, otp_code: str) -> str:
        """Genera template HTML para OTP de registro"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Código de Verificación - Flevo</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #162a52 0%, #2c4a7a 50%, #162a52 100%); min-height: 100vh; padding: 10px; }}
                .email-wrapper {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 20px 40px rgba(22, 42, 82, 0.3); }}
                
                .header {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 50%, #162a52 100%); color: white; text-align: center; padding: 30px 20px; position: relative; }}
                .header-content {{ position: relative; z-index: 2; }}
                .logo {{ font-size: 32px; font-weight: 900; margin-bottom: 10px; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); background: linear-gradient(45deg, #ffffff, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
                .subtitle {{ font-size: 16px; opacity: 0.95; font-weight: 300; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }}
                .verification-badge {{ background: rgba(246, 173, 85, 0.2); border: 2px solid #f6ad55; color: #f6ad55; padding: 6px 15px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 15px; display: inline-block; }}
                
                .content {{ padding: 30px 20px; background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%); }}
                .hero-image {{ text-align: center; margin-bottom: 25px; }}
                .hero-icon {{ font-size: 48px; background: linear-gradient(135deg, #162a52, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; filter: drop-shadow(0 2px 4px rgba(22, 42, 82, 0.2)); }}
                .greeting {{ font-size: 20px; color: #162a52; margin-bottom: 20px; font-weight: 700; text-align: center; }}
                .message {{ color: #4a5568; line-height: 1.6; margin-bottom: 25px; font-size: 15px; text-align: center; }}
                
                .welcome-section {{ background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border: 2px solid #f6ad55; border-radius: 15px; padding: 25px 15px; text-align: center; margin: 25px 0; position: relative; }}
                .welcome-section::before {{ content: '🎉'; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #162a52, #2c4a7a); color: white; padding: 10px; border-radius: 50%; font-size: 18px; border: 3px solid #f6ad55; }}
                .welcome-title {{ color: #162a52; font-weight: 800; margin-bottom: 15px; font-size: 18px; margin-top: 10px; }}
                .welcome-text {{ color: #4a5568; font-size: 15px; line-height: 1.5; }}
                
                .otp-section {{ background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border: 2px solid #f6ad55; border-radius: 15px; padding: 25px 15px; text-align: center; margin: 25px 0; position: relative; }}
                .otp-section::before {{ content: '🔐'; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #162a52, #2c4a7a); color: white; padding: 10px; border-radius: 50%; font-size: 18px; border: 3px solid #f6ad55; }}
                .otp-label {{ color: #162a52; font-weight: 700; margin-bottom: 15px; font-size: 16px; margin-top: 10px; }}
                .otp-code {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 100%); color: white; font-size: 28px; font-weight: 900; padding: 15px 20px; border-radius: 10px; letter-spacing: 8px; display: inline-block; box-shadow: 0 8px 20px rgba(22, 42, 82, 0.3); border: 3px solid #f6ad55; text-shadow: 0 1px 2px rgba(0,0,0,0.3); }}
                
                .info-section {{ background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border: 2px solid #f6ad55; color: #e65100; padding: 20px 15px; border-radius: 15px; margin: 25px 0; position: relative; }}
                .info-section::before {{ content: 'ℹ️'; position: absolute; top: -15px; left: 20px; background: #f6ad55; color: white; padding: 10px; border-radius: 50%; font-size: 16px; border: 3px solid white; }}
                .info-title {{ font-weight: 800; margin-bottom: 15px; margin-left: 15px; font-size: 16px; color: #162a52; }}
                .info-section ul {{ margin: 10px 0 0 25px; }}
                .info-section li {{ margin: 8px 0; font-weight: 600; font-size: 13px; }}
                
                .divider {{ height: 2px; background: linear-gradient(90deg, transparent, #f6ad55, #162a52, #f6ad55, transparent); margin: 25px 0; border-radius: 1px; }}
                
                .footer {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 100%); color: white; padding: 25px 20px; text-align: center; position: relative; }}
                .footer-content {{ position: relative; z-index: 2; }}
                .footer-logo {{ font-size: 24px; font-weight: 900; margin-bottom: 15px; letter-spacing: 2px; background: linear-gradient(45deg, #ffffff, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
                .footer-text {{ color: rgba(255,255,255,0.9); font-size: 12px; margin: 8px 0; line-height: 1.4; }}
                .footer-brand {{ color: #f6ad55; font-weight: 700; }}
                .footer-tagline {{ color: #f6ad55; font-weight: 600; font-size: 14px; margin-top: 10px; }}
                
                @media only screen and (max-width: 480px) {{
                    body {{ padding: 5px; }}
                    .email-wrapper {{ border-radius: 10px; }}
                    .header {{ padding: 20px 15px; }}
                    .logo {{ font-size: 28px; letter-spacing: 1px; }}
                    .subtitle {{ font-size: 14px; }}
                    .verification-badge {{ font-size: 11px; padding: 5px 12px; }}
                    .content {{ padding: 20px 15px; }}
                    .hero-icon {{ font-size: 40px; }}
                    .greeting {{ font-size: 18px; margin-bottom: 15px; }}
                    .message {{ font-size: 14px; margin-bottom: 20px; }}
                    .welcome-section {{ padding: 20px 10px; margin: 20px 0; }}
                    .welcome-title {{ font-size: 16px; }}
                    .welcome-text {{ font-size: 14px; }}
                    .otp-section {{ padding: 20px 10px; margin: 20px 0; }}
                    .otp-label {{ font-size: 15px; margin-bottom: 12px; }}
                    .otp-code {{ font-size: 24px; padding: 12px 15px; letter-spacing: 6px; }}
                    .info-section {{ padding: 15px 10px; margin: 20px 0; }}
                    .info-title {{ font-size: 15px; margin-left: 10px; }}
                    .info-section ul {{ margin-left: 20px; }}
                    .info-section li {{ font-size: 12px; }}
                    .footer {{ padding: 20px 15px; }}
                    .footer-logo {{ font-size: 20px; }}
                    .footer-text {{ font-size: 11px; }}
                    .footer-tagline {{ font-size: 13px; }}
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="header">
                    <div class="header-content">
                        <div class="logo">🏆 FLEVO</div>
                        <div class="subtitle">Tu programa de lealtad favorito</div>
                        <div class="verification-badge">🔐 Verificación de Registro</div>
                    </div>
                </div>
                
                <div class="content">
                    <div class="hero-image">
                        <div class="hero-icon">🔐🏆</div>
                    </div>
                    
                    <div class="greeting">Estimado <strong>{nombre}</strong> 👋</div>
                    
                    <div class="welcome-section">
                        <div class="welcome-title">🎉 ¡Bienvenido a Flevo!</div>
                        <div class="welcome-text">Estamos emocionados de tenerte en nuestra plataforma de lealtad. Para completar tu registro y comenzar a acumular puntos, necesitamos verificar tu email.</div>
                    </div>
                    
                    <div class="message">
                        Usa el siguiente código de verificación para activar tu cuenta Flevo:
                    </div>
                    
                    <div class="otp-section">
                        <div class="otp-label">Tu código de verificación</div>
                        <div class="otp-code">{otp_code}</div>
                    </div>
                    
                    <div class="info-section">
                        <div class="info-title">Información importante</div>
                        <ul>
                            <li>Este código expira en <strong>10 minutos</strong></li>
                            <li>Solo puede ser usado <strong>una vez</strong></li>
                            <li>Ingresa este código en la aplicación para activar tu cuenta</li>
                            <li>Si no solicitaste este registro, ignora este email</li>
                        </ul>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div class="message">
                        Una vez verificado tu email, podrás acceder a todas las funcionalidades de Flevo y comenzar a <strong>ganar puntos increíbles</strong>.
                    </div>
                </div>
                
                <div class="footer">
                    <div class="footer-content">
                        <div class="footer-logo">🏆 FLEVO</div>
                        <div class="footer-text">Este es un email automático, no respondas a este mensaje.</div>
                        <div class="footer-text">© 2025 <span class="footer-brand">Flevo App</span> - Sistema de Autenticación</div>
                        <div class="footer-tagline">Tu programa de lealtad de confianza</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_password_reset_template(nombre: str, otp_code: str) -> str:
        """Genera template HTML para recuperación de contraseña"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recuperación de Contraseña - Flevo</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #162a52 0%, #2c4a7a 50%, #162a52 100%); min-height: 100vh; padding: 10px; }}
                .email-wrapper {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 20px 40px rgba(22, 42, 82, 0.3); }}
                
                /* HEADER */
                .header {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 50%, #162a52 100%); color: white; text-align: center; padding: 30px 20px; position: relative; }}
                .header-content {{ position: relative; z-index: 2; }}
                .logo {{ font-size: 32px; font-weight: 900; margin-bottom: 10px; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); background: linear-gradient(45deg, #ffffff, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
                .subtitle {{ font-size: 16px; opacity: 0.95; font-weight: 300; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }}
                .security-badge {{ background: rgba(246, 173, 85, 0.2); border: 2px solid #f6ad55; color: #f6ad55; padding: 6px 15px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 15px; display: inline-block; }}
                
                /* BODY CONTENT */
                .content {{ padding: 30px 20px; background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%); }}
                .hero-image {{ text-align: center; margin-bottom: 25px; }}
                .hero-icon {{ font-size: 48px; background: linear-gradient(135deg, #162a52, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; filter: drop-shadow(0 2px 4px rgba(22, 42, 82, 0.2)); }}
                .greeting {{ font-size: 20px; color: #162a52; margin-bottom: 20px; font-weight: 700; text-align: center; }}
                .message {{ color: #4a5568; line-height: 1.6; margin-bottom: 25px; font-size: 15px; text-align: center; }}
                
                /* OTP SECTION */
                .otp-section {{ background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border: 2px solid #f6ad55; border-radius: 15px; padding: 25px 15px; text-align: center; margin: 25px 0; position: relative; }}
                .otp-section::before {{ content: '🔐'; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #162a52, #2c4a7a); color: white; padding: 10px; border-radius: 50%; font-size: 18px; border: 3px solid #f6ad55; }}
                .otp-label {{ color: #162a52; font-weight: 700; margin-bottom: 15px; font-size: 16px; margin-top: 10px; }}
                .otp-code {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 100%); color: white; font-size: 28px; font-weight: 900; padding: 15px 20px; border-radius: 10px; letter-spacing: 8px; display: inline-block; box-shadow: 0 8px 20px rgba(22, 42, 82, 0.3); border: 3px solid #f6ad55; text-shadow: 0 1px 2px rgba(0,0,0,0.3); }}
                
                /* LOYALTY SECTION */
                .loyalty-section {{ background: linear-gradient(135deg, #f6ad55 0%, #ff8f00 100%); color: white; padding: 20px 15px; border-radius: 15px; text-align: center; margin: 25px 0; position: relative; box-shadow: 0 6px 15px rgba(246, 173, 85, 0.3); }}
                .loyalty-section::before {{ content: '🏆'; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: white; color: #f6ad55; padding: 10px; border-radius: 50%; font-size: 18px; border: 3px solid #162a52; }}
                .loyalty-title {{ font-weight: 800; font-size: 18px; margin-bottom: 10px; margin-top: 10px; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }}
                .loyalty-text {{ font-size: 14px; opacity: 0.95; line-height: 1.4; }}
                
                /* WARNING SECTION */
                .warning {{ background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border: 2px solid #f6ad55; color: #e65100; padding: 20px 15px; border-radius: 15px; margin: 25px 0; position: relative; }}
                .warning::before {{ content: '⚠️'; position: absolute; top: -15px; left: 20px; background: #f6ad55; color: white; padding: 10px; border-radius: 50%; font-size: 16px; border: 3px solid white; }}
                .warning-title {{ font-weight: 800; margin-bottom: 15px; margin-left: 15px; font-size: 16px; color: #162a52; }}
                .warning ul {{ margin: 10px 0 0 25px; }}
                .warning li {{ margin: 8px 0; font-weight: 600; font-size: 13px; }}
                
                .divider {{ height: 2px; background: linear-gradient(90deg, transparent, #f6ad55, #162a52, #f6ad55, transparent); margin: 25px 0; border-radius: 1px; }}
                
                /* FOOTER */
                .footer {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 100%); color: white; padding: 25px 20px; text-align: center; position: relative; }}
                .footer-content {{ position: relative; z-index: 2; }}
                .footer-logo {{ font-size: 24px; font-weight: 900; margin-bottom: 15px; letter-spacing: 2px; background: linear-gradient(45deg, #ffffff, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
                .footer-text {{ color: rgba(255,255,255,0.9); font-size: 12px; margin: 8px 0; line-height: 1.4; }}
                .footer-brand {{ color: #f6ad55; font-weight: 700; }}
                .footer-tagline {{ color: #f6ad55; font-weight: 600; font-size: 14px; margin-top: 10px; }}
                
                /* MOBILE RESPONSIVE */
                @media only screen and (max-width: 480px) {{
                    body {{ padding: 5px; }}
                    .email-wrapper {{ border-radius: 10px; }}
                    .header {{ padding: 20px 15px; }}
                    .logo {{ font-size: 28px; letter-spacing: 1px; }}
                    .subtitle {{ font-size: 14px; }}
                    .security-badge {{ font-size: 11px; padding: 5px 12px; }}
                    .content {{ padding: 20px 15px; }}
                    .hero-icon {{ font-size: 40px; }}
                    .greeting {{ font-size: 18px; margin-bottom: 15px; }}
                    .message {{ font-size: 14px; margin-bottom: 20px; }}
                    .otp-section {{ padding: 20px 10px; margin: 20px 0; }}
                    .otp-label {{ font-size: 15px; margin-bottom: 12px; }}
                    .otp-code {{ font-size: 24px; padding: 12px 15px; letter-spacing: 6px; }}
                    .loyalty-section {{ padding: 15px 10px; margin: 20px 0; }}
                    .loyalty-title {{ font-size: 16px; }}
                    .loyalty-text {{ font-size: 13px; }}
                    .warning {{ padding: 15px 10px; margin: 20px 0; }}
                    .warning-title {{ font-size: 15px; margin-left: 10px; }}
                    .warning ul {{ margin-left: 20px; }}
                    .warning li {{ font-size: 12px; }}
                    .footer {{ padding: 20px 15px; }}
                    .footer-logo {{ font-size: 20px; }}
                    .footer-text {{ font-size: 11px; }}
                    .footer-tagline {{ font-size: 13px; }}
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <!-- HEADER -->
                <div class="header">
                    <div class="header-content">
                        <div class="logo">🏆 FLEVO</div>
                        <div class="subtitle">Tu programa de lealtad favorito</div>
                        <div class="security-badge">🛡️ Recuperación Segura</div>
                    </div>
                </div>
                
                <!-- BODY CONTENT -->
                <div class="content">
                    <div class="hero-image">
                        <div class="hero-icon">🔐🏆</div>
                    </div>
                    
                    <div class="greeting">¡Hola <strong>{nombre}</strong>! 👋</div>
                    
                    <div class="message">
                        Hemos recibido una solicitud para restablecer la contraseña de tu cuenta Flevo.<br>
                        Como parte de nuestro compromiso con la seguridad de tus <strong>puntos y recompensas</strong>,<br>
                        usa el siguiente código de verificación:
                    </div>
                    
                    <!-- OTP SECTION -->
                    <div class="otp-section">
                        <div class="otp-label">Tu código de verificación seguro</div>
                        <div class="otp-code">{otp_code}</div>
                    </div>
                    
                    <!-- LOYALTY SECTION -->
                    <div class="loyalty-section">
                        <div class="loyalty-title">🎯 Protección Total Flevo</div>
                        <div class="loyalty-text">Mantenemos seguros tus puntos, recompensas y beneficios exclusivos.<br>Tu lealtad es nuestro compromiso.</div>
                    </div>
                    
                    <!-- WARNING SECTION -->
                    <div class="warning">
                        <div class="warning-title">Información de Seguridad Importante</div>
                        <ul>
                            <li>Este código expira en <strong>10 minutos</strong></li>
                            <li>Solo puede ser usado <strong>una vez</strong></li>
                            <li>Nunca compartas este código con nadie</li>
                            <li>Si no solicitaste este cambio, ignora este email</li>
                        </ul>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div class="message">
                        Para completar el proceso, ingresa este código en la aplicación Flevo junto con tu nueva contraseña.<br>
                        <strong>¡Sigue acumulando puntos y disfrutando de increíbles recompensas!</strong>
                    </div>
                </div>
                
                <!-- FOOTER -->
                <div class="footer">
                    <div class="footer-content">
                        <div class="footer-logo">🏆 FLEVO</div>
                        <div class="footer-text">Este es un email automático, no respondas a este mensaje.</div>
                        <div class="footer-text">© 2025 <span class="footer-brand">Flevo App</span> - Sistema de Autenticación</div>
                        <div class="footer-tagline">Tu programa de lealtad de confianza</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_welcome_template(nombre: str) -> str:
        """Genera template HTML para email de bienvenida"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>¡Bienvenido a Flevo!</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #162a52 0%, #2c4a7a 50%, #162a52 100%); min-height: 100vh; padding: 10px; }}
                .email-wrapper {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 20px 40px rgba(22, 42, 82, 0.3); }}
                
                .header {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 50%, #162a52 100%); color: white; text-align: center; padding: 30px 20px; position: relative; }}
                .header-content {{ position: relative; z-index: 2; }}
                .logo {{ font-size: 32px; font-weight: 900; margin-bottom: 10px; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); background: linear-gradient(45deg, #ffffff, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
                .subtitle {{ font-size: 16px; opacity: 0.95; font-weight: 300; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }}
                .welcome-badge {{ background: rgba(246, 173, 85, 0.2); border: 2px solid #f6ad55; color: #f6ad55; padding: 6px 15px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 15px; display: inline-block; }}
                
                .content {{ padding: 30px 20px; background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%); }}
                .hero-image {{ text-align: center; margin-bottom: 25px; }}
                .hero-icon {{ font-size: 48px; background: linear-gradient(135deg, #162a52, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; filter: drop-shadow(0 2px 4px rgba(22, 42, 82, 0.2)); }}
                .greeting {{ font-size: 20px; color: #162a52; margin-bottom: 20px; font-weight: 700; text-align: center; }}
                .message {{ color: #4a5568; line-height: 1.6; margin-bottom: 25px; font-size: 15px; text-align: center; }}
                
                .welcome-section {{ background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border: 2px solid #f6ad55; border-radius: 15px; padding: 25px 15px; text-align: center; margin: 25px 0; position: relative; }}
                .welcome-section::before {{ content: '🎉'; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #162a52, #2c4a7a); color: white; padding: 10px; border-radius: 50%; font-size: 18px; border: 3px solid #f6ad55; }}
                .welcome-title {{ color: #162a52; font-weight: 800; margin-bottom: 15px; font-size: 18px; margin-top: 10px; }}
                .welcome-text {{ color: #4a5568; font-size: 15px; line-height: 1.5; }}
                
                .benefits-section {{ background: linear-gradient(135deg, #f6ad55 0%, #ff8f00 100%); color: white; padding: 20px 15px; border-radius: 15px; text-align: center; margin: 25px 0; position: relative; box-shadow: 0 6px 15px rgba(246, 173, 85, 0.3); }}
                .benefits-section::before {{ content: '🏆'; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: white; color: #f6ad55; padding: 10px; border-radius: 50%; font-size: 18px; border: 3px solid #162a52; }}
                .benefits-title {{ font-weight: 800; font-size: 18px; margin-bottom: 15px; margin-top: 10px; text-shadow: 0 1px 2px rgba(0,0,0,0.2); }}
                .benefits-list {{ text-align: left; margin: 15px 0; }}
                .benefit-item {{ margin: 8px 0; font-size: 14px; opacity: 0.95; }}
                
                .cta-section {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 100%); color: white; padding: 20px 15px; border-radius: 15px; text-align: center; margin: 25px 0; box-shadow: 0 6px 15px rgba(22, 42, 82, 0.3); }}
                .cta-title {{ font-weight: 800; font-size: 18px; margin-bottom: 15px; text-shadow: 0 1px 2px rgba(0,0,0,0.3); }}
                .cta-text {{ font-size: 14px; opacity: 0.95; line-height: 1.4; }}
                
                .divider {{ height: 2px; background: linear-gradient(90deg, transparent, #f6ad55, #162a52, #f6ad55, transparent); margin: 25px 0; border-radius: 1px; }}
                
                .footer {{ background: linear-gradient(135deg, #162a52 0%, #2c4a7a 100%); color: white; padding: 25px 20px; text-align: center; position: relative; }}
                .footer-content {{ position: relative; z-index: 2; }}
                .footer-logo {{ font-size: 24px; font-weight: 900; margin-bottom: 15px; letter-spacing: 2px; background: linear-gradient(45deg, #ffffff, #f6ad55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
                .footer-text {{ color: rgba(255,255,255,0.9); font-size: 12px; margin: 8px 0; line-height: 1.4; }}
                .footer-brand {{ color: #f6ad55; font-weight: 700; }}
                .footer-tagline {{ color: #f6ad55; font-weight: 600; font-size: 14px; margin-top: 10px; }}
                
                @media only screen and (max-width: 480px) {{
                    body {{ padding: 5px; }}
                    .email-wrapper {{ border-radius: 10px; }}
                    .header {{ padding: 20px 15px; }}
                    .logo {{ font-size: 28px; letter-spacing: 1px; }}
                    .subtitle {{ font-size: 14px; }}
                    .welcome-badge {{ font-size: 11px; padding: 5px 12px; }}
                    .content {{ padding: 20px 15px; }}
                    .hero-icon {{ font-size: 40px; }}
                    .greeting {{ font-size: 18px; margin-bottom: 15px; }}
                    .message {{ font-size: 14px; margin-bottom: 20px; }}
                    .welcome-section {{ padding: 20px 10px; margin: 20px 0; }}
                    .welcome-title {{ font-size: 16px; }}
                    .welcome-text {{ font-size: 14px; }}
                    .benefits-section {{ padding: 15px 10px; margin: 20px 0; }}
                    .benefits-title {{ font-size: 16px; }}
                    .benefit-item {{ font-size: 13px; }}
                    .cta-section {{ padding: 15px 10px; margin: 20px 0; }}
                    .cta-title {{ font-size: 16px; }}
                    .cta-text {{ font-size: 13px; }}
                    .footer {{ padding: 20px 15px; }}
                    .footer-logo {{ font-size: 20px; }}
                    .footer-text {{ font-size: 11px; }}
                    .footer-tagline {{ font-size: 13px; }}
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="header">
                    <div class="header-content">
                        <div class="logo">🏆 FLEVO</div>
                        <div class="subtitle">Tu programa de lealtad favorito</div>
                        <div class="welcome-badge">🎉 ¡Bienvenido!</div>
                    </div>
                </div>
                
                <div class="content">
                    <div class="hero-image">
                        <div class="hero-icon">🎉🏆</div>
                    </div>
                    
                    <div class="greeting">¡Hola <strong>{nombre}</strong>! 👋</div>
                    
                    <div class="message">
                        ¡Bienvenido a la familia Flevo! 🎊<br>
                        Tu cuenta ha sido creada exitosamente y ya puedes comenzar a<br>
                        <strong>acumular puntos y disfrutar de increíbles recompensas</strong>.
                    </div>
                    
                    <div class="welcome-section">
                        <div class="welcome-title">🚀 ¡Tu aventura de recompensas comienza ahora!</div>
                        <div class="welcome-text">Estás a un paso de descubrir un mundo lleno de beneficios exclusivos, puntos y premios increíbles.</div>
                    </div>
                    
                    <div class="benefits-section">
                        <div class="benefits-title">🎯 Lo que puedes hacer con Flevo</div>
                        <div class="benefits-list">
                            <div class="benefit-item">🔥 Acumula puntos con cada compra</div>
                            <div class="benefit-item">🎁 Canjea recompensas exclusivas</div>
                            <div class="benefit-item">⭐ Accede a ofertas especiales</div>
                            <div class="benefit-item">🏅 Sube de nivel y desbloquea beneficios</div>
                            <div class="benefit-item">💎 Disfruta de experiencias únicas</div>
                        </div>
                    </div>
                    
                    <div class="cta-section">
                        <div class="cta-title">🎊 ¡Comienza a ganar puntos hoy!</div>
                        <div class="cta-text">Inicia sesión en tu cuenta y descubre todas las formas de ganar puntos y obtener recompensas increíbles.</div>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div class="message">
                        Gracias por unirte a Flevo. Estamos emocionados de tenerte como parte de nuestra comunidad.<br>
                        <strong>¡Que comience la diversión! 🚀</strong>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="footer-content">
                        <div class="footer-logo">🏆 FLEVO</div>
                        <div class="footer-text">Este es un email automático, no respondas a este mensaje.</div>
                        <div class="footer-text">© 2025 <span class="footer-brand">Flevo App</span> - Sistema de Autenticación</div>
                        <div class="footer-tagline">Tu programa de lealtad de confianza</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def send_welcome_email(email: str, nombre: str) -> bool:
        """Envía email de bienvenida vía SMTP"""
        try:
            from app.config.settings import settings
            
            if not settings.smtp_username or not settings.smtp_password:
                return EmailService._send_simulated_welcome_email(email, nombre)
            
            html_content = EmailService.get_welcome_template(nombre)
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "🏆 ¡Bienvenido a Flevo! Tu aventura de recompensas comienza"
            msg['From'] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            msg['To'] = email
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
            server.quit()
            
            log_info("Email de bienvenida enviado exitosamente", email=email)
            return True
            
        except Exception as e:
            log_error("Error enviando email de bienvenida", error=e)
            return EmailService._send_simulated_welcome_email(email, nombre)
    
    @staticmethod
    def _send_simulated_welcome_email(email: str, nombre: str) -> bool:
        """Envía email de bienvenida simulado (para desarrollo)"""
        log_info("Email de bienvenida simulado", email=email)
        
        print(f"\n{'='*60}")
        print(f"🎉 EMAIL DE BIENVENIDA ENVIADO A: {email}")
        print(f"👋 USUARIO: {nombre}")
        print(f"🏆 ¡Bienvenido a Flevo!")
        print(f"{'='*60}\n")
        
        return True
    
    @staticmethod
    def send_password_reset_email(email: str, nombre: str, otp_code: str) -> bool:
        """Envía email de recuperación de contraseña vía SMTP"""
        try:
            from app.config.settings import settings
            
            # Si no hay configuración SMTP, usar modo simulado
            if not settings.smtp_username or not settings.smtp_password:
                return EmailService._send_simulated_email(email, nombre, otp_code)
            
            html_content = EmailService.get_password_reset_template(nombre, otp_code)
            
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "🏆 Flevo - Código de Recuperación Segura"
            msg['From'] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            msg['To'] = email
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
            server.quit()
            
            log_info("Email enviado exitosamente", email=email)
            return True
            
        except Exception as e:
            log_error("Error enviando email", error=e)
            # Fallback a modo simulado
            return EmailService._send_simulated_email(email, nombre, otp_code)
    
    @staticmethod
    def _send_simulated_email(email: str, nombre: str, otp_code: str) -> bool:
        """Envía email simulado (para desarrollo)"""
        log_info("Email simulado", email=email, otp_code=otp_code)
        
        print(f"\n{'='*60}")
        print(f"📧 EMAIL SIMULADO ENVIADO A: {email}")
        print(f"🔑 CÓDIGO OTP: {otp_code}")
        print(f"⏰ EXPIRA EN: 10 minutos")
        print(f"{'='*60}\n")
        
        return True
    
    @staticmethod
    def send_registration_otp_email(email: str, otp_code: str) -> bool:
        """Envía email con código OTP para registro"""
        try:
            from app.config.settings import settings
            
            # Si no hay configuración SMTP, usar modo simulado
            if not settings.smtp_username or not settings.smtp_password:
                return EmailService._send_simulated_registration_otp(email, otp_code)
            
            html_content = EmailService.get_registration_otp_template("Usuario", otp_code)
            
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "🏆 Flevo - Código de Verificación de Registro"
            msg['From'] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            msg['To'] = email
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
            server.quit()
            
            log_info("Email de OTP de registro enviado exitosamente", email=email)
            return True
            
        except Exception as e:
            log_error("Error enviando email de OTP de registro", error=e)
            return EmailService._send_simulated_registration_otp(email, otp_code)
    
    @staticmethod
    def _send_simulated_registration_otp(email: str, otp_code: str) -> bool:
        """Envía email de OTP de registro simulado (para desarrollo)"""
        log_info("Email de OTP de registro simulado", email=email, otp_code=otp_code)
        
        print(f"\n{'='*60}")
        print(f"📧 EMAIL OTP REGISTRO ENVIADO A: {email}")
        print(f"🔑 CÓDIGO OTP: {otp_code}")
        print(f"⏰ EXPIRA EN: 10 minutos")
        print(f"🎉 PROPÓSITO: Verificación de registro")
        print(f"{'='*60}\n")
        
        return True