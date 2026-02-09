# app/application/config.py

import os, json
from dotenv import load_dotenv
from typing import List

load_dotenv(override=False)

class Settings:
    PROJECT_NAME = "Financial Metrics API"
    VERSION = "0.1.0"

    LANGUAGE = os.getenv("LANGUAGE", "EN")

    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 8000))

    API_LOG_DIR = os.getenv(
            "API_LOG_DIR",
            "app/platform/observability/logs",
        )
    
    API_LOG_INFO = os.getenv("API_LOG_INFO", "api_access_info.log")
    API_LOG_DEBUG = os.getenv("API_LOG_DEBUG", "api_access_debug.log")
    API_LOG_WARNING = os.getenv("API_LOG_WARNING", "api_access_warning.log")
    API_LOG_ERROR = os.getenv("API_LOG_ERROR", "api_access_error.log")
    API_LOG_CRITICAL = os.getenv("API_LOG_CRITICAL", "api_access_critical.log")

    ASSET_CACHE_DIR = os.getenv("ASSET_CACHE_DIR", "app/infrastructure/cache")
    EXT_CACHE = os.getenv("EXT_CACHE", "parquet")
    COMPRESSION = os.getenv("COMPRESSION", "BROTLI")

    API_LOG = os.getenv(
        "API_LOG",
        "app/platform/observability/logs/api_access.log",
    )
    REL_LOG = os.getenv(
        "REL_LOG_API",
        "app/platform/observability/logs/performance_summary.json",
    )

    RISK_FREE_RATE = float(os.getenv("RISK_FREE_RATE", 0.10))
    DEFAULT_BENCHMARK = os.getenv("DEFAULT_BENCHMARK", "^BVSP")
    DATA_PERIOD = os.getenv("DATA_PERIOD", "2y")
    ANNUALIZATION_FACTOR = int(os.getenv("ANNUALIZATION_FACTOR", 252))

    DB_TYPE = os.getenv("DB_TYPO", "sqlite")
    DB_DIR = os.getenv("DB_DIR", "app/infrastructure/db/sqlite")
    DB_PATH = os.getenv(
        "DB_PATH",
        f"{DB_DIR}/governance.db",
    )
 
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    @staticmethod
    def _load_enabled_services() -> List[str]:
        raw = os.getenv("ENABLED_SERVICES")
        if not raw:
            return ["basic_metrics"]

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return [s.strip() for s in raw.split(",")]

    ENABLED_SERVICES: List[str] = _load_enabled_services()

    def is_service_enabled(self, service_name: str) -> bool:
        return service_name in self.ENABLED_SERVICES

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = "gpt-4.1-nano"

settings = Settings()
