#!/usr/bin/env python3
"""
ROLLBACK SCRIPT - Backend Optimization
Revierte las optimizaciones implementadas para manejar miles de negocios
"""

import os
import shutil
from datetime import datetime

def create_rollback():
    print("🔄 INICIANDO ROLLBACK - Backend Optimization")
    print("=" * 50)
    
    # 1. Revertir BusinessService
    print("📝 Revirtiendo BusinessService...")
    business_service_original = '''from app.models.business import Business
from app.utils.logger import log_info

class BusinessService:
    @staticmethod
    def get_all_businesses(user_id: int = None):
        log_info("Obteniendo todos los negocios")
        return Business.get_all(user_id)
    
    @staticmethod
    def get_business_by_id(business_id: int, user_id: int = None):
        log_info(f"Obteniendo negocio con ID: {business_id}")
        return Business.get_by_id(business_id, user_id)
    
    @staticmethod
    def get_business_profile(business_id: int):
        log_info(f"Obteniendo perfil del negocio: {business_id}")
        return Business.get_profile(business_id)
    
    @staticmethod
    def update_business_profile(business_id: int, profile_data: dict):
        log_info(f"Actualizando perfil del negocio: {business_id}")
        return Business.update_profile(business_id, profile_data)'''
    
    with open('app/services/business_service.py', 'w', encoding='utf-8') as f:
        f.write(business_service_original)
    
    # 2. Revertir BusinessController
    print("📝 Revirtiendo BusinessController...")
    business_controller_original = '''from fastapi import HTTPException
from app.services.business_service import BusinessService
from app.schemas.business import BusinessProfileUpdate

class BusinessController:
    @staticmethod
    def get_businesses(current_user: dict = None):
        try:
            user_id = current_user["id"] if current_user else None
            businesses = BusinessService.get_all_businesses(user_id)
            return {"data": businesses}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_business(business_id: int, current_user: dict = None):
        try:
            user_id = current_user["id"] if current_user else None
            business = BusinessService.get_business_by_id(business_id, user_id)
            if not business:
                raise HTTPException(status_code=404, detail="Negocio no encontrado")
            return {"data": business}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_business_profile(business_id: int, current_user: dict):
        try:
            profile = BusinessService.get_business_profile(business_id)
            if not profile:
                raise HTTPException(status_code=404, detail="Perfil del negocio no encontrado")
            return {"success": True, "data": profile}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_business_profile(business_id: int, profile_data: BusinessProfileUpdate, current_user: dict):
        try:
            success = BusinessService.update_business_profile(business_id, profile_data.dict(exclude_unset=True))
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el perfil del negocio")
            return {"success": True, "message": "Perfil actualizado exitosamente"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")'''
    
    with open('app/controllers/business_controller.py', 'w', encoding='utf-8') as f:
        f.write(business_controller_original)
    
    # 3. Revertir Routes
    print("📝 Revirtiendo Routes...")
    business_routes_original = '''from fastapi import APIRouter, Depends
from app.controllers.business_controller import BusinessController
from app.utils.auth_middleware import get_current_user

router = APIRouter(prefix="/api/businesses", tags=["businesses"])

@router.get("")
async def get_businesses(current_user: dict = Depends(get_current_user)):
    """Lista todos los negocios disponibles"""
    return BusinessController.get_businesses(current_user)

@router.get("/{business_id}")
async def get_business(business_id: int, current_user: dict = Depends(get_current_user)):
    """Obtiene información detallada del negocio"""
    return BusinessController.get_business(business_id, current_user)'''
    
    with open('app/routes/businesses.py', 'w', encoding='utf-8') as f:
        f.write(business_routes_original)
    
    # 4. Revertir Business Model (eliminar métodos optimizados)
    print("📝 Revirtiendo Business Model...")
    business_model_rollback = '''from app.config.database import get_db_connection
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
                                   WHEN ur.total_coupons IS NULL THEN ''
                                   WHEN ur.reclamado = 0 THEN 0
                                   WHEN ur.reclamado = 1 THEN 1
                                   ELSE ''
                               END as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        LEFT JOIN (
                            SELECT business_id, 
                                   COUNT(*) as total_coupons,
                                   MAX(reclamado) as reclamado
                            FROM user_rewards 
                            WHERE user_id = %s AND status IN ('vigente', 'reclamado')
                            GROUP BY business_id
                        ) ur ON b.id = ur.business_id
                        WHERE b.active = 1 
                        ORDER BY b.name
                    """, (user_id,))
                else:
                    cursor.execute("""
                        SELECT b.*, m.municipio, '' as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        WHERE b.active = 1 
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
                                   WHEN ur.total_coupons IS NULL THEN ''
                                   WHEN ur.reclamado = 0 THEN 0
                                   WHEN ur.reclamado = 1 THEN 1
                                   ELSE ''
                               END as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        LEFT JOIN (
                            SELECT business_id, 
                                   COUNT(*) as total_coupons,
                                   MAX(reclamado) as reclamado
                            FROM user_rewards 
                            WHERE user_id = %s AND status IN ('vigente', 'reclamado')
                            GROUP BY business_id
                        ) ur ON b.id = ur.business_id
                        WHERE b.id = %s AND b.active = 1
                    """, (user_id, business_id))
                else:
                    cursor.execute("""
                        SELECT b.*, m.municipio, '' as unclaimed_coupons
                        FROM businesses b 
                        LEFT JOIN municipalities m ON b.municipality_id = m.id 
                        WHERE b.id = %s AND b.active = 1
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
                if business['unclaimed_coupons'] == '':
                    business['unclaimed_coupons'] = ''
                else:
                    business['unclaimed_coupons'] = int(business['unclaimed_coupons'])
            except (ValueError, TypeError):
                pass
        
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
                    WHERE b.id = %s AND b.active = 1
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
                    WHERE id = %s AND active = 1
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
            connection.close()'''
    
    with open('app/models/business.py', 'w', encoding='utf-8') as f:
        f.write(business_model_rollback)
    
    # 5. Revertir main.py (eliminar middleware de compresión)
    print("📝 Revirtiendo main.py...")
    main_rollback = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, user, businesses, business_portal, rewards
from app.config.database import init_db
import uvicorn

app = FastAPI(
    title="Auth API",
    description="API REST para autenticación de usuarios",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(businesses.router)
app.include_router(business_portal.router)
app.include_router(rewards.router)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Auth API funcionando correctamente"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)'''
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_rollback)
    
    # 6. Eliminar archivos de optimización
    print("🗑️ Eliminando archivos de optimización...")
    files_to_remove = [
        'optimize_database.sql',
        'test_performance.py'
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"   ✅ Eliminado: {file}")
    
    print("\n" + "=" * 50)
    print("✅ ROLLBACK COMPLETADO")
    print("\n📋 Cambios revertidos:")
    print("   • BusinessService: Eliminada paginación y búsqueda")
    print("   • BusinessController: Revertido a métodos originales")
    print("   • Routes: Eliminados parámetros de paginación")
    print("   • Business Model: Eliminados métodos optimizados")
    print("   • main.py: Eliminado middleware de compresión")
    print("   • Archivos de optimización eliminados")
    print("\n🔄 El sistema ha vuelto al estado anterior a las optimizaciones")

if __name__ == "__main__":
    create_rollback()