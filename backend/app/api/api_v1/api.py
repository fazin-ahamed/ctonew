from fastapi import APIRouter
from app.api.api_v1.endpoints import tenants, crm, finance, hrm, projects, support, automation, ai

api_router = APIRouter()
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(crm.router, prefix="/crm", tags=["crm"])
api_router.include_router(finance.router, prefix="/finance", tags=["finance"])
api_router.include_router(hrm.router, prefix="/hrm", tags=["hrm"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(support.router, prefix="/support", tags=["support"])
api_router.include_router(automation.router, prefix="/automation", tags=["automation"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
