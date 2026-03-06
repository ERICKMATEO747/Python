#!/usr/bin/env python3
"""
Script completo para llenar todas las tablas
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import bcrypt

# Cargar variables de entorno
load_dotenv()

def populate_all_data():
    """Llena todas las tablas con datos completos"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("=== VERIFICANDO DATOS EXISTENTES ===")
            
            # Verificar businesses
            cursor.execute("SELECT COUNT(*) as count FROM businesses")
            business_count = cursor.fetchone()['count']
            print(f"Businesses existentes: {business_count}")
            
            # Verificar municipalities
            cursor.execute("SELECT COUNT(*) as count FROM municipalities")
            municipality_count = cursor.fetchone()['count']
            print(f"Municipalities existentes: {municipality_count}")
            
            # Verificar users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            print(f"Users existentes: {user_count}")
            
            print("\n=== LLENANDO DATOS ===")
            
            # 1. MUNICIPALITIES (si no existen)
            if municipality_count == 0:
                print("1. Agregando municipalities...")
                cursor.execute("""
                    INSERT INTO municipalities (municipio, state) VALUES
                    ('Papantla', 'Veracruz'),
                    ('Coatzintla', 'Veracruz'),
                    ('Poza Rica', 'Veracruz'),
                    ('Tuxpan', 'Veracruz'),
                    ('Xalapa', 'Veracruz'),
                    ('Veracruz', 'Veracruz')
                """)
                connection.commit()
                print("✅ Municipalities agregados")
            
            # 2. BUSINESSES (agregar más si hay pocos)
            if business_count < 10:
                print("2. Agregando businesses...")
                cursor.execute("""
                    INSERT INTO businesses (name, category, address, municipality_id, phone, email, description, rating, visits_for_prize) VALUES
                    ('Pizzería Don Luigi', 'Restaurante', 'Av. Juárez 234', 1, '7841111111', 'info@donluigi.com', 'Pizzas artesanales al horno de leña', 4.6, 8),
                    ('Librería Cervantes', 'Librería', 'Calle Morelos 45', 2, '7822222222', 'ventas@cervantes.com', 'Libros y material educativo', 4.1, 5),
                    ('Taller Mecánico El Rayo', 'Automotriz', 'Carretera Nacional Km 5', 3, '7823333333', 'contacto@elrayo.com', 'Servicio automotriz especializado', 4.3, 4),
                    ('Panadería La Espiga', 'Panadería', 'Plaza Principal 12', 4, '7834444444', 'info@laespiga.com', 'Pan fresco y repostería', 4.7, 10),
                    ('Ferretería Construmax', 'Ferretería', 'Av. Construcción 89', 1, '7845555555', 'ventas@construmax.com', 'Materiales de construcción', 4.2, 6),
                    ('Estética Bella Vista', 'Belleza', 'Calle Belleza 23', 2, '7826666666', 'citas@bellavista.com', 'Servicios de belleza y estética', 4.5, 7),
                    ('Farmacia San Rafael', 'Farmacia', 'Av. Salud 67', 3, '7837777777', 'info@sanrafael.com', 'Medicamentos y productos de salud', 4.4, 5),
                    ('Mariscos El Puerto', 'Restaurante', 'Malecón 156', 4, '7848888888', 'reservas@elpuerto.com', 'Mariscos frescos del Golfo', 4.8, 6)
                """)
                connection.commit()
                print("✅ Businesses agregados")
            
            # 3. BUSINESS MENU
            cursor.execute("SELECT COUNT(*) as count FROM business_menu")
            menu_count = cursor.fetchone()['count']
            
            if menu_count < 20:
                print("3. Agregando menús...")
                # Obtener IDs reales de businesses
                cursor.execute("SELECT id FROM businesses ORDER BY id")
                business_ids = [row['id'] for row in cursor.fetchall()]
                
                menu_items = []
                for i, bid in enumerate(business_ids[:8]):  # Primeros 8 businesses
                    menu_items.extend([
                        (bid, f'Producto Especial {i+1}', f'Producto destacado del negocio {i+1}', 100.00 + (i*10), 'Especiales'),
                        (bid, f'Servicio Premium {i+1}', f'Servicio premium del negocio {i+1}', 200.00 + (i*20), 'Servicios'),
                        (bid, f'Combo Familiar {i+1}', f'Combo familiar del negocio {i+1}', 300.00 + (i*15), 'Combos')
                    ])
                
                cursor.executemany("""
                    INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                """, menu_items)
                connection.commit()
                print("✅ Menús agregados")
            
            # 4. USERS
            if user_count == 0:
                print("4. Creando usuarios...")
                password = "password123"
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
                hashed_str = hashed.decode('utf-8')
                
                users_data = [
                    ('Juan Pérez', 'juan@test.com', hashed_str, 1),
                    ('María García', 'maria@test.com', hashed_str, 1),
                    ('Carlos López', 'carlos@test.com', hashed_str, 1),
                    ('Ana Martínez', 'ana@test.com', hashed_str, 1),
                    ('Luis Rodríguez', 'luis@test.com', hashed_str, 1),
                    ('Sofia Hernández', 'sofia@test.com', hashed_str, 1),
                    ('Diego Morales', 'diego@test.com', hashed_str, 1)
                ]
                
                cursor.executemany("""
                    INSERT INTO users (nombre, email, password, user_type_id)
                    VALUES (%s, %s, %s, %s)
                """, users_data)
                connection.commit()
                print("✅ Usuarios creados")
            
            # 5. USER VISITS
            cursor.execute("SELECT COUNT(*) as count FROM user_visits")
            visits_count = cursor.fetchone()['count']
            
            if visits_count < 30:
                print("5. Agregando visitas...")
                # Obtener IDs reales
                cursor.execute("SELECT id FROM businesses ORDER BY id")
                business_ids = [row['id'] for row in cursor.fetchall()]
                cursor.execute("SELECT id FROM users ORDER BY id")
                user_ids = [row['id'] for row in cursor.fetchall()]
                
                current_month = datetime.now().strftime('%Y-%m')
                base_date = datetime.now() - timedelta(days=20)
                
                visits_data = []
                for i in range(40):
                    visit_date = base_date + timedelta(days=i % 20, hours=i % 12)
                    user_id = user_ids[i % len(user_ids)]
                    business_id = business_ids[i % len(business_ids)]
                    visits_data.append((user_id, business_id, visit_date, current_month))
                
                cursor.executemany("""
                    INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                    VALUES (%s, %s, %s, %s)
                """, visits_data)
                connection.commit()
                print("✅ Visitas agregadas")
            
            # 6. USER ROUNDS
            cursor.execute("SELECT COUNT(*) as count FROM user_rounds")
            rounds_count = cursor.fetchone()['count']
            
            if rounds_count < 15:
                print("6. Creando rondas...")
                # Obtener IDs reales
                cursor.execute("SELECT id FROM businesses ORDER BY id LIMIT 5")
                business_ids = [row['id'] for row in cursor.fetchall()]
                cursor.execute("SELECT id FROM users ORDER BY id")
                user_ids = [row['id'] for row in cursor.fetchall()]
                
                rounds_data = []
                for user_id in user_ids[:5]:  # Primeros 5 usuarios
                    for business_id in business_ids[:3]:  # Primeros 3 businesses
                        progress = (user_id + business_id) % 6
                        rounds_data.append((user_id, business_id, 1, progress, False, False))
                
                cursor.executemany("""
                    INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, is_completed, is_reward_claimed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, rounds_data)
                connection.commit()
                print("✅ Rondas creadas")
            
            print("\n=== VERIFICACIÓN FINAL ===")
            
            # Verificar datos finales
            tables = ['municipalities', 'businesses', 'business_menu', 'users', 'user_visits', 'user_rounds']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"{table}: {count} registros")
        
        connection.close()
        print("\n🎉 ¡Todas las tablas llenadas exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Llenando todas las tablas...")
    if populate_all_data():
        print("\n✅ Proceso completado")
        print("\n🔑 Credenciales de prueba:")
        print("Email: juan@test.com, maria@test.com, carlos@test.com, etc.")
        print("Password: password123")
        print("\n📡 Endpoints disponibles:")
        print("- GET /api/businesses")
        print("- GET /api/municipalities") 
        print("- GET /api/user/visits (requiere auth)")
    else:
        print("❌ Error en el proceso")