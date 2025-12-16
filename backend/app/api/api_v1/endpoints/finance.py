from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.finance import Invoice, Expense
from app.schemas.finance import InvoiceCreate, InvoiceRead, ExpenseCreate, ExpenseRead
from app.db.session import get_db

router = APIRouter()

@router.get("/invoices", response_model=List[InvoiceRead])
async def read_invoices(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Invoice).where(Invoice.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/invoices", response_model=InvoiceRead)
async def create_invoice(
    invoice_in: InvoiceCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    invoice = Invoice(**invoice_in.model_dump(), tenant_id=tenant_id)
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice

@router.get("/expenses", response_model=List[ExpenseRead])
async def read_expenses(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Expense).where(Expense.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/expenses", response_model=ExpenseRead)
async def create_expense(
    expense_in: ExpenseCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    expense = Expense(**expense_in.model_dump(), tenant_id=tenant_id)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense
