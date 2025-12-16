from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.hrm import Employee, Leave
from app.schemas.hrm import EmployeeCreate, EmployeeRead, LeaveCreate, LeaveRead
from app.db.session import get_db

router = APIRouter()

@router.get("/employees", response_model=List[EmployeeRead])
async def read_employees(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Employee).where(Employee.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/employees", response_model=EmployeeRead)
async def create_employee(
    employee_in: EmployeeCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    employee = Employee(**employee_in.model_dump(), tenant_id=tenant_id)
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return employee

@router.get("/leaves", response_model=List[LeaveRead])
async def read_leaves(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Leave).where(Leave.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/leaves", response_model=LeaveRead)
async def create_leave(
    leave_in: LeaveCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    leave = Leave(**leave_in.model_dump(), tenant_id=tenant_id)
    db.add(leave)
    await db.commit()
    await db.refresh(leave)
    return leave
