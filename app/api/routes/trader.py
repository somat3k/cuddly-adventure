from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.trader import (
    PredictRequest,
    PredictResponse,
    TraderStatus,
    TrainRequest,
    TrainResponse,
)
from app.services.ml_trader import trader_service

router = APIRouter(prefix="/trader", tags=["trader"])


@router.post("/train", response_model=TrainResponse, summary="Train the ML model")
def train(request: TrainRequest) -> TrainResponse:
    if len(request.features) != len(request.labels):
        raise HTTPException(
            status_code=422,
            detail="features and labels must have the same length",
        )
    return trader_service.train(request.features, request.labels)


@router.post(
    "/predict", response_model=PredictResponse, summary="Predict BUY/SELL/HOLD signal"
)
def predict(request: PredictRequest) -> PredictResponse:
    try:
        return trader_service.predict(request.features)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/status", response_model=TraderStatus, summary="Get model status")
def status() -> TraderStatus:
    return TraderStatus(
        is_trained=trader_service.is_trained,
        model_type=trader_service.model_type,
    )
