from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.support import Ticket
from app.schemas.support import TicketCreate, TicketRead
from app.db.session import get_db

router = APIRouter()

@router.get("/tickets", response_model=List[TicketRead])
async def read_tickets(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Ticket).where(Ticket.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/tickets", response_model=TicketRead)
async def create_ticket(
    ticket_in: TicketCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    ticket = Ticket(**ticket_in.model_dump(), tenant_id=tenant_id)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket
