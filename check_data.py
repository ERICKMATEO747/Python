#!/usr/bin/env python3
"""
Script para verificar datos existentes
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def check_existing_data():
    """Verifica qué datos existen en la base de datos"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            print("=== VERIFICANDO DATOS EXISTENTES ===")
            
            # Verificar businesses
            cursor.execute("SELECT id, name FROM businesses ORDER BY id")
            businesses = cursor.fetchall()
            print(f"\n📊 BUSINESSES ({len(businesses)}):")
            for business in businesses:
                print(f"  ID {business['id']}: {business['name']}")
            
            # Verificar users
            cursor.execute("SELECT id, nombre, email FROM users ORDER BY id")
            users = cursor.fetchall()
            print(f"\n👥 USERS ({len(users)}):")
            for user in users:
                print(f"  ID {user['id']}: {user['nombre']} ({user['email']})")
            
            # Verificar municipalities
            cursor.execute("SELECT id, municipio FROM municipalities ORDER BY id")
            municipalities = cursor.fetchall()
            print(f"\n🏘️ MUNICIPALITIES ({len(municipalities)}):")
            for mun in municipalities:
                print(f"  ID {mun['id']}: {mun['municipio']}")
            
            # Verificar business_menu
            cursor.execute("SELECT COUNT(*) as count FROM business_menu")
            result = cursor.fetchone()
            menu_count = result['count'] if result else 0
            print(f"\n🍽️ BUSINESS_MENU: {menu_count} items")
            
            # Verificar user_visits
            cursor.execute("SELECT COUNT(*) as count FROM user_visits")
            result = cursor.fetchone()
            visits_count = result['count'] if result else 0
            print(f"\n📅 USER_VISITS: {visits_count} visits")
            
            # Verificar user_rounds
            cursor.execute("SELECT COUNT(*) as count FROM user_rounds")
            result = cursor.fetchone()
            rounds_count = result['count'] if result else 0
            print(f"\n🔄 USER_ROUNDS: {rounds_count} rounds")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_existing_data()