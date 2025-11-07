from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re
from app.utils.security import SecurityValidator
from app.models.user_type import UserType

class UserRegister(BaseModel):
    """Schema para registro de usuario"""
    nombre: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    password: str
    user_type_hash: str
    
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
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v
    
    @validator('user_type_hash')
    def validate_user_type_hash(cls, v):
        if not v or len(v) != 64:
            raise ValueError('Código de tipo de usuario inválido')
        
        # Verificar que el hash existe en la BD (con manejo de errores)
        try:
            user_type = UserType.get_by_hash(v)
            if not user_type:
                raise ValueError('Tipo de usuario no válido')
        except Exception:
            # Si hay error de BD (tabla no existe), usar tipo por defecto
            if v != 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456':
                raise ValueError('Tipo de usuario no válido')
        
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
    user_type: str

class TokenResponse(BaseModel):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse