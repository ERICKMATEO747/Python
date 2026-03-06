from fastapi import HTTPException
from app.services.admin_service import AdminService
from app.schemas.admin import BusinessCreate, BusinessUpdate, UserCreate, UserUpdate, AdminDashboardFilters
from typing import Dict, List, Optional

class AdminController:
    
    @staticmethod
    def get_dashboard(filters: Optional[AdminDashboardFilters] = None):
        """Obtiene dashboard de administrador"""
        try:
            dashboard_data = AdminService.get_dashboard_stats(filters)
            return {"success": True, "data": dashboard_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo dashboard: {str(e)}")
    
    @staticmethod
    def get_all_businesses(page: int = 1, limit: int = 20, search: Optional[str] = None):
        """Obtiene todos los negocios con paginación"""
        try:
            businesses = AdminService.get_all_businesses(page, limit, search)
            return {"success": True, "data": businesses}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo negocios: {str(e)}")
    
    @staticmethod
    def create_business(business_data: BusinessCreate, current_user: Dict):
        """Crea un nuevo negocio"""
        try:
            business = AdminService.create_business(business_data, current_user["id"])
            return {"success": True, "message": "Negocio creado exitosamente", "data": business}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creando negocio: {str(e)}")
    
    @staticmethod
    def update_business(business_id: int, business_data: BusinessUpdate, current_user: Dict):
        """Actualiza un negocio"""
        try:
            business = AdminService.update_business(business_id, business_data, current_user["id"])
            if not business:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            return {"success": True, "message": "Negocio actualizado exitosamente", "data": business}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error actualizando negocio: {str(e)}")
    
    @staticmethod
    def delete_business(business_id: int, current_user: Dict):
        """Elimina (desactiva) un negocio"""
        try:
            success = AdminService.delete_business(business_id, current_user["id"])
            if not success:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            return {"success": True, "message": "Negocio eliminado exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error eliminando negocio: {str(e)}")
    
    @staticmethod
    def get_all_users(page: int = 1, limit: int = 20, search: Optional[str] = None, user_type: Optional[int] = None):
        """Obtiene todos los usuarios con paginación"""
        try:
            users = AdminService.get_all_users(page, limit, search, user_type)
            return {"success": True, "data": users}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo usuarios: {str(e)}")
    
    @staticmethod
    def create_user(user_data: UserCreate, current_user: Dict):
        """Crea un nuevo usuario"""
        try:
            user = AdminService.create_user(user_data, current_user["id"])
            return {"success": True, "message": "Usuario creado exitosamente", "data": user}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creando usuario: {str(e)}")
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate, current_user: Dict):
        """Actualiza un usuario"""
        try:
            user = AdminService.update_user(user_id, user_data, current_user["id"])
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"success": True, "message": "Usuario actualizado exitosamente", "data": user}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error actualizando usuario: {str(e)}")
    
    @staticmethod
    def get_system_stats():
        """Obtiene estadísticas del sistema"""
        try:
            stats = AdminService.get_system_stats()
            return {"success": True, "data": stats}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")