from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.mixins import TenantMixin
import uuid

class Ticket(Base, TenantMixin):
    __tablename__ = "support_ticket"
    
    subject: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="open") # open, in_progress, closed
    priority: Mapped[str] = mapped_column(String, default="medium")
    customer_email: Mapped[str] = mapped_column(String)
    assigned_to: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True) # User ID
