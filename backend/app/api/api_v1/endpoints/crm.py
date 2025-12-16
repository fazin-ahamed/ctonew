from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.crm import Lead
from app.schemas.crm import LeadCreate, LeadRead
from app.db.session import get_db

router = APIRouter()

@router.get("/leads", response_model=List[LeadRead])
async def read_leads(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve leads for current tenant.
    """
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    
    query = select(Lead).where(Lead.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/leads", response_model=LeadRead)
async def create_lead(
    lead_in: LeadCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Create new lead.
    """
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    
    lead = Lead(**lead_in.model_dump(), tenant_id=tenant_id)
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    
    return lead
