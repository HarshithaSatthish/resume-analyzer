from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AI Resume Analyzer"
    app_env: str = "development"
    debug: bool = True

    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "resume_analyzer"
    mongodb_max_pool_size: int = 50
    mongodb_min_pool_size: int = 5
    mongodb_server_selection_timeout_ms: int = 5000
    mongodb_connect_timeout_ms: int = 5000

    jwt_secret_key: str = "change-this-to-a-long-random-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    max_upload_size_mb: int = 5
    upload_dir: str = "uploads"
    reports_dir: str = "reports"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    spacy_model: str = "en_core_web_sm"

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        if not path.is_absolute():
            path = self.base_dir / path
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def reports_path(self) -> Path:
        path = Path(self.reports_dir)
        if not path.is_absolute():
            path = self.base_dir / path
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def skills_dataset_path(self) -> Path:
        return self.base_dir.parent / "dataset" / "skills.json"


settings = Settings()
