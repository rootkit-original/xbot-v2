# 🔧 API Reference

Documentação completa da API do XBot v2 para desenvolvedores.

## 🎯 Visão Geral

A API do XBot v2 oferece acesso programático completo a todas as funcionalidades do sistema de trading. Ela é baseada em REST e retorna dados em formato JSON.

### Características Principais

- ✅ **RESTful API** com endpoints intuitivos
- ✅ **Autenticação JWT** para segurança
- ✅ **Rate limiting** para proteção
- ✅ **Documentação OpenAPI/Swagger** integrada
- ✅ **WebSockets** para dados em tempo real
- ✅ **Paginação** automática para grandes datasets
- ✅ **Filtros e ordenação** flexíveis

### Base URL

```
Development: http://localhost:8080/api/v1
Production: https://your-domain.com/api/v1
```

### Formato de Resposta

Todas as respostas seguem o padrão:

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully",
  "timestamp": "2024-03-15T10:30:00Z",
  "request_id": "uuid-here"
}
```

## 🔐 Autenticação

### Login

**Endpoint:** `POST /auth/login`

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "your-password"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "user": {
      "id": "user-123",
      "username": "admin",
      "permissions": ["read", "write", "admin"]
    }
  }
}
```

### Refresh Token

**Endpoint:** `POST /auth/refresh`

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Logout

**Endpoint:** `POST /auth/logout`

```http
POST /api/v1/auth/logout
Authorization: Bearer {access_token}
```

## 🤖 Bot Management

### Create Bot

**Endpoint:** `POST /bots`

```http
POST /api/v1/bots
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Scalping BTC",
  "strategy": "scalping_conservative",
  "capital": 1000.0,
  "symbols": ["BTCUSDT", "ETHUSDT"],
  "config": {
    "stop_loss": 1.0,
    "take_profit": 2.0,
    "max_positions": 3,
    "risk_per_trade": 2.0
  }
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "bot_id": "bot-123",
    "name": "Scalping BTC",
    "strategy": "scalping_conservative",
    "status": "stopped",
    "capital": 1000.0,
    "created_at": "2024-03-15T10:30:00Z"
  }
}
```

### Get Bot

**Endpoint:** `GET /bots/{bot_id}`

```http
GET /api/v1/bots/bot-123
Authorization: Bearer {access_token}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "bot_id": "bot-123",
    "name": "Scalping BTC",
    "strategy": "scalping_conservative",
    "status": "running",
    "capital": 1000.0,
    "balance": 1045.67,
    "pnl": 45.67,
    "pnl_percent": 4.57,
    "positions": [
      {
        "position_id": "pos-456",
        "symbol": "BTCUSDT",
        "side": "long",
        "quantity": 0.023,
        "entry_price": 43250.00,
        "current_price": 43450.00,
        "pnl": 4.60,
        "created_at": "2024-03-15T10:25:00Z"
      }
    ],
    "performance": {
      "total_trades": 45,
      "winning_trades": 32,
      "losing_trades": 13,
      "win_rate": 71.1,
      "profit_factor": 1.85,
      "max_drawdown": 5.2
    },
    "created_at": "2024-03-15T09:00:00Z",
    "last_trade_at": "2024-03-15T10:25:00Z"
  }
}
```

### List Bots

**Endpoint:** `GET /bots`

```http
GET /api/v1/bots?page=1&limit=20&status=running&strategy=scalping_conservative
Authorization: Bearer {access_token}
```

**Query Parameters:**

- `page` (int): Página atual (default: 1)
- `limit` (int): Itens por página (default: 20, max: 100)
- `status` (string): Filtrar por status (`running`, `stopped`, `error`)
- `strategy` (string): Filtrar por estratégia
- `sort` (string): Ordenação (`created_at`, `name`, `pnl`, `win_rate`)
- `order` (string): Direção (`asc`, `desc`)

**Response:**

```json
{
  "success": true,
  "data": {
    "bots": [
      {
        "bot_id": "bot-123",
        "name": "Scalping BTC",
        "strategy": "scalping_conservative",
        "status": "running",
        "pnl": 45.67,
        "win_rate": 71.1
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 5,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### Update Bot

**Endpoint:** `PUT /bots/{bot_id}`

```http
PUT /api/v1/bots/bot-123
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Scalping BTC Updated",
  "config": {
    "stop_loss": 1.5,
    "take_profit": 3.0,
    "max_positions": 5
  }
}
```

### Delete Bot

**Endpoint:** `DELETE /bots/{bot_id}`

```http
DELETE /api/v1/bots/bot-123
Authorization: Bearer {access_token}
```

## 🎮 Bot Control

### Start Bot

**Endpoint:** `POST /bots/{bot_id}/start`

```http
POST /api/v1/bots/bot-123/start
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "force": false,
  "demo_mode": false
}
```

### Stop Bot

**Endpoint:** `POST /bots/{bot_id}/stop`

```http
POST /api/v1/bots/bot-123/stop
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "force": false,
  "close_positions": true
}
```

### Pause Bot

**Endpoint:** `POST /bots/{bot_id}/pause`

```http
POST /api/v1/bots/bot-123/pause
Authorization: Bearer {access_token}
```

### Resume Bot

**Endpoint:** `POST /bots/{bot_id}/resume`

```http
POST /api/v1/bots/bot-123/resume
Authorization: Bearer {access_token}
```

## 💼 Portfolio Management

### Get Portfolio

**Endpoint:** `GET /portfolio`

```http
GET /api/v1/portfolio
Authorization: Bearer {access_token}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "total_balance": 15234.56,
    "total_pnl": 1234.56,
    "total_pnl_percent": 8.83,
    "available_balance": 8900.00,
    "invested_balance": 6334.56,
    "positions": [
      {
        "symbol": "BTCUSDT",
        "side": "long",
        "quantity": 0.15,
        "average_price": 42500.00,
        "current_price": 43200.00,
        "pnl": 105.00,
        "pnl_percent": 2.47
      }
    ],
    "asset_allocation": {
      "BTC": 45.2,
      "ETH": 30.1,
      "BNB": 15.3,
      "USDT": 9.4
    },
    "performance": {
      "daily_pnl": 89.34,
      "weekly_pnl": 456.78,
      "monthly_pnl": 1234.56,
      "max_drawdown": 8.5,
      "sharpe_ratio": 1.85
    }
  }
}
```

### Get Portfolio History

**Endpoint:** `GET /portfolio/history`

```http
GET /api/v1/portfolio/history?period=30d&granularity=1d
Authorization: Bearer {access_token}
```

**Query Parameters:**

- `period`: `1d`, `7d`, `30d`, `90d`, `1y`
- `granularity`: `1h`, `4h`, `1d`, `1w`

## 📊 Positions

### Get Positions

**Endpoint:** `GET /positions`

```http
GET /api/v1/positions?status=open&bot_id=bot-123
Authorization: Bearer {access_token}
```

**Query Parameters:**

- `status`: `open`, `closed`, `all`
- `bot_id`: Filtrar por bot específico
- `symbol`: Filtrar por símbolo
- `side`: `long`, `short`

**Response:**

```json
{
  "success": true,
  "data": {
    "positions": [
      {
        "position_id": "pos-456",
        "bot_id": "bot-123",
        "bot_name": "Scalping BTC",
        "symbol": "BTCUSDT",
        "side": "long",
        "quantity": 0.023,
        "entry_price": 43250.00,
        "current_price": 43450.00,
        "pnl": 4.60,
        "pnl_percent": 1.06,
        "stop_loss": 42817.50,
        "take_profit": 44115.00,
        "status": "open",
        "created_at": "2024-03-15T10:25:00Z"
      }
    ],
    "summary": {
      "total_positions": 5,
      "open_positions": 3,
      "total_pnl": 89.34,
      "unrealized_pnl": 23.45,
      "realized_pnl": 65.89
    }
  }
}
```

### Close Position

**Endpoint:** `POST /positions/{position_id}/close`

```http
POST /api/v1/positions/pos-456/close
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "quantity": 0.023,
  "price": null
}
```

## 📈 Market Data

### Get Prices

**Endpoint:** `GET /market/prices`

```http
GET /api/v1/market/prices?symbols=BTCUSDT,ETHUSDT,BNBUSDT
Authorization: Bearer {access_token}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "prices": [
      {
        "symbol": "BTCUSDT",
        "price": 43250.00,
        "change_24h": 1.25,
        "change_24h_percent": 2.98,
        "volume_24h": 25678.45,
        "updated_at": "2024-03-15T10:30:00Z"
      }
    ]
  }
}
```

### Get Klines

**Endpoint:** `GET /market/klines`

```http
GET /api/v1/market/klines?symbol=BTCUSDT&interval=1h&limit=100
Authorization: Bearer {access_token}
```

**Query Parameters:**

- `symbol`: Par de trading
- `interval`: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`
- `limit`: Número de candles (max: 1000)
- `start_time`: Timestamp de início
- `end_time`: Timestamp de fim

**Response:**

```json
{
  "success": true,
  "data": {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "klines": [
      {
        "open_time": 1710489600000,
        "close_time": 1710493199999,
        "open": 43200.00,
        "high": 43450.00,
        "low": 43150.00,
        "close": 43250.00,
        "volume": 123.45,
        "trades": 1567
      }
    ]
  }
}
```

## 📊 Strategies

### List Strategies

**Endpoint:** `GET /strategies`

```http
GET /api/v1/strategies
Authorization: Bearer {access_token}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "strategies": [
      {
        "name": "scalping_conservative",
        "display_name": "Scalping Conservador",
        "description": "Estratégia de scalping com baixo risco",
        "risk_level": "low",
        "timeframe": ["1m", "5m"],
        "markets": ["spot"],
        "parameters": {
          "stop_loss": {
            "default": 1.0,
            "min": 0.5,
            "max": 3.0,
            "description": "Stop loss em %"
          },
          "take_profit": {
            "default": 2.0,
            "min": 1.0,
            "max": 5.0,
            "description": "Take profit em %"
          }
        }
      }
    ]
  }
}
```

### Get Strategy

**Endpoint:** `GET /strategies/{strategy_name}`

```http
GET /api/v1/strategies/scalping_conservative
Authorization: Bearer {access_token}
```

### Backtest Strategy

**Endpoint:** `POST /strategies/{strategy_name}/backtest`

```http
POST /api/v1/strategies/scalping_conservative/backtest
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "symbols": ["BTCUSDT"],
  "start_date": "2024-01-01",
  "end_date": "2024-03-01",
  "capital": 10000.0,
  "parameters": {
    "stop_loss": 1.0,
    "take_profit": 2.0
  }
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "backtest_id": "bt-789",
    "status": "completed",
    "results": {
      "total_return": 15.67,
      "total_return_percent": 15.67,
      "total_trades": 145,
      "winning_trades": 98,
      "losing_trades": 47,
      "win_rate": 67.6,
      "profit_factor": 1.85,
      "max_drawdown": 8.5,
      "sharpe_ratio": 1.42,
      "trades": [
        {
          "symbol": "BTCUSDT",
          "side": "long",
          "entry_time": "2024-01-15T10:30:00Z",
          "exit_time": "2024-01-15T11:45:00Z",
          "entry_price": 42500.00,
          "exit_price": 43350.00,
          "quantity": 0.235,
          "pnl": 199.75,
          "pnl_percent": 4.71
        }
      ]
    }
  }
}
```

## 🔔 Notifications

### Get Notifications

**Endpoint:** `GET /notifications`

```http
GET /api/v1/notifications?read=false&type=alert&limit=50
Authorization: Bearer {access_token}
```

**Query Parameters:**

- `read`: `true`, `false`, `all`
- `type`: `alert`, `trade`, `system`, `info`
- `bot_id`: Filtrar por bot
- `limit`: Máximo de notificações

**Response:**

```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "notification_id": "notif-123",
        "type": "trade",
        "title": "Nova posição aberta",
        "message": "Bot 'Scalping BTC' abriu posição LONG em BTCUSDT",
        "read": false,
        "priority": "normal",
        "bot_id": "bot-123",
        "created_at": "2024-03-15T10:30:00Z"
      }
    ],
    "unread_count": 5
  }
}
```

### Mark as Read

**Endpoint:** `POST /notifications/{notification_id}/read`

```http
POST /api/v1/notifications/notif-123/read
Authorization: Bearer {access_token}
```

## 📊 Analytics

### Get Performance Metrics

**Endpoint:** `GET /analytics/performance`

```http
GET /api/v1/analytics/performance?period=30d&bot_id=bot-123
Authorization: Bearer {access_token}
```

### Get Risk Metrics

**Endpoint:** `GET /analytics/risk`

```http
GET /api/v1/analytics/risk?period=30d
Authorization: Bearer {access_token}
```

## 🌐 WebSocket API

### Connection

```javascript
const ws = new WebSocket('wss://your-domain.com/api/v1/ws');

// Authenticate after connection
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'your-jwt-token'
  }));
};
```

### Subscribe to Events

```javascript
// Subscribe to bot updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'bot_updates',
  bot_id: 'bot-123'
}));

// Subscribe to portfolio updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'portfolio_updates'
}));

// Subscribe to market data
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'market_data',
  symbols: ['BTCUSDT', 'ETHUSDT']
}));
```

### Event Types

#### Bot Update

```json
{
  "type": "bot_update",
  "bot_id": "bot-123",
  "data": {
    "status": "running",
    "pnl": 123.45,
    "positions": 3,
    "last_trade": "2024-03-15T10:30:00Z"
  }
}
```

#### New Trade

```json
{
  "type": "new_trade",
  "bot_id": "bot-123",
  "data": {
    "position_id": "pos-456",
    "symbol": "BTCUSDT",
    "side": "long",
    "quantity": 0.023,
    "price": 43250.00,
    "timestamp": "2024-03-15T10:30:00Z"
  }
}
```

#### Price Update

```json
{
  "type": "price_update",
  "symbol": "BTCUSDT",
  "data": {
    "price": 43250.00,
    "change_24h": 1.25,
    "volume": 12345.67,
    "timestamp": "2024-03-15T10:30:00Z"
  }
}
```

## 🚨 Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "Insufficient funds to execute trade",
    "details": {
      "required": 1000.00,
      "available": 500.00
    }
  },
  "timestamp": "2024-03-15T10:30:00Z",
  "request_id": "uuid-here"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Token inválido ou expirado |
| `FORBIDDEN` | 403 | Permissões insuficientes |
| `NOT_FOUND` | 404 | Recurso não encontrado |
| `VALIDATION_ERROR` | 400 | Dados de entrada inválidos |
| `INSUFFICIENT_FUNDS` | 400 | Saldo insuficiente |
| `BOT_NOT_FOUND` | 404 | Bot não encontrado |
| `BOT_ALREADY_RUNNING` | 409 | Bot já está executando |
| `POSITION_NOT_FOUND` | 404 | Posição não encontrada |
| `MARKET_CLOSED` | 400 | Mercado fechado |
| `RATE_LIMIT_EXCEEDED` | 429 | Muitas requisições |
| `INTERNAL_SERVER_ERROR` | 500 | Erro interno do servidor |

## 🔧 Rate Limiting

O sistema implementa rate limiting para proteger a API:

### Limits

- **Authentication**: 10 req/min por IP
- **Bot operations**: 60 req/min por usuário
- **Market data**: 300 req/min por usuário
- **WebSocket connections**: 10 por usuário

### Headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1710493200
```

## 📚 SDK Examples

### Python SDK

```python
from xbot_sdk import XBotClient

# Initialize client
client = XBotClient(
    base_url="https://api.example.com",
    api_key="your-api-key"
)

# Create bot
bot = client.bots.create(
    name="My Bot",
    strategy="scalping_conservative",
    capital=1000.0,
    symbols=["BTCUSDT"]
)

# Start bot
client.bots.start(bot.bot_id)

# Get portfolio
portfolio = client.portfolio.get()
print(f"Total PnL: ${portfolio.total_pnl}")
```

### JavaScript SDK

```javascript
import XBotClient from 'xbot-sdk-js';

const client = new XBotClient({
  baseURL: 'https://api.example.com',
  apiKey: 'your-api-key'
});

// Create bot
const bot = await client.bots.create({
  name: 'My Bot',
  strategy: 'scalping_conservative',
  capital: 1000.0,
  symbols: ['BTCUSDT']
});

// Start bot
await client.bots.start(bot.bot_id);

// Subscribe to updates
client.ws.subscribe('bot_updates', bot.bot_id, (update) => {
  console.log('Bot update:', update);
});
```

---

🔧 **Uma API completa e poderosa para integrar o XBot v2 em qualquer aplicação!**