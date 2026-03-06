from app.config.database import get_db_connection
from app.utils.logger import log_error
from typing import List, Dict, Optional
import json

class Business:
    @staticmethod
    def get_all(user_id: int = None) -> List[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                if user_id:
                    cursor.execute("""
                        SELECT b.*, m.municipio,
                               CASE 
                                   WHEN ur.total_coupons IS NULL THEN NULL
                                   WHEN ur.reclamado = FALSE THEN 0
                                   WHEN ur.reclamado = TRUE THEN 1
                                   ELSE NULL
                               END as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        LEFT JOIN (
                            SELECT business_id, 
                                   COUNT(*) as total_coupons,
                                   BOOL_OR(reclamado) as reclamado
                            FROM user_rewards 
                            WHERE user_id = %s AND status IN ('vigente', 'reclamado')
                            GROUP BY business_id
                        ) ur ON b.id = ur.business_id
                        WHERE b.active = TRUE 
                        ORDER BY b.name
                    """, (user_id,))
                else:
                    cursor.execute("""
                        SELECT b.*, m.municipio, NULL as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        WHERE b.active = TRUE 
                        ORDER BY b.name
                    """)
                
                businesses = cursor.fetchall()
                return [Business._format_business_data(business) for business in businesses]
        except Exception as e:
            log_error("Error obteniendo negocios", error=e)
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(business_id: int, user_id: int = None) -> Optional[Dict]:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                if user_id:
                    cursor.execute("""
                        SELECT b.*, m.municipio,
                               CASE 
                                   WHEN ur.total_coupons IS NULL THEN NULL
                                   WHEN ur.reclamado = FALSE THEN 0
                                   WHEN ur.reclamado = TRUE THEN 1
                                   ELSE NULL
                               END as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        LEFT JOIN (
                            SELECT business_id, 
                                   COUNT(*) as total_coupons,
                                   BOOL_OR(reclamado) as reclamado
                            FROM user_rewards 
                            WHERE user_id = %s AND status IN ('vigente', 'reclamado')
                            GROUP BY business_id
                        ) ur ON b.id = ur.business_id
                        WHERE b.id = %s AND b.active = TRUE
                    """, (user_id, business_id))
                else:
                    cursor.execute("""
                        SELECT b.*, m.municipio, NULL as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        WHERE b.id = %s AND b.active = TRUE
                    """, (business_id,))
                
                business = cursor.fetchone()
                return Business._format_business_data(business) if business else None
        except Exception as e:
            log_error("Error obteniendo negocio", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def _format_business_data(business: Dict) -> Dict:
        """Formatea los datos JSON del negocio"""
        if not business:
            return business
        
        # Parsear campos JSON
        if business.get('opening_hours'):
            try:
                business['opening_hours'] = json.loads(business['opening_hours'])
            except (json.JSONDecodeError, TypeError):
                business['opening_hours'] = None
        
        if business.get('working_days'):
            try:
                business['working_days'] = json.loads(business['working_days'])
            except (json.JSONDecodeError, TypeError):
                business['working_days'] = None
        
        if business.get('payment_methods'):
            try:
                business['payment_methods'] = json.loads(business['payment_methods'])
            except (json.JSONDecodeError, TypeError):
                business['payment_methods'] = None
        
        # Convertir unclaimed_coupons a int si es numérico
        if business.get('unclaimed_coupons') is not None:
            try:
                business['unclaimed_coupons'] = int(business['unclaimed_coupons'])
            except (ValueError, TypeError):
                business['unclaimed_coupons'] = 0
        else:
            business['unclaimed_coupons'] = 0
        
        return business
    

    
    @staticmethod
    def get_profile(business_id: int) -> Optional[Dict]:
        """Obtiene perfil completo del negocio para edición"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT b.id, b.name, b.address, m.municipio, b.phone, b.email, 
                           b.payment_methods, b.delivery_options, b.image_url, b.logo,
                           b.opening_hours, b.working_days, b.website, b.facebook, 
                           b.instagram, b.whatsapp
                    FROM businesses b
                    LEFT JOIN municipalities m ON b.municipality_id = m.id
                    WHERE b.id = %s AND b.active = TRUE
                """, (business_id,))
                business = cursor.fetchone()
                return Business._format_business_data(business) if business else None
        except Exception as e:
            log_error("Error obteniendo perfil del negocio", error=e)
            return None
        finally:
            connection.close()
    
    @staticmethod
    def update_profile(business_id: int, profile_data: Dict) -> bool:
        """Actualiza perfil del negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Convertir campos a formato adecuado
                opening_hours = profile_data.get('opening_hours')
                if isinstance(opening_hours, (dict, list)):
                    opening_hours = json.dumps(opening_hours)
                elif opening_hours == "":
                    opening_hours = None
                
                working_days = profile_data.get('working_days')
                if isinstance(working_days, list):
                    working_days = json.dumps(working_days)
                elif working_days == "":
                    working_days = None
                
                payment_methods = profile_data.get('payment_methods')
                if isinstance(payment_methods, list):
                    payment_methods = json.dumps(payment_methods)
                elif payment_methods == "":
                    payment_methods = None
                
                delivery_options = profile_data.get('delivery_options')
                if isinstance(delivery_options, list):
                    delivery_options = json.dumps(delivery_options)
                elif delivery_options == "":
                    delivery_options = None
                
                # Validar JSON antes de insertar
                try:
                    if payment_methods and payment_methods != "null":
                        json.loads(payment_methods)
                    if delivery_options and delivery_options != "null":
                        json.loads(delivery_options)
                    if working_days and working_days != "null":
                        json.loads(working_days)
                    if opening_hours and opening_hours != "null":
                        json.loads(opening_hours)
                except json.JSONDecodeError as je:
                    log_error(f"Error de JSON: {je}. payment_methods={payment_methods}, delivery_options={delivery_options}")
                    return False
                
                cursor.execute("""
                    UPDATE businesses SET 
                        phone = %s, email = %s, payment_methods = %s, 
                        delivery_options = %s, image_url = %s, logo = %s,
                        opening_hours = %s, working_days = %s, website = %s,
                        facebook = %s, instagram = %s, whatsapp = %s
                    WHERE id = %s AND active = TRUE
                """, (
                    profile_data.get('phone') or None,
                    profile_data.get('email') or None,
                    payment_methods or None,
                    delivery_options or None,
                    profile_data.get('image_url') or None,
                    profile_data.get('logo') or None,
                    opening_hours or None,
                    working_days or None,
                    profile_data.get('website') or None,
                    profile_data.get('facebook') or None,
                    profile_data.get('instagram') or None,
                    profile_data.get('whatsapp') or None,
                    business_id
                ))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            log_error(f"Error actualizando perfil del negocio. Datos: {profile_data}. SQL params: phone={profile_data.get('phone')}, email={profile_data.get('email')}, payment_methods={payment_methods}, delivery_options={delivery_options}, opening_hours={opening_hours}, working_days={working_days}", error=e)
            connection.rollback()
            return False
        finally:
            connection.close()