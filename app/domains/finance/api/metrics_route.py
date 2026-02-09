# app\domains\finance\api\metrics_route.py
 
from fastapi import APIRouter, Request, Depends
from app.application.config import settings
from app.domains.finance.schemas.metrics_schema import BasicMetricsRequest, BasicMetricsResponse
from app.domains.finance.services.basic_metrics_service import BasicMetricsService
from app.platform.analytics.engine.basic_metrics import BasicMetricsEngine
from app.application.assemblers.metrics_assembler import MetricsResponseAssembler
from app.application.guards.service_guard import service_guard
from app.platform.observability.log_assembler import Log
from app.application.interfaces.dependencies import get_metrics_service, get_engine
from app.application.errors.semantic_error import ApplicationError

router = APIRouter(prefix="/api/v1", tags=["Finance"])

@router.post("/basic-metrics", response_model=BasicMetricsResponse, dependencies=[Depends(service_guard("basic_metrics"))])
async def get_basic_metrics(
    request: Request,
    params: BasicMetricsRequest,
    service: BasicMetricsService = Depends(get_metrics_service),
    engine: BasicMetricsEngine = Depends(get_engine),
    assembler: MetricsResponseAssembler = Depends()
):
    
    request.state.payload = params.model_dump()

    Log(service_name="basic-metrics", params=params, request_id=request.state.request_id).info()

    if (params.ai_analysis) and (not settings.OPENAI_API_KEY):
        raise ApplicationError("NO_API_KEYS") 
    
    res, ai_analysis = service.get_metrics(**params.model_dump())

    manifest = engine.metadata()
    Log(service_name="basic-metrics", params=manifest, request_id=request.state.request_id).debug()

    return assembler.build(
        request_id=getattr(request.state, "request_id", "unknown"),
        engine_manifest=manifest,
        result=res,
        ai_analysis=ai_analysis
    )
