from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class TrainRequest(BaseModel):
    features: List[List[float]] = Field(
        ..., description="2-D array of OHLCV feature rows"
    )
    labels: List[int] = Field(
        ..., description="Target labels: 1=BUY, -1=SELL, 0=HOLD"
    )


class TrainResponse(BaseModel):
    message: str
    samples_trained: int


class PredictRequest(BaseModel):
    features: List[float] = Field(
        ..., description="Single feature row (e.g. OHLCV values)"
    )


class PredictResponse(BaseModel):
    signal: Signal
    confidence: float = Field(..., ge=0.0, le=1.0)


class TraderStatus(BaseModel):
    model_config = {"protected_namespaces": ()}

    is_trained: bool
    model_type: str
