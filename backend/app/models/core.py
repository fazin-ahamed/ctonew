from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import uuid

class Tenant(Base):
    __tablename__ = "tenant"
    
    name: Mapped[str] = mapped_column(String, index=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    plan: Mapped[str] = mapped_column(String, default="free")
    
    # Relationships
    members: Mapped[list["TenantUser"]] = relationship("TenantUser", back_populates="tenant", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "user"
    
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    supabase_id: Mapped[str] = mapped_column(String, unique=True, index=True) # Link to Supabase Auth
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    tenants: Mapped[list["TenantUser"]] = relationship("TenantUser", back_populates="user")

class TenantUser(Base):
    __tablename__ = "tenant_user"
    
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    role: Mapped[str] = mapped_column(String, default="member") # owner, admin, member
    
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="tenants")
