from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.broker import Order, OrderRequest, Portfolio
from app.services.broker import broker_service

router = APIRouter(prefix="/broker", tags=["broker"])


@router.post("/order", response_model=Order, summary="Place a new order")
def place_order(request: OrderRequest) -> Order:
    return broker_service.place_order(request)


@router.get("/orders", response_model=List[Order], summary="List all orders")
def list_orders() -> List[Order]:
    return broker_service.get_orders()


@router.get("/portfolio", response_model=Portfolio, summary="Get current portfolio")
def get_portfolio() -> Portfolio:
    return broker_service.get_portfolio()


@router.delete(
    "/order/{order_id}", response_model=Order, summary="Cancel an open order"
)
def cancel_order(order_id: str) -> Order:
    try:
        return broker_service.cancel_order(order_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
