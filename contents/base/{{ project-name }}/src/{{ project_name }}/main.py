import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
import uvicorn
from fastapi import FastAPI

from .management import serve as serve_management
from .router import router
from .settings import settings

log = structlog.get_logger()


def setup_telemetry() -> None:
    """Initialize OpenTelemetry tracing when OTEL_EXPORTER_OTLP_ENDPOINT is configured."""
    if not settings.otel_exporter_otlp_endpoint:
        return
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource.create({"service.name": settings.otel_service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint))
    )
    trace.set_tracer_provider(provider)


def configure_logging() -> None:
    """Configure structlog with JSON output when LOGGING_STRUCTURED=true."""
    processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    if settings.logging_structured:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    log.info("{{ project-name }} started", port=settings.port)
    yield
    log.info("{{ project-name }} stopped")


def create_app() -> FastAPI:
    configure_logging()
    setup_telemetry()

    app = FastAPI(
        title="{{ ProjectName }}",
        lifespan=lifespan,
    )
    app.include_router(router)
    return app


app = create_app()


async def run() -> None:
    service_config = uvicorn.Config(
        "{{ project_name }}.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
    service_server = uvicorn.Server(service_config)
    await asyncio.gather(
        service_server.serve(),
        serve_management(settings),
    )


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
