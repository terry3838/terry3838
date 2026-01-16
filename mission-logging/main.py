import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import FastAPI, Request


def configure_logging() -> logging.Logger:
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=200_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    for name in ("uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        uv_logger.handlers.clear()
        uv_logger.propagate = True

    logger = logging.getLogger("app")
    logger.info("Logging configured. Log file: %s", log_file)
    return logger


logger = configure_logging()
app = FastAPI()


@app.middleware("http")
async def request_logging(request: Request, call_next):
    start = time.perf_counter()
    logger.info("request start: %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("request error: %s %s", request.method, request.url.path)
        raise
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request end: %s %s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.get("/")
def root():
    logger.debug("root endpoint called")
    return {"status": "ok"}


@app.get("/health")
def health():
    logger.debug("health endpoint called")
    return {"status": "healthy"}


@app.get("/logs/demo")
def logs_demo():
    logger.debug("demo log: debug")
    logger.info("demo log: info")
    logger.warning("demo log: warning")
    logger.error("demo log: error")
    return {"message": "logged debug/info/warning/error"}
