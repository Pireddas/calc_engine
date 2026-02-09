# app/infrastructure/market_data/yfinance_repository.py

import yfinance as yf
from datetime import date
from functools import lru_cache
import pandas as pd
 
from app.domains.finance.repositories.market_data import BasicRepository
from app.infrastructure.market_data.validators import validate_ticker
from app.application.errors.semantic_error import ApplicationError
 
class YFinanceBasicRepository(BasicRepository):

    @lru_cache(maxsize=256)
    def fetch_data(
        self,
        tickers: tuple[str, ...],
        start_date: date | None,
        end_date: date | None,
        period: str | None,
    ) -> pd.DataFrame:

        for ticker in tickers:
            if not validate_ticker(ticker):
                raise ApplicationError("INV_TICKERS")
            
        if start_date:
            params = {
                "start": start_date,
                "end": (end_date or date.today()),
            }
        else:
            if not period:
                raise ApplicationError("INV_SDATE")
            params = {"period": period}

        df = yf.download(
            tickers=list(tickers),
            progress=False,
            auto_adjust=True,
            **params,
        )

        if df.empty:
            raise ApplicationError("NO_DATA")

        if "Close" not in df.columns:
            raise ApplicationError("INV_CLOSE_COLUMNS")

        close_prices = df["Close"]
        
        for ticker in tickers:
            series = close_prices[ticker].dropna()
            if len(series) < 5:
                raise ApplicationError("INV_HIST_PRICE")

        close_prices = df["Close"]
        asset = close_prices[tickers[0]].dropna()
        bench = close_prices[tickers[1]].dropna()

        return asset, bench

# class YFinancePortfolioRepository(PortfolioRepository):

#     @lru_cache(maxsize=256)
#     def fetch_data(
#         self,
#         tickers: tuple[str, ...],
#         start_date: date | None,
#         end_date: date | None,
#     ) -> pd.DataFrame:

#         for ticker in tickers:
#             if not validate_ticker(ticker):
#                 msg, name = Error400.error(id, "INV_TICKER")
#                 FastLog.write_error(name=name, message=msg)
#                 raise ValueError(f"{msg} {ticker}")

#         params = {
#                 "start": start_date,
#                 "end": (end_date or date.today()),
#             }


#         return yf.download(
#             tickers=list(tickers),
#             progress=False,
#             auto_adjust=True,
#             **params,
#         )
    
# class YFinanceRiskRepository(RiskRepository):

#     @lru_cache(maxsize=256)
#     def fetch_data(
#         self,
#         ticker: str,
#         start_date: date | None,
#         end_date: date | None,
#     ) -> pd.DataFrame:

#         if not validate_ticker(ticker):
#             msg, name = Error400.error(id, "INV_TICKER")
#             FastLog.write_error(name=name, message=msg)
#             raise ValueError(f"{msg} {ticker}")

#         params = {
#                 "start": start_date,
#                 "end": (end_date or date.today()),
#             }


#         return yf.download(
#             tickers=ticker,
#             progress=False,
#             auto_adjust=True,
#             **params,
#         )