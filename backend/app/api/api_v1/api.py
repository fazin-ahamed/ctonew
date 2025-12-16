from fastapi import APIRouter
from app.api.api_v1.endpoints import tenants, crm

api_router = APIRouter()
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(crm.router, prefix="/crm", tags=["crm"])
