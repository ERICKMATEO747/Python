from fastapi import HTTPException
from app.services.dashboard_service import DashboardService
from app.models.audit_log import AuditLog

class DashboardController:
    """Controlador para dashboard de negocios"""
    
    @staticmethod
    def get_business_dashboard(business_id: int, current_user: dict):
        """Obtiene dashboard completo del negocio"""
        try:
            # Registrar acceso al dashboard
            AuditLog.log_action(
                user_id=current_user['id'],
                action_type='DASHBOARD_ACCESS',
                description=f"Acceso al dashboard del negocio {business_id}",
                business_id=business_id
            )
            
            dashboard_data = DashboardService.get_business_dashboard(business_id)
            
            if not dashboard_data:
                raise HTTPException(status_code=404, detail="No se pudo obtener datos del dashboard")
            
            return {
                "success": True,
                "data": dashboard_data
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")