from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusinessResponse(BaseModel):
    id: int
    name: str
    category: str
    address: Optional[str]
    municipality_id: Optional[int]
    municipio: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    logo: Optional[str]
    description: Optional[str]
    rating: Optional[float]
    facebook: Optional[str]
    instagram: Optional[str]
    tiktok: Optional[str]
    whatsapp: Optional[str]
    active: bool
    created_at: datetime