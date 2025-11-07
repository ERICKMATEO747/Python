from app.config.database import get_db_connection
from app.utils.logger import log_info

def update_social_media_icons():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Actualizar con iconos reales de redes sociales
            updates = [
                (1, 'https://cdn-icons-png.flaticon.com/512/124/124010.png', 'https://cdn-icons-png.flaticon.com/512/2111/2111463.png', 'https://cdn-icons-png.flaticon.com/512/3046/3046120.png', 'https://cdn-icons-png.flaticon.com/512/733/733585.png'),
                (2, 'https://cdn-icons-png.flaticon.com/512/124/124010.png', 'https://cdn-icons-png.flaticon.com/512/2111/2111463.png', 'https://cdn-icons-png.flaticon.com/512/3046/3046120.png', 'https://cdn-icons-png.flaticon.com/512/733/733585.png'),
                (3, 'https://cdn-icons-png.flaticon.com/512/124/124010.png', 'https://cdn-icons-png.flaticon.com/512/2111/2111463.png', 'https://cdn-icons-png.flaticon.com/512/3046/3046120.png', 'https://cdn-icons-png.flaticon.com/512/733/733585.png'),
                (4, 'https://cdn-icons-png.flaticon.com/512/124/124010.png', 'https://cdn-icons-png.flaticon.com/512/2111/2111463.png', 'https://cdn-icons-png.flaticon.com/512/3046/3046120.png', 'https://cdn-icons-png.flaticon.com/512/733/733585.png'),
                (5, 'https://cdn-icons-png.flaticon.com/512/124/124010.png', 'https://cdn-icons-png.flaticon.com/512/2111/2111463.png', 'https://cdn-icons-png.flaticon.com/512/3046/3046120.png', 'https://cdn-icons-png.flaticon.com/512/733/733585.png')
            ]
            
            for business_id, facebook_icon, instagram_icon, tiktok_icon, whatsapp_icon in updates:
                cursor.execute("""
                    UPDATE businesses SET 
                    facebook = %s,
                    instagram = %s, 
                    tiktok = %s,
                    whatsapp = %s
                    WHERE id = %s
                """, (facebook_icon, instagram_icon, tiktok_icon, whatsapp_icon, business_id))
            
            connection.commit()
            log_info("Iconos de redes sociales actualizados correctamente")
            
    except Exception as e:
        log_info(f"Error actualizando iconos: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    update_social_media_icons()