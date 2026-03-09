# Test Insights CLI

Command-line interface for pushing and querying test results via the Test Insights API.

## Installation

```bash
cd cli
pip install uv
uv pip install -e .
```

The `ti` command is then available on your PATH.

## Configuration

The CLI stores its configuration in `~/.config/test-insights/config.json`. This file is managed automatically — you do not need to edit it by hand.

The following keys are persisted:

| Key | Description |
|---|---|
| `api_url` | Base URL of the Test Insights API |
| `access_token` | JWT access token for authenticated requests |
| `refresh_token` | JWT refresh token used to obtain new access tokens |

The default API URL is `http://localhost:8000`. To point the CLI at a different server, pass `--api-url` at login:

```bash
ti auth login --api-url https://your-api-host
```

The URL is saved and used for all subsequent commands. Access tokens are refreshed automatically when they expire — no manual re-login required.

## Authentication

```bash
# Log in (prompts for email and password)
ti auth login

# Log in against a non-default API URL
ti auth login --api-url http://localhost:8000

# Show the currently authenticated user
ti auth whoami

# Log out and clear stored tokens
ti auth logout
```

## Initial Setup

Before test results can be pushed, a team, project, and suite must exist. Any authenticated user can perform this setup:

```bash
# 1. Create a team
ti teams create --name "My Team"

# 2. Create a project under that team
ti projects create --team-id <team-id> --name "My Project"

# 3. Create a suite under that project
ti suites create --project-id <project-id> --name "My Suite"
```

The `suite-id` returned in step 3 is what CI pipelines use with `ti push`.

## Commands

### `ti push`

Parse a test result file and push it to a suite.

```bash
ti push <suite-id> --format <fmt> --file <path>

# Read from stdin
cat results.xml | ti push <suite-id> --format junit
```

Supported formats: `junit`, `pytest-json`, `go-json`, `tap`

Branch and commit SHA are auto-detected from CI environment variables (GitHub Actions, GitLab CI, Jenkins, CircleCI). They can also be supplied explicitly:

```bash
ti push <suite-id> --format junit --file results.xml --branch main --commit abc123
```

### `ti teams`

```bash
ti teams list
ti teams create --name "My Team" [--description "..."]
ti teams get <team-id>
ti teams delete <team-id>
```

### `ti projects`

```bash
ti projects list --team-id <team-id>
ti projects create --team-id <team-id> --name "My Project" [--description "..."]
ti projects get <project-id>
ti projects delete <project-id>
```

### `ti suites`

```bash
ti suites list --project-id <project-id>
ti suites create --project-id <project-id> --name "My Suite" [--description "..."]
ti suites get <suite-id>
ti suites delete <suite-id>
```

### `ti runs`

```bash
ti runs list --suite-id <suite-id>
ti runs get <run-id>
```
