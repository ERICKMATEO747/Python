from fastapi import APIRouter, Depends, Query
from app.controllers.dashboard_controller import DashboardController
from app.controllers.reward_controller import RewardController
from app.controllers.menu_controller import MenuController
from app.models.audit_log import AuditLog
from app.utils.role_middleware import require_business, RoleMiddleware
from app.schemas.reward import RewardCreate, RewardUpdate
from app.schemas.business import MenuItemCreate, MenuItemUpdate, LoyaltyConfigUpdate, QRValidation, BusinessProfileUpdate
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/business", tags=["Business Portal"])

# Dashboard
@router.get("/{business_id}/dashboard")
async def get_dashboard(
    business_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Dashboard completo del negocio"""
    return DashboardController.get_business_dashboard(business_id, current_user)

# Perfil del Negocio
@router.get("/{business_id}/profile")
async def get_business_profile(
    business_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene perfil del negocio para edición"""
    from app.controllers.business_controller import BusinessController
    return BusinessController.get_business_profile(business_id, current_user)

@router.put("/{business_id}/profile")
async def update_business_profile(
    business_id: int,
    profile_data: BusinessProfileUpdate,
    current_user: dict = Depends(require_business)
):
    """Actualiza perfil del negocio"""
    # Validar ownership manualmente
    from app.config.database import get_db_connection
    from fastapi import HTTPException
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT owner_user_id FROM businesses 
                WHERE id = %s AND active = 1
            """, (business_id,))
            
            business = cursor.fetchone()
            if not business:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            
            if business.get('owner_user_id') != current_user['id']:
                raise HTTPException(status_code=403, detail="No tienes permisos para este negocio")
    finally:
        connection.close()
    
    from app.controllers.business_controller import BusinessController
    return BusinessController.update_business_profile(business_id, profile_data, current_user)

# Gestión de Menú
@router.get("/{business_id}/menu")
async def get_menu(
    business_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene menú del negocio"""
    return MenuController.get_business_menu(business_id)

@router.get("/{business_id}/menu/items/{item_id}")
async def get_menu_item(
    business_id: int,
    item_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene item específico del menú"""
    return MenuController.get_menu_item(business_id, item_id)

@router.post("/{business_id}/menu/items")
async def create_menu_item(
    business_id: int,
    item_data: MenuItemCreate,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Crea item de menú"""
    return MenuController.create_menu_item(business_id, item_data, current_user)

@router.put("/{business_id}/menu/items/{item_id}")
async def update_menu_item(
    business_id: int,
    item_id: int,
    item_data: MenuItemUpdate,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Actualiza item de menú"""
    return MenuController.update_menu_item(business_id, item_id, item_data, current_user)

@router.delete("/{business_id}/menu/items/{item_id}")
async def delete_menu_item(
    business_id: int,
    item_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Elimina item de menú"""
    return MenuController.delete_menu_item(business_id, item_id, current_user)

# Gestión de Premios
@router.get("/{business_id}/rewards")
async def get_rewards(
    business_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene premios del negocio"""
    return RewardController.get_business_rewards(business_id)

@router.post("/{business_id}/rewards")
async def create_reward(
    business_id: int,
    reward_data: RewardCreate,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Crea nuevo premio"""
    reward_data.business_id = business_id
    return RewardController.create_reward(reward_data)

@router.put("/{business_id}/rewards/{reward_id}")
async def update_reward(
    business_id: int,
    reward_id: int,
    reward_data: RewardUpdate,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Actualiza premio"""
    return RewardController.update_reward(reward_id, reward_data)

@router.delete("/{business_id}/rewards/{reward_id}")
async def delete_reward(
    business_id: int,
    reward_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Elimina premio"""
    return RewardController.delete_reward(reward_id, current_user)

# Configuración del Programa de Lealtad
@router.get("/{business_id}/loyalty-config")
async def get_loyalty_config(
    business_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene configuración del programa de lealtad"""
    from app.services.loyalty_service import LoyaltyService
    return LoyaltyService.get_config(business_id)

@router.put("/{business_id}/loyalty-config")
async def update_loyalty_config(
    business_id: int,
    config_data: LoyaltyConfigUpdate,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Actualiza configuración del programa de lealtad"""
    from app.services.loyalty_service import LoyaltyService
    return LoyaltyService.update_config(business_id, config_data, current_user)

# Audit Trail
@router.get("/{business_id}/audit")
async def get_audit_logs(
    business_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    action_type: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene logs de auditoría del negocio"""
    start_dt = datetime.fromisoformat(start_date) if start_date else None
    end_dt = datetime.fromisoformat(end_date) if end_date else None
    
    logs = AuditLog.get_business_logs(
        business_id=business_id,
        start_date=start_dt,
        end_date=end_dt,
        action_type=action_type,
        limit=limit,
        offset=offset
    )
    
    return {"success": True, "data": logs}

# Progreso de Cliente
@router.get("/{business_id}/customer/{user_id}/progress")
async def get_customer_progress(
    business_id: int,
    user_id: int,
    current_user: dict = Depends(RoleMiddleware.validate_business_ownership)
):
    """Obtiene progreso de un cliente específico"""
    from app.services.customer_service import CustomerService
    return CustomerService.get_customer_progress(user_id, business_id)

# Validación QR
@router.post("/validate-qr")
async def validate_qr(
    qr_data: QRValidation,
    current_user: dict = Depends(RoleMiddleware.validate_business_user)
):
    """Valida código QR para registrar visita"""
    from app.models.user_visit import UserVisit
    from app.config.database import get_db_connection
    from datetime import datetime
    
    try:
        # Verificar QR
        qr_info = UserVisit.verify_qr_code(qr_data.qr_token)
        if not qr_info:
            return {
                "success": False, 
                "error": "Código QR inválido o expirado",
                "message": "El código QR escaneado no es válido o ha expirado. Por favor, solicita al cliente que genere un nuevo código QR desde la aplicación."
            }
        
        user_id = qr_info['user_id']
        qr_business_id = qr_info['business_id']
        
        # Verificar que el QR sea para este negocio
        if qr_business_id != qr_data.business_id:
            return {
                "success": False, 
                "error": "QR de otro negocio",
                "message": "Este código QR pertenece a otro negocio. Verifica que el cliente esté mostrando el QR correcto para tu establecimiento."
            }
        
        # Verificar ownership del negocio
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT owner_user_id, name FROM businesses 
                    WHERE id = %s AND active = 1
                """, (qr_data.business_id,))
                
                business = cursor.fetchone()
                if not business:
                    return {
                        "success": False, 
                        "error": "Negocio no encontrado",
                        "message": "No se pudo encontrar la información del negocio. Contacta al soporte técnico."
                    }
                
                if business['owner_user_id'] != current_user['id']:
                    return {
                        "success": False, 
                        "error": "Sin permisos",
                        "message": "No tienes permisos para registrar visitas en este negocio. Verifica que estés usando la cuenta correcta."
                    }
                
                # Obtener nombre del usuario
                cursor.execute("SELECT nombre FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                if not user:
                    return {
                        "success": False, 
                        "error": "Cliente no encontrado",
                        "message": "No se pudo encontrar la información del cliente. Es posible que la cuenta haya sido eliminada."
                    }
                
                # Verificar si ya visitó en los últimos 5 minutos
                from datetime import timedelta
                five_minutes_ago = datetime.now() - timedelta(minutes=5)
                
                cursor.execute("""
                    SELECT visit_date FROM user_visits 
                    WHERE user_id = %s AND business_id = %s AND visit_date >= %s
                    ORDER BY visit_date DESC LIMIT 1
                """, (user_id, qr_data.business_id, five_minutes_ago))
                
                recent_visit = cursor.fetchone()
                if recent_visit:
                    last_visit = recent_visit['visit_date']
                    time_diff = datetime.now() - last_visit
                    minutes_ago = int(time_diff.total_seconds() / 60)
                    
                    return {
                        "success": False, 
                        "error": "Visita ya registrada",
                        "message": f"{user['nombre']} ya registró una visita hace {minutes_ago} minuto(s). Debe esperar 5 minutos entre visitas."
                    }
                
                # Registrar visita
                success = UserVisit.register_visit(user_id, qr_data.business_id, datetime.now())
                if not success:
                    return {
                        "success": False, 
                        "error": "Error al registrar",
                        "message": "Ocurrió un problema al registrar la visita. Inténtalo nuevamente en unos momentos."
                    }
                
                # Enviar notificaciones push al cliente
                from app.services.push_notification_service import PushNotificationService
                from app.services.websocket_service import websocket_service
                import asyncio
                
                try:
                    # Obtener progreso actual del usuario
                    cursor.execute("""
                        SELECT ur.progress_in_round, b.visits_for_prize
                        FROM user_rounds ur
                        JOIN businesses b ON ur.business_id = b.id
                        WHERE ur.user_id = %s AND ur.business_id = %s AND ur.is_completed = 0
                        ORDER BY ur.id DESC LIMIT 1
                    """, (user_id, qr_data.business_id))
                    
                    progress_data = cursor.fetchone()
                    if progress_data:
                        progress = progress_data['progress_in_round']
                        max_visits = progress_data['visits_for_prize']
                    else:
                        progress = 1
                        max_visits = 6
                    
                    # Preparar datos para notificación
                    visit_notification_data = {
                        'id': None,
                        'progress_in_round': progress,
                        'max_visits_per_round': max_visits
                    }
                    
                    # Enviar notificación push
                    push_service = PushNotificationService()
                    push_service.notify_visit_registered(
                        user_id,
                        business['name'],
                        visit_notification_data
                    )
                    
                    # Enviar WebSocket
                    asyncio.create_task(
                        websocket_service.notify_visit_registered(
                            user_id,
                            qr_data.business_id,
                            visit_notification_data
                        )
                    )
                    
                except Exception as notification_error:
                    # Log error pero no fallar la respuesta
                    print(f"Error enviando notificaciones: {notification_error}")
                
                return {
                    "success": True,
                    "message": f"¡Visita registrada exitosamente para {user['nombre']}!",
                    "data": {
                        "customer_name": user['nombre'],
                        "business_name": business['name'],
                        "visit_date": datetime.now().isoformat()
                    }
                }
        finally:
            connection.close()
            
    except Exception as e:
        return {
            "success": False, 
            "error": "Error del sistema",
            "message": "Ocurrió un error inesperado en el sistema. Por favor, inténtalo nuevamente. Si el problema persiste, contacta al soporte técnico."
        }