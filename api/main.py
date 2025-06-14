from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from api.routers import cats_routers
from api.logging.logger import configure_logging
from api.scripts.populate_db import populate_database
from api.metrics.prometheus import (
    REQUEST_COUNTER,
    ERROR_COUNTER,
    REQUEST_LATENCY
)

# Define o lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa na startup
    await populate_database()
    yield
    # Executa na shutdown (se necessário)
    # ex: fechar conexões, limpar cache, etc

app = FastAPI(
    title="Cat API - SRE Challenge",
    lifespan=lifespan
)

# Setup logging
configure_logging()

# Setup Prometheus metrics via Instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Middleware customizado para métricas
@app.middleware("http")
async def prometheus_metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)
    REQUEST_COUNTER.labels(method=method, endpoint=endpoint).inc()
    if response.status_code >= 400:
        ERROR_COUNTER.labels(
            method=method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()
    return response

# Include routers
app.include_router(cats_routers.router)

@app.get("/healthz", tags=["health"])
def health_check():
    return {"status": "ok"}

# Executa o app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
