# Webhooks - XBot v2

## Índice
- [Visão Geral](#visão-geral)
- [Configuração](#configuração)
- [Tipos de Webhooks](#tipos-de-webhooks)
- [Estrutura de Dados](#estrutura-de-dados)
- [Autenticação](#autenticação)
- [Implementação](#implementação)
- [Monitoramento](#monitoramento)
- [Troubleshooting](#troubleshooting)

## Visão Geral

O XBot v2 suporta webhooks para receber sinais de trading em tempo real de fontes externas como TradingView, MetaTrader, ou sistemas personalizados.

### Características Principais
- ⚡ **Processamento em tempo real** - Latência < 100ms
- 🔒 **Autenticação segura** - HMAC SHA-256
- 📊 **Monitoramento completo** - Logs e métricas
- 🔄 **Retry automático** - Tratamento de falhas
- 📋 **Validação rigorosa** - Estrutura de dados

## Configuração

### Configuração Básica

```json
{
  "webhooks": {
    "enabled": true,
    "port": 3000,
    "path": "/webhook",
    "security": {
      "enabled": true,
      "secret": "your-webhook-secret-key",
      "algorithm": "sha256"
    },
    "timeout": 5000,
    "maxRetries": 3,
    "rateLimiting": {
      "enabled": true,
      "maxRequests": 100,
      "windowMs": 60000
    }
  }
}
```

### Configuração Avançada

```json
{
  "webhooks": {
    "enabled": true,
    "port": 3000,
    "ssl": {
      "enabled": true,
      "cert": "./certs/cert.pem",
      "key": "./certs/key.pem"
    },
    "cors": {
      "enabled": true,
      "origins": ["https://tradingview.com"]
    },
    "logging": {
      "level": "info",
      "file": "./logs/webhooks.log"
    },
    "monitoring": {
      "prometheus": {
        "enabled": true,
        "port": 9090
      }
    }
  }
}
```

## Tipos de Webhooks

### 1. Sinais de Trading

#### Buy Signal
```json
{
  "type": "signal",
  "action": "buy",
  "symbol": "BTCUSDT",
  "strategy": "scalping_conservative",
  "price": 45000.00,
  "quantity": 0.001,
  "stopLoss": 44500.00,
  "takeProfit": 45500.00,
  "timeframe": "1m",
  "timestamp": "2024-01-15T10:30:00Z",
  "metadata": {
    "source": "TradingView",
    "confidence": 0.85,
    "indicators": {
      "rsi": 32.5,
      "macd": 0.12,
      "ema": 44980.0
    }
  }
}
```

#### Sell Signal
```json
{
  "type": "signal",
  "action": "sell",
  "symbol": "BTCUSDT",
  "strategy": "mean_reversion",
  "price": 45000.00,
  "quantity": 0.001,
  "stopLoss": 45500.00,
  "takeProfit": 44500.00,
  "timeframe": "5m",
  "timestamp": "2024-01-15T10:35:00Z"
}
```

### 2. Comandos de Controle

#### Pausar Trading
```json
{
  "type": "control",
  "action": "pause",
  "symbol": "BTCUSDT",
  "reason": "High volatility",
  "duration": 300,
  "timestamp": "2024-01-15T10:40:00Z"
}
```

#### Ajustar Posição
```json
{
  "type": "control",
  "action": "adjust_position",
  "symbol": "BTCUSDT",
  "positionId": "pos_123456",
  "newStopLoss": 44800.00,
  "newTakeProfit": 45200.00,
  "timestamp": "2024-01-15T10:45:00Z"
}
```

### 3. Alertas de Mercado

#### Alerta de Volatilidade
```json
{
  "type": "alert",
  "category": "volatility",
  "symbol": "BTCUSDT",
  "message": "High volatility detected",
  "severity": "high",
  "data": {
    "volatility": 0.05,
    "threshold": 0.03
  },
  "timestamp": "2024-01-15T10:50:00Z"
}
```

## Estrutura de Dados

### Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `type` | string | Tipo do webhook (signal, control, alert) |
| `action` | string | Ação a ser executada |
| `symbol` | string | Par de moedas |
| `timestamp` | string | Timestamp ISO 8601 |

### Campos Opcionais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `strategy` | string | Nome da estratégia |
| `price` | number | Preço de referência |
| `quantity` | number | Quantidade |
| `stopLoss` | number | Stop loss |
| `takeProfit` | number | Take profit |
| `metadata` | object | Dados adicionais |

### Validação de Schema

```javascript
const webhookSchema = {
  type: "object",
  required: ["type", "action", "symbol", "timestamp"],
  properties: {
    type: {
      type: "string",
      enum: ["signal", "control", "alert"]
    },
    action: {
      type: "string",
      enum: ["buy", "sell", "pause", "resume", "adjust_position"]
    },
    symbol: {
      type: "string",
      pattern: "^[A-Z]{3,}USDT$"
    },
    price: {
      type: "number",
      minimum: 0
    },
    quantity: {
      type: "number",
      minimum: 0
    },
    timestamp: {
      type: "string",
      format: "date-time"
    }
  }
};
```

## Autenticação

### HMAC Signature

O XBot v2 usa HMAC SHA-256 para autenticação de webhooks:

```javascript
const crypto = require('crypto');

function generateSignature(payload, secret) {
  return crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(payload))
    .digest('hex');
}

// Exemplo de uso
const payload = {
  type: "signal",
  action: "buy",
  symbol: "BTCUSDT"
};

const signature = generateSignature(payload, 'your-secret-key');
```

### Headers Necessários

```http
POST /webhook HTTP/1.1
Host: your-bot-server.com
Content-Type: application/json
X-Webhook-Signature: sha256=<signature>
X-Webhook-Timestamp: 1642248600
User-Agent: YourService/1.0
```

### Verificação de Timestamp

```javascript
function verifyTimestamp(timestamp, tolerance = 300) {
  const now = Math.floor(Date.now() / 1000);
  const webhookTime = parseInt(timestamp);
  
  return Math.abs(now - webhookTime) <= tolerance;
}
```

## Implementação

### Servidor Webhook Básico

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.json());

// Middleware de autenticação
function authenticateWebhook(req, res, next) {
  const signature = req.headers['x-webhook-signature'];
  const timestamp = req.headers['x-webhook-timestamp'];
  
  if (!verifyTimestamp(timestamp)) {
    return res.status(401).json({ error: 'Invalid timestamp' });
  }
  
  const expectedSignature = generateSignature(req.body, process.env.WEBHOOK_SECRET);
  
  if (signature !== `sha256=${expectedSignature}`) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  next();
}

// Endpoint principal
app.post('/webhook', authenticateWebhook, async (req, res) => {
  try {
    const webhook = req.body;
    
    // Validar schema
    const isValid = validateSchema(webhook);
    if (!isValid) {
      return res.status(400).json({ error: 'Invalid schema' });
    }
    
    // Processar webhook
    await processWebhook(webhook);
    
    res.json({ status: 'success' });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(3000, () => {
  console.log('Webhook server running on port 3000');
});
```

### Processamento de Webhooks

```javascript
async function processWebhook(webhook) {
  switch (webhook.type) {
    case 'signal':
      await processSignal(webhook);
      break;
    case 'control':
      await processControl(webhook);
      break;
    case 'alert':
      await processAlert(webhook);
      break;
    default:
      throw new Error(`Unknown webhook type: ${webhook.type}`);
  }
}

async function processSignal(signal) {
  const { action, symbol, strategy, price, quantity, stopLoss, takeProfit } = signal;
  
  if (action === 'buy') {
    await tradingEngine.executeBuyOrder({
      symbol,
      strategy,
      price,
      quantity,
      stopLoss,
      takeProfit
    });
  } else if (action === 'sell') {
    await tradingEngine.executeSellOrder({
      symbol,
      strategy,
      price,
      quantity,
      stopLoss,
      takeProfit
    });
  }
}
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const webhookLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minuto
  max: 100, // máximo 100 requests por minuto
  message: {
    error: 'Too many webhook requests, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/webhook', webhookLimiter);
```

## Monitoramento

### Métricas Prometheus

```javascript
const client = require('prom-client');

const webhookCounter = new client.Counter({
  name: 'webhook_requests_total',
  help: 'Total number of webhook requests',
  labelNames: ['type', 'status']
});

const webhookDuration = new client.Histogram({
  name: 'webhook_processing_duration_seconds',
  help: 'Time spent processing webhooks',
  labelNames: ['type']
});

// Uso no handler
app.post('/webhook', async (req, res) => {
  const start = Date.now();
  
  try {
    await processWebhook(req.body);
    webhookCounter.inc({ type: req.body.type, status: 'success' });
    res.json({ status: 'success' });
  } catch (error) {
    webhookCounter.inc({ type: req.body.type, status: 'error' });
    res.status(500).json({ error: 'Internal server error' });
  } finally {
    const duration = (Date.now() - start) / 1000;
    webhookDuration.observe({ type: req.body.type }, duration);
  }
});
```

### Dashboard de Monitoramento

```javascript
// Endpoint de status
app.get('/webhook/status', (req, res) => {
  res.json({
    status: 'running',
    uptime: process.uptime(),
    requests: {
      total: webhookCounter.get(),
      lastMinute: getRecentRequests(60)
    },
    performance: {
      averageLatency: getAverageLatency(),
      errorRate: getErrorRate()
    }
  });
});
```

## Troubleshooting

### Problemas Comuns

#### 1. Signature Mismatch
```bash
# Verificar se o secret está correto
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=correct_signature" \
  -d '{"type":"signal","action":"buy","symbol":"BTCUSDT","timestamp":"2024-01-15T10:30:00Z"}'
```

#### 2. Timeout Issues
```javascript
// Configurar timeout adequado
const server = app.listen(3000, () => {
  server.timeout = 5000; // 5 segundos
});
```

#### 3. Rate Limiting
```javascript
// Implementar exponential backoff
async function retryWebhook(webhook, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await processWebhook(webhook);
      return;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000); // exponential backoff
    }
  }
}
```

### Logs de Debug

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'webhook-debug.log' }),
    new winston.transports.Console()
  ]
});

// Uso nos handlers
app.post('/webhook', (req, res) => {
  logger.debug('Received webhook', {
    headers: req.headers,
    body: req.body,
    ip: req.ip
  });
});
```

### Teste de Conectividade

```bash
# Teste básico
curl -X GET http://localhost:3000/webhook/health

# Teste com payload
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=test" \
  -d '{"type":"signal","action":"buy","symbol":"BTCUSDT","timestamp":"2024-01-15T10:30:00Z"}'
```

## Integração com TradingView

### Pine Script Exemplo

```pinescript
//@version=5
strategy("XBot Webhook", overlay=true)

// Configurações
webhook_url = input.string("https://your-server.com/webhook", "Webhook URL")
secret = input.string("your-secret", "Secret Key")

// Sinais
longCondition = ta.crossover(ta.sma(close, 14), ta.sma(close, 28))
shortCondition = ta.crossunder(ta.sma(close, 14), ta.sma(close, 28))

// Enviar webhook
if longCondition
    strategy.entry("Long", strategy.long)
    alert('{"type":"signal","action":"buy","symbol":"' + syminfo.ticker + '","price":' + str.tostring(close) + ',"timestamp":"' + str.tostring(timenow) + '"}', alert.freq_once_per_bar)

if shortCondition
    strategy.entry("Short", strategy.short)
    alert('{"type":"signal","action":"sell","symbol":"' + syminfo.ticker + '","price":' + str.tostring(close) + ',"timestamp":"' + str.tostring(timenow) + '"}', alert.freq_once_per_bar)
```

## Boas Práticas

### Segurança
- ✅ Sempre use HTTPS em produção
- ✅ Valide timestamps para prevenir replay attacks
- ✅ Implemente rate limiting
- ✅ Use secrets fortes e únicos
- ✅ Monitore tentativas de autenticação falhadas

### Performance
- ✅ Processe webhooks de forma assíncrona
- ✅ Use connection pooling
- ✅ Implemente circuit breakers
- ✅ Cache dados frequentemente acessados
- ✅ Monitore latência e throughput

### Confiabilidade
- ✅ Implemente retry automático
- ✅ Use dead letter queues
- ✅ Mantenha logs detalhados
- ✅ Configure alertas de falha
- ✅ Teste regularmente a conectividade