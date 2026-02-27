from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import broker, trader

app = FastAPI(
    title="ML Trader API",
    description="Machine learning trading server with broker integration.",
    version="0.1.0",
)

app.include_router(trader.router)
app.include_router(broker.router)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict:
    return {"status": "ok"}
