# app/platform/analytics/metadata/manifests.py
from datetime import date
from app.application.config import settings

def basic_metrics_manifest():
    return {
        "engine": "basic_metrics",
        "engine_version": "1.1.0",
        "formula_version": "basic_metrics",
        "dataframe_version": "close_prices_adjusted",
        "assumptions": {
            "annualization_factor": settings.ANNUALIZATION_FACTOR,
            "returns": "simple",
            "risk_free_rate": "annualized",
            "risk_free_tx": settings.RISK_FREE_RATE,
        },
        "created_at": date(2025, 10, 27).isoformat(),
        "effective_date": date(2025, 11, 3).isoformat()
    } 

def tail_risk_manifest():
    return {
        "engine": "tail_risk",
        "engine_version": "1.2.0",
        "formula_version": "historical_var_cvar",
        "dataframe_version": "close_prices_adjusted",
        "assumptions": "iid_returns",
        "created_at": date(2024, 8, 11).isoformat(),
        "effective_date": date(2024, 8, 15).isoformat()
    } 

def portifolio_manifest():
    return {
        "engine": "portfolio_metrics",
        "version": "1.3.0",
        "formula_version": "expected_risk_portfolio",
        "dataframe_version": "close_prices_adjusted",
        "weights": "equal_weight",
        "annualization_factor": settings.ANNUALIZATION_FACTOR,
        "risk_free_rate": "annualized",
        "risk_free_tx": settings.RISK_FREE_RATE,
        "created_at": date(2025, 12, 18).isoformat(),
        "effective_date": date(2025, 12, 21).isoformat()
    } 

def return_portfolio_manifest():
    return {
        "engine": "portfolio_metrics",
        "version": "1.4.0",
        "formula_version": "expected_return_portfolio",
        "annualization_factor": settings.ANNUALIZATION_FACTOR,
        "dataframe_version": "close_prices_adjusted",
        "created_at": date(2026, 1, 1).isoformat(),
        "effective_date": date(2026, 1, 3).isoformat()
    } 

def individual_portfolio_manifest():
    return {
        "engine": "portfolio_metrics",
        "version": "1.5.0",
        "formula_version": "individual_metrics_portfolio",
        "dataframe_version": "close_prices_adjusted",
        "weights": "equal_weight",
        "annualization_factor": settings.ANNUALIZATION_FACTOR,
        "risk_free_rate": "annualized",
        "risk_free_tx": settings.RISK_FREE_RATE,
        "created_at": date(2024, 11, 15).isoformat(),
        "effective_date": date(2024, 11, 17).isoformat()
    } 

def correlation_portfolio_manifest():
    return {
        "engine": "portfolio_metrics",
        "version": "1.6.0",
        "formula_version": "correlation_matrix_portfolio",
        "dataframe_version": "close_prices_adjusted",
        "method": "pearson",
        "created_at": date(2026, 1, 1).isoformat(),
        "effective_date": date(2026, 1, 3).isoformat()
    } 
