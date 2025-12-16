# Business OS

**Business OS** is an AI-native, modular, multi-tenant operating system for businesses. It unifies CRM, HRM, Finance, Projects, Support, Automation, and AI workflows into a single platform.

> **Note:** This repository contains the initial System Design and Product Requirements.

## 📚 Documentation

Detailed documentation is available in [PRD_AND_SYSTEM_DESIGN.md](./PRD_AND_SYSTEM_DESIGN.md).

It covers:
- Product Vision & Scope
- Functional Requirements (CRM, HRM, Finance, etc.)
- System Architecture (FastAPI, React, PostgreSQL + pgvector)
- Database Design (RLS, Multi-tenancy)
- Backend & Frontend Architecture
- Security & Deployment Strategy

## 🚀 Technology Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS, shadcn/ui
- **Backend:** FastAPI, SQLAlchemy (Async), Celery
- **Database:** PostgreSQL (with pgvector), Redis
- **Auth:** Supabase Auth
- **Infrastructure:** Railway (Backend/DB), Cloudflare R2 (Storage)

## 🏗 Project Structure (Planned)

The project will follow a monorepo-style structure:

```
/
├── backend/            # FastAPI application
├── frontend/           # React application
└── PRD_AND_SYSTEM_DESIGN.md
```

Please refer to the detailed design document for the implementation roadmap.
