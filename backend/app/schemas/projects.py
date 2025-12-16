from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    project_id: UUID
    assigned_to: Optional[UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
