from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import date

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    position: str
    department: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True

class LeaveBase(BaseModel):
    employee_id: UUID
    start_date: date
    end_date: date
    reason: str
    status: str = "pending"

class LeaveCreate(LeaveBase):
    pass

class LeaveRead(LeaveBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
