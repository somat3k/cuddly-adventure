from __future__ import annotations

import uuid
from typing import Dict, List

from app.schemas.broker import Order, OrderRequest, OrderSide, OrderStatus, Portfolio


class BrokerService:
    """In-memory paper-trading broker."""

    def __init__(self, initial_cash: float = 100_000.0) -> None:
        self._cash = initial_cash
        self._positions: Dict[str, int] = {}
        self._orders: Dict[str, Order] = {}

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def place_order(self, request: OrderRequest) -> Order:
        order = Order(
            order_id=str(uuid.uuid4()),
            symbol=request.symbol,
            side=request.side,
            quantity=request.quantity,
            price=request.price,
            status=OrderStatus.OPEN,
        )
        self._orders[order.order_id] = order
        self._fill_order(order)
        return order

    def _fill_order(self, order: Order) -> None:
        """Immediately fill the order (paper trading)."""
        price = order.price or 0.0
        cost = price * order.quantity

        if order.side == OrderSide.BUY:
            self._cash -= cost
            self._positions[order.symbol] = (
                self._positions.get(order.symbol, 0) + order.quantity
            )
        else:
            self._cash += cost
            self._positions[order.symbol] = (
                self._positions.get(order.symbol, 0) - order.quantity
            )

        order.status = OrderStatus.FILLED

    def get_orders(self) -> List[Order]:
        return list(self._orders.values())

    def cancel_order(self, order_id: str) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(f"Order {order_id!r} not found")
        if order.status != OrderStatus.OPEN:
            raise ValueError(f"Order {order_id!r} cannot be cancelled (status={order.status})")
        order.status = OrderStatus.CANCELLED
        return order

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    def get_portfolio(self) -> Portfolio:
        return Portfolio(cash=self._cash, positions=dict(self._positions))


# module-level singleton shared across requests
broker_service = BrokerService()
