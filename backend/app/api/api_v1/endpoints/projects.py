from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.projects import Project, Task
from app.schemas.projects import ProjectCreate, ProjectRead, TaskCreate, TaskRead
from app.db.session import get_db

router = APIRouter()

@router.get("/projects", response_model=List[ProjectRead])
async def read_projects(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Project).where(Project.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/projects", response_model=ProjectRead)
async def create_project(
    project_in: ProjectCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    project = Project(**project_in.model_dump(), tenant_id=tenant_id)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.get("/tasks", response_model=List[TaskRead])
async def read_tasks(
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    query = select(Task).where(Task.tenant_id == tenant_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/tasks", response_model=TaskRead)
async def create_task(
    task_in: TaskCreate,
    current_tenant_id: str = Depends(deps.get_current_tenant),
    db: AsyncSession = Depends(get_db),
):
    from uuid import UUID
    tenant_id = UUID(current_tenant_id)
    task = Task(**task_in.model_dump(), tenant_id=tenant_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
