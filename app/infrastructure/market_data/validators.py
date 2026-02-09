# app\infrastructure\market_data\validators.py

import yfinance as yf
from functools import lru_cache

@lru_cache(maxsize=256)
def validate_ticker(ticker: str) -> bool:
    """
    Verifica se o ticker existe e tem negociações recentes.
    """
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        return not hist.empty
    except:
        return False
