from app.config.database import get_db_connection
from app.utils.logger import log_info

def remove_duplicate_businesses():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Encontrar duplicados por nombre
            cursor.execute("""
                SELECT name, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM businesses 
                GROUP BY name 
                HAVING COUNT(*) > 1
            """)
            duplicates = cursor.fetchall()
            
            if not duplicates:
                log_info("No se encontraron negocios duplicados")
                return
            
            for duplicate in duplicates:
                ids = duplicate['ids'].split(',')
                # Mantener el primer ID, eliminar los demás
                ids_to_delete = ids[1:]
                
                log_info(f"Eliminando duplicados de '{duplicate['name']}': {ids_to_delete}")
                
                # Eliminar menús de negocios duplicados
                for business_id in ids_to_delete:
                    cursor.execute("DELETE FROM business_menu WHERE business_id = %s", (business_id,))
                
                # Eliminar negocios duplicados
                cursor.execute(f"DELETE FROM businesses WHERE id IN ({','.join(['%s'] * len(ids_to_delete))})", ids_to_delete)
            
            connection.commit()
            log_info("Duplicados eliminados exitosamente")
            
    except Exception as e:
        log_info(f"Error eliminando duplicados: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    remove_duplicate_businesses()