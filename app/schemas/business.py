from pydantic import BaseModel, Field
from typing import Optional, List, Union
from decimal import Decimal

class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    available: bool = Field(default=True)
    image_url: Optional[str] = Field(None, max_length=500)

class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    available: Optional[bool] = None
    image_url: Optional[str] = Field(None, max_length=500)

class LoyaltyConfigUpdate(BaseModel):
    visits_per_round: Optional[int] = Field(None, ge=1, le=50)
    daily_reward_limit: Optional[int] = Field(None, ge=0, le=100)
    program_active: Optional[bool] = None
    auto_generate_rewards: Optional[bool] = None
    reward_expiry_days: Optional[int] = Field(None, ge=1, le=365)

class BusinessSettingsUpdate(BaseModel):
    visits_for_prize: Optional[int] = Field(None, ge=1, le=50)
    max_daily_rewards: Optional[int] = Field(None, ge=0, le=100)
    loyalty_program_active: Optional[bool] = None
    reward_generation_enabled: Optional[bool] = None

class QRValidation(BaseModel):
    qr_token: str = Field(..., min_length=1)
    business_id: int = Field(..., gt=0)

class BusinessProfileUpdate(BaseModel):
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=200)
    facebook: Optional[str] = Field(None, max_length=200)
    instagram: Optional[str] = Field(None, max_length=200)
    whatsapp: Optional[str] = Field(None, max_length=20)
    payment_methods: Optional[Union[str, List[str]]] = None
    delivery_options: Optional[Union[str, List[str]]] = None
    image_url: Optional[str] = Field(None, max_length=500)
    logo: Optional[str] = Field(None, max_length=500)
    opening_hours: Optional[Union[str, dict]] = None
    working_days: Optional[Union[str, List[str]]] = None