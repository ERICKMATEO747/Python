from fastapi import APIRouter, Depends, Query
from app.controllers.admin_controller import AdminController
from app.schemas.admin import BusinessCreate, BusinessUpdate, UserCreate, UserUpdate, AdminDashboardFilters
from app.utils.admin_middleware import AdminMiddleware
from typing import Optional

router = APIRouter(prefix="/api/admin", tags=["Admin Panel"])

# Dashboard
@router.get("/dashboard")
async def get_admin_dashboard(
    start_date: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    municipality_id: Optional[int] = Query(None, description="ID del municipio"),
    category: Optional[str] = Query(None, description="Categoría de negocio"),
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Dashboard principal del administrador con estadísticas generales
    
    - **start_date**: Filtro de fecha inicio (opcional)
    - **end_date**: Filtro de fecha fin (opcional)
    - **municipality_id**: Filtro por municipio (opcional)
    - **category**: Filtro por categoría (opcional)
    """
    filters = AdminDashboardFilters(
        start_date=start_date,
        end_date=end_date,
        municipality_id=municipality_id,
        category=category
    )
    return AdminController.get_dashboard(filters)

@router.get("/stats")
async def get_system_stats(
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """Obtiene estadísticas generales del sistema"""
    return AdminController.get_system_stats()

# Gestión de Negocios
@router.get("/businesses")
async def get_all_businesses(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre, categoría o dirección"),
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Obtiene todos los negocios con paginación y búsqueda
    
    - **page**: Número de página (mínimo 1)
    - **limit**: Elementos por página (1-100)
    - **search**: Término de búsqueda (opcional)
    """
    return AdminController.get_all_businesses(page, limit, search)

@router.post("/businesses")
async def create_business(
    business_data: BusinessCreate,
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Crea un nuevo negocio
    
    - **name**: Nombre del negocio
    - **category**: Categoría del negocio
    - **address**: Dirección
    - **municipality_id**: ID del municipio
    - **phone**: Teléfono
    - **owner_email**: Email del propietario (debe existir)
    - **visits_for_prize**: Visitas necesarias para premio (default: 6)
    """
    return AdminController.create_business(business_data, current_user)

@router.put("/businesses/{business_id}")
async def update_business(
    business_id: int,
    business_data: BusinessUpdate,
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Actualiza un negocio existente
    
    - **business_id**: ID del negocio a actualizar
    - Todos los campos son opcionales
    """
    return AdminController.update_business(business_id, business_data, current_user)

@router.delete("/businesses/{business_id}")
async def delete_business(
    business_id: int,
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Elimina (desactiva) un negocio
    
    - **business_id**: ID del negocio a eliminar
    """
    return AdminController.delete_business(business_id, current_user)

# Gestión de Usuarios
@router.get("/users")
async def get_all_users(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    search: Optional[str] = Query(None, description="Búsqueda por nombre o email"),
    user_type: Optional[str] = Query(None, description="Filtro por tipo de usuario (1=cliente, 2=negocio, 3=admin)"),
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Obtiene todos los usuarios con paginación y filtros
    
    - **page**: Número de página (mínimo 1)
    - **limit**: Elementos por página (1-100)
    - **search**: Término de búsqueda (opcional)
    - **user_type**: Filtro por tipo (1=cliente, 2=negocio, 3=admin)
    """
    # Convertir user_type de string a int o None
    user_type_int = None
    if user_type and user_type.strip():
        try:
            user_type_int = int(user_type)
        except ValueError:
            pass
    
    return AdminController.get_all_users(page, limit, search, user_type_int)

@router.post("/users")
async def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Crea un nuevo usuario
    
    - **nombre**: Nombre completo
    - **email**: Email (opcional pero recomendado)
    - **telefono**: Teléfono (opcional)
    - **password**: Contraseña
    - **user_type**: Tipo de usuario (1=cliente, 2=negocio, 3=admin)
    """
    return AdminController.create_user(user_data, current_user)

@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Actualiza un usuario existente
    
    - **user_id**: ID del usuario a actualizar
    - Todos los campos son opcionales
    """
    return AdminController.update_user(user_id, user_data, current_user)

# Gestión de Suscripciones
@router.get("/subscriptions")
async def get_all_subscriptions(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    status: Optional[str] = Query(None, description="Filtro por estado (trial, active, pending_payment, expired)"),
    plan_type: Optional[str] = Query(None, description="Filtro por tipo de plan (monthly, bimonthly, semiannual, annual)"),
    expiring_soon: bool = Query(False, description="Filtro para suscripciones que vencen pronto"),
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Obtiene todas las suscripciones con paginación y filtros
    
    - **page**: Número de página (mínimo 1)
    - **limit**: Elementos por página (1-100)
    - **status**: Filtro por estado (opcional)
    - **plan_type**: Filtro por tipo de plan (opcional)
    - **expiring_soon**: Filtro para suscripciones que vencen en 7 días
    """
    # Convertir strings vacíos a None
    if status == "":
        status = None
    if plan_type == "":
        plan_type = None
    
    return {"success": True, "data": {"subscriptions": [], "pagination": {"page": page, "limit": limit, "total": 0, "pages": 0}}}

# Gestión de Pagos
@router.get("/payments")
async def get_all_payments(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(20, ge=1, le=100, description="Elementos por página"),
    status: Optional[str] = Query(None, description="Filtro por estado (pending, completed, failed, refunded)"),
    method: Optional[str] = Query(None, description="Filtro por método (stripe, mercadopago, cash, transfer)"),
    start_date: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Obtiene todos los pagos con paginación y filtros
    
    - **page**: Número de página (mínimo 1)
    - **limit**: Elementos por página (1-100)
    - **status**: Filtro por estado (opcional)
    - **method**: Filtro por método de pago (opcional)
    - **start_date**: Filtro de fecha inicio (opcional)
    - **end_date**: Filtro de fecha fin (opcional)
    """
    # Convertir strings vacíos a None
    if status == "":
        status = None
    if method == "":
        method = None
    if start_date == "":
        start_date = None
    if end_date == "":
        end_date = None
    
    return {"success": True, "data": {"payments": [], "pagination": {"page": page, "limit": limit, "total": 0, "pages": 0}}}

# Gestión de Alertas de Facturación
@router.get("/billing/alerts")
async def get_billing_alerts(
    priority: Optional[str] = Query(None, description="Filtro por prioridad (low, medium, high, critical)"),
    status: Optional[str] = Query(None, description="Filtro por estado (active, resolved, dismissed)"),
    current_user: dict = Depends(AdminMiddleware.require_admin)
):
    """
    Obtiene alertas de facturación y pagos
    
    - **priority**: Filtro por prioridad (opcional)
    - **status**: Filtro por estado (opcional)
    """
    # Convertir strings vacíos a None
    if priority == "":
        priority = None
    if status == "":
        status = None
    
    return {"success": True, "data": {"alerts": []}}