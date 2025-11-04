import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config.settings import settings
from app.models.user import User
from typing import Optional, Dict

class AuthService:
    """Servicio de autenticación con lógica de negocio"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Encripta la contraseña usando bcrypt con 12 salt rounds"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifica la contraseña con bcrypt"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Genera un JWT token con expiración de 24 horas"""
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expire_hours)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    @staticmethod
    def register_user(nombre: str, email: Optional[str], telefono: Optional[str], password: str) -> Dict:
        """Registra un nuevo usuario"""
        # Verificar si el email o teléfono ya existen
        if email:
            existing_user = User.get_by_email(email)
            if existing_user:
                raise ValueError("El email ya está registrado")
        
        if telefono:
            existing_user = User.get_by_telefono(telefono)
            if existing_user:
                raise ValueError("El teléfono ya está registrado")
        
        # Encriptar contraseña y crear usuario
        hashed_password = AuthService.hash_password(password)
        user = User.create(nombre, email, telefono, hashed_password)
        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict]:
        """Autentica un usuario y retorna sus datos si es válido"""
        user = User.get_by_email(email)
        if not user:
            return None
        
        if not AuthService.verify_password(password, user['password']):
            return None
        
        # Retornar usuario sin contraseña
        return {
            "id": user['id'],
            "nombre": user['nombre'],
            "email": user['email'],
            "telefono": user['telefono']
        }