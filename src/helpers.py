import time
from uuid import uuid4
from fastapi import Request
from loguru import logger


def configure_logging():
    logger.remove()
    logger.add(
        lambda msg: print(msg),
        format="{time} | {level} | {message} | {extra}",
        serialize=False,
    )


async def log_request_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id
    with logger.contextualize(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        query_params=str(request.query_params),
    ):
        logger.info("request received")
        response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response


async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
