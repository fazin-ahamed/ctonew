from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID

class TenantBase(BaseModel):
    name: str
    slug: str
    plan: str = "free"

class TenantCreate(TenantBase):
    pass

class TenantRead(TenantBase):
    id: UUID
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    supabase_id: str

class UserRead(UserBase):
    id: UUID
    supabase_id: str
    
    class Config:
        from_attributes = True
