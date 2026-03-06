#!/usr/bin/env python3
"""
Script para llenar las tablas con datos dummy
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Cargar variables de entorno
load_dotenv()

def populate_tables():
    """Llena las tablas con datos dummy"""
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
            
            if business_count < 10:
                cursor.execute("""
                    INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating, visits_for_prize) VALUES
                    ('Pizzería Don Luigi', 'Restaurante', 'Av. Juárez 234', 1, '7841111111', 'info@donluigi.com', 'Pizzas artesanales al horno de leña', 4.6, 8),
                    ('Librería Cervantes', 'Librería', 'Calle Morelos 45', 2, '7822222222', 'ventas@cervantes.com', 'Libros y material educativo', 4.1, 5),
                    ('Taller Mecánico El Rayo', 'Automotriz', 'Carretera Nacional Km 5', 3, '7823333333', 'contacto@elrayo.com', 'Servicio automotriz especializado', 4.3, 4),
                    ('Panadería La Espiga', 'Panadería', 'Plaza Principal 12', 4, '7834444444', 'info@laespiga.com', 'Pan fresco y repostería', 4.7, 10),
                    ('Ferretería Construmax', 'Ferretería', 'Av. Construcción 89', 1, '7845555555', 'ventas@construmax.com', 'Materiales de construcción', 4.2, 6),
                    ('Estética Bella Vista', 'Belleza', 'Calle Belleza 23', 2, '7826666666', 'citas@bellavista.com', 'Servicios de belleza y estética', 4.5, 7),
                    ('Farmacia San Rafael', 'Farmacia', 'Av. Salud 67', 3, '7837777777', 'info@sanrafael.com', 'Medicamentos y productos de salud', 4.4, 5),
                    ('Restaurante Mariscos El Puerto', 'Restaurante', 'Malecón 156', 4, '7848888888', 'reservas@elpuerto.com', 'Mariscos frescos del Golfo', 4.8, 6)
                """)
                print("✅ Más businesses agregados")
            
            print("Agregando menús para todos los businesses...")
            cursor.execute("SELECT COUNT(*) as count FROM business_menu")
            result = cursor.fetchone()
            menu_count = result['count'] if result else 0
            
            if menu_count < 50:
                cursor.execute("""
                    INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria) VALUES
                    -- Restaurante El Totonaco (id: 1)
                    (1, 'Pizza Margherita', 'Pizza clásica con tomate, mozzarella y albahaca', 180.00, 'Pizzas'),
                    (1, 'Pizza Pepperoni', 'Pizza con pepperoni y queso mozzarella', 220.00, 'Pizzas'),
                    (1, 'Lasaña Boloñesa', 'Lasaña tradicional italiana', 250.00, 'Pastas'),
                    (1, 'Tiramisu', 'Postre italiano tradicional', 85.00, 'Postres'),
                    -- Café Vanilla (id: 2)
                    (2, 'Novela Bestseller', 'Últimos lanzamientos literarios', 350.00, 'Libros'),
                    (2, 'Cuaderno Universitario', 'Cuaderno de 200 hojas', 45.00, 'Papelería'),
                    (2, 'Pluma Gel', 'Pluma de tinta gel azul', 25.00, 'Papelería'),
                    -- Pizzería Don Luigi (id: 3)
                    (3, 'Cambio de Aceite', 'Servicio completo de cambio de aceite', 450.00, 'Servicios'),
                    (3, 'Afinación Mayor', 'Afinación completa del motor', 1200.00, 'Servicios'),
                    (3, 'Balanceo y Rotación', 'Balanceo y rotación de llantas', 280.00, 'Servicios'),
                    -- Librería Cervantes (id: 4)
                    (4, 'Pan Dulce Surtido', 'Variedad de pan dulce mexicano', 8.00, 'Panadería'),
                    (4, 'Pastel de Chocolate', 'Pastel de chocolate para 8 personas', 320.00, 'Pasteles'),
                    (4, 'Concha de Vainilla', 'Concha tradicional mexicana', 12.00, 'Panadería'),
                    (4, 'Café de Olla', 'Café tradicional con canela', 35.00, 'Bebidas'),
                    -- Taller El Rayo (id: 5)
                    (5, 'Cemento Portland', 'Bulto de cemento de 50kg', 180.00, 'Construcción'),
                    (5, 'Martillo Profesional', 'Martillo de acero forjado', 250.00, 'Herramientas'),
                    (5, 'Pintura Vinílica', 'Pintura para interiores 4L', 320.00, 'Pintura')
                """)
                print("✅ Menús completos agregados")
            
            print("Creando usuarios de prueba...")
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE email LIKE '%@test.com'")
            result = cursor.fetchone()
            test_users = result['count'] if result else 0
            
            if test_users == 0:
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
            
            if visits_count < 20:
                # Crear visitas para el mes actual
                current_month = datetime.now().strftime('%Y-%m')
                base_date = datetime.now() - timedelta(days=15)
                
                visits_data = []
                for i in range(25):
                    visit_date = base_date + timedelta(days=i % 15, hours=i % 12)
                    user_id = (i % 5) + 1  # Usuarios 1-5
                    business_id = (i % 5) + 1  # Businesses 1-5
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
            
            if rounds_count < 10:
                rounds_data = []
                for user_id in range(1, 6):  # Usuarios 1-5
                    for business_id in range(1, 6):  # Businesses 1-5
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
    print("🚀 Llenando tablas con datos dummy...")
    if populate_tables():
        print("✅ Proceso completado exitosamente")
        print("\n📊 Datos agregados:")
        print("- 10 businesses con menús completos")
        print("- 5 usuarios de prueba (password: password123)")
        print("- 25 visitas distribuidas en el mes")
        print("- 15 rondas de lealtad en progreso")
        print("\n🔑 Usuarios de prueba:")
        print("- juan@test.com")
        print("- maria@test.com") 
        print("- carlos@test.com")
        print("- ana@test.com")
        print("- luis@test.com")
    else:
        print("❌ Error llenando datos")