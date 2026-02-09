# app/application/dependencies.py

from fastapi import Depends
from app.domains.finance.repositories.market_data import BasicRepository
from app.infrastructure.market_data.yfinance_repository import YFinanceBasicRepository
from app.domains.finance.services.basic_metrics_service import BasicMetricsService
from app.platform.analytics.engine.basic_metrics import BasicMetricsEngine


def get_market_repo() -> BasicRepository:
    return YFinanceBasicRepository()


def get_metrics_service(
    repo: BasicRepository = Depends(get_market_repo),
) -> BasicMetricsService:
    return BasicMetricsService(market_data_repo=repo)


def get_engine() -> BasicMetricsEngine:
    return BasicMetricsEngine()
