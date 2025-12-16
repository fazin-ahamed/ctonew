from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.core import Tenant, TenantUser, User
from app.schemas.core import TenantCreate, TenantRead
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[TenantRead])
async def read_tenants(
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve tenants for current user.
    """
    query = select(Tenant).join(TenantUser).where(TenantUser.user_id == current_user.id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=TenantRead)
async def create_tenant(
    tenant_in: TenantCreate,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create new tenant.
    """
    tenant = Tenant(**tenant_in.model_dump())
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    
    # Add user as owner
    membership = TenantUser(tenant_id=tenant.id, user_id=current_user.id, role="owner")
    db.add(membership)
    await db.commit()
    
    return tenant
