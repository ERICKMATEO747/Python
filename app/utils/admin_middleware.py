from fastapi import HTTPException, Depends
from app.services.auth_service import get_current_user
from typing import Dict

class AdminMiddleware:
    """Middleware para validar permisos de administrador"""
    
    @staticmethod
    def require_admin(current_user: Dict = Depends(get_current_user)) -> Dict:
        """Requiere que el usuario sea administrador"""
        if not current_user:
            raise HTTPException(status_code=401, detail="No autenticado")
        
        # Verificar si es admin (user_type_id = 3)
        if current_user.get("user_type") != 3:
            raise HTTPException(
                status_code=403, 
                detail="Acceso denegado. Se requieren permisos de administrador"
            )
        
        return current_user
    
    @staticmethod
    def require_admin_or_business(current_user: Dict = Depends(get_current_user)) -> Dict:
        """Requiere que el usuario sea admin o propietario de negocio"""
        if not current_user:
            raise HTTPException(status_code=401, detail="No autenticado")
        
        user_type = current_user.get("user_type")
        if user_type not in [2, 3]:  # negocio o admin
            raise HTTPException(
                status_code=403, 
                detail="Acceso denegado. Se requieren permisos de negocio o administrador"
            )
        
        return current_user