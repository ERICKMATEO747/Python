from app.config.database_sqlite import get_db_connection
from app.utils.logger import log_info, log_error
from app.models.user_type import UserType
from typing import Optional, Dict

class User:
    """Modelo para operaciones de usuario en la base de datos"""
    
    @staticmethod
    def create(nombre: str, email: Optional[str], telefono: Optional[str], hashed_password: str, user_type_hash: str) -> Dict:
        """Crea un nuevo usuario en la base de datos"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            # Obtener user_type_id por hash con fallback
            try:
                user_type = UserType.get_by_hash(user_type_hash)
                if not user_type:
                    user_type = {'id': 1, 'type_name': 'cliente'}
            except Exception:
                user_type = {'id': 1, 'type_name': 'cliente'}
            
            cursor.execute(
                "INSERT INTO users (nombre, email, telefono, password, user_type_id) VALUES (?, ?, ?, ?, ?)",
                (nombre, email, telefono, hashed_password, user_type['id'])
            )
            user_id = cursor.lastrowid
            connection.commit()
            return {
                "id": user_id,
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "user_type": user_type['id']
            }
        except Exception as e:
            log_error("Error creando usuario", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """Obtiene un usuario por email"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, nombre, email, telefono, password, user_type_id as user_type FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            connection.close()
    
    @staticmethod
    def get_by_telefono(telefono: str) -> Optional[Dict]:
        """Obtiene un usuario por teléfono"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE telefono = ?", (telefono,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por ID"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, nombre, email, telefono, user_type_id as user_type FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            connection.close()