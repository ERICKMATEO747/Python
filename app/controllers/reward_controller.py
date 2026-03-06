from fastapi import HTTPException
from app.services.reward_service import RewardService
from app.schemas.reward import RewardCreate, RewardUpdate, CouponGenerate, CouponClaim, CouponRedeem, CouponQRValidation
from datetime import datetime

class RewardController:
    @staticmethod
    def create_reward(reward_data: RewardCreate):
        """Crea un nuevo premio para un negocio"""
        try:
            reward_id = RewardService.create_reward(
                reward_data.business_id,
                reward_data.title,
                reward_data.description,
                reward_data.terms_conditions,
                reward_data.validity_days
            )
            
            if not reward_id:
                raise HTTPException(status_code=400, detail="No se pudo crear el premio")
            
            return {
                "success": True,
                "message": "Premio creado exitosamente",
                "reward_id": reward_id
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_reward_by_id(reward_id: int):
        """Obtiene un premio específico por ID"""
        try:
            reward = RewardService.get_reward_by_id(reward_id)
            if not reward:
                raise HTTPException(status_code=404, detail="Premio no encontrado")
            
            return {
                "success": True,
                "data": reward
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_business_rewards(business_id: int):
        """Obtiene todos los premios activos de un negocio"""
        try:
            rewards = RewardService.get_business_rewards(business_id)
            return {
                "success": True,
                "data": rewards,
                "total": len(rewards)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def update_reward(reward_id: int, reward_data: RewardUpdate):
        """Actualiza un premio"""
        try:
            update_data = reward_data.dict(exclude_unset=True)
            success = RewardService.update_reward(reward_id, **update_data)
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el premio")
            
            return {
                "success": True,
                "message": "Premio actualizado exitosamente"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def generate_coupon(coupon_data: CouponGenerate):
        """Genera un cupón de premio para el usuario basado en rondas"""
        try:
            coupon = RewardService.check_and_generate_reward(
                coupon_data.user_id,
                coupon_data.business_id
            )
            
            if not coupon:
                raise HTTPException(
                    status_code=400, 
                    detail="No se puede generar cupón. Verifica que hayas completado las visitas requeridas en la ronda actual."
                )
            
            return {
                "success": True,
                "message": f"¡Felicidades! Has completado la ronda {coupon.get('round_number', 1)} y ganado un premio",
                "data": coupon
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def get_user_rewards(user_id: int):
        """Obtiene todos los cupones del usuario"""
        try:
            rewards = RewardService.get_user_rewards(user_id)
            return {
                "success": True,
                "data": rewards
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def claim_coupon(coupon_data: CouponClaim, user_id: int):
        """Reclama un cupón y completa la ronda"""
        from app.models.audit_log import AuditLog
        
        try:
            result = RewardService.claim_coupon(coupon_data.coupon_id, user_id)
            
            if not result["success"]:
                raise HTTPException(status_code=400, detail=result["error"])
            
            # Registrar en audit trail
            AuditLog.log_action(
                user_id=user_id,
                action_type='REWARD_CLAIM',
                description=f"Cupón {coupon_data.coupon_id} reclamado",
                new_values={
                    "coupon_id": coupon_data.coupon_id,
                    "round_completed": result.get("round_completed"),
                    "new_round_started": result.get("new_round_started")
                }
            )
            
            return {
                "success": True,
                "message": result["message"],
                "data": {
                    "round_completed": result.get("round_completed"),
                    "new_round_started": result.get("new_round_started")
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def redeem_coupon(coupon_data: CouponRedeem, user_id: int):
        """Redime un cupón (usado en el negocio)"""
        from app.models.audit_log import AuditLog
        from app.config.database import get_db_connection
        
        try:
            # Obtener datos del cupón antes de redimir
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT business_id FROM user_rewards WHERE id = %s",
                    (coupon_data.coupon_id,)
                )
                coupon = cursor.fetchone()
                business_id = coupon['business_id'] if coupon else None
            connection.close()
            
            success = RewardService.redeem_coupon(coupon_data.coupon_id, user_id)
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo redimir el cupón")
            
            # Registrar en audit trail
            AuditLog.log_action(
                user_id=user_id,
                action_type='REWARD_REDEEM',
                description=f"Cupón {coupon_data.coupon_id} redimido en negocio",
                business_id=business_id,
                new_values={
                    "coupon_id": coupon_data.coupon_id,
                    "redeemed_at": datetime.now().isoformat()
                }
            )
            
            return {
                "success": True,
                "message": "Cupón redimido exitosamente",
                "data": {
                    "coupon_id": coupon_data.coupon_id,
                    "redeemed_at": datetime.now().isoformat(),
                    "business_id": business_id
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def delete_reward(reward_id: int, current_user: dict):
        """Elimina un premio"""
        from app.models.audit_log import AuditLog
        from app.config.database import get_db_connection
        
        try:
            # Obtener datos del premio antes de eliminar
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT business_id, title FROM rewards WHERE id = %s",
                    (reward_id,)
                )
                reward = cursor.fetchone()
                if not reward:
                    raise HTTPException(status_code=404, detail="Premio no encontrado")
                
                business_id = reward['business_id']
                reward_title = reward['title']
            connection.close()
            
            success = RewardService.delete_reward(reward_id)
            
            if not success:
                raise HTTPException(status_code=400, detail="No se pudo eliminar el premio")
            
            # Registrar en audit trail
            AuditLog.log_action(
                user_id=current_user['id'],
                action_type='REWARD_DELETE',
                description=f"Premio eliminado: {reward_title}",
                business_id=business_id,
                old_values={"reward_id": reward_id, "title": reward_title}
            )
            
            return {
                "success": True,
                "message": "Premio eliminado exitosamente"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    @staticmethod
    def validate_coupon_qr(qr_data: CouponQRValidation):
        """Valida un código QR de cupón"""
        try:
            result = RewardService.validate_coupon_qr(qr_data.qr_token, qr_data.business_id)
            
            if result["valid"]:
                return {
                    "success": True,
                    "message": result["message"],
                    "data": result["coupon"]
                }
            else:
                raise HTTPException(status_code=400, detail=result["error"])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")