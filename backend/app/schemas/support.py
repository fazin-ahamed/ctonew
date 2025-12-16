from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TicketBase(BaseModel):
    subject: str
    description: str
    status: str = "open"
    priority: str = "medium"
    customer_email: str
    assigned_to: Optional[UUID] = None

class TicketCreate(TicketBase):
    pass

class TicketRead(TicketBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
