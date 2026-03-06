from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import Dict, List, Optional

class MenuService:
    """Servicio para gestión de menú"""
    
    @staticmethod
    def get_business_menu(business_id: int) -> Dict:
        """Obtiene el menú completo de un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Obtener información del negocio
                cursor.execute("""
                    SELECT name FROM businesses WHERE id = %s AND active = 1
                """, (business_id,))
                
                business = cursor.fetchone()
                if not business:
                    return {"business_id": business_id, "business_name": "Negocio no encontrado", "menu_items": []}
                
                # Obtener items del menú
                cursor.execute("""
                    SELECT id, producto as name, descripcion as description, precio as price, 
                           categoria as category, disponible as available, created_at
                    FROM business_menu
                    WHERE business_id = %s
                    ORDER BY categoria, producto
                """, (business_id,))
                
                menu_items = cursor.fetchall()
                
                return {
                    "business_id": business_id,
                    "business_name": business['name'],
                    "menu_items": menu_items
                }
        except Exception as e:
            log_error("Error obteniendo menú", error=e)
            return {"business_id": business_id, "business_name": "Error", "menu_items": []}
        finally:
            connection.close()
    
    @staticmethod
    def create_menu_item(business_id: int, item_data: Dict) -> Optional[int]:
        """Crea un nuevo item de menú"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria, disponible)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    business_id,
                    item_data['name'],
                    item_data.get('description'),
                    item_data['price'],
                    item_data['category'],
                    item_data.get('available', True)
                ))
                
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            log_error("Error creando item de menú", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def get_menu_item(item_id: int) -> Optional[Dict]:
        """Obtiene un item específico del menú"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM business_menu WHERE id = %s
                """, (item_id,))
                
                return cursor.fetchone()
        except Exception as e:
            log_error("Error obteniendo item de menú", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def update_menu_item(item_id: int, update_data: Dict) -> bool:
        """Actualiza un item de menú"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                fields = []
                values = []
                
                # Mapear campos inglés -> español
                field_mapping = {
                    'name': 'producto',
                    'description': 'descripcion', 
                    'price': 'precio',
                    'category': 'categoria',
                    'available': 'disponible'
                }
                
                for field, value in update_data.items():
                    if value is not None and field in field_mapping:
                        fields.append(f"{field_mapping[field]} = %s")
                        values.append(value)
                
                if fields:
                    values.append(item_id)
                    query = f"UPDATE business_menu SET {', '.join(fields)} WHERE id = %s"
                    cursor.execute(query, values)
                    connection.commit()
                    return cursor.rowcount > 0
                
                return False
        except Exception as e:
            log_error("Error actualizando item de menú", error=e)
            return False
        finally:
            connection.close()
    
    @staticmethod
    def delete_menu_item(item_id: int) -> bool:
        """Elimina un item de menú"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM business_menu WHERE id = %s", (item_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            log_error("Error eliminando item de menú", error=e)
            return False
        finally:
            connection.close()