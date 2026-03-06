#!/usr/bin/env python3
"""
Script para verificar tipos de usuario y funcionalidades de admin
"""

from app.config.database import get_db_connection

def check_admin_features():
    """Verifica las funcionalidades de administrador existentes"""
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            print("=== ANÁLISIS DE FUNCIONALIDADES DE ADMINISTRADOR ===\n")
            
            # 1. Verificar tipos de usuario
            try:
                cursor.execute("SELECT * FROM user_types ORDER BY id")
                user_types = cursor.fetchall()
                print("1. TIPOS DE USUARIO:")
                for ut in user_types:
                    print(f"   - ID: {ut['id']}, Tipo: {ut['type_name']}, Hash: {ut.get('type_hash', 'N/A')}, Activo: {ut.get('active', 'N/A')}")
            except Exception as e:
                print(f"   Error: {e}")
            
            # 2. Verificar usuarios administradores
            try:
                cursor.execute("""
                    SELECT u.id, u.nombre, u.email, ut.type_name 
                    FROM users u 
                    LEFT JOIN user_types ut ON u.user_type_id = ut.id 
                    WHERE u.user_type_id != 1 OR ut.type_name != 'cliente'
                    ORDER BY u.id
                """)
                admin_users = cursor.fetchall()
                print(f"\n2. USUARIOS NO-CLIENTE ({len(admin_users)}):")
                for user in admin_users:
                    print(f"   - {user['nombre']} ({user['email']}) - Tipo: {user.get('type_name', 'N/A')}")
            except Exception as e:
                print(f"   Error: {e}")
            
            # 3. Verificar negocios con propietarios
            try:
                cursor.execute("""
                    SELECT b.id, b.name, u.nombre as owner_name, u.email as owner_email
                    FROM businesses b
                    LEFT JOIN users u ON b.owner_user_id = u.id
                    WHERE b.active = 1
                    LIMIT 5
                """)
                businesses = cursor.fetchall()
                print(f"\n3. NEGOCIOS CON PROPIETARIOS (primeros 5):")
                for biz in businesses:
                    owner = f"{biz.get('owner_name', 'Sin propietario')} ({biz.get('owner_email', 'N/A')})"
                    print(f"   - {biz['name']} - Propietario: {owner}")
            except Exception as e:
                print(f"   Error: {e}")
            
            # 4. Verificar tablas de auditoría
            try:
                cursor.execute("SHOW TABLES LIKE '%audit%'")
                audit_tables = cursor.fetchall()
                print(f"\n4. TABLAS DE AUDITORÍA:")
                for table in audit_tables:
                    print(f"   - {list(table.values())[0]}")
            except Exception as e:
                print(f"   Error: {e}")
                
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        connection.close()

def analyze_endpoints():
    """Analiza los endpoints disponibles"""
    print("\n=== ANÁLISIS DE ENDPOINTS ===\n")
    
    endpoints = {
        "Autenticación": ["/api/auth/register", "/api/auth/login"],
        "Usuarios": ["/api/user/*"],
        "Negocios (Público)": ["/api/businesses", "/api/businesses/{id}"],
        "Portal de Negocio": [
            "/api/business/{id}/dashboard",
            "/api/business/{id}/profile", 
            "/api/business/{id}/menu",
            "/api/business/{id}/rewards",
            "/api/business/{id}/loyalty-config",
            "/api/business/validate-qr"
        ],
        "Premios": ["/api/rewards/*"],
        "Lealtad": ["/api/loyalty/*"],
        "Notificaciones": ["/api/notifications/*"],
        "Municipios": ["/api/municipalities"]
    }
    
    for category, routes in endpoints.items():
        print(f"{category}:")
        for route in routes:
            print(f"   - {route}")
        print()

if __name__ == "__main__":
    check_admin_features()
    analyze_endpoints()