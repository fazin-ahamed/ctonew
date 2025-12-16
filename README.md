# Business OS

A comprehensive AI-native SaaS platform.

## Architecture

- **Frontend**: React, Vite, TailwindCSS, Zustand
- **Backend**: FastAPI, SQLAlchemy (Async), Alembic, Celery
- **Database**: PostgreSQL with pgvector
- **Auth**: Supabase Auth

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend dev outside docker)
- Python 3.11+ (for local backend dev outside docker)

### Running Locally

1. Clone the repo
2. Copy environment variables:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```
3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The API will be available at http://localhost:8000
The Frontend will be available at http://localhost:5173

### Database Migrations

To run migrations:

```bash
docker-compose exec backend alembic upgrade head
```

## Modules

- Core (Tenants, Users, RBAC)
- CRM
- Finance
- HRM
- Projects
- Support
- Automation (Workflow Engine)
- AI Gateway

## Deployment

### Railway (Backend)

1. Connect GitHub repo to Railway.
2. Add PostgreSQL and Redis plugins.
3. Set environment variables.
4. Deploy `backend` directory.

### Vercel / Cloudflare Pages (Frontend)

1. Connect GitHub repo.
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Set environment variables.
