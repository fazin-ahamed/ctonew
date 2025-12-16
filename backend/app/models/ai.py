from sqlalchemy import String, Integer, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from app.db.base_class import Base
from app.models.mixins import TenantMixin

class AIRequestLog(Base, TenantMixin):
    __tablename__ = "ai_request_log"
    
    provider: Mapped[str] = mapped_column(String) # openai, anthropic
    model: Mapped[str] = mapped_column(String)
    prompt_tokens: Mapped[int] = mapped_column(Integer)
    completion_tokens: Mapped[int] = mapped_column(Integer)
    cost: Mapped[float] = mapped_column(Float)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=True) # avoiding reserved word

class AIMemory(Base, TenantMixin):
    __tablename__ = "ai_memory"
    
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Vector] = mapped_column(Vector(1536)) # OpenAI embedding size usually
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=True)

class PromptTemplate(Base, TenantMixin):
    __tablename__ = "ai_prompt_template"
    
    name: Mapped[str] = mapped_column(String)
    template: Mapped[str] = mapped_column(Text)
    input_variables: Mapped[list[str]] = mapped_column(JSON) # e.g. ["customer_name", "topic"]
    model_config_data: Mapped[dict] = mapped_column(JSON, nullable=True) # e.g. {"temperature": 0.7}
