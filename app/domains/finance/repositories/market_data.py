# app/domains/finance/repositories/market_data.py

import pandas as pd
from datetime import date
from typing import Tuple

class BasicRepository:
    def fetch_data(
        self,
        tickers: Tuple[str, ...],
        start_date: date | None,
        end_date: date | None,
        period: str | None,
    ) -> pd.DataFrame:
        raise NotImplementedError
