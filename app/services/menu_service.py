from app.models.business_menu import BusinessMenu
from app.utils.logger import log_info

class MenuService:
    @staticmethod
    def get_business_menu(business_id: int):
        log_info(f"Obteniendo menú del negocio: {business_id}")
        return BusinessMenu.get_by_business_id(business_id)