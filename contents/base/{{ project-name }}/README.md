# {{ ProjectName }}

A basic FastAPI service with platform plumbing (observability, health, CI, Docker)
and no resource dependencies. Add persistence, caching, or messaging as the service grows.

## Development

```bash
# Install dependencies
uv sync --group dev

# Run the service
uv run uvicorn {{ project_name }}.main:app --reload --port {{ service_port }}

# Run tests
uv run pytest

# Run via entrypoint
uv run {{ project-name }}
```

## Endpoints

| Port | Path | Description |
|------|------|-------------|
| `{{ service_port }}` | `GET /` | Service identity stub |
| `{{ management_port }}` | `GET /health/readiness` | Readiness probe |
| `{{ management_port }}` | `GET /health/liveness` | Liveness probe |
| `{{ management_port }}` | `GET /metrics` | Prometheus metrics |

## Configuration

Copy `.env.example` to `.env` and fill in values. Configuration is loaded from environment variables.

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `{{ service_port }}` | Service port |
| `MANAGEMENT_PORT` | `{{ management_port }}` | Health/readiness port |
| `LOG_LEVEL` | `INFO` | Log level |
