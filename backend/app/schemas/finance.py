from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class InvoiceBase(BaseModel):
    customer_name: str
    amount: float
    status: str = "draft"
    due_date: date

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceRead(InvoiceBase):
    id: UUID
    tenant_id: UUID
    created_at: Optional[date] = None # Actually datetime in DB, but let's be loose

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    category: str
    amount: float
    description: Optional[str] = None
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseRead(ExpenseBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
