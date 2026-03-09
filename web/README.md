# Test Insights Web

Next.js 15 dashboard for viewing and navigating test results.

## Configuration

The web app is configured via a single environment variable:

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Base URL of the Test Insights API |

Tokens are stored in `localStorage` (`access_token`, `refresh_token`) and refreshed automatically when they expire.

## Running locally

```bash
cd web
pnpm install
pnpm dev
```

The app is available at `http://localhost:3000`. To point it at a non-default API:

```bash
NEXT_PUBLIC_API_URL=http://your-api-host:8000 pnpm dev
```

## Running with Docker Compose

From the repo root:

```bash
docker compose up
```

The web container is available at `http://localhost:3000`. The API URL is baked into the Next.js build at image build time via the `NEXT_PUBLIC_API_URL` build arg. To override it:

```bash
NEXT_PUBLIC_API_URL=https://your-api-host docker compose up --build
```

## Authentication

Navigate to `http://localhost:3000` — unauthenticated users are redirected to `/login` automatically.

Default credentials (set by the API on first startup):

| Field | Value |
|---|---|
| Email | `admin@example.com` |
| Password | `changeme` |

## Initial Setup

The dashboard is read-only until a team, project, and suite exist. After logging in, a team, project, and suite must be created before any test results will appear. This can be done via the CLI:

```bash
ti auth login
ti teams create --name "My Team"
ti projects create --team-id <team-id> --name "My Project"
ti suites create --project-id <project-id> --name "My Suite"
```

Once a suite exists, CI pipelines can push results to it using `ti push` and they will appear in the dashboard.

## Pages

| Route | Description |
|---|---|
| `/login` | Login page |
| `/dashboard` | Overview |
| `/teams` | List of teams |
| `/teams/[id]` | Team detail with projects |
| `/projects/[id]` | Project detail with suites |
| `/suites/[id]` | Suite detail with test runs and charts |
| `/runs/[id]` | Individual test run with pass/fail breakdown |
