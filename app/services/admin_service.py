from app.config.database import get_db_connection
from app.schemas.admin import BusinessCreate, BusinessUpdate, UserCreate, UserUpdate, AdminDashboardFilters
from app.models.user import User
from app.utils.logger import log_info, log_error
from typing import Dict, List, Optional
import bcrypt
import json
from datetime import datetime, timedelta

class AdminService:
    
    @staticmethod
    def get_dashboard_stats(filters: Optional[AdminDashboardFilters] = None) -> Dict:
        """Obtiene estadísticas para el dashboard de admin"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                stats = {}
                
                # Filtros de fecha
                date_filter = ""
                date_params = []
                if filters and filters.start_date:
                    date_filter += " AND created_at >= %s"
                    date_params.append(filters.start_date)
                if filters and filters.end_date:
                    date_filter += " AND created_at <= %s"
                    date_params.append(filters.end_date)
                
                # Total de usuarios
                cursor.execute(f"SELECT COUNT(*) as total FROM users WHERE 1=1{date_filter}", date_params)
                stats['total_users'] = cursor.fetchone()['total']
                
                # Total de negocios
                cursor.execute(f"SELECT COUNT(*) as total FROM businesses WHERE active = TRUE{date_filter}", date_params)
                stats['total_businesses'] = cursor.fetchone()['total']
                
                # Total de cupones
                cursor.execute(f"SELECT COUNT(*) as total FROM user_rewards WHERE 1=1{date_filter}", date_params)
                stats['total_coupons'] = cursor.fetchone()['total']
                
                # Cupones por estado
                cursor.execute("""
                    SELECT status, COUNT(*) as count 
                    FROM user_rewards 
                    GROUP BY status
                """)
                stats['coupons_by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
                
                # Negocios por categoría
                cursor.execute("""
                    SELECT category, COUNT(*) as count 
                    FROM businesses 
                    WHERE active = TRUE 
                    GROUP BY category 
                    ORDER BY count DESC
                """)
                stats['businesses_by_category'] = cursor.fetchall()
                
                # Usuarios por tipo
                cursor.execute("""
                    SELECT ut.type_name, COUNT(u.id) as count
                    FROM user_types ut
                    LEFT JOIN users u ON ut.id = u.user_type_id
                    GROUP BY ut.id, ut.type_name
                """)
                stats['users_by_type'] = cursor.fetchall()
                
                # Actividad reciente (últimos 7 días)
                seven_days_ago = datetime.now() - timedelta(days=7)
                cursor.execute("""
                    SELECT DATE(created_at) as date, COUNT(*) as count
                    FROM users 
                    WHERE created_at >= %s
                    GROUP BY DATE(created_at)
                    ORDER BY date
                """, (seven_days_ago,))
                stats['recent_user_registrations'] = cursor.fetchall()
                
                return stats
                
        except Exception as e:
            log_error("Error obteniendo estadísticas de dashboard", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def get_all_businesses(page: int = 1, limit: int = 20, search: Optional[str] = None) -> Dict:
        """Obtiene todos los negocios con paginación"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                offset = (page - 1) * limit
                
                # Construir query con búsqueda
                search_filter = ""
                search_params = []
                if search:
                    search_filter = " AND (b.name ILIKE %s OR b.category ILIKE %s OR b.address ILIKE %s)"
                    search_term = f"%{search}%"
                    search_params = [search_term, search_term, search_term]
                
                # Obtener total
                cursor.execute(f"""
                    SELECT COUNT(*) as total 
                    FROM businesses b 
                    WHERE 1=1{search_filter}
                """, search_params)
                total = cursor.fetchone()['total']
                
                # Obtener negocios
                cursor.execute(f"""
                    SELECT b.*, m.municipio, u.nombre as owner_name, u.email as owner_email
                    FROM businesses b
                    LEFT JOIN municipalities m ON b.municipality_id = m.id
                    LEFT JOIN users u ON b.owner_user_id = u.id
                    WHERE 1=1{search_filter}
                    ORDER BY b.created_at DESC
                    LIMIT %s OFFSET %s
                """, search_params + [limit, offset])
                
                businesses = cursor.fetchall()
                
                return {
                    "businesses": businesses,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "pages": (total + limit - 1) // limit
                    }
                }
                
        except Exception as e:
            log_error("Error obteniendo negocios", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def create_business(business_data: BusinessCreate, admin_id: int) -> Dict:
        """Crea un nuevo negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar si el propietario existe
                cursor.execute("SELECT id, user_type_id FROM users WHERE email = %s", (business_data.owner_email,))
                owner = cursor.fetchone()
                
                if not owner:
                    raise ValueError(f"No existe un usuario con email {business_data.owner_email}")
                
                # Convertir listas y dicts a JSON
                opening_hours_json = json.dumps(business_data.opening_hours) if business_data.opening_hours else None
                working_days_json = json.dumps(business_data.working_days) if business_data.working_days else None
                payment_methods_json = json.dumps(business_data.payment_methods) if business_data.payment_methods else None
                
                # Crear negocio
                cursor.execute("""
                    INSERT INTO businesses (
                        name, category, address, municipality_id, phone, email, description,
                        image_url, logo, facebook, instagram, tiktok, whatsapp,
                        opening_hours, working_days, delivery_available, payment_methods,
                        visits_for_prize, owner_user_id, active
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING id
                """, (
                    business_data.name, business_data.category, business_data.address,
                    business_data.municipality_id, business_data.phone, business_data.email,
                    business_data.description, business_data.image_url, business_data.logo,
                    business_data.facebook, business_data.instagram, business_data.tiktok,
                    business_data.whatsapp, opening_hours_json, working_days_json,
                    business_data.delivery_available, payment_methods_json,
                    business_data.visits_for_prize, owner['id'], True
                ))
                
                business_id = cursor.fetchone()['id']
                connection.commit()
                
                log_info(f"Negocio creado por admin {admin_id}", business_id=business_id)
                
                return {"id": business_id, "name": business_data.name}
                
        except Exception as e:
            connection.rollback()
            log_error("Error creando negocio", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def update_business(business_id: int, business_data: BusinessUpdate, admin_id: int) -> Optional[Dict]:
        """Actualiza un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar que el negocio existe
                cursor.execute("SELECT id, name FROM businesses WHERE id = %s", (business_id,))
                business = cursor.fetchone()
                
                if not business:
                    return None
                
                # Construir query de actualización dinámicamente
                update_fields = []
                update_values = []
                
                for field, value in business_data.dict(exclude_unset=True).items():
                    if field in ['opening_hours', 'working_days', 'payment_methods'] and value is not None:
                        update_fields.append(f"{field} = %s")
                        update_values.append(json.dumps(value))
                    else:
                        update_fields.append(f"{field} = %s")
                        update_values.append(value)
                
                if update_fields:
                    update_values.append(business_id)
                    cursor.execute(f"""
                        UPDATE businesses 
                        SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, update_values)
                    
                    connection.commit()
                    log_info(f"Negocio actualizado por admin {admin_id}", business_id=business_id)
                
                return {"id": business_id, "name": business['name']}
                
        except Exception as e:
            connection.rollback()
            log_error("Error actualizando negocio", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def delete_business(business_id: int, admin_id: int) -> bool:
        """Elimina (desactiva) un negocio"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE businesses 
                    SET active = FALSE, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND active = TRUE
                """, (business_id,))
                
                if cursor.rowcount > 0:
                    connection.commit()
                    log_info(f"Negocio eliminado por admin {admin_id}", business_id=business_id)
                    return True
                
                return False
                
        except Exception as e:
            connection.rollback()
            log_error("Error eliminando negocio", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def get_all_users(page: int = 1, limit: int = 20, search: Optional[str] = None, user_type: Optional[int] = None) -> Dict:
        """Obtiene todos los usuarios con paginación"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                offset = (page - 1) * limit
                
                # Construir filtros
                filters = []
                params = []
                
                if search:
                    filters.append("(u.nombre ILIKE %s OR u.email ILIKE %s)")
                    search_term = f"%{search}%"
                    params.extend([search_term, search_term])
                
                if user_type is not None:
                    filters.append("u.user_type_id = %s")
                    params.append(user_type)
                
                where_clause = " AND ".join(filters) if filters else "1=1"
                
                # Obtener total
                cursor.execute(f"""
                    SELECT COUNT(*) as total 
                    FROM users u 
                    WHERE {where_clause}
                """, params)
                total = cursor.fetchone()['total']
                
                # Obtener usuarios
                cursor.execute(f"""
                    SELECT u.id, u.nombre, u.email, u.telefono, u.created_at,
                           ut.type_name as user_type_name, u.user_type_id
                    FROM users u
                    LEFT JOIN user_types ut ON u.user_type_id = ut.id
                    WHERE {where_clause}
                    ORDER BY u.created_at DESC
                    LIMIT %s OFFSET %s
                """, params + [limit, offset])
                
                users = cursor.fetchall()
                
                return {
                    "users": users,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "pages": (total + limit - 1) // limit
                    }
                }
                
        except Exception as e:
            log_error("Error obteniendo usuarios", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def create_user(user_data: UserCreate, admin_id: int) -> Dict:
        """Crea un nuevo usuario"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar si ya existe
                if user_data.email:
                    cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
                    if cursor.fetchone():
                        raise ValueError(f"Ya existe un usuario con email {user_data.email}")
                
                if user_data.telefono:
                    cursor.execute("SELECT id FROM users WHERE telefono = %s", (user_data.telefono,))
                    if cursor.fetchone():
                        raise ValueError(f"Ya existe un usuario con teléfono {user_data.telefono}")
                
                # Hash de contraseña
                hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
                
                # Crear usuario
                cursor.execute("""
                    INSERT INTO users (nombre, email, telefono, password, user_type_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (user_data.nombre, user_data.email, user_data.telefono, hashed_password, user_data.user_type))
                
                user_id = cursor.fetchone()['id']
                connection.commit()
                
                log_info(f"Usuario creado por admin {admin_id}", user_id=user_id)
                
                return {
                    "id": user_id,
                    "nombre": user_data.nombre,
                    "email": user_data.email,
                    "user_type": user_data.user_type
                }
                
        except Exception as e:
            connection.rollback()
            log_error("Error creando usuario", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate, admin_id: int) -> Optional[Dict]:
        """Actualiza un usuario"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Verificar que el usuario existe
                cursor.execute("SELECT id, nombre FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                
                if not user:
                    return None
                
                # Construir query de actualización dinámicamente
                update_fields = []
                update_values = []
                
                for field, value in user_data.dict(exclude_unset=True).items():
                    update_fields.append(f"{field} = %s")
                    update_values.append(value)
                
                if update_fields:
                    update_values.append(user_id)
                    cursor.execute(f"""
                        UPDATE users 
                        SET {', '.join(update_fields)}
                        WHERE id = %s
                    """, update_values)
                    
                    connection.commit()
                    log_info(f"Usuario actualizado por admin {admin_id}", user_id=user_id)
                
                return {"id": user_id, "nombre": user['nombre']}
                
        except Exception as e:
            connection.rollback()
            log_error("Error actualizando usuario", error=e)
            raise
        finally:
            connection.close()
    
    @staticmethod
    def get_system_stats() -> Dict:
        """Obtiene estadísticas generales del sistema"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                stats = {}
                
                # Estadísticas básicas
                cursor.execute("SELECT COUNT(*) as total FROM users")
                stats['total_users'] = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM businesses WHERE active = TRUE")
                stats['total_businesses'] = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM user_rewards")
                stats['total_rewards'] = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM user_visits")
                stats['total_visits'] = cursor.fetchone()['total']
                
                # Estadísticas de actividad (último mes)
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM users 
                    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                """)
                stats['new_users_last_month'] = cursor.fetchone()['count']
                
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM user_visits 
                    WHERE visit_date >= CURRENT_DATE - INTERVAL '30 days'
                """)
                stats['visits_last_month'] = cursor.fetchone()['count']
                
                return stats
                
        except Exception as e:
            log_error("Error obteniendo estadísticas del sistema", error=e)
            raise
        finally:
            connection.close()