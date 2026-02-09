# app/platform/analytics/engine/basic_metrics.py
import numpy as np
import pandas as pd
from app.platform.analytics.metadata.manifests import basic_metrics_manifest

class BasicMetricsEngine:
    manifest = basic_metrics_manifest()

    def metadata(self):
        return self.manifest

    def calculate(self, asset, benchmark, rf_rate: float):
        returns = asset.pct_change().dropna()
        bench_returns = benchmark.pct_change().dropna()

        num_years = (asset.index[-1] - asset.index[0]).days / 365.25

        total_return = (asset.iloc[-1] / asset.iloc[0]) - 1
        bench_total_return = (benchmark.iloc[-1] / benchmark.iloc[0]) - 1
        cagr = (1 + total_return) ** (1 / num_years) - 1 if num_years > 0 else 0

        vol_daily = returns.std()
        vol_ann = vol_daily * np.sqrt(252)
        vol_bench_ann = bench_returns.std() * np.sqrt(252)

        rf_periodo = (1 + rf_rate) ** num_years - 1
        vol_periodo = vol_daily * np.sqrt(len(returns))

        sharpe_periodo = (total_return - rf_periodo) / vol_periodo if vol_periodo != 0 else 0
        sharpe_ann = (cagr - rf_rate) / vol_ann if vol_ann != 0 else 0

        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        max_drawdown = ((cumulative - peak) / peak).min()

        combined = pd.concat([returns, bench_returns], axis=1).dropna()
        correlation = combined.corr().iloc[0, 1] if not combined.empty else 0

        beta = correlation * (vol_ann / vol_bench_ann) if vol_bench_ann != 0 else 0

        return {
            "total_return": float(total_return),
            "benchmark_return": float(bench_total_return),
            "cagr": float(cagr),
            "volatility_daily": float(vol_daily),
            "volatility_ann": float(vol_ann),
            "max_drawdown": float(max_drawdown),
            "sharpe_period": float(sharpe_periodo),
            "sharpe_ann": float(sharpe_ann),
            "correlation": float(correlation),
            "beta": float(beta),
        }
