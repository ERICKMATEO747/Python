import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import settings
from app.models.user_sqlite import User
from app.config.database_sqlite import get_db_connection
from typing import Optional, Dict

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict]:
    """Obtiene el usuario actual desde el token JWT"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    user = AuthService.verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return user

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
    def register_user(nombre: str, email: Optional[str], telefono: Optional[str], password: str, user_type_hash: str) -> Dict:
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
        user = User.create(nombre, email, telefono, hashed_password, user_type_hash)
        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict]:
        """Autentica un usuario y retorna sus datos si es válido"""
        user = User.get_by_email(email)
        if not user:
            return None
        
        if not AuthService.verify_password(password, user['password']):
            return None
        
        # Datos base del usuario
        user_data = {
            "id": user['id'],
            "nombre": user['nombre'],
            "email": user['email'],
            "telefono": user['telefono'],
            "user_type": user['user_type']
        }
        
        # Si es usuario tipo negocio (2), agregar business_id
        if user['user_type'] == 2:
            connection = get_db_connection()
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT id FROM businesses WHERE name LIKE ? LIMIT 1",
                    ('%' + user['nombre'].split()[0] + '%',)
                )
                business = cursor.fetchone()
                if business:
                    user_data['business_id'] = business[0]
            finally:
                connection.close()
        
        return user_data
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """Verifica y decodifica un JWT token"""
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            user_id = int(payload.get("sub"))
            if user_id is None:
                return None
            
            user = User.get_by_id(user_id)
            if user is None:
                return None
            
            return {
                "id": user['id'],
                "nombre": user['nombre'],
                "email": user['email'],
                "telefono": user['telefono'],
                "user_type": user.get('user_type', 1)
            }
        except JWTError:
            return None