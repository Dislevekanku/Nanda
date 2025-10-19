# MedSpa Agent

MedSpa Agent is a FastAPI-based backend that powers an automated concierge for medical spas. The Week 1 milestone assembles the core infrastructure for database, API, integrations, and LLM scaffolding.

## Features

- **Dockerized stack** with FastAPI app, Postgres (pgvector), and Redis services.
- **SQLAlchemy models** with Alembic migrations for accounts, staff, services, clients, appointments, conversations, messages, and automation events.
- **Seed data** for Glow MedSpa with providers, services, and clients.
- **Authenticated API skeleton** featuring routers for auth, clients, appointments, conversations, automations, and services.
- **Integration stubs** for Google Calendar, Stripe, and Twilio to prepare future tooling.
- **Conversation state machine** to track agent progress.
- **LLM helper layer** with intent parsing and tool registry.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11 (for local development without Docker)

### Setup

1. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

2. Start the stack:

   ```bash
   docker compose up --build
   ```

3. Apply database migrations:

   ```bash
   docker compose exec app alembic upgrade head
   ```

4. Seed demo data:

   ```bash
   docker compose exec db psql -U postgres -d medspa -f /code/seed_data.sql
   ```

5. Access the API at `http://localhost:8000`. Interactive docs are available at `/docs`.

### Running Locally Without Docker

1. Install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set environment variables (see `.env.example`).

3. Run the server:

   ```bash
   uvicorn app.main:app --reload
   ```

### Database Migrations

Generate a new migration:

```bash
alembic revision --autogenerate -m "short description"
```

Apply migrations:

```bash
alembic upgrade head
```

### Testing

Run unit tests:

```bash
pytest
```

## Project Structure

```
app/
  api/                # FastAPI routers
  core/               # Settings and security
  db/                 # SQLAlchemy models and sessions
  integrations/       # External service stubs
  services/           # Tool interface layer
  state_machine.py    # Conversation state machine
  llm_agent.py        # LLM helper functions
alembic/              # Migration configuration and scripts
seed_data.sql         # Demo data
rls_policies.sql      # RLS policy examples
```

## Next Steps (Week 2 Preview)

- Connect the LLM agent to real tool calls and Supabase functions.
- Expand test coverage for API routes and RLS policies.
- Implement background jobs via Redis queues.
- Deploy the stack to a staging environment (Railway, Fly.io, or Vercel Edge + Supabase DB).
