from typing import List, Optional
import openai
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ai import AIRequestLog
from app.models.mixins import TenantMixin
import uuid

class AIGateway:
    def __init__(self, tenant_id: uuid.UUID, db: AsyncSession):
        self.tenant_id = tenant_id
        self.db = db
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def chat_completion(self, messages: List[dict], model: str = "gpt-3.5-turbo"):
        # TODO: Check limits/quotas for tenant
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        # Track usage
        usage = response.usage
        log = AIRequestLog(
            tenant_id=self.tenant_id,
            provider="openai",
            model=model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            cost=0.0, # Calculate based on pricing
            metadata_={"response_id": response.id}
        )
        self.db.add(log)
        await self.db.commit()
        
        return response.choices[0].message.content

    async def create_embedding(self, text: str):
        response = await self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
