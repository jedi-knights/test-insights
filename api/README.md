# Test Insights API

FastAPI backend for the Test Insights platform. Provides a fully async REST API backed by PostgreSQL.

## Architecture

The API follows **hexagonal architecture** (ports & adapters):

```
api/src/api/
├── domain/         # Plain Python dataclasses — no framework dependencies
├── ports/          # Repository ABCs (interfaces)
├── application/    # DTOs and use cases — depend only on port ABCs
├── adapters/
│   ├── inbound/    # HTTP routers (FastAPI)
│   └── outbound/   # SQLAlchemy async repositories
└── infrastructure/ # Config, JWT, bcrypt, DB session, seed
```

Use cases depend only on port ABCs. The single DI wiring point is `adapters/inbound/http/dependencies.py`, which constructs repositories and injects them into use cases.

## Configuration

All settings are read from environment variables (or a `.env` file in `api/`):

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://testinsights:testinsights@localhost:5432/testinsights` | Async PostgreSQL connection string |
| `SECRET_KEY` | `dev-secret-change-in-production` | JWT signing key — **must be changed in production** |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `ADMIN_EMAIL` | `admin@example.com` | Default admin user email |
| `ADMIN_PASSWORD` | `changeme` | Default admin user password |
| `ADMIN_FULL_NAME` | `Admin` | Default admin user display name |

Generate a strong secret key with:

```bash
openssl rand -hex 32
```

## Running locally

```bash
cd api
uv sync

# Start a local PostgreSQL instance (or use docker compose up postgres -d from the repo root)
cp .env.example .env  # edit DATABASE_URL and SECRET_KEY as needed

# Run migrations
uv run alembic upgrade head

# Start the dev server
uv run uvicorn api.main:app --reload
```

The API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Database migrations

Migrations are managed with Alembic:

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Downgrade one step
uv run alembic downgrade -1
```

The `alembic.ini` connection string is used for local development only. In Docker the `DATABASE_URL` environment variable is used at runtime.

## Admin user

On startup the API automatically provisions a default admin user if one does not already exist. Credentials are controlled by the `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `ADMIN_FULL_NAME` environment variables. Change these before deploying to production.

## Authentication

All endpoints except `/api/v1/auth/*` and `/api/v1/health` require:

```
Authorization: Bearer <access_token>
```

JWT access tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES`. When a request returns `401`, clients should use the refresh token to obtain a new token pair from `POST /api/v1/auth/refresh`. Refresh tokens are single-use — each refresh rotates both tokens. Revoked tokens are tracked in the `token_blocklist` table.

## Endpoints

### Auth

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Create a new user account |
| `POST` | `/api/v1/auth/login` | Obtain access + refresh tokens |
| `POST` | `/api/v1/auth/logout` | Revoke refresh token |
| `POST` | `/api/v1/auth/refresh` | Rotate token pair |
| `GET`  | `/api/v1/auth/me` | Current authenticated user |

### Teams

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/teams` | List all teams |
| `POST` | `/api/v1/teams` | Create a team |
| `GET` | `/api/v1/teams/{id}` | Get a team |
| `PUT` | `/api/v1/teams/{id}` | Update a team |
| `DELETE` | `/api/v1/teams/{id}` | Delete a team |
| `GET` | `/api/v1/teams/{id}/metrics` | Pass-rate trend and totals |

### Projects

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/teams/{team_id}/projects` | List projects for a team |
| `POST` | `/api/v1/teams/{team_id}/projects` | Create a project |
| `GET` | `/api/v1/projects/{id}` | Get a project |
| `PUT` | `/api/v1/projects/{id}` | Update a project |
| `DELETE` | `/api/v1/projects/{id}` | Delete a project |
| `GET` | `/api/v1/projects/{id}/metrics` | Project metrics |

### Suites

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/projects/{project_id}/suites` | List suites for a project |
| `POST` | `/api/v1/projects/{project_id}/suites` | Create a suite |
| `GET` | `/api/v1/suites/{id}` | Get a suite |
| `PUT` | `/api/v1/suites/{id}` | Update a suite |
| `DELETE` | `/api/v1/suites/{id}` | Delete a suite |
| `GET` | `/api/v1/suites/{id}/metrics` | Suite pass-rate trend |

### Runs & Cases

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/suites/{suite_id}/runs` | List runs for a suite |
| `POST` | `/api/v1/suites/{suite_id}/runs` | Create a run |
| `GET` | `/api/v1/runs/{id}` | Get a run with test cases |
| `POST` | `/api/v1/runs/{id}/cases` | Bulk-create test cases |

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Health check (no auth required) |

## Running tests

```bash
cd api
uv run pytest
```

## Key files

| File | Purpose |
|---|---|
| `src/api/main.py` | FastAPI app and lifespan handler |
| `src/api/infrastructure/config.py` | Pydantic settings |
| `src/api/infrastructure/security.py` | JWT and bcrypt helpers |
| `src/api/adapters/inbound/http/dependencies.py` | DI wiring |
| `src/api/adapters/outbound/persistence/database.py` | Async DB session |
| `alembic/versions/` | Migration files |
