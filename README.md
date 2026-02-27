# cuddly-adventure

Machine-learning trading server built with **FastAPI** + **Uvicorn**.

## Features

| Area | Details |
|------|---------|
| **ML Trader** | Train a `RandomForestClassifier` on OHLCV features; predict `BUY / SELL / HOLD` signals with a confidence score |
| **Broker** | Paper-trading broker: place market/limit orders, list orders, view portfolio, cancel open orders |
| **API docs** | Auto-generated Swagger UI at `/docs` and ReDoc at `/redoc` |

## Project structure

```
app/
  main.py                 # FastAPI application factory
  api/routes/
    trader.py             # /trader/* endpoints
    broker.py             # /broker/* endpoints
  schemas/
    trader.py             # Pydantic models for trader
    broker.py             # Pydantic models for broker
  services/
    ml_trader.py          # MLTraderService (sklearn wrapper)
    broker.py             # BrokerService (in-memory paper trading)
tests/
  test_trader.py
  test_broker.py
requirements.txt
```

## Getting started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn app.main:app --reload

# 3. Open API docs
open http://127.0.0.1:8000/docs
```

## API overview

### Trader

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/trader/train` | Train the ML model |
| `POST` | `/trader/predict` | Get a BUY/SELL/HOLD signal |
| `GET` | `/trader/status` | Check whether the model is trained |

### Broker

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/broker/order` | Place a new order |
| `GET` | `/broker/orders` | List all orders |
| `GET` | `/broker/portfolio` | Get current portfolio |
| `DELETE` | `/broker/order/{order_id}` | Cancel an open order |

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Server health check |

## Running tests

```bash
pytest tests/ -v
```
