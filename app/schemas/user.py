from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserProfileResponse(BaseModel):
    id: int
    nombre: str
    email: Optional[EmailStr]
    telefono: Optional[str]
    municipality_id: Optional[int]
    municipio: Optional[str]
    avatar: Optional[str]
    created_at: datetime

class UserProfileUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    municipality_id: Optional[int] = None
    avatar: Optional[str] = None

class VisitCreate(BaseModel):
    business_id: int
    user_id: int
    visit_date: datetime

class QRValidation(BaseModel):
    qr_token: str
    business_id: int