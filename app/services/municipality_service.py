from app.models.municipality import Municipality
from app.utils.logger import log_info

class MunicipalityService:
    @staticmethod
    def get_all_municipalities():
        log_info("Obteniendo todos los municipios")
        return Municipality.get_all()