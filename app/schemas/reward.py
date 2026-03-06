from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RewardCreate(BaseModel):
    business_id: int
    title: str
    description: str
    terms_conditions: str
    validity_days: int = 30

class RewardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    terms_conditions: Optional[str] = None
    validity_days: Optional[int] = None
    is_active: Optional[bool] = None

class RewardResponse(BaseModel):
    id: int
    business_id: int
    title: str
    description: str
    terms_conditions: str
    validity_days: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class CouponGenerate(BaseModel):
    user_id: int
    business_id: int

class CouponClaim(BaseModel):
    coupon_id: int

class CouponRedeem(BaseModel):
    coupon_id: int

class CouponQRValidation(BaseModel):
    qr_token: str
    business_id: int

class UserRewardResponse(BaseModel):
    id: int
    user_id: int
    business_id: int
    reward_id: int
    coupon_code: str
    qr_code: str
    expires_at: datetime
    claimed_at: Optional[datetime] = None
    redeemed_at: Optional[datetime] = None
    status: str
    business_name: Optional[str] = None
    reward_title: Optional[str] = None
    reward_description: Optional[str] = None
    created_at: datetime