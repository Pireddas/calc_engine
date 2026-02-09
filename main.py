# main.py
# $env:OPENAI_API_KEY="your_api_key_here"
# poetry run uvicorn main:app --reload

import uvicorn
from fastapi import FastAPI, Security
from fastapi.security import APIKeyHeader
from contextlib import asynccontextmanager

from app.application.config import settings
from app.application.bootstrap import init_api_key_db

from app.domains.finance.api import metrics_route
# from app.domains.portfolio.api import portfolio_route
# from app.domains.risk.api import risk_route

from app.domains.auth.api import api_key_route
from app.platform.observability.logging_middleware import PerformanceLoggingMiddleware
from app.platform.observability.auth_middleware import SQLiteAuthMiddleware
from app.application.middlewares.request_id import RequestIDMiddleware
from app.application.errors.semantic_error import ApplicationError
from app.application.errors.handlers import semantic_error_handler

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

# -----------------------
# Lifespan (BOOTSTRAP)
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_api_key_db()
    yield
    print("Application shutdown")

# -----------------------
# Application
# -----------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    dependencies=[Security(api_key_header)],
    lifespan=lifespan,
)

# -----------------------
# Middlewares
# -----------------------
app.add_middleware(PerformanceLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SQLiteAuthMiddleware)

# -----------------------
# Routers
# -----------------------
app.include_router(metrics_route.router)
# app.include_router(risk_route.router)
# app.include_router(portfolio_route.router)
app.include_router(api_key_route.router)

# -----------------------
# Error
# -----------------------
app.add_exception_handler(ApplicationError, semantic_error_handler)

# -----------------------
# Local execution only
# -----------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
