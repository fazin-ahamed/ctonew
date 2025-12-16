# Business OS - Product Requirements Document & System Design

**Version:** 1.0.0
**Status:** DRAFT
**Date:** October 26, 2023

---

## 1. Product Vision

**Business OS** is an AI-native, modular, multi-tenant operating system for businesses that unifies CRM, HRM, Finance, Projects, Support, Automation, and AI workflows into a single platform. It aims to replace fragmented tools like Zoho, HubSpot, Notion, Slack, QuickBooks, and Zapier with one unified workspace where AI is embedded into every workflow, not added as an afterthought.

### Core Goals
- **Unified Workspace:** Single pane of glass for all business operations.
- **AI-Native:** AI embedded in every module (summaries, generation, decision making).
- **Enterprise-Grade Security:** Strong tenant isolation via RLS, encryption, and RBAC.
- **Modular Architecture:** Businesses enable only what they need.
- **Free-First:** Low operational cost allowing a generous free tier.

---

## 2. Target Users

1.  **Freelancers & Solo Founders:** Need an all-in-one tool to manage their entire business without context switching.
2.  **Startups & SMBs:** Need scalable tools that grow with them without breaking the bank.
3.  **Enterprises:** Require strict RBAC, audit logs, and departmental separation.
4.  **Developers:** Build extensions and integrations on top of the API/Workflow engine.

---

## 3. Functional Requirements

### 3.1. Core Platform
The foundation of the system.
- **Multi-Tenancy:** Strict data isolation per tenant.
- **Authentication:** Email/Password, Social Auth via Supabase.
- **User Management:** Invite flows, profile management.
- **RBAC:** Granular permissions (Role-Based Access Control) definable per tenant.
- **Audit Logs:** Immutable logs for all sensitive actions (login, delete, export).
- **Feature Flags:** Enable/disable modules per tenant.

### 3.2. CRM Module
- **Leads & Contacts:** Management with AI enrichment.
- **Deals & Pipelines:** Drag-and-drop Kanban view.
- **Activities:** Call logs, emails, meetings.
- **AI Features:** Meeting summaries, email drafting, lead scoring.

### 3.3. Finance Module
- **Invoicing:** Creation, PDF generation, tracking.
- **Expenses:** Receipt scanning (AI), approval workflows.
- **Payroll (Basic):** Employee salary records and processing status.
- **Reports:** P&L, Cash Flow (generated via SQL aggregation).

### 3.4. HRM Module
- **Employee Directory:** Profiles, documents.
- **Attendance:** Check-in/out, timesheets.
- **Leave Management:** Request/Approval workflows.
- **AI Features:** Performance review summaries, policy Q&A.

### 3.5. Projects Module
- **Task Management:** List, Board, Calendar views.
- **Milestones:** Project tracking.
- **Collaboration:** Comments, mentions.
- **AI Features:** Subtask generation, project risk analysis.

### 3.6. Support Module
- **Ticketing:** Email-to-ticket, portal submission.
- **SLA Tracking:** Timers and breach alerts.
- **AI Features:** Suggested replies, ticket summarization, sentiment analysis.

### 3.7. Automation / Workflow Engine
A visual builder to glue everything together.
- **Triggers:** Webhook, Schedule, Event (e.g., "New Lead").
- **Actions:** CRUD operations, Email, Slack, Internal Notification.
- **Logic:** If/Else, Loop.
- **AI Nodes:** "Generate Text", "Analyze Sentiment".

### 3.8. AI Gateway
- **BYOK (Bring Your Own Key):** Tenants provide their own API keys for OpenAI, Anthropic, etc.
- **Provider Switching:** Abstraction layer to switch models easily.
- **Usage Tracking:** Token counting and cost estimation per tenant.
- **Memory:** Vector database (pgvector) to store and retrieve context.

---

## 4. Non-Functional Requirements

- **Performance:** API response time < 200ms for P95.
- **Scalability:** Horizontal scaling for API and Workers.
- **Security:** Zero-trust architecture between frontend and backend.
- **Reliability:** 99.9% Uptime target.
- **Compliance:** GDPR ready (Data export/delete), Audit trails.

---

## 5. System Architecture

### 5.1. High-Level Architecture

```mermaid
graph TD
    User[User / Browser] -->|HTTPS| CDN[Cloudflare / Vercel]
    CDN --> FE[Frontend SPA (React/Vite)]
    
    FE -->|API Calls| API[Backend API (FastAPI)]
    
    subgraph "Infrastructure (Railway)"
        API -->|Auth| Supabase[Supabase Auth]
        API -->|Read/Write| DB[(PostgreSQL + pgvector)]
        API -->|Async Tasks| Redis[Redis Queue]
        
        Worker[Celery Workers] -->|Pop Tasks| Redis
        Worker -->|Update| DB
        Worker -->|AI Calls| LLM[LLM Providers (OpenAI/Anthropic)]
    end
    
    subgraph "Storage"
        API -->|Files| R2[Cloudflare R2]
    end
```

### 5.2. Tech Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React, TypeScript, Vite, TailwindCSS, shadcn/ui, Zustand | Modern, type-safe, fast, accessible UI components. |
| **Backend** | FastAPI (Python), SQLAlchemy 2.0 (Async) | High performance, native async support, excellent ecosystem for AI/Data. |
| **Database** | PostgreSQL, pgvector | Robust relational data + vector search in one engine. RLS for security. |
| **Auth** | Supabase Auth | Managed authentication handling (JWT), secure. |
| **Queue** | Celery + Redis | Robust background task processing (emails, AI jobs). |
| **Migrations** | Alembic | Standard for Python/SQLAlchemy. |
| **Infrastructure** | Railway.app, Cloudflare R2 | Cost-effective, simple deployment, scales from zero. |

---

## 6. Database Design & Security

### 6.1. Tenant Isolation Strategy
**Row Level Security (RLS)** is the primary mechanism.
- Every table (except system catalogs) **MUST** have a `tenant_id` column.
- The `tenant_id` is a Foreign Key to a `tenants` table.
- RLS Policies enforce that a user can only select/insert/update/delete rows where `tenant_id` matches their session's `tenant_id`.
- **Bypass:** Only Super Admin or specific background system jobs can bypass RLS.

### 6.2. Schema Overview (Key Tables)

- `tenants`: Stores organization details.
- `users`: Stores user profiles, links to `auth.users` (Supabase).
- `roles`: Definition of roles (Admin, Member, etc.) per tenant.
- `permissions`: Granular capabilities linked to roles.
- `crm_leads`, `crm_deals`: CRM data.
- `fin_invoices`, `fin_expenses`: Finance data.
- `tasks`, `projects`: Project management.
- `workflows`, `workflow_executions`: Automation engine.
- `ai_conversations`, `ai_messages`: Chat history.
- `embeddings`: Vector storage for RAG.

### 6.3. SQLAlchemy Base Model & Mixins

```python
# app/core/database.py
from sqlalchemy import Column, String, DateTime, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

class TenantMixin:
    @declared_attr
    def tenant_id(cls):
        return mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

### 6.4. RLS Policy Example (SQL)

```sql
-- Enable RLS
ALTER TABLE crm_leads ENABLE ROW LEVEL SECURITY;

-- Create Policy
CREATE POLICY tenant_isolation_policy ON crm_leads
    USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Note: The backend middleware must set 'app.current_tenant' for every request.
```

---

## 7. Backend Architecture

### 7.1. Folder Structure

```
backend/
├── alembic/                # Database migrations
├── app/
│   ├── api/
│   │   ├── v1/             # API Version 1
│   │   │   ├── endpoints/  # Route handlers grouped by module
│   │   │   └── router.py   # Main router
│   │   └── deps.py         # Dependencies (DB session, Current User)
│   ├── core/
│   │   ├── config.py       # Environment variables
│   │   ├── security.py     # JWT handling, Password hashing
│   │   ├── database.py     # DB connection & Session factory
│   │   └── events.py       # Startup/Shutdown events
│   ├── models/             # SQLAlchemy Models (Domain Driven)
│   │   ├── core.py         # User, Tenant, Role
│   │   ├── crm.py
│   │   ├── finance.py
│   │   └── ...
│   ├── schemas/            # Pydantic Models (Request/Response)
│   │   ├── core.py
│   │   └── ...
│   ├── services/           # Business Logic Layer
│   │   ├── auth_service.py
│   │   ├── ai_service.py
│   │   └── ...
│   ├── workers/            # Celery Tasks
│   │   ├── celery_app.py
│   │   └── tasks.py
│   └── main.py             # FastAPI Entrypoint
├── tests/
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

### 7.2. Authentication & RBAC Middleware

The middleware intercepts every request, validates the JWT, extracts the `tenant_id`, and sets it in the DB session/context for RLS.

```python
# app/api/deps.py (Simplified)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = verify_jwt(token)
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    
    # Set RLS context for this session
    await db.execute(text(f"set app.current_tenant = '{tenant_id}'"))
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_permission(permission: str):
    def dependency(user: User = Depends(get_current_user)):
        if permission not in user.role.permissions:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return dependency
```

### 7.3. Background Jobs (Celery)
Used for heavy lifting:
- Sending emails.
- Processing large file imports.
- Running long AI chains.
- Aggregating analytics.

---

## 8. Frontend Architecture

### 8.1. Folder Structure

```
frontend/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── ui/             # Generic UI components (shadcn/ui)
│   │   ├── layout/         # Shell, Sidebar, Navbar
│   │   └── shared/         # Reusable app components
│   ├── features/           # Modular feature organization
│   │   ├── auth/
│   │   ├── crm/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── store/
│   │   ├── finance/
│   │   └── workflows/
│   ├── hooks/              # Global hooks
│   ├── lib/                # Utilities (axios, cn, formatters)
│   ├── pages/              # Route components
│   ├── store/              # Global state (Zustand)
│   └── types/              # TypeScript definitions
├── index.html
├── tailwind.config.js
└── vite.config.ts
```

### 8.2. UI/UX Principles
- **Sidebar Navigation:** Context-aware sidebar that changes based on the active module.
- **Data Tables:** Robust tables with filtering, sorting, pagination, and bulk actions (TanStack Table).
- **Forms:** React Hook Form + Zod for validation.
- **Optimistic Updates:** UI updates immediately before API confirms (using React Query / TanStack Query).

---

## 9. Automation Engine Design

The workflow engine allows users to build logic visually.

### 9.1. Data Model

```python
class Workflow(Base, TenantMixin, UUIDMixin, TimestampMixin):
    __tablename__ = "workflows"
    name: Mapped[str]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    trigger_type: Mapped[str] # e.g., 'webhook', 'schedule', 'event'
    trigger_config: Mapped[dict] # JSONB
    nodes: Mapped[list[dict]] # JSONB: Adjacency list or node definitions
    edges: Mapped[list[dict]] # JSONB: Connections

class WorkflowExecution(Base, TenantMixin, UUIDMixin, TimestampMixin):
    __tablename__ = "workflow_executions"
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workflows.id"))
    status: Mapped[str] # 'pending', 'running', 'completed', 'failed'
    logs: Mapped[dict] # JSONB: Step-by-step execution logs
```

### 9.2. Execution Logic
1.  **Trigger:** An event (API call, cron, DB hook) instantiates a `WorkflowExecution`.
2.  **Queue:** The execution ID is pushed to Redis.
3.  **Worker:** Celery worker picks up the job.
4.  **Traverse:** The worker traverses the graph defined in `nodes` and `edges`.
5.  **Execute:** For each node, it calls a specific handler (e.g., `send_email(context)`).
6.  **Context:** Data flows from node to node via a context dictionary.

---

## 10. AI Gateway Design

### 10.1. Adapter Pattern
To support multiple providers (OpenAI, Anthropic, etc.) without code changes.

```python
class AIProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def generate_embedding(self, text: str) -> list[float]:
        pass

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    # ... implementation

class AnthropicProvider(AIProvider):
    # ... implementation

class AIGateway:
    def get_provider(self, tenant_config) -> AIProvider:
        if tenant_config.provider == 'openai':
            return OpenAIProvider(tenant_config.api_key)
        # ...
```

### 10.2. Memory (RAG)
1.  User query comes in.
2.  Generate embedding for query.
3.  Search `embeddings` table (pgvector) for relevant documents within `tenant_id`.
4.  Inject relevant chunks into System Prompt.
5.  Send to LLM.

---

## 11. Infrastructure & Deployment

### 11.1. Railway Setup
- **Service 1: Backend API** (FastAPI) - Scaled based on CPU/RAM.
- **Service 2: Celery Worker** (Python) - Scaled based on Queue depth.
- **Service 3: Postgres** - Managed DB with pgvector extension.
- **Service 4: Redis** - For Celery broker and result backend.

### 11.2. CI/CD
- **GitHub Actions:**
    - On Push: Run Linter (Ruff), Tests (Pytest).
    - On Merge to Main: Build Docker image, Push to Registry, Trigger Railway Deploy.

### 11.3. Environment Variables
- `DATABASE_URL`
- `REDIS_URL`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `OPENAI_API_KEY` (Global fallback, though tenants bring their own)
- `SECRET_KEY` (For JWT signing if not using Supabase solely)

---

## 12. Security & Compliance

### 12.1. Security Layers
1.  **Transport:** TLS 1.3 everywhere.
2.  **Edge:** Cloudflare WAF (DDoS protection, rate limiting).
3.  **Application:** Input validation (Pydantic), Authorization (RBAC).
4.  **Database:** RLS (Tenant Isolation), Encryption at rest (AES-256).

### 12.2. Compliance
- **GDPR:** "Right to be Forgotten" - cascading deletes for a tenant's data.
- **Audit:** All sensitive writes go to `audit_logs` table.

