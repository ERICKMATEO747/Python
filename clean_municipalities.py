#!/usr/bin/env python3
"""
Script directo para limpiar municipios duplicados
"""

from app.config.database import get_db_connection

def clean_duplicates():
    """Elimina duplicados manteniendo solo el primer registro de cada municipio"""
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Contar registros antes
            cursor.execute("SELECT COUNT(*) as total FROM municipalities")
            before_count = cursor.fetchone()['total']
            
            # Eliminar duplicados manteniendo solo el ID más bajo de cada municipio
            delete_query = """
            DELETE m1 FROM municipalities m1
            INNER JOIN municipalities m2 
            WHERE m1.municipio = m2.municipio 
            AND m1.state = m2.state 
            AND m1.id > m2.id
            """
            
            cursor.execute(delete_query)
            deleted_count = cursor.rowcount
            
            # Confirmar cambios
            connection.commit()
            
            # Contar registros después
            cursor.execute("SELECT COUNT(*) as total FROM municipalities")
            after_count = cursor.fetchone()['total']
            
            print(f"✅ Limpieza completada:")
            print(f"   • Antes: {before_count} registros")
            print(f"   • Eliminados: {deleted_count} duplicados")
            print(f"   • Después: {after_count} registros únicos")
            
    except Exception as e:
        connection.rollback()
        print(f"❌ Error: {e}")
        
    finally:
        connection.close()

if __name__ == "__main__":
    print("🧹 Limpiando municipios duplicados...")
    clean_duplicates()