#!/usr/bin/env python3
"""
Script para llenar solo los datos faltantes
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import bcrypt

# Cargar variables de entorno
load_dotenv()

def fill_missing_data():
    """Llena solo los datos que faltan"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("=== LLENANDO DATOS FALTANTES ===")
            
            # 1. BUSINESS MENU (si está vacío)
            cursor.execute("SELECT COUNT(*) as count FROM business_menu")
            menu_count = cursor.fetchone()['count']
            
            if menu_count == 0:
                print("1. Agregando menús...")
                # Obtener IDs reales de businesses
                cursor.execute("SELECT id, name FROM businesses ORDER BY id")
                businesses = cursor.fetchall()
                
                menu_items = []
                for i, business in enumerate(businesses):
                    bid = business['id']
                    name = business['name']
                    menu_items.extend([
                        (bid, f'Producto Especial - {name}', f'Producto destacado de {name}', 100.00 + (i*10), 'Especiales'),
                        (bid, f'Servicio Premium - {name}', f'Servicio premium de {name}', 200.00 + (i*20), 'Servicios'),
                        (bid, f'Combo Familiar - {name}', f'Combo familiar de {name}', 300.00 + (i*15), 'Combos')
                    ])
                
                cursor.executemany("""
                    INSERT INTO business_menu (business_id, producto, descripcion, precio, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                """, menu_items)
                connection.commit()
                print(f"✅ {len(menu_items)} menús agregados")
            
            # 2. USER VISITS (si hay pocas)
            cursor.execute("SELECT COUNT(*) as count FROM user_visits")
            visits_count = cursor.fetchone()['count']
            
            if visits_count < 20:
                print("2. Agregando visitas...")
                # Obtener IDs reales
                cursor.execute("SELECT id FROM businesses ORDER BY id")
                business_ids = [row['id'] for row in cursor.fetchall()]
                cursor.execute("SELECT id FROM users ORDER BY id")
                user_ids = [row['id'] for row in cursor.fetchall()]
                
                if user_ids and business_ids:
                    current_month = datetime.now().strftime('%Y-%m')
                    base_date = datetime.now() - timedelta(days=20)
                    
                    visits_data = []
                    for i in range(30):
                        visit_date = base_date + timedelta(days=i % 20, hours=i % 12)
                        user_id = user_ids[i % len(user_ids)]
                        business_id = business_ids[i % len(business_ids)]
                        visits_data.append((user_id, business_id, visit_date, current_month))
                    
                    cursor.executemany("""
                        INSERT INTO user_visits (user_id, business_id, visit_date, visit_month)
                        VALUES (%s, %s, %s, %s)
                    """, visits_data)
                    connection.commit()
                    print(f"✅ {len(visits_data)} visitas agregadas")
            
            # 3. USER ROUNDS (si hay pocas)
            cursor.execute("SELECT COUNT(*) as count FROM user_rounds")
            rounds_count = cursor.fetchone()['count']
            
            if rounds_count < 10:
                print("3. Creando rondas...")
                # Obtener IDs reales
                cursor.execute("SELECT id FROM businesses ORDER BY id LIMIT 4")
                business_ids = [row['id'] for row in cursor.fetchall()]
                cursor.execute("SELECT id FROM users ORDER BY id")
                user_ids = [row['id'] for row in cursor.fetchall()]
                
                if user_ids and business_ids:
                    rounds_data = []
                    for user_id in user_ids:
                        for business_id in business_ids[:3]:  # Solo primeros 3 businesses
                            progress = (user_id + business_id) % 6
                            rounds_data.append((user_id, business_id, 1, progress, False, False))
                    
                    cursor.executemany("""
                        INSERT INTO user_rounds (user_id, business_id, round_number, progress_in_round, is_completed, is_reward_claimed)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, rounds_data)
                    connection.commit()
                    print(f"✅ {len(rounds_data)} rondas creadas")
            
            print("\n=== VERIFICACIÓN FINAL ===")
            
            # Verificar datos finales
            tables = ['municipalities', 'businesses', 'business_menu', 'users', 'user_visits', 'user_rounds']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"{table}: {count} registros")
            
            # Mostrar algunos datos de ejemplo
            print("\n=== DATOS DE EJEMPLO ===")
            
            cursor.execute("SELECT id, name, category FROM businesses LIMIT 5")
            businesses = cursor.fetchall()
            print("Businesses:")
            for b in businesses:
                print(f"  {b['id']}: {b['name']} ({b['category']})")
            
            cursor.execute("SELECT id, municipio FROM municipalities LIMIT 5")
            municipalities = cursor.fetchall()
            print("Municipalities:")
            for m in municipalities:
                print(f"  {m['id']}: {m['municipio']}")
            
            cursor.execute("SELECT id, nombre, email FROM users LIMIT 5")
            users = cursor.fetchall()
            print("Users:")
            for u in users:
                print(f"  {u['id']}: {u['nombre']} ({u['email']})")
        
        connection.close()
        print("\n🎉 ¡Datos faltantes agregados exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Llenando datos faltantes...")
    if fill_missing_data():
        print("\n✅ Proceso completado")
        print("\n🔑 Credenciales de prueba:")
        print("Email: juan@test.com, maria@test.com, carlos@test.com, etc.")
        print("Password: password123")
        print("\n📡 Endpoints para probar:")
        print("- GET http://localhost:8000/api/businesses")
        print("- GET http://localhost:8000/api/municipalities") 
        print("- POST http://localhost:8000/api/auth/login")
        print("- GET http://localhost:8000/api/user/visits (requiere auth)")
    else:
        print("❌ Error en el proceso")