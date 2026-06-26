from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = {{ service_port }}
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
