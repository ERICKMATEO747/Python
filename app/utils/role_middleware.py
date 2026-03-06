from fastapi import HTTPException, status, Depends
from app.utils.auth_middleware import get_current_user
from typing import Dict, List

class RoleMiddleware:
    """Middleware para validación de roles y permisos"""
    
    @staticmethod
    def require_role(allowed_roles: List[int]):
        """Decorator para requerir roles específicos"""
        def role_checker(current_user: Dict = Depends(get_current_user)) -> Dict:
            user_type = current_user.get('user_type', 1)
            if user_type not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Acceso denegado. Rol requerido: {allowed_roles}"
                )
            return current_user
        return role_checker
    
    @staticmethod
    def require_business_owner(current_user: Dict = Depends(get_current_user)) -> Dict:
        """Valida que el usuario sea tipo negocio (2)"""
        if current_user.get('user_type') != 2:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo usuarios tipo negocio pueden acceder"
            )
        return current_user
    
    @staticmethod
    def validate_business_ownership(business_id: int, current_user: Dict = Depends(get_current_user)) -> Dict:
        """Valida que el negocio pertenezca al usuario"""
        from app.config.database import get_db_connection
        
        if current_user.get('user_type') != 2:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo usuarios tipo negocio pueden acceder"
            )
        
        # Verificar ownership del negocio
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT owner_user_id FROM businesses 
                    WHERE id = %s AND active = 1
                """, (business_id,))
                
                business = cursor.fetchone()
                if not business:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Negocio no encontrado"
                    )
                
                if business.get('owner_user_id') != current_user['id']:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permisos para este negocio"
                    )
                
                return current_user
        finally:
            connection.close()

    @staticmethod
    def validate_business_user(current_user: Dict = Depends(get_current_user)) -> Dict:
        """Valida que el usuario sea tipo negocio sin verificar ownership específico"""
        if current_user.get('user_type') != 2:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo usuarios tipo negocio pueden acceder"
            )
        return current_user

# Shortcuts para roles comunes
require_client = RoleMiddleware.require_role([1])
require_business = RoleMiddleware.require_role([2])
require_admin = RoleMiddleware.require_role([3])
require_business_or_admin = RoleMiddleware.require_role([2, 3])