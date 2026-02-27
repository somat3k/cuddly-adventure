from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(str, Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


class OrderRequest(BaseModel):
    symbol: str = Field(..., description="Ticker symbol, e.g. AAPL")
    side: OrderSide
    quantity: PositiveInt = Field(..., description="Number of shares/contracts")
    price: Optional[PositiveFloat] = Field(
        None, description="Limit price; None for market orders"
    )


class Order(BaseModel):
    order_id: str
    symbol: str
    side: OrderSide
    quantity: int
    price: Optional[float]
    status: OrderStatus


class Portfolio(BaseModel):
    cash: float = Field(..., description="Available cash balance")
    positions: dict[str, int] = Field(
        default_factory=dict,
        description="Map of symbol -> quantity held",
    )
