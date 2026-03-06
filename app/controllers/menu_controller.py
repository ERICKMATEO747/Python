from fastapi import HTTPException
from app.services.menu_service import MenuService
from app.models.audit_log import AuditLog
from app.schemas.business import MenuItemCreate, MenuItemUpdate

class MenuController:
    """Controlador para gestión de menú"""
    
    @staticmethod
    def get_business_menu(business_id: int):
        """Obtiene el menú completo del negocio"""
        try:
            menu = MenuService.get_business_menu(business_id)
            return {
                "success": True,
                "data": menu
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_menu_item(business_id: int, item_id: int):
        """Obtiene un item específico del menú"""
        try:
            item = MenuService.get_menu_item(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            
            if item['business_id'] != business_id:
                raise HTTPException(status_code=403, detail="No tienes permisos para este item")
            
            return {
                "success": True,
                "data": {
                    "id": item['id'],
                    "name": item['producto'],
                    "description": item['descripcion'],
                    "price": float(item['precio']),
                    "category": item['categoria'],
                    "available": bool(item['disponible']),
                    "created_at": item['created_at']
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def create_menu_item(business_id: int, item_data: MenuItemCreate, current_user: dict):
        """Crea un nuevo item de menú"""
        try:
            item_id = MenuService.create_menu_item(business_id, item_data.dict())
            
            if not item_id:
                raise HTTPException(status_code=400, detail="No se pudo crear el item")
            
            # Registrar en audit trail
            AuditLog.log_action(
                user_id=current_user['id'],
                action_type='MENU_UPDATE',
                description=f"Item de menú creado: {item_data.name}",
                business_id=business_id,
                new_values={"item_id": item_id, "name": item_data.name, "price": float(item_data.price)}
            )
            
            return {
                "success": True,
                "message": "Item agregado al menú",
                "data": {
                    "item_id": item_id,
                    "name": item_data.name,
                    "price": item_data.price
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_menu_item(business_id: int, item_id: int, item_data: MenuItemUpdate, current_user: dict):
        """Actualiza un item de menú"""
        try:
            # Obtener datos anteriores
            old_item = MenuService.get_menu_item(item_id)
            if not old_item:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            
            # Verificar ownership
            if old_item['business_id'] != business_id:
                raise HTTPException(status_code=403, detail="No tienes permisos para este item")
            
            update_data = item_data.dict(exclude_unset=True)
            success = MenuService.update_menu_item(item_id, update_data)
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el item")
            
            # Registrar en audit trail
            AuditLog.log_action(
                user_id=current_user['id'],
                action_type='MENU_UPDATE',
                description=f"Item de menú actualizado: {old_item['name']}",
                business_id=business_id,
                old_values={"name": old_item['name'], "price": float(old_item['price'])},
                new_values=update_data
            )
            
            return {
                "success": True,
                "message": "Item actualizado exitosamente"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def delete_menu_item(business_id: int, item_id: int, current_user: dict):
        """Elimina un item de menú"""
        try:
            # Obtener datos del item
            item = MenuService.get_menu_item(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            
            # Verificar ownership
            if item['business_id'] != business_id:
                raise HTTPException(status_code=403, detail="No tienes permisos para este item")
            
            success = MenuService.delete_menu_item(item_id)
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo eliminar el item")
            
            # Registrar en audit trail
            AuditLog.log_action(
                user_id=current_user['id'],
                action_type='MENU_UPDATE',
                description=f"Item de menú eliminado: {item['name']}",
                business_id=business_id,
                old_values={"item_id": item_id, "name": item['name']}
            )
            
            return {
                "success": True,
                "message": "Item eliminado exitosamente"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")