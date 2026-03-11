#!/usr/bin/env python3
import sqlite3
from datetime import datetime

def create_menus_for_businesses():
    conn = sqlite3.connect('auth_api.db')
    cursor = conn.cursor()
    
    # Crear tabla de menús si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_menus (
            id INTEGER PRIMARY KEY,
            business_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            item_name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses (id)
        )
    ''')
    
    # Limpiar menús existentes
    cursor.execute("DELETE FROM business_menus")
    
    # Menús por negocio
    menus = {
        # 1. Restaurante El Totonaco
        1: [
            ("Platillos Principales", "Mole Poblano", "Pollo en mole poblano con arroz y tortillas", 180.00, "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"),
            ("Platillos Principales", "Pescado a la Veracruzana", "Huachinango fresco con salsa veracruzana", 220.00, "https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=300"),
            ("Platillos Principales", "Chiles en Nogada", "Chiles poblanos rellenos con nogada", 195.00, "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f?w=300"),
            ("Antojitos", "Sopes Veracruzanos", "Sopes con frijoles, queso y salsa verde", 85.00, "https://images.unsplash.com/photo-1615870216519-2f9fa2707595?w=300"),
            ("Antojitos", "Empanadas de Camarón", "Empanadas rellenas de camarón (3 piezas)", 120.00, "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300"),
            ("Bebidas", "Agua de Jamaica", "Agua fresca natural de jamaica", 35.00, "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300"),
            ("Bebidas", "Horchata de Coco", "Horchata tradicional con coco", 40.00, "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300")
        ],
        
        # 2. Café Vanilla
        2: [
            ("Cafés Especiales", "Café de Olla", "Café tradicional con canela y piloncillo", 45.00, "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300"),
            ("Cafés Especiales", "Cappuccino Vainilla", "Cappuccino con esencia de vainilla local", 65.00, "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=300"),
            ("Cafés Especiales", "Latte Caramelo", "Latte con jarabe de caramelo artesanal", 70.00, "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=300"),
            ("Postres", "Flan de Vainilla", "Flan casero con vainilla de Papantla", 55.00, "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=300"),
            ("Postres", "Cheesecake de Café", "Cheesecake con café veracruzano", 75.00, "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=300"),
            ("Desayunos", "Molletes Especiales", "Molletes con frijoles, queso y pico de gallo", 85.00, "https://images.unsplash.com/photo-1571091655789-405eb7a3a3a8?w=300"),
            ("Bebidas Frías", "Frappé de Vainilla", "Frappé helado con vainilla natural", 80.00, "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=300")
        ],
        
        # 3. Pizzería Don Juan
        3: [
            ("Pizzas Tradicionales", "Pizza Margherita", "Salsa de tomate, mozzarella y albahaca fresca", 165.00, "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"),
            ("Pizzas Tradicionales", "Pizza Pepperoni", "Salsa de tomate, mozzarella y pepperoni", 185.00, "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"),
            ("Pizzas Especiales", "Pizza Hawaiana", "Jamón, piña, mozzarella y salsa de tomate", 195.00, "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=300"),
            ("Pizzas Especiales", "Pizza Mexicana", "Chorizo, jalapeños, cebolla y queso", 210.00, "https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=300"),
            ("Entradas", "Pan de Ajo", "Pan artesanal con mantequilla de ajo", 65.00, "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"),
            ("Entradas", "Alitas BBQ", "Alitas de pollo en salsa barbacoa (8 piezas)", 125.00, "https://images.unsplash.com/photo-1527477396000-e27163b481c2?w=300"),
            ("Bebidas", "Refresco 600ml", "Coca-Cola, Pepsi o Sprite", 30.00, "https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=300")
        ],
        
        # 4. Tacos El Buen Sabor
        4: [
            ("Tacos", "Tacos de Pastor", "Tacos al pastor con piña (orden de 4)", 80.00, "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300"),
            ("Tacos", "Tacos de Carnitas", "Tacos de carnitas con cebolla y cilantro (orden de 4)", 85.00, "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=300"),
            ("Tacos", "Tacos de Pollo", "Tacos de pollo asado con guacamole (orden de 4)", 75.00, "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f?w=300"),
            ("Quesadillas", "Quesadilla de Queso", "Quesadilla grande con queso Oaxaca", 65.00, "https://images.unsplash.com/photo-1618040996337-56904b7850b9?w=300"),
            ("Quesadillas", "Quesadilla de Pastor", "Quesadilla con carne al pastor y queso", 95.00, "https://images.unsplash.com/photo-1615870216519-2f9fa2707595?w=300"),
            ("Extras", "Guacamole", "Guacamole fresco con totopos", 45.00, "https://images.unsplash.com/photo-1553621042-f6e147245754?w=300"),
            ("Bebidas", "Agua de Horchata", "Agua fresca de horchata", 25.00, "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300"),
            ("Bebidas", "Agua de Tamarindo", "Agua fresca de tamarindo", 25.00, "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300")
        ],
        
        # 5. Heladería Tropical
        5: [
            ("Helados Artesanales", "Helado de Mango", "Helado cremoso de mango manila", 35.00, "https://images.unsplash.com/photo-1488900128323-21503983a07e?w=300"),
            ("Helados Artesanales", "Helado de Coco", "Helado de coco con trozos naturales", 40.00, "https://images.unsplash.com/photo-1567206563064-6f60f40a2b57?w=300"),
            ("Helados Artesanales", "Helado de Maracuyá", "Helado tropical de maracuyá", 45.00, "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=300"),
            ("Paletas", "Paleta de Limón", "Paleta natural de limón con chile", 20.00, "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300"),
            ("Paletas", "Paleta de Sandía", "Paleta refrescante de sandía", 18.00, "https://images.unsplash.com/photo-1571091655789-405eb7a3a3a8?w=300"),
            ("Especialidades", "Banana Split Tropical", "Plátano con 3 bolas de helado y frutas", 120.00, "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=300"),
            ("Bebidas", "Malteada de Fresa", "Malteada cremosa de fresa natural", 65.00, "https://images.unsplash.com/photo-1541544181051-e46607bc22a4?w=300"),
            ("Bebidas", "Smoothie de Piña", "Smoothie refrescante de piña colada", 70.00, "https://images.unsplash.com/photo-1546173159-315724a31696?w=300")
        ],
        
        # 6. Panadería La Espiga
        6: [
            ("Pan Dulce", "Conchas", "Conchas tradicionales de vainilla y chocolate", 12.00, "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"),
            ("Pan Dulce", "Orejas", "Orejas de hojaldre con azúcar", 15.00, "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=300"),
            ("Pan Dulce", "Cuernitos", "Cuernitos rellenos de crema", 18.00, "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=300"),
            ("Pan Salado", "Bolillos", "Bolillos frescos del día (3 piezas)", 10.00, "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=300"),
            ("Pan Salado", "Pan Integral", "Pan integral con semillas", 35.00, "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=300"),
            ("Pasteles", "Pastel de Tres Leches", "Rebanada de pastel tres leches", 45.00, "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=300"),
            ("Pasteles", "Pastel de Chocolate", "Rebanada de pastel de chocolate", 50.00, "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300"),
            ("Bebidas", "Café Americano", "Café americano recién hecho", 25.00, "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300"),
            ("Bebidas", "Chocolate Caliente", "Chocolate caliente tradicional", 35.00, "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=300")
        ]
    }
    
    # Insertar todos los menús
    for business_id, items in menus.items():
        for category, name, description, price, image_url in items:
            cursor.execute('''
                INSERT INTO business_menus (business_id, category, item_name, description, price, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (business_id, category, name, description, price, image_url))
    
    conn.commit()
    conn.close()
    
    print("=== MENUS AGREGADOS EXITOSAMENTE ===")
    print("[OK] Restaurante El Totonaco: 7 platillos (Mole, Pescado, Chiles, Sopes, etc.)")
    print("[OK] Cafe Vanilla: 7 items (Cafes especiales, Postres, Desayunos)")
    print("[OK] Pizzeria Don Juan: 7 items (Pizzas tradicionales, Especiales, Entradas)")
    print("[OK] Tacos El Buen Sabor: 8 items (Tacos, Quesadillas, Extras, Bebidas)")
    print("[OK] Heladeria Tropical: 8 items (Helados, Paletas, Especialidades, Bebidas)")
    print("[OK] Panaderia La Espiga: 9 items (Pan dulce, Pan salado, Pasteles, Bebidas)")
    print(f"\nTotal: {sum(len(items) for items in menus.values())} items de menu agregados")

if __name__ == "__main__":
    create_menus_for_businesses()