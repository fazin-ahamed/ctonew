from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID

class PromptTemplateBase(BaseModel):
    name: str
    template: str
    input_variables: List[str]
    model_config_data: Optional[Dict[str, Any]] = None

class PromptTemplateCreate(PromptTemplateBase):
    pass

class PromptTemplateRead(PromptTemplateBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True

class AICompletionRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
