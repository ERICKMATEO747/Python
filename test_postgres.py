#!/usr/bin/env python3
"""
Script de prueba simple para PostgreSQL
"""

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def test_connection():
    """Prueba la conexión básica a PostgreSQL"""
    try:
        DATABASE_URL = os.getenv('DATABASE_URL')
        print(f"Conectando a: {DATABASE_URL[:50]}...")
        
        connection = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        
        with connection.cursor() as cursor:
            # Probar consulta simple
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa: {version['version']}")
            
            # Probar creación de tabla simple
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100)
                )
            """)
            
            # Probar COUNT
            cursor.execute("SELECT COUNT(*) as count FROM test_table")
            result = cursor.fetchone()
            print(f"✅ COUNT funciona: {result['count']}")
            
            # Limpiar
            cursor.execute("DROP TABLE IF EXISTS test_table")
            connection.commit()
            
        connection.close()
        print("✅ Prueba completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"❌ Tipo: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection()