# -*- coding: utf-8 -*-
"""
Script para probar los menus de todos los negocios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.controllers.menu_controller_sqlite import MenuController

def test_all_menus():
    print("=== PROBANDO MENUS DE TODOS LOS NEGOCIOS ===")
    
    try:
        # Probar menú de cada negocio individualmente
        for business_id in range(1, 7):
            print(f"\n--- NEGOCIO {business_id} ---")
            result = MenuController.get_business_menu(business_id)
            
            if result["success"]:
                data = result["data"]
                print(f"Negocio: {data['business_name']}")
                
                categories = data["menu"]["categories"]
                print(f"Categorias: {len(categories)}")
                
                total_items = 0
                for category in categories:
                    items_count = len(category["items"])
                    total_items += items_count
                    print(f"  - {category['name']}: {items_count} items")
                    
                    # Mostrar algunos items
                    for item in category["items"][:2]:  # Solo primeros 2
                        print(f"    * {item['name']} - ${item['price']}")
                
                print(f"Total items: {total_items}")
            else:
                print(f"Error obteniendo menu: {result}")
    
    except Exception as e:
        print(f"Error en prueba: {str(e)}")
    
    print("\n=== PROBANDO ENDPOINT DE TODOS LOS MENUS ===")
    
    try:
        result = MenuController.get_all_menus()
        
        if result["success"]:
            data = result["data"]
            print(f"Total negocios con menu: {data['total_businesses']}")
            
            total_items_all = 0
            for business in data["businesses"]:
                items_count = sum(len(cat["items"]) for cat in business["menu"]["categories"])
                total_items_all += items_count
                print(f"- {business['business_name']} ({business['business_category']}): {items_count} items")
            
            print(f"\nGran total de items: {total_items_all}")
        else:
            print(f"Error obteniendo todos los menus: {result}")
            
    except Exception as e:
        print(f"Error en prueba de todos los menus: {str(e)}")

if __name__ == "__main__":
    test_all_menus()