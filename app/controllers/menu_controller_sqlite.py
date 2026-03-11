from fastapi import HTTPException
from app.config.database_sqlite import get_db_connection
from typing import Dict, List

class MenuController:
    @staticmethod
    def get_business_menu(business_id: int) -> Dict:
        """Obtiene el menú completo de un negocio desde la base de datos"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            
            # Verificar que el negocio existe
            cursor.execute("SELECT name FROM businesses WHERE id = ?", (business_id,))
            business = cursor.fetchone()
            
            if not business:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            
            # Obtener items del menú agrupados por categoría
            cursor.execute("""
                SELECT category, item_name, description, price, image_url, available
                FROM business_menus 
                WHERE business_id = ? AND available = 1
                ORDER BY category, item_name
            """, (business_id,))
            
            menu_items = cursor.fetchall()
            
            if not menu_items:
                return {
                    "success": True,
                    "data": {
                        "business_id": business_id,
                        "business_name": business["name"],
                        "menu": {"categories": []}
                    }
                }
            
            # Agrupar items por categoría
            categories = {}
            for item in menu_items:
                category_name = item["category"]
                if category_name not in categories:
                    categories[category_name] = []
                
                categories[category_name].append({
                    "name": item["item_name"],
                    "description": item["description"],
                    "price": item["price"],
                    "image": item["image_url"]
                })
            
            # Convertir a formato de respuesta
            menu_categories = []
            for category_name, items in categories.items():
                menu_categories.append({
                    "name": category_name,
                    "items": items
                })
            
            return {
                "success": True,
                "data": {
                    "business_id": business_id,
                    "business_name": business["name"],
                    "menu": {
                        "categories": menu_categories
                    }
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo menú: {str(e)}")
        finally:
            connection.close()
    
    @staticmethod
    def get_all_menus() -> Dict:
        """Obtiene todos los menús de todos los negocios"""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            
            # Obtener todos los negocios con sus menús
            cursor.execute("""
                SELECT 
                    b.id as business_id,
                    b.name as business_name,
                    b.category as business_category,
                    m.category as menu_category,
                    m.item_name,
                    m.description,
                    m.price,
                    m.image_url
                FROM businesses b
                LEFT JOIN business_menus m ON b.id = m.business_id AND m.available = 1
                ORDER BY b.id, m.category, m.item_name
            """)
            
            results = cursor.fetchall()
            
            # Agrupar por negocio
            businesses = {}
            for row in results:
                business_id = row["business_id"]
                
                if business_id not in businesses:
                    businesses[business_id] = {
                        "business_id": business_id,
                        "business_name": row["business_name"],
                        "business_category": row["business_category"],
                        "categories": {}
                    }
                
                # Si hay items de menú
                if row["menu_category"]:
                    category_name = row["menu_category"]
                    if category_name not in businesses[business_id]["categories"]:
                        businesses[business_id]["categories"][category_name] = []
                    
                    businesses[business_id]["categories"][category_name].append({
                        "name": row["item_name"],
                        "description": row["description"],
                        "price": row["price"],
                        "image": row["image_url"]
                    })
            
            # Convertir a formato final
            business_list = []
            for business_data in businesses.values():
                categories = []
                for category_name, items in business_data["categories"].items():
                    categories.append({
                        "name": category_name,
                        "items": items
                    })
                
                business_list.append({
                    "business_id": business_data["business_id"],
                    "business_name": business_data["business_name"],
                    "business_category": business_data["business_category"],
                    "menu": {"categories": categories}
                })
            
            return {
                "success": True,
                "data": {
                    "businesses": business_list,
                    "total_businesses": len(business_list)
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo menús: {str(e)}")
        finally:
            connection.close()