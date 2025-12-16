from sqlalchemy import String, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from app.models.mixins import TenantMixin
import uuid
import datetime

class Invoice(Base, TenantMixin):
    __tablename__ = "finance_invoice"
    
    customer_name: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="draft") # draft, sent, paid, overdue
    due_date: Mapped[datetime.date] = mapped_column(Date)

class Expense(Base, TenantMixin):
    __tablename__ = "finance_expense"
    
    category: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date)

class Payroll(Base, TenantMixin):
    __tablename__ = "finance_payroll"
    
    employee_name: Mapped[str] = mapped_column(String)
    salary: Mapped[float] = mapped_column(Float)
    pay_date: Mapped[datetime.date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, paid
