from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class DataConfig:
    raw_dir: Path = PROJECT_ROOT / "data" / "raw"
    processed_dir: Path = PROJECT_ROOT / "data" / "processed"
    synthetic_seed: int = 42
    n_customers: int = 5_000
    n_transactions: int = 100_000


@dataclass
class ModelConfig:
    isolation_forest_contamination: float = 0.02
    random_forest_n_estimators: int = 100
    random_forest_max_depth: Optional[int] = None


@dataclass
class RiskConfig:
    score_weights_path: Path = PROJECT_ROOT / "src" / "risk_scoring" / "score_weights.yaml"


@dataclass
class LLMConfig:
    provider: str = os.getenv("SECURESAR_LLM_PROVIDER", "bedrock")  # or "local"
    bedrock_model_id: str = os.getenv("SECURESAR_BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    region_name: str = os.getenv("AWS_REGION", "us-east-1")
    use_real_llm: bool = os.getenv("SECURESAR_USE_REAL_LLM", "false").lower() == "true"


@dataclass
class DatabaseConfig:
    postgres_dsn: str = os.getenv(
        "SECURESAR_POSTGRES_DSN",
        "postgresql://postgres:postgres@localhost:5432/securesar",
    )


@dataclass
class OpenSearchConfig:
    endpoint: str = os.getenv("SECURESAR_OPENSEARCH_ENDPOINT", "https://localhost:9200")
    sar_index: str = os.getenv("SECURESAR_OPENSEARCH_SAR_INDEX", "sar_templates")


@dataclass
class S3Config:
    bucket_name: str = os.getenv("SECURESAR_S3_BUCKET", "securesar-artifacts")


@dataclass
class SecurityConfig:
    jwt_secret_key: str = os.getenv("SECURESAR_JWT_SECRET", "change-me-in-production")
    jwt_algorithm: str = "HS256"


@dataclass
class AppConfig:
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    opensearch: OpenSearchConfig = field(default_factory=OpenSearchConfig)
    s3: S3Config = field(default_factory=S3Config)
    security: SecurityConfig = field(default_factory=SecurityConfig)


def load_config(overrides: Optional[Dict[str, Any]] = None) -> AppConfig:
    """
    Load application configuration, optionally applying overrides for tests.
    """
    cfg = AppConfig()
    if overrides:
        for key, value in overrides.items():
            if hasattr(cfg, key):
                setattr(cfg, key, value)
    return cfg

