# Architecture Overview

The MedSpa Agent backend is composed of modular layers that mirror Week 1 objectives.

## High-Level Diagram

```
┌────────────────────┐       ┌────────────────┐
│ FastAPI Routers    │◄──────│ Auth Middleware│
└────────┬───────────┘       └──────┬─────────┘
         │                            │
         ▼                            ▼
┌────────────────────┐       ┌────────────────┐
│ Service Layer      │──────►│ Integrations   │ (Calendar, Payments, SMS stubs)
└────────┬───────────┘       └────────────────┘
         │
         ▼
┌────────────────────┐
│ State Machine      │
├────────────────────┤
│ LLM Agent Helpers  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ SQLAlchemy Models  │◄── Alembic Migrations / Seed Data
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ Postgres + pgvector│
└────────────────────┘
```

## Components

### API Layer

- `app/api/routes/*` implements routers for auth, clients, appointments, conversations, automations, and services.
- `app/api/deps.py` centralizes dependency injection for database sessions and JWT validation.

### Core Configuration

- `app/core/config.py` loads environment variables using Pydantic `BaseSettings`.
- `app/core/security.py` provides password hashing and JWT helpers.

### Database Layer

- `app/db/models/` defines SQLAlchemy models aligned with the Week 1 schema.
- `alembic/` hosts migration configuration and an initial migration creating all tables with pgvector extension.
- `seed_data.sql` populates demo content for Glow MedSpa.
- `rls_policies.sql` sketches row-level security policies for Supabase/Postgres.

### Integrations & Services

- `app/integrations/` includes stubs for Google Calendar, Stripe, and Twilio.
- `app/services/__init__.py` exposes integration functions for the agent tool registry.

### Agent Logic

- `app/state_machine.py` implements the `AgentState` enum and `next_state` function.
- `app/llm_agent.py` provides intent parsing and tool invocation scaffolding.

### Tooling & Operations

- `docker-compose.yml` orchestrates FastAPI, Postgres (pgvector), and Redis containers.
- `.env.example` documents environment variables required for local and cloud deployments.
- `.pre-commit-config.yaml` enforces formatting and linting (Black, isort, Flake8).

## Week 2 Objectives

- Integrate real calendar/payment/SMS APIs and handle secrets securely.
- Expand authentication to include Supabase Auth or OAuth providers.
- Connect Redis for background job processing and state persistence.
- Build end-to-end conversation flows powered by an LLM with function calling.
