from sqlalchemy import String, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.mixins import TenantMixin
import uuid
import datetime

class Project(Base, TenantMixin):
    __tablename__ = "project_project"
    
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")
    milestones: Mapped[list["Milestone"]] = relationship("Milestone", back_populates="project")

class Task(Base, TenantMixin):
    __tablename__ = "project_task"
    
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="todo") # todo, in_progress, done
    priority: Mapped[str] = mapped_column(String, default="medium")
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project_project.id"))
    assigned_to: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True) # User ID
    
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

class Milestone(Base, TenantMixin):
    __tablename__ = "project_milestone"
    
    name: Mapped[str] = mapped_column(String)
    due_date: Mapped[datetime.date] = mapped_column(Date)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project_project.id"))
    
    project: Mapped["Project"] = relationship("Project", back_populates="milestones")
