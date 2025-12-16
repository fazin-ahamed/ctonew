from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.automation import Workflow
from app.schemas.automation import WorkflowCreate, WorkflowRead
from app.db.session import get_db

router = APIRouter()

@router.get("/workflows", response_model=List[WorkflowRead])
async def read_workflows(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Workflow).where(Workflow.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/workflows", response_model=WorkflowRead)
async def create_workflow(
    workflow_in: WorkflowCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    workflow = Workflow(**workflow_in.model_dump(), tenant_id=tenant_id)
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return workflow
