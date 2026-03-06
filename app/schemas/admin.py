from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class BusinessCreate(BaseModel):
    name: str
    category: str
    address: str
    municipality_id: Optional[int] = None
    phone: str
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    logo: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    whatsapp: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    working_days: Optional[List[str]] = None
    delivery_available: bool = False
    payment_methods: Optional[List[str]] = None
    visits_for_prize: int = 6
    owner_email: EmailStr  # Email del propietario
    
    @validator('municipality_id', pre=True)
    def empty_str_to_none_int(cls, v):
        if v == "" or v is None:
            return None
        return v
    
    @validator('email', pre=True)
    def empty_str_to_none_email(cls, v):
        if v == "":
            return None
        return v

class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    municipality_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    logo: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    whatsapp: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    working_days: Optional[List[str]] = None
    delivery_available: Optional[bool] = None
    payment_methods: Optional[List[str]] = None
    visits_for_prize: Optional[int] = None
    active: Optional[bool] = None

class UserCreate(BaseModel):
    nombre: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    password: str
    user_type: int = 1  # 1=cliente, 2=negocio, 3=admin
    
    @validator('user_type')
    def validate_user_type(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('user_type debe ser 1 (cliente), 2 (negocio) o 3 (admin)')
        return v

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    user_type: Optional[int] = None
    active: Optional[bool] = None
    
    @validator('user_type')
    def validate_user_type(cls, v):
        if v is not None and v not in [1, 2, 3]:
            raise ValueError('user_type debe ser 1 (cliente), 2 (negocio) o 3 (admin)')
        return v

class AdminDashboardFilters(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    municipality_id: Optional[int] = None
    category: Optional[str] = None
    
    @validator('start_date', 'end_date', 'category', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v
    
    @validator('municipality_id', pre=True)
    def empty_str_to_none_int(cls, v):
        if v == "" or v is None:
            return None
        return v