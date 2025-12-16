from sqlalchemy import String, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.mixins import TenantMixin
import uuid
import enum

class DealStage(str, enum.Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"

class Lead(Base, TenantMixin):
    __tablename__ = "crm_lead"
    
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    company: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="new")
    source: Mapped[str] = mapped_column(String, nullable=True)
    
    deals: Mapped[list["Deal"]] = relationship("Deal", back_populates="lead")

class Deal(Base, TenantMixin):
    __tablename__ = "crm_deal"
    
    title: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float, default=0.0)
    stage: Mapped[DealStage] = mapped_column(String, default=DealStage.NEW)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("crm_lead.id"), nullable=True)
    
    lead: Mapped["Lead"] = relationship("Lead", back_populates="deals")
    activities: Mapped[list["Activity"]] = relationship("Activity", back_populates="deal")

class Activity(Base, TenantMixin):
    __tablename__ = "crm_activity"
    
    type: Mapped[str] = mapped_column(String) # call, email, meeting
    summary: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    deal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("crm_deal.id"), nullable=True)
    
    deal: Mapped["Deal"] = relationship("Deal", back_populates="activities")
