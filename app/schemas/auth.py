from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re
from app.utils.security import SecurityValidator

class UserRegister(BaseModel):
    """Schema para registro de usuario"""
    nombre: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    password: str
    
    @validator('nombre')
    def validate_nombre(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        # Sanitizar input
        sanitized = SecurityValidator.sanitize_input(v)
        if len(sanitized) < 2:
            raise ValueError('Nombre contiene caracteres no válidos')
        return sanitized
    
    @validator('telefono')
    def validate_telefono(cls, v):
        if v is not None:
            if not SecurityValidator.validate_phone_format(v):
                raise ValueError('Formato de teléfono inválido')
            clean_phone = re.sub(r'[^0-9+]', '', v)
            return clean_phone
        return v
    
    @validator('password')
    def validate_password(cls, v):
        is_valid, message = SecurityValidator.validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v
    
    @validator('email')
    def validate_contact_info(cls, v, values):
        telefono = values.get('telefono')
        if not v and not telefono:
            raise ValueError('Debe proporcionar al menos email o teléfono')
        return v

class UserLogin(BaseModel):
    """Schema para login de usuario"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema para respuesta de usuario (sin contraseña)"""
    id: int
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class TokenResponse(BaseModel):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse