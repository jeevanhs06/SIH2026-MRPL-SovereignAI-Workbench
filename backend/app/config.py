from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = REPO_ROOT / "data"
DEFAULT_KNOWLEDGE_BASE_ROOT = REPO_ROOT / "knowledge_base"


class Settings(BaseSettings):
    app_name: str = "SovereignAI Workbench API"
    app_env: str = "development"
    offline_mode: bool = True
    max_upload_size_bytes: int = 10 * 1024 * 1024
    allowed_upload_extensions: set[str] = Field(
        default_factory=lambda: {".txt", ".md", ".pdf", ".png", ".jpg", ".jpeg"}
    )
    model_endpoint: str = "http://127.0.0.1:11434"

    data_root: Path = DEFAULT_DATA_ROOT
    input_dir: Path = DEFAULT_DATA_ROOT / "inputs"
    output_dir: Path = DEFAULT_DATA_ROOT / "outputs"
    tmp_dir: Path = DEFAULT_DATA_ROOT / "tmp"
    vector_store_dir: Path = DEFAULT_DATA_ROOT / "vector_store"
    audit_dir: Path = DEFAULT_DATA_ROOT / "audit"
    knowledge_base_dir: Path = DEFAULT_KNOWLEDGE_BASE_ROOT

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SOVAI_", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    for directory in [
        settings.data_root,
        settings.input_dir,
        settings.output_dir,
        settings.tmp_dir,
        settings.vector_store_dir,
        settings.audit_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    return settings
