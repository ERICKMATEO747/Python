from fastapi import APIRouter, Depends
from app.utils.auth_simple import get_current_user

router = APIRouter(prefix="/api/menu", tags=["menu"])

@router.get("/{business_id}")
async def get_business_menu(business_id: int, current_user: dict = Depends(get_current_user)):
    """Obtiene el menú de un negocio específico"""
    
    # Datos dummy de menú según el negocio
    menus = {
        1: {  # Restaurante El Totonaco
            "categories": [
                {
                    "id": 1,
                    "name": "Platillos Principales",
                    "items": [
                        {"id": 1, "name": "Mole Poblano", "price": 180.00, "description": "Tradicional mole con pollo", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"},
                        {"id": 2, "name": "Chiles en Nogada", "price": 220.00, "description": "Platillo típico veracruzano", "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"},
                        {"id": 3, "name": "Pescado a la Veracruzana", "price": 250.00, "description": "Pescado fresco con salsa veracruzana", "image": "https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=300"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Bebidas",
                    "items": [
                        {"id": 4, "name": "Agua de Jamaica", "price": 35.00, "description": "Agua fresca natural", "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300"},
                        {"id": 5, "name": "Cerveza Nacional", "price": 45.00, "description": "Cerveza fría", "image": "https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300"}
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
                        {"id": 2, "name": "Cappuccino", "price": 55.00, "description": "Café espresso con espuma de leche", "image": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=300"},
                        {"id": 3, "name": "Americano", "price": 40.00, "description": "Café negro tradicional", "image": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=300"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Postres",
                    "items": [
                        {"id": 4, "name": "Cheesecake de Vainilla", "price": 85.00, "description": "Pastel de queso con vainilla", "image": "https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300"},
                        {"id": 5, "name": "Brownie", "price": 70.00, "description": "Brownie de chocolate", "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=300"}
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
                        {"id": 2, "name": "Pizza Pepperoni", "price": 220.00, "description": "Pepperoni y queso mozzarella", "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=300"},
                        {"id": 3, "name": "Pizza Hawaiana", "price": 200.00, "description": "Jamón y piña", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Bebidas",
                    "items": [
                        {"id": 4, "name": "Refresco", "price": 35.00, "description": "Bebida gaseosa fría", "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300"}
                    ]
                }
            ]
        },
        4: {  # Tacos El Buen Sabor
            "categories": [
                {
                    "id": 1,
                    "name": "Tacos",
                    "items": [
                        {"id": 1, "name": "Tacos de Pastor", "price": 15.00, "description": "Tacos con carne al pastor", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"},
                        {"id": 2, "name": "Tacos de Carnitas", "price": 18.00, "description": "Tacos de carnitas tradicionales", "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=300"},
                        {"id": 3, "name": "Tacos de Pollo", "price": 16.00, "description": "Tacos de pollo asado", "image": "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f?w=300"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Quesadillas",
                    "items": [
                        {"id": 4, "name": "Quesadilla de Queso", "price": 45.00, "description": "Quesadilla tradicional de queso", "image": "https://images.unsplash.com/photo-1618040996337-56904b7850b9?w=300"},
                        {"id": 5, "name": "Quesadilla de Pastor", "price": 55.00, "description": "Quesadilla con carne al pastor", "image": "https://images.unsplash.com/photo-1615870216519-2f9fa2fa4b5b?w=300"}
                    ]
                }
            ]
        },
        5: {  # Heladería Tropical
            "categories": [
                {
                    "id": 1,
                    "name": "Helados Artesanales",
                    "items": [
                        {"id": 1, "name": "Helado de Mango", "price": 35.00, "description": "Helado natural de mango", "image": "https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300"},
                        {"id": 2, "name": "Helado de Coco", "price": 40.00, "description": "Helado cremoso de coco", "image": "https://images.unsplash.com/photo-1567206563064-6f60f40a2b57?w=300"},
                        {"id": 3, "name": "Helado de Fresa", "price": 38.00, "description": "Helado natural de fresa", "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=300"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Paletas",
                    "items": [
                        {"id": 4, "name": "Paleta de Limón", "price": 25.00, "description": "Paleta refrescante de limón", "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300"},
                        {"id": 5, "name": "Paleta de Tamarindo", "price": 28.00, "description": "Paleta de tamarindo con chile", "image": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=300"}
                    ]
                }
            ]
        },
        6: {  # Panadería La Espiga
            "categories": [
                {
                    "id": 1,
                    "name": "Pan Dulce",
                    "items": [
                        {"id": 1, "name": "Conchas", "price": 12.00, "description": "Pan dulce tradicional", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"},
                        {"id": 2, "name": "Cuernitos", "price": 15.00, "description": "Pan en forma de cuerno", "image": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"},
                        {"id": 3, "name": "Orejas", "price": 18.00, "description": "Pan hojaldrado dulce", "image": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=300"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Pasteles",
                    "items": [
                        {"id": 4, "name": "Pastel de Tres Leches", "price": 85.00, "description": "Pastel tradicional de tres leches", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300"},
                        {"id": 5, "name": "Pastel de Chocolate", "price": 90.00, "description": "Pastel de chocolate húmedo", "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=300"}
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
                    {"id": 1, "name": "Platillo Especial", "price": 150.00, "description": "Especialidad de la casa", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"}
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