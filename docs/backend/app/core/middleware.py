from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import logging
from typing import Callable

logger = logging.getLogger("pharma_ai")

async def log_requests_middleware(request: Request, call_next: Callable) -> Response:
    """Log all requests"""
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - "
            f"Completed in {process_time:.2f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
    """Simple rate limiting"""
    # TODO: Implement Redis-based rate limiting
    response = await call_next(request)
    return response