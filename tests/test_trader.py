from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.ml_trader import MLTraderService, trader_service

client = TestClient(app)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FEATURES = [
    [100.0, 101.0, 99.0, 100.5, 1_000],
    [101.0, 103.0, 100.0, 102.0, 1_200],
    [102.0, 104.0, 101.0, 103.5, 1_100],
    [103.0, 104.5, 102.0, 104.0, 900],
    [104.0, 105.0, 103.0, 104.5, 800],
]
_LABELS = [1, 1, 0, -1, -1]


def _train() -> None:
    client.post("/trader/train", json={"features": _FEATURES, "labels": _LABELS})


# ---------------------------------------------------------------------------
# /trader/status
# ---------------------------------------------------------------------------


def test_trader_status_untrained(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = MLTraderService()
    monkeypatch.setattr("app.api.routes.trader.trader_service", svc)
    resp = client.get("/trader/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_trained"] is False
    assert data["model_type"] == "RandomForestClassifier"


# ---------------------------------------------------------------------------
# /trader/train
# ---------------------------------------------------------------------------


def test_train_success() -> None:
    resp = client.post(
        "/trader/train", json={"features": _FEATURES, "labels": _LABELS}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["samples_trained"] == len(_LABELS)
    assert "trained" in data["message"].lower()


def test_train_mismatched_lengths() -> None:
    resp = client.post(
        "/trader/train",
        json={"features": _FEATURES, "labels": _LABELS[:-1]},
    )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# /trader/predict
# ---------------------------------------------------------------------------


def test_predict_after_training() -> None:
    _train()
    resp = client.post("/trader/predict", json={"features": _FEATURES[0]})
    assert resp.status_code == 200
    data = resp.json()
    assert data["signal"] in ("BUY", "SELL", "HOLD")
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_without_training(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = MLTraderService()
    monkeypatch.setattr("app.api.routes.trader.trader_service", svc)
    resp = client.post("/trader/predict", json={"features": _FEATURES[0]})
    assert resp.status_code == 400
