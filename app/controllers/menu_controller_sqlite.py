from fastapi import HTTPException

class MenuController:
    @staticmethod
    def get_business_menu(business_id: int):
        try:
            # Datos dummy de menú según el negocio
            menus = {
                1: {  # Restaurante El Totonaco
                    "categories": [
                        {
                            "id": 1,
                            "name": "Platillos Principales",
                            "items": [
                                {"id": 1, "name": "Mole Poblano", "price": 180.00, "description": "Tradicional mole con pollo", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"},
                                {"id": 2, "name": "Chiles en Nogada", "price": 220.00, "description": "Platillo típico veracruzano", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"},
                                {"id": 3, "name": "Pescado a la Veracruzana", "price": 250.00, "description": "Pescado fresco con salsa veracruzana", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"}
                            ]
                        },
                        {
                            "id": 2,
                            "name": "Bebidas",
                            "items": [
                                {"id": 4, "name": "Agua de Jamaica", "price": 35.00, "description": "Agua fresca natural", "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300"},
                                {"id": 5, "name": "Cerveza Nacional", "price": 45.00, "description": "Cerveza fría", "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300"}
                            ]
                        }
                    ]
                },
                2: {  # Café Vanilla
                    "categories": [
                        {
                            "id": 1,
                            "name": "Cafés Especiales",
                            "items": [
                                {"id": 1, "name": "Café Vanilla Latte", "price": 65.00, "description": "Café con vainilla de la región", "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=300"},
                                {"id": 2, "name": "Cappuccino", "price": 55.00, "description": "Café espresso con espuma de leche", "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=300"},
                                {"id": 3, "name": "Americano", "price": 40.00, "description": "Café negro tradicional", "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=300"}
                            ]
                        },
                        {
                            "id": 2,
                            "name": "Postres",
                            "items": [
                                {"id": 4, "name": "Cheesecake de Vainilla", "price": 85.00, "description": "Pastel de queso con vainilla", "image": "https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300"},
                                {"id": 5, "name": "Brownie", "price": 70.00, "description": "Brownie de chocolate", "image": "https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300"}
                            ]
                        }
                    ]
                },
                3: {  # Pizzería Don Juan
                    "categories": [
                        {
                            "id": 1,
                            "name": "Pizzas Artesanales",
                            "items": [
                                {"id": 1, "name": "Pizza Margherita", "price": 180.00, "description": "Tomate, mozzarella y albahaca", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"},
                                {"id": 2, "name": "Pizza Pepperoni", "price": 220.00, "description": "Pepperoni y queso mozzarella", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"},
                                {"id": 3, "name": "Pizza Hawaiana", "price": 200.00, "description": "Jamón y piña", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"}
                            ]
                        }
                    ]
                }
            }
            
            # Menú genérico para otros negocios
            default_menu = {
                "categories": [
                    {
                        "id": 1,
                        "name": "Menú Principal",
                        "items": [
                            {"id": 1, "name": "Platillo Especial", "price": 150.00, "description": "Especialidad de la casa", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"},
                            {"id": 2, "name": "Bebida del Día", "price": 45.00, "description": "Bebida refrescante", "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300"}
                        ]
                    }
                ]
            }
            
            menu = menus.get(business_id, default_menu)
            
            return {
                "success": True,
                "data": {
                    "business_id": business_id,
                    "menu": menu
                }
            }
            
        except Exception as e:
            return {
                "success": True,
                "data": {
                    "business_id": business_id,
                    "menu": {
                        "categories": [
                            {
                                "id": 1,
                                "name": "Menú Principal",
                                "items": [
                                    {"id": 1, "name": "Platillo Especial", "price": 150.00, "description": "Especialidad de la casa", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"}
                                ]
                            }
                        ]
                    }
                }
            }