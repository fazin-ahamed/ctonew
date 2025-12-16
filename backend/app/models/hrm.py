from sqlalchemy import String, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.mixins import TenantMixin
import uuid
import datetime

class Employee(Base, TenantMixin):
    __tablename__ = "hrm_employee"
    
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    position: Mapped[str] = mapped_column(String)
    department: Mapped[str] = mapped_column(String, nullable=True)
    
    attendance: Mapped[list["Attendance"]] = relationship("Attendance", back_populates="employee")
    leaves: Mapped[list["Leave"]] = relationship("Leave", back_populates="employee")

class Attendance(Base, TenantMixin):
    __tablename__ = "hrm_attendance"
    
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("hrm_employee.id"))
    check_in: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    check_out: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    employee: Mapped["Employee"] = relationship("Employee", back_populates="attendance")

class Leave(Base, TenantMixin):
    __tablename__ = "hrm_leave"
    
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("hrm_employee.id"))
    start_date: Mapped[datetime.date] = mapped_column(Date)
    end_date: Mapped[datetime.date] = mapped_column(Date)
    reason: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, approved, rejected
    
    employee: Mapped["Employee"] = relationship("Employee", back_populates="leaves")
