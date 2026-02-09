# app\domains\finance\schemas\metrics_schema.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

# --- INPUT SCHEMA ---
class BasicMetricsRequest(BaseModel):
    ticker: str = Field(..., json_schema_extra={"example": "PETR4.SA"}, description="Ticker do ativo")
    benchmark: Optional[str] = Field(None, json_schema_extra={"example": "^BVSP"}, description="Benchmark para comparação")
    start_date: Optional[str] = Field(None, json_schema_extra={"example": "2023-01-01"}, description="Data de início (AAAA-MM-DD)")
    end_date: Optional[str] = Field(None, json_schema_extra={"example": "2023-12-31"}, description="Data de fim (AAAA-MM-DD)")
    ai_analysis: Optional[bool] = Field(False, description="Incluir análise de IA nos resultados")

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v):
        if v is None: return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("O formato da data deve ser YYYY-MM-DD")

# --- COMPONENT SCHEMAS ---
class SettingsUsed(BaseModel):
    period: str
    risk_free_rate: float

class RequestParameters(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class BasicMetricsResults(BaseModel):
    # Retornos
    total_return: float = Field(..., description="Retorno absoluto do ativo no período")
    benchmark_return: float = Field(..., description="Retorno absoluto do benchmark no período")
    cagr: float = Field(..., description="Taxa de crescimento anual composta (Anualizado)")
    
    # Risco
    volatility_daily: float = Field(..., description="Desvio padrão dos retornos diários")
    volatility_ann: float = Field(..., description="Volatilidade anualizada (Std Dev * sqrt(252))")
    max_drawdown: float = Field(..., description="Maior queda do pico ao vale no período")
    
    # Eficiência
    sharpe_period: float = Field(..., description="Sharpe calculado sobre o período total")
    sharpe_ann: float = Field(..., description="Sharpe anualizado")
    
    # Comparativos
    correlation: float = Field(..., description="Correlação com o benchmark")
    beta: float = Field(..., description="Sensibilidade (Beta) em relação ao benchmark")

class Specmetrics(BaseModel):
    engine: str = Field(..., description="Versão do motor de cálculo")
    engine_version: str = Field(..., description="Versão do motor de cálculo de métricas básicas")
    effective_date: Optional[str] = Field(None, json_schema_extra={"example": "2023-12-31"}, description="Data de início da vigência (AAAA-MM-DD)")
 

class EngineSpec(BaseModel):
    engine_metrics: Specmetrics
    
# --- OUTPUT SCHEMA ---
class BasicMetricsResponse(BaseModel):
    request_id: str = Field(..., description="Hash único da requisição para auditoria")
    engine_specification: EngineSpec
    symbol: str
    benchmark_ref: str
    settings_used: SettingsUsed
    parameters: RequestParameters
    results: BasicMetricsResults
    ai_analysis: Optional[str] = Field(None, description="Análise gerada por IA, se solicitada")