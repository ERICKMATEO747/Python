#!/usr/bin/env python3
"""
Script para llenar las tablas con datos dummy (corregido)
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Cargar variables de entorno
load_dotenv()

def populate_data_fixed():
    """Llena las tablas con datos dummy usando solo IDs existentes"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("Agregando más businesses...")
            cursor.execute("SELECT COUNT(*) as count FROM businesses")
            result = cursor.fetchone()
            business_count = result['count'] if result else 0
            
            if business_count < 8:
                cursor.execute("""
                    INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating, visits_for_prize) VALUES
                    ('Pizzería Don Luigi', 'Restaurante', 'Av. Juárez 234', 1, '7841111111', 'info@donluigi.com', 'Pizzas artesanales al horno de leña', 4.6, 8),
                    ('Librería Cervantes', 'Librería', 'Calle Morelos 45', 2, '7822222222', 'ventas@cervantes.com', 'Libros y material educativo', 4.1, 5),
                    ('Taller Mecánico El Rayo', 'Automotriz', 'Carretera Nacional Km 5', 3, '7823333333', 'contacto@elrayo.com', 'Servicio automotriz especializado', 4.3, 4),
                    ('Panadería La Espiga', 'Panadería', 'Plaza Principal 12', 4, '7834444444', 'info@laespiga.com', 'Pan fresco y repostería', 4.7, 10),
                    ('Ferretería Construmax', 'Ferretería', 'Av. Construcción 89', 1, '7845555555', 'ventas@construmax.com', 'Materiales de construcción', 4.2, 6),
                    ('Estética Bella Vista', 'Belleza', 'Calle Belleza 23', 2, '7826666666', 'citas@bellavista.com', 'Servicios de belleza y estética', 4.5, 7)
                """)
                print("✅ Más businesses agregados")
            
            print("Agregando menús para businesses existentes...")
            cursor.execute("SELECT COUNT(*) as count FROM business_menu")
            result = cursor.fetchone()
            menu_count = result['count'] if result else 0
            
            if menu_count == 0:
                cursor.execute("""
                    INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria) VALUES
                    -- Restaurante El Totonaco (id: 1)
                    (1, 'Mole de Olla', 'Mole tradicional veracruzano con pollo', 85.00, 'Platillos'),
                    (1, 'Pescado a la Veracruzana', 'Pescado fresco con salsa veracruzana', 120.00, 'Platillos'),
                    (1, 'Agua de Chía con Limón', 'Bebida refrescante natural', 30.00, 'Bebidas'),
                    (1, 'Café de Olla', 'Café tradicional con canela y piloncillo', 45.00, 'Cafés'),
                    -- Café Vanilla (id: 2)
                    (2, 'Café de Olla', 'Café tradicional con canela y piloncillo', 45.00, 'Cafés'),
                    (2, 'Flan de Vainilla', 'Postre con vainilla de Papantla', 55.00, 'Postres'),
                    (2, 'Torta de Jamón', 'Torta veracruzana con ingredientes frescos', 65.00, 'Alimentos'),
                    (2, 'Cappuccino', 'Café espresso con leche espumada', 50.00, 'Cafés'),
                    -- Pizzería Don Luigi (id: 3)
                    (3, 'Pizza Margherita', 'Pizza clásica con tomate, mozzarella y albahaca', 180.00, 'Pizzas'),
                    (3, 'Pizza Pepperoni', 'Pizza con pepperoni y queso mozzarella', 220.00, 'Pizzas'),
                    (3, 'Lasaña Boloñesa', 'Lasaña tradicional italiana', 250.00, 'Pastas'),
                    (3, 'Tiramisu', 'Postre italiano tradicional', 85.00, 'Postres'),
                    -- Librería Cervantes (id: 4)
                    (4, 'Novela Bestseller', 'Últimos lanzamientos literarios', 350.00, 'Libros'),
                    (4, 'Cuaderno Universitario', 'Cuaderno de 200 hojas', 45.00, 'Papelería'),
                    (4, 'Pluma Gel', 'Pluma de tinta gel azul', 25.00, 'Papelería'),
                    (4, 'Diccionario Español', 'Diccionario completo del español', 280.00, 'Libros'),
                    -- Taller El Rayo (id: 5)
                    (5, 'Cambio de Aceite', 'Servicio completo de cambio de aceite', 450.00, 'Servicios'),
                    (5, 'Afinación Mayor', 'Afinación completa del motor', 1200.00, 'Servicios'),
                    (5, 'Balanceo y Rotación', 'Balanceo y rotación de llantas', 280.00, 'Servicios'),
                    -- Panadería La Espiga (id: 6)
                    (6, 'Pan Dulce Surtido', 'Variedad de pan dulce mexicano', 8.00, 'Panadería'),
                    (6, 'Pastel de Chocolate', 'Pastel de chocolate para 8 personas', 320.00, 'Pasteles'),
                    (6, 'Concha de Vainilla', 'Concha tradicional mexicana', 12.00, 'Panadería'),
                    -- Ferretería Construmax (id: 7)
                    (7, 'Cemento Portland', 'Bulto de cemento de 50kg', 180.00, 'Construcción'),
                    (7, 'Martillo Profesional', 'Martillo de acero forjado', 250.00, 'Herramientas'),
                    (7, 'Pintura Vinílica', 'Pintura para interiores 4L', 320.00, 'Pintura'),
                    -- Estética Bella Vista (id: 8)
                    (8, 'Corte de Cabello', 'Corte y peinado profesional', 150.00, 'Servicios'),
                    (8, 'Manicure Completo', 'Manicure con esmaltado', 120.00, 'Servicios'),
                    (8, 'Facial Hidratante', 'Tratamiento facial completo', 280.00, 'Tratamientos')
                """)
                print("✅ Menús agregados")
            
            print("Creando usuarios de prueba...")
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            users_count = result['count'] if result else 0
            
            if users_count == 0:
                # Contraseña hasheada para "password123"
                hashed_password = "$2b$12$LQv3c1yqBFVyE6sGT1uCUOrvgddHtfkUNjZA9W8WaW5vUOQCORAK."
                
                cursor.execute("""
                    INSERT INTO users (nombre, email, password, user_type_id) VALUES
                    ('Juan Pérez', 'juan@test.com', %s, 1),
                    ('María García', 'maria@test.com', %s, 1),
                    ('Carlos López', 'carlos@test.com', %s, 1),
                    ('Ana Martínez', 'ana@test.com', %s, 1),
                    ('Luis Rodríguez', 'luis@test.com', %s, 1)
                """, (hashed_password, hashed_password, hashed_password, hashed_password, hashed_password))
                print("✅ Usuarios de prueba creados")
            
            print("Agregando visitas de ejemplo...")
            cursor.execute("SELECT COUNT(*) as count FROM user_visits")
            result = cursor.fetchone()
            visits_count = result['count'] if result else 0
            
            if visits_count == 0:
                # Crear visitas para el mes actual usando solo businesses existentes
                current_month = datetime.now().strftime('%Y-%m')
                base_date = datetime.now() - timedelta(days=15)
                
                visits_data = []
                for i in range(20):
                    visit_date = base_date + timedelta(days=i % 15, hours=i % 12)
                    user_id = (i % 5) + 1  # Usuarios 1-5
                    business_id = (i % 2) + 1  # Solo businesses 1-2 (existentes)
                    visits_data.append((user_id, business_id, visit_date, current_month))
                
                cursor.executemany("""
                    INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                    VALUES (%s, %s, %s, %s)
                """, visits_data)
                print("✅ Visitas de ejemplo agregadas")
            
            print("Creando rondas de ejemplo...")
            cursor.execute("SELECT COUNT(*) as count FROM user_rounds")
            result = cursor.fetchone()
            rounds_count = result['count'] if result else 0
            
            if rounds_count == 0:
                rounds_data = []
                for user_id in range(1, 6):  # Usuarios 1-5
                    for business_id in range(1, 3):  # Solo businesses 1-2 (existentes)
                        progress = (user_id + business_id) % 6  # Progreso variable
                        rounds_data.append((user_id, business_id, 1, progress, False, False))
                
                cursor.executemany("""
                    INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, is_completed, is_reward_claimed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, rounds_data)
                print("✅ Rondas de ejemplo creadas")
            
            connection.commit()
            print("🎉 ¡Datos dummy agregados exitosamente!")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Llenando tablas con datos dummy (versión corregida)...")
    if populate_data_fixed():
        print("✅ Proceso completado exitosamente")
        print("\n📊 Datos agregados:")
        print("- 8 businesses con menús completos")
        print("- 5 usuarios de prueba (password: password123)")
        print("- 20 visitas distribuidas en el mes")
        print("- 10 rondas de lealtad en progreso")
        print("\n🔑 Usuarios de prueba:")
        print("- juan@test.com")
        print("- maria@test.com") 
        print("- carlos@test.com")
        print("- ana@test.com")
        print("- luis@test.com")
    else:
        print("❌ Error llenando datos")