#!/usr/bin/env python3
"""
Script para eliminar municipios duplicados
Mantiene el registro con ID más bajo y elimina los duplicados
"""

from app.config.database import get_db_connection
from app.utils.logger import log_info, log_error

def remove_duplicate_municipalities():
    """Elimina municipios duplicados basándose en el nombre"""
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Encontrar duplicados
            find_duplicates_query = """
            SELECT municipio, COUNT(*) as count, GROUP_CONCAT(id ORDER BY id) as ids
            FROM municipalities 
            GROUP BY municipio 
            HAVING COUNT(*) > 1
            """
            
            cursor.execute(find_duplicates_query)
            duplicates = cursor.fetchall()
            
            if not duplicates:
                print("✅ No se encontraron municipios duplicados")
                return
            
            print(f"🔍 Encontrados {len(duplicates)} municipios con duplicados:")
            
            total_deleted = 0
            
            for duplicate in duplicates:
                municipio = duplicate['municipio']
                ids = duplicate['ids'].split(',')
                keep_id = ids[0]  # Mantener el ID más bajo
                delete_ids = ids[1:]  # Eliminar los demás
                
                print(f"📍 {municipio}: Manteniendo ID {keep_id}, eliminando IDs {', '.join(delete_ids)}")
                
                # Eliminar duplicados
                for delete_id in delete_ids:
                    delete_query = "DELETE FROM municipalities WHERE id = %s"
                    cursor.execute(delete_query, (delete_id,))
                    total_deleted += 1
            
            # Confirmar cambios
            connection.commit()
            
            print(f"\n✅ Proceso completado:")
            print(f"   • {len(duplicates)} municipios tenían duplicados")
            print(f"   • {total_deleted} registros duplicados eliminados")
            
            # Mostrar estadísticas finales
            cursor.execute("SELECT COUNT(*) as total FROM municipalities")
            total_remaining = cursor.fetchone()['total']
            print(f"   • {total_remaining} municipios únicos restantes")
            
    except Exception as e:
        connection.rollback()
        log_error("Error eliminando duplicados", error=e)
        print(f"❌ Error: {e}")
        
    finally:
        connection.close()

def show_duplicates_preview():
    """Muestra vista previa de duplicados sin eliminar"""
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT municipio, COUNT(*) as count, GROUP_CONCAT(id ORDER BY id) as ids
            FROM municipalities 
            GROUP BY municipio 
            HAVING COUNT(*) > 1
            ORDER BY count DESC, municipio
            """
            
            cursor.execute(query)
            duplicates = cursor.fetchall()
            
            if not duplicates:
                print("✅ No hay municipios duplicados")
                return
            
            print(f"🔍 VISTA PREVIA - {len(duplicates)} municipios duplicados:")
            print("-" * 60)
            
            for duplicate in duplicates:
                municipio = duplicate['municipio']
                count = duplicate['count']
                ids = duplicate['ids']
                print(f"📍 {municipio} ({count} veces) - IDs: {ids}")
            
            print("-" * 60)
            print(f"Total de registros duplicados a eliminar: {sum(d['count'] - 1 for d in duplicates)}")
            
    except Exception as e:
        log_error("Error consultando duplicados", error=e)
        print(f"❌ Error: {e}")
        
    finally:
        connection.close()

def main():
    """Función principal"""
    print("🗂️  ELIMINADOR DE MUNICIPIOS DUPLICADOS")
    print("=" * 50)
    
    # Mostrar vista previa
    show_duplicates_preview()
    
    if input("\n¿Proceder con la eliminación? (s/N): ").lower() == 's':
        print("\n🔄 Eliminando duplicados...")
        remove_duplicate_municipalities()
    else:
        print("❌ Operación cancelada")

if __name__ == "__main__":
    main()