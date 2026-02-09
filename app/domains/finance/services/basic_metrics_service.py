# app\domains\finance\services\basic_metrics_service.py

import json
from app.application.config import settings
from app.platform.analytics.engine.basic_metrics import BasicMetricsEngine
from app.application.gpt.analyze_text import AnalyzeTextUseCase
from app.domains.finance.contract.prompt_contract import FinanceiroPromptContract

class BasicMetricsService:
    def __init__(
        self,
        market_data_repo,
        risk_free_rate: float | None = None,
        period: str | None = None,
    ):
        self.market_data_repo = market_data_repo
        self.rf_rate = risk_free_rate or settings.RISK_FREE_RATE
        self.period = period or settings.DATA_PERIOD

    def get_prices(
        self,
        tickers: list[str],
        start_date=None,
        end_date=None,
    ):
        return self.market_data_repo.fetch_data(
            tickers=tuple(tickers),
            start_date=start_date,
            end_date=end_date,
            period=self.period,
        )

    def get_metrics(
        self,
        ticker: str,
        benchmark: str = None,
        start_date: str = None,
        end_date: str = None,
        ai_analysis: bool = False,
    ):

        target_bench = benchmark or settings.DEFAULT_BENCHMARK
        tickers_tuple = tuple(sorted([ticker, target_bench]))

        asset, bench = self.market_data_repo.fetch_data(
            tickers=tickers_tuple,
            start_date=start_date,
            end_date=end_date,
            period=self.period,
        )      

        # --- CÁLCULOS FINANCEIROS ---    
        self.engine = BasicMetricsEngine()
        results = self.engine.calculate(asset, bench, self.rf_rate)
        use_case = AnalyzeTextUseCase()
        payload = {
            "symbol": ticker,
            "benchmark_ref": target_bench,
            "settings_used": {
                "period": self.period,
                "risk_free_rate": self.rf_rate
            },
            "parameters": {
                "start_date": start_date,
                "end_date": end_date
            },
            "results": results
        }

        payload_string = json.dumps(payload, ensure_ascii=False)
        ai_analysis = None if not ai_analysis else use_case.execute(FinanceiroPromptContract(), payload_string)
        # --- format to genai prompt ---

        return {
            "symbol": ticker,
            "benchmark_ref": target_bench,
            "settings_used": {"period": self.period, "risk_free_rate": self.rf_rate},
            "parameters": {"start_date": start_date, "end_date": end_date},
            "results": results
        }, ai_analysis
        ################################################################################

