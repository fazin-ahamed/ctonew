from sqlalchemy import String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.mixins import TenantMixin
import uuid

class Workflow(Base, TenantMixin):
    __tablename__ = "automation_workflow"
    
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    trigger_type: Mapped[str] = mapped_column(String) # webhook, schedule, event
    definition: Mapped[dict] = mapped_column(JSON) # The visual graph data
    
    executions: Mapped[list["WorkflowExecution"]] = relationship("WorkflowExecution", back_populates="workflow")

class WorkflowExecution(Base, TenantMixin):
    __tablename__ = "automation_execution"
    
    workflow_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("automation_workflow.id"))
    status: Mapped[str] = mapped_column(String) # pending, running, completed, failed
    logs: Mapped[dict] = mapped_column(JSON, nullable=True)
    result: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="executions")
