from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.config import settings
from jose import jwt, JWTError
from app.models.core import User, TenantUser
from sqlalchemy import select

security = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token.credentials, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    
    # Fetch user from DB
    result = await db.execute(select(User).where(User.supabase_id == user_id))
    user = result.scalars().first()
    
    if not user:
        # Auto-create user if missing (optional, or throw 401)
        # For strictness, usually we wait for a webhook to create the user, but for now throw error
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    return user

async def get_current_tenant(
    x_tenant_id: str = Header(..., alias="X-Tenant-ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> str:
    # Verify user belongs to tenant
    # We accept UUID string as header
    try:
        from uuid import UUID
        tenant_uuid = UUID(x_tenant_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Tenant ID format")

    result = await db.execute(
        select(TenantUser).where(
            TenantUser.user_id == current_user.id,
            TenantUser.tenant_id == tenant_uuid
        )
    )
    membership = result.scalars().first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this tenant")
    
    return str(tenant_uuid)
