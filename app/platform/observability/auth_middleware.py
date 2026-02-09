# app\platform\observability\auth_middleware.py
 
import sqlite3, hashlib, os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.application.config import settings
from app.platform.observability.logger import FastLog
from app.platform.observability.err_logger.error_assembler import Error

class SQLiteAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        id=getattr(request.state, 'request_id', 'unknown')

        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        api_key = request.headers.get("X-API-KEY")
        
        if not api_key: ####################
            msg, name = Error.error(id, "AUS_API_KEY")
            FastLog.write_error(name=name, message=msg)
            return JSONResponse(
                status_code=msg["Status"], 
                content={"detail": msg["Error"]}
            )

        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        db_path = settings.DB_PATH
        
        if not os.path.exists(db_path):
            msg, name = Error.error(id, "SERVICE_UNAV")
            FastLog.write_error(name=name, message=msg)
            return JSONResponse(
                status_code=msg["Status"], 
                content={"detail": msg["Error"]}
            )

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Buscamos apenas chaves ativas
            cursor.execute(
                "SELECT owner FROM api_keys WHERE key_hash = ? AND active = 1", 
                (key_hash,)
            )
            result = cursor.fetchone()
            conn.close()

            if not result: #########################
                msg, name = Error.error(id, "INV_API_KEY")
                FastLog.write_error(name=name, message=msg)
                return JSONResponse(
                    status_code=msg["Status"], 
                    content={"detail": f"{msg["Error"]}"}
                )

            request.state.user = result[0]
            
        except Exception as e: ######################
            msg, name = Error.error(id, "GENERIC_ERR_500")
            FastLog.write_error(name=name, message=msg)
            return JSONResponse(
                status_code=msg["Status"], 
                content={"detail": f"{msg["Error"]} {str(e)}"}
            )

        return await call_next(request)
