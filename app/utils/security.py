import re
from typing import Optional
from fastapi import Request
import time

class SecurityValidator:
    """Validador de seguridad para inputs"""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitiza input removiendo caracteres peligrosos"""
        if not text:
            return ""
        # Remover caracteres SQL peligrosos
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
        sanitized = text
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        return sanitized.strip()
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone_format(phone: str) -> bool:
        """Valida formato de teléfono"""
        clean_phone = re.sub(r'[^0-9+]', '', phone)
        return len(clean_phone) >= 10 and len(clean_phone) <= 15
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Valida fortaleza de contraseña"""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe tener al menos una mayúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe tener al menos una minúscula"
        
        if not re.search(r'[0-9]', password):
            return False, "La contraseña debe tener al menos un número"
        
        return True, "Contraseña válida"

class RateLimiter:
    """Rate limiter simple en memoria"""
    
    def __init__(self):
        self.requests = {}
        self.max_requests = 5
        self.window_seconds = 300  # 5 minutos
    
    def is_allowed(self, client_ip: str) -> bool:
        """Verifica si la IP puede hacer más requests"""
        current_time = time.time()
        
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Limpiar requests antiguos
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window_seconds
        ]
        
        # Verificar límite
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        
        # Agregar request actual
        self.requests[client_ip].append(current_time)
        return True

# Instancia global del rate limiter
rate_limiter = RateLimiter()