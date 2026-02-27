from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.broker import BrokerService, broker_service

client = TestClient(app)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BUY_ORDER = {
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 10,
    "price": 150.0,
}

_SELL_ORDER = {
    "symbol": "AAPL",
    "side": "SELL",
    "quantity": 5,
    "price": 155.0,
}


# ---------------------------------------------------------------------------
# /broker/portfolio
# ---------------------------------------------------------------------------


def test_initial_portfolio(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = BrokerService(initial_cash=100_000.0)
    monkeypatch.setattr("app.api.routes.broker.broker_service", svc)
    resp = client.get("/broker/portfolio")
    assert resp.status_code == 200
    data = resp.json()
    assert data["cash"] == pytest.approx(100_000.0)
    assert data["positions"] == {}


# ---------------------------------------------------------------------------
# /broker/order  (POST)
# ---------------------------------------------------------------------------


def test_place_buy_order(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = BrokerService()
    monkeypatch.setattr("app.api.routes.broker.broker_service", svc)
    resp = client.post("/broker/order", json=_BUY_ORDER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["symbol"] == "AAPL"
    assert data["side"] == "BUY"
    assert data["status"] == "FILLED"
    assert "order_id" in data


def test_place_sell_order(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = BrokerService()
    monkeypatch.setattr("app.api.routes.broker.broker_service", svc)
    resp = client.post("/broker/order", json=_SELL_ORDER)
    assert resp.status_code == 200
    data = resp.json()
    assert data["side"] == "SELL"
    assert data["status"] == "FILLED"


# ---------------------------------------------------------------------------
# /broker/orders  (GET)
# ---------------------------------------------------------------------------


def test_list_orders(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = BrokerService()
    monkeypatch.setattr("app.api.routes.broker.broker_service", svc)
    client.post("/broker/order", json=_BUY_ORDER)
    resp = client.get("/broker/orders")
    assert resp.status_code == 200
    orders = resp.json()
    assert len(orders) == 1


# ---------------------------------------------------------------------------
# /broker/order/{order_id}  (DELETE)
# ---------------------------------------------------------------------------


def test_cancel_order_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = BrokerService()
    monkeypatch.setattr("app.api.routes.broker.broker_service", svc)
    resp = client.delete("/broker/order/nonexistent-id")
    assert resp.status_code == 404


def test_cancel_filled_order_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = BrokerService()
    monkeypatch.setattr("app.api.routes.broker.broker_service", svc)
    order_resp = client.post("/broker/order", json=_BUY_ORDER)
    order_id = order_resp.json()["order_id"]
    # Order is already FILLED, cancellation should be 409
    resp = client.delete(f"/broker/order/{order_id}")
    assert resp.status_code == 409
