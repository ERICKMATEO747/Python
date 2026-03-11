from fastapi import HTTPException
from app.models.user_visit_sqlite import UserVisit
from app.models.user_sqlite import User
import qrcode
import io
import base64
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from PIL import Image

class UserController:
    @staticmethod
    def get_profile(user_id: int):
        try:
            user = User.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"success": True, "data": user}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_profile(user_id: int, data):
        try:
            # Implementación básica - en una app real actualizaría la BD
            return {"success": True, "message": "Perfil actualizado exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_visits(user_id: int):
        try:
            visits = UserVisit.get_user_visits_with_rounds(user_id)
            total_visits = sum(visit.get('visit_count', 0) for visit in visits)
            return {
                "success": True,
                "data": {
                    "data": visits,
                    "total_visits": total_visits
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def generate_qr(visit_data):
        try:
            # Crear payload para el JWT
            payload = {
                "user_id": visit_data.user_id,
                "business_id": visit_data.business_id,
                "visit_date": visit_data.visit_date.isoformat(),
                "exp": datetime.utcnow() + timedelta(hours=24)  # Expira en 24 horas
            }
            
            # Generar token JWT
            secret_key = os.getenv("JWT_SECRET_KEY", "default-secret-key")
            qr_token = jwt.encode(payload, secret_key, algorithm="HS256")
            
            # Generar código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_token)
            qr.make(fit=True)
            
            # Crear imagen QR
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir a base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            qr_data_url = f"data:image/png;base64,{qr_base64}"
            
            return {
                "success": True,
                "message": "Código QR generado exitosamente",
                "data": {
                    "qr_code": qr_data_url,
                    "qr_token": qr_token,
                    "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generando código QR: {str(e)}")
    
    @staticmethod
    def validate_qr_visit(qr_token: str, business_id: int, current_user: dict):
        try:
            # Decodificar y validar JWT
            secret_key = os.getenv("JWT_SECRET_KEY", "default-secret-key")
            
            try:
                payload = jwt.decode(qr_token, secret_key, algorithms=["HS256"])
            except JWTError:
                raise HTTPException(status_code=400, detail="Código QR inválido o expirado")
            
            # Validar que el business_id coincida
            if payload.get("business_id") != business_id:
                raise HTTPException(status_code=400, detail="El código QR no corresponde a este negocio")
            
            # Validar que el usuario coincida
            if payload.get("user_id") != current_user["id"]:
                raise HTTPException(status_code=400, detail="El código QR no corresponde a este usuario")
            
            # Registrar la visita en la base de datos
            visit_id = UserVisit.register_visit(
                user_id=current_user["id"],
                business_id=business_id,
                visit_date=datetime.fromisoformat(payload.get("visit_date"))
            )
            
            return {
                "success": True,
                "message": "Visita registrada exitosamente",
                "data": {
                    "visit_id": visit_id,
                    "business_id": business_id,
                    "user_id": current_user["id"],
                    "visit_date": payload.get("visit_date"),
                    "points_earned": 1
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error validando código QR: {str(e)}")