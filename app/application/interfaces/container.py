# app/application/container.py
 
from app.infrastructure.market_data.yfinance_repository import YFinanceBasicRepository
from app.domains.finance.services.basic_metrics_service import BasicMetricsService

market_data = YFinanceBasicRepository()
service = BasicMetricsService(market_data)
