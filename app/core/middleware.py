"""FastAPI middleware registration for CORS, request logging, and timing."""

import time
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core import constants
from app.core.logging import logger


def register_middleware(app: FastAPI) -> None:
    """Register CORS, request logging, and execution timing middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=constants.CORS_ORIGINS,
        allow_credentials=constants.CORS_ALLOW_CREDENTIALS,
        allow_methods=constants.CORS_ALLOW_METHODS,
        allow_headers=constants.CORS_ALLOW_HEADERS,
    )

    @app.middleware("http")
    async def log_and_time_request(request: Request, call_next: Any) -> Response:
        """Log incoming requests, record roundtrip latency, and log completion."""
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"
        query = f"?{request.url.query}" if request.url.query else ""
        logger.info(f"Incoming request: {request.method} {request.url.path}{query} from {client_ip}")

        try:
            response: Response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(f"Failed request: {request.method} {request.url.path}{query} after {duration_ms:.2f}ms")
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
        logger.info(
            f"Completed request: {request.method} {request.url.path} -> {response.status_code} ({duration_ms:.2f}ms)"
        )
        return response
