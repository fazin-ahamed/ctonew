from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = False
    trigger_type: str
    definition: Dict[str, Any]

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowRead(WorkflowBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
