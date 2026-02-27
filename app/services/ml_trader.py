from __future__ import annotations

from typing import List

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from app.schemas.trader import PredictResponse, Signal, TrainResponse

# label integer -> Signal mapping (matches TrainRequest docs)
_LABEL_MAP = {1: Signal.BUY, -1: Signal.SELL, 0: Signal.HOLD}
_SIGNAL_TO_LABEL = {v: k for k, v in _LABEL_MAP.items()}


class MLTraderService:
    """Wraps a scikit-learn classifier and exposes train/predict operations."""

    def __init__(self) -> None:
        self._model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._is_trained = False

    @property
    def is_trained(self) -> bool:
        return self._is_trained

    @property
    def model_type(self) -> str:
        return type(self._model).__name__

    def train(self, features: List[List[float]], labels: List[int]) -> TrainResponse:
        X = np.array(features, dtype=float)
        y = np.array(labels, dtype=int)
        self._model.fit(X, y)
        self._is_trained = True
        return TrainResponse(
            message="Model trained successfully",
            samples_trained=len(y),
        )

    def predict(self, features: List[float]) -> PredictResponse:
        if not self._is_trained:
            raise RuntimeError("Model has not been trained yet")
        X = np.array([features], dtype=float)
        label = int(self._model.predict(X)[0])
        probas = self._model.predict_proba(X)[0]
        confidence = float(np.max(probas))
        signal = _LABEL_MAP.get(label, Signal.HOLD)
        return PredictResponse(signal=signal, confidence=confidence)


# module-level singleton shared across requests
trader_service = MLTraderService()
