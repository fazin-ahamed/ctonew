from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: Optional[str] = None
    status: str = "new"

class LeadCreate(LeadBase):
    pass

class LeadRead(LeadBase):
    id: UUID
    tenant_id: UUID
    
    class Config:
        from_attributes = True
