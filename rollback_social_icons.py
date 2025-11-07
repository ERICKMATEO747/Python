from app.config.database import get_db_connection
from app.utils.logger import log_info

def rollback_social_media_icons():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Restaurar URLs originales de redes sociales
            updates = [
                (1, 'https://facebook.com/elsabor', 'https://instagram.com/elsabor', 'https://tiktok.com/@elsabor', 'https://wa.me/523312345678'),
                (2, 'https://facebook.com/cafecentral', 'https://instagram.com/cafecentral', 'https://tiktok.com/@cafecentral', 'https://wa.me/523387654321'),
                (3, 'https://facebook.com/tiendafashion', 'https://instagram.com/tiendafashion', 'https://tiktok.com/@tiendafashion', 'https://wa.me/523398765432'),
                (4, 'https://facebook.com/farmaciasalud', 'https://instagram.com/farmaciasalud', 'https://tiktok.com/@farmaciasalud', 'https://wa.me/523376543210'),
                (5, 'https://facebook.com/gimnasiofit', 'https://instagram.com/gimnasiofit', 'https://tiktok.com/@gimnasiofit', 'https://wa.me/523365432109')
            ]
            
            for business_id, facebook_url, instagram_url, tiktok_url, whatsapp_url in updates:
                cursor.execute("""
                    UPDATE businesses SET 
                    facebook = %s,
                    instagram = %s, 
                    tiktok = %s,
                    whatsapp = %s
                    WHERE id = %s
                """, (facebook_url, instagram_url, tiktok_url, whatsapp_url, business_id))
            
            connection.commit()
            log_info("Rollback de iconos de redes sociales completado")
            
    except Exception as e:
        log_info(f"Error en rollback: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    rollback_social_media_icons()