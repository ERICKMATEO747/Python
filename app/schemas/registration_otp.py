from pydantic import BaseModel, EmailStr

class RegistrationOTPRequest(BaseModel):
    """Schema para solicitar código OTP de registro"""
    email: EmailStr