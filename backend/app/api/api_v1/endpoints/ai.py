from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.ai import PromptTemplate
from app.schemas.ai import PromptTemplateCreate, PromptTemplateRead, AICompletionRequest
from app.db.session import get_db
from app.services.ai_gateway import AIGateway

router = APIRouter()

@router.get("/templates", response_model=List[PromptTemplateRead])
async def read_templates(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(PromptTemplate).where(PromptTemplate.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/templates", response_model=PromptTemplateRead)
async def create_template(
    template_in: PromptTemplateCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    template = PromptTemplate(**template_in.model_dump(), tenant_id=tenant_id)
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template

@router.post("/completion")
async def generate_completion(
    request: AICompletionRequest,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    
    gateway = AIGateway(tenant_id=tenant_id, db=db)
    response = await gateway.chat_completion(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return {"content": response}
