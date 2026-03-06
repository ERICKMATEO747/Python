from app.models.business import Business
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
        return Business.update_profile(business_id, profile_data)