from app.models.business_sqlite import Business
from typing import List, Dict, Optional

class BusinessService:
    @staticmethod
    def get_all_businesses(user_id: int = None) -> List[Dict]:
        return Business.get_all(user_id)
    
    @staticmethod
    def get_business_by_id(business_id: int, user_id: int = None) -> Optional[Dict]:
        return Business.get_by_id(business_id, user_id)
    
    @staticmethod
    def get_business_profile(business_id: int) -> Optional[Dict]:
        return Business.get_by_id(business_id)
    
    @staticmethod
    def update_business_profile(business_id: int, profile_data: Dict) -> bool:
        # Implementación básica - en una app real actualizaría la BD
        return True