from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    # The platform injects SERVER_PORT (the PAO env contract); PORT stays honored for local runs.
    # Without the alias the service reads only PORT and silently binds its compiled-in default,
    # ignoring the port the platform gave it (S3).
    port: int = Field(
        default={{ service_port }},
        validation_alias=AliasChoices("server_port", "port"),
    )
    management_port: int = {{ management_port }}
    log_level: str = "INFO"
    logging_structured: bool = False

    # OpenTelemetry — injected by platform at deploy time
    otel_service_name: str = "{{ project-name }}"
    otel_exporter_otlp_endpoint: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
