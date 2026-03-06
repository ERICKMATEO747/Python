#!/usr/bin/env python3
"""
Script para llenar las tablas paso a paso
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Cargar variables de entorno
load_dotenv()

def populate_step_by_step():
    """Llena las tablas paso a paso con commits intermedios"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        # PASO 1: Agregar businesses
        print("PASO 1: Agregando businesses...")
        with connection.cursor() as cursor:
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
                connection.commit()
                print("✅ Businesses agregados y confirmados")
        
        # PASO 2: Verificar businesses existentes
        print("PASO 2: Verificando businesses...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM businesses ORDER BY id")
            businesses = cursor.fetchall()
            print(f"Businesses disponibles: {len(businesses)}")
            for b in businesses:
                print(f"  ID {b['id']}: {b['name']}")
        
        # PASO 3: Agregar menús solo para businesses existentes
        print("PASO 3: Agregando menús...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM business_menu")
            result = cursor.fetchone()
            menu_count = result['count'] if result else 0
            
            if menu_count == 0:
                # Obtener IDs reales de businesses
                cursor.execute("SELECT id FROM businesses ORDER BY id")
                business_ids = [row['id'] for row in cursor.fetchall()]
                
                menu_items = []
                for bid in business_ids[:6]:  # Solo primeros 6 businesses
                    if bid == 1:  # Restaurante El Totonaco
                        menu_items.extend([
                            (bid, 'Mole de Olla', 'Mole tradicional veracruzano con pollo', 85.00, 'Platillos'),
                            (bid, 'Pescado a la Veracruzana', 'Pescado fresco con salsa veracruzana', 120.00, 'Platillos'),
                            (bid, 'Agua de Chía con Limón', 'Bebida refrescante natural', 30.00, 'Bebidas')
                        ])
                    elif bid == 2:  # Café Vanilla
                        menu_items.extend([
                            (bid, 'Café de Olla', 'Café tradicional con canela y piloncillo', 45.00, 'Cafés'),
                            (bid, 'Flan de Vainilla', 'Postre con vainilla de Papantla', 55.00, 'Postres'),
                            (bid, 'Torta de Jamón', 'Torta veracruzana con ingredientes frescos', 65.00, 'Alimentos')
                        ])
                    else:  # Otros businesses
                        menu_items.extend([
                            (bid, f'Producto Especial {bid}', f'Producto destacado del negocio {bid}', 100.00, 'Especiales'),
                            (bid, f'Servicio Premium {bid}', f'Servicio premium del negocio {bid}', 200.00, 'Servicios')
                        ])
                
                cursor.executemany("""
                    INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                """, menu_items)
                connection.commit()
                print("✅ Menús agregados y confirmados")
        
        # PASO 4: Crear usuarios
        print("PASO 4: Creando usuarios...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            users_count = result['count'] if result else 0
            
            if users_count == 0:
                hashed_password = "$2b$12$LQv3c1yqBFVyE6sGT1uCUOrvgddHtfkUNjZA9W8WaW5vUOQCORAK."
                
                cursor.execute("""
                    INSERT INTO users (nombre, email, password, user_type_id) VALUES
                    ('Juan Pérez', 'juan@test.com', %s, 1),
                    ('María García', 'maria@test.com', %s, 1),
                    ('Carlos López', 'carlos@test.com', %s, 1),
                    ('Ana Martínez', 'ana@test.com', %s, 1),
                    ('Luis Rodríguez', 'luis@test.com', %s, 1)
                """, (hashed_password, hashed_password, hashed_password, hashed_password, hashed_password))
                connection.commit()
                print("✅ Usuarios creados y confirmados")
        
        # PASO 5: Agregar visitas
        print("PASO 5: Agregando visitas...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM user_visits")
            result = cursor.fetchone()
            visits_count = result['count'] if result else 0
            
            if visits_count == 0:
                current_month = datetime.now().strftime('%Y-%m')
                base_date = datetime.now() - timedelta(days=15)
                
                # Obtener IDs reales
                cursor.execute("SELECT id FROM businesses ORDER BY id LIMIT 4")
                business_ids = [row['id'] for row in cursor.fetchall()]
                
                visits_data = []
                for i in range(20):
                    visit_date = base_date + timedelta(days=i % 15, hours=i % 12)
                    user_id = (i % 5) + 1
                    business_id = business_ids[i % len(business_ids)]
                    visits_data.append((user_id, business_id, visit_date, current_month))
                
                cursor.executemany("""
                    INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                    VALUES (%s, %s, %s, %s)
                """, visits_data)
                connection.commit()
                print("✅ Visitas agregadas y confirmadas")
        
        # PASO 6: Crear rondas
        print("PASO 6: Creando rondas...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM user_rounds")
            result = cursor.fetchone()
            rounds_count = result['count'] if result else 0
            
            if rounds_count == 0:
                # Obtener IDs reales
                cursor.execute("SELECT id FROM businesses ORDER BY id LIMIT 3")
                business_ids = [row['id'] for row in cursor.fetchall()]
                
                rounds_data = []
                for user_id in range(1, 6):
                    for business_id in business_ids:
                        progress = (user_id + business_id) % 6
                        rounds_data.append((user_id, business_id, 1, progress, False, False))
                
                cursor.executemany("""
                    INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, is_completed, is_reward_claimed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, rounds_data)
                connection.commit()
                print("✅ Rondas creadas y confirmadas")
        
        connection.close()
        print("🎉 ¡Todos los datos agregados exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Llenando tablas paso a paso...")
    if populate_step_by_step():
        print("✅ Proceso completado exitosamente")
        print("\n🔑 Usuarios de prueba (password: password123):")
        print("- juan@test.com")
        print("- maria@test.com") 
        print("- carlos@test.com")
        print("- ana@test.com")
        print("- luis@test.com")
    else:
        print("❌ Error llenando datos")