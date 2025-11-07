from app.models.business import Business
from app.utils.logger import log_info

class BusinessService:
    @staticmethod
    def get_all_businesses():
        log_info("Obteniendo todos los negocios")
        return Business.get_all()
    
    @staticmethod
    def get_business_by_id(business_id: int):
        log_info(f"Obteniendo negocio con ID: {business_id}")
        return Business.get_by_id(business_id)