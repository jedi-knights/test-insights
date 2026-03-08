# Test Insights

> Track, visualize, and trend test results across every CI/build system in one place.

Test Insights is an open-source, self-hosted platform for aggregating test results from any CI pipeline. It provides a hierarchical view of your quality data — **Team → Project → Test Suite → Test Run → Test Case** — with pass-rate trends, duration analytics, and a CLI for pushing results from any build system.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Monorepo Structure](#monorepo-structure)
- [API](#api)
- [CLI](#cli)
- [Web Dashboard](#web-dashboard)
- [Configuration](#configuration)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Universal format support** — ingest JUnit XML, pytest JSON, Go test JSON, and TAP reports
- **CI-aware** — automatically detects GitHub Actions, GitLab CI, Jenkins, and CircleCI environments and captures build metadata
- **Hierarchical data model** — organize results by Team → Project → Suite → Run → Case
- **Pass-rate trends** — daily aggregated pass-rate charts per suite, project, and team
- **JWT authentication** — secure register/login/logout with single-use refresh token rotation
- **REST API** — FastAPI-powered, fully async, with OpenAPI docs at `/docs`
- **CLI tool** — `ti push` sends results from any shell or CI step in one command
- **Web dashboard** — Next.js 14 App Router UI with Recharts visualizations
- **Docker Compose** — spin up the entire stack with a single command

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Clients                          │
│   Browser (Next.js)     CLI (ti)     External Scripts   │
└────────────┬───────────────┬────────────────┬───────────┘
             │               │                │
             ▼               ▼                ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI  (Hexagonal Architecture)           │
│                                                         │
│  Inbound: HTTP Routers → Use Cases → Port ABCs          │
│  Outbound: SQLAlchemy Repositories → PostgreSQL         │
└─────────────────────────────────────────────────────────┘
```

The API follows **hexagonal architecture** (ports & adapters):

- **Domain entities** are plain Python dataclasses with no framework dependencies
- **Port ABCs** define repository interfaces; use cases depend only on these
- **Adapters** (SQLAlchemy repositories) implement the ports
- **`dependencies.py`** is the single DI wiring point — the only place repositories are constructed

---

## Prerequisites

| Tool | Version |
|------|---------|
| Docker | ≥ 24 |
| Docker Compose | ≥ 2.20 |
| Python *(dev only)* | ≥ 3.13 |
| uv *(dev only)* | latest |
| Node.js *(dev only)* | ≥ 20 |
| pnpm *(dev only)* | ≥ 9 |

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/jedi-knights/test-insights.git
cd test-insights

# 2. Create your environment file
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# 3. Start all services
docker compose up --build

# 4. Open the web dashboard
open http://localhost:3000

# 5. API docs
open http://localhost:8000/docs
```

Services:

| Service | URL |
|---------|-----|
| Web dashboard | http://localhost:3000 |
| API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

---

## Monorepo Structure

```
test-insights/
├── .env.example            # Root environment template
├── docker-compose.yml      # Full-stack orchestration
│
├── api/                    # FastAPI backend
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── alembic/            # Database migrations
│   └── src/api/
│       ├── domain/         # Entities & enums (framework-free)
│       ├── ports/          # Repository ABCs
│       ├── application/    # DTOs & use cases
│       ├── adapters/       # HTTP routers + SQLAlchemy repositories
│       └── infrastructure/ # Config, JWT, bcrypt
│
├── cli/                    # `ti` command-line tool
│   ├── pyproject.toml
│   └── src/ti/
│       ├── parsers/        # JUnit, pytest-json, go-json, TAP
│       ├── commands/       # auth, teams, projects, suites, runs, push
│       └── client/         # httpx wrapper with auto token-refresh
│
└── web/                    # Next.js 14 frontend
    ├── package.json
    └── src/
        ├── app/            # App Router pages
        ├── components/     # UI, charts, shared components
        ├── lib/            # API client, auth context & hooks
        └── types/          # TypeScript interfaces & enums
```

---

## API

### Authentication

All endpoints except `/api/v1/auth/*` and `/api/v1/health` require:

```
Authorization: Bearer <access_token>
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Create account |
| `POST` | `/api/v1/auth/login` | Obtain token pair |
| `POST` | `/api/v1/auth/logout` | Revoke refresh token |
| `POST` | `/api/v1/auth/refresh` | Rotate tokens |
| `GET`  | `/api/v1/auth/me` | Current user info |

### Resources

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET/POST` | `/api/v1/teams` | List / create teams |
| `GET/PUT/DELETE` | `/api/v1/teams/{id}` | Get / update / delete team |
| `GET` | `/api/v1/teams/{id}/metrics` | Pass-rate trend + totals |
| `GET/POST` | `/api/v1/teams/{team_id}/projects` | List / create projects |
| `GET/PUT/DELETE` | `/api/v1/projects/{id}` | Get / update / delete project |
| `GET` | `/api/v1/projects/{id}/metrics` | Project metrics |
| `GET/POST` | `/api/v1/projects/{project_id}/suites` | List / create suites |
| `GET/PUT/DELETE` | `/api/v1/suites/{id}` | Get / update / delete suite |
| `GET` | `/api/v1/suites/{id}/metrics` | Suite pass-rate trend |
| `GET/POST` | `/api/v1/suites/{suite_id}/runs` | List / create runs |
| `GET` | `/api/v1/runs/{id}` | Run detail with test cases |
| `POST` | `/api/v1/runs/{id}/cases` | Bulk-create test cases |
| `GET` | `/api/v1/health` | Health check |

Full interactive docs available at `http://localhost:8000/docs`.

---

## CLI

Install the CLI from the `cli/` directory:

```bash
cd cli
uv pip install -e .
```

### Authentication

```bash
# Log in (prompts for email and password)
ti auth login --api-url http://localhost:8000

# Show current user
ti auth whoami

# Log out
ti auth logout
```

### Push test results

```bash
# JUnit XML
ti push <suite-id> --format junit --file report.xml

# pytest JSON (pytest-json-report plugin)
ti push <suite-id> --format pytest-json --file report.json

# Go test JSON (go test -json)
go test ./... -json | ti push <suite-id> --format go-json

# TAP
ti push <suite-id> --format tap --file results.tap

# Override branch/commit (auto-detected from CI env vars)
ti push <suite-id> --format junit --file report.xml \
  --branch main --commit abc1234
```

**Supported CI environments** (auto-detected, metadata captured):

- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Local (fallback)

### Resource management

```bash
ti teams list
ti teams create --name "Platform" --description "Platform team"

ti projects list <team-id>
ti projects create <team-id> --name "API Gateway"

ti suites list <project-id>
ti suites create <project-id> --name "Unit Tests"

ti runs list <suite-id>
ti runs get <run-id>
```

### Example CI step (GitHub Actions)

```yaml
- name: Run tests
  run: pytest --json-report --json-report-file=report.json

- name: Push results
  run: ti push ${{ vars.SUITE_ID }} --format pytest-json --file report.json
  env:
    TI_API_URL: ${{ vars.TI_API_URL }}
```

---

## Web Dashboard

The web dashboard provides:

- **Dashboard** — team overview with total counts
- **Teams** — list all teams, drill into metrics
- **Team detail** — projects list, pass-rate trend chart
- **Project detail** — suites list, aggregated metrics
- **Suite detail** — run history, stacked test-count bar chart, duration trend
- **Run detail** — full test case list with status badges and error messages

Authentication uses `localStorage`-persisted JWT with automatic token refresh on 401 responses.

---

## Configuration

### Root `.env`

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `testinsights` | Database user |
| `POSTGRES_PASSWORD` | `testinsights` | Database password |
| `POSTGRES_DB` | `testinsights` | Database name |
| `SECRET_KEY` | *(required)* | JWT signing key — generate with `openssl rand -hex 32` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | API URL for the web client |

### CLI config

The CLI stores credentials in `~/.config/test-insights/config.json`. Set the API URL at login:

```bash
ti auth login --api-url https://your-instance.example.com
```

---

## Development

### API

```bash
cd api
uv sync
# Start a local Postgres (or use docker compose up postgres)
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn api.main:app --reload
```

### CLI

```bash
cd cli
uv sync
uv pip install -e .
ti --help
```

### Web

```bash
cd web
pnpm install
pnpm dev
```

### Running the full stack locally

```bash
docker compose up postgres -d   # just the database
# then run api and web in dev mode as above
```

---

## Data Model

```
Team
 └── Project
      └── TestSuite
           └── TestRun  (build_system, branch, commit_sha, status, metadata JSONB)
                └── TestCase  (name, classname, status, duration, error_message)
```

**Run statuses:** `running` · `passed` · `failed` · `error`
**Case statuses:** `passed` · `failed` · `error` · `skipped`
**Build systems:** `github_actions` · `gitlab_ci` · `jenkins` · `circleci` · `local` · `unknown`

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests where applicable
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `chore:`, etc.
5. Open a pull request against `main`

Please open an issue first for significant changes so the approach can be discussed.

---

## License

This project is licensed under the [MIT License](LICENSE).
