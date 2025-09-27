# SDK - XBot v2

## Índice
- [Visão Geral](#visão-geral)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [API Reference](#api-reference)
- [Exemplos de Uso](#exemplos-de-uso)
- [TypeScript Support](#typescript-support)
- [Error Handling](#error-handling)
- [Monitoramento](#monitoramento)

## Visão Geral

O XBot v2 SDK fornece uma interface programática completa para interagir com o sistema de trading. Desenvolvido em JavaScript/TypeScript com suporte nativo ao Node.js.

### Características Principais
- 🚀 **Performance otimizada** - WebSocket e REST APIs
- 🔒 **Autenticação segura** - JWT e API Keys
- 📊 **Real-time data** - Streaming de preços e ordens
- 🛡️ **Type-safe** - Suporte completo ao TypeScript
- 🔄 **Auto-retry** - Recuperação automática de falhas
- 📈 **Rate limiting** - Controle de requisições

## Instalação

### NPM
```bash
npm install xbot-v2-sdk
```

### Yarn
```bash
yarn add xbot-v2-sdk
```

### CDN
```html
<script src="https://cdn.jsdelivr.net/npm/xbot-v2-sdk@latest/dist/xbot.min.js"></script>
```

## Configuração

### Configuração Básica

```javascript
const { XBotClient } = require('xbot-v2-sdk');

const client = new XBotClient({
  apiKey: 'your-api-key',
  apiSecret: 'your-api-secret',
  baseUrl: 'https://api.xbot.com',
  testnet: false // true para ambiente de teste
});
```

### Configuração Avançada

```javascript
const client = new XBotClient({
  apiKey: process.env.XBOT_API_KEY,
  apiSecret: process.env.XBOT_API_SECRET,
  baseUrl: 'https://api.xbot.com',
  testnet: process.env.NODE_ENV === 'development',
  timeout: 30000, // 30 segundos
  retries: 3,
  rateLimiting: {
    enabled: true,
    maxRequests: 1200,
    interval: 60000 // por minuto
  },
  websocket: {
    enabled: true,
    reconnect: true,
    maxReconnectAttempts: 5
  }
});
```

## API Reference

### Autenticação

#### Login
```javascript
await client.auth.login('username', 'password');
```

#### Verificar Token
```javascript
const isValid = await client.auth.verifyToken();
```

#### Logout
```javascript
await client.auth.logout();
```

### Dados de Mercado

#### Obter Preços
```javascript
// Preço atual
const price = await client.market.getPrice('BTCUSDT');

// Múltiplos preços
const prices = await client.market.getPrices(['BTCUSDT', 'ETHUSDT']);

// Histórico de preços
const history = await client.market.getHistory('BTCUSDT', '1h', 100);
```

#### Ticker 24h
```javascript
const ticker = await client.market.getTicker24h('BTCUSDT');
console.log({
  symbol: ticker.symbol,
  price: ticker.price,
  change: ticker.priceChangePercent,
  volume: ticker.volume
});
```

#### Order Book
```javascript
const orderBook = await client.market.getOrderBook('BTCUSDT', 100);
console.log({
  bids: orderBook.bids.slice(0, 5),
  asks: orderBook.asks.slice(0, 5)
});
```

### Trading

#### Executar Ordem
```javascript
// Ordem de compra
const buyOrder = await client.trading.buy({
  symbol: 'BTCUSDT',
  quantity: 0.001,
  price: 45000, // opcional para market order
  type: 'LIMIT', // MARKET, LIMIT, STOP_LOSS, STOP_LOSS_LIMIT
  timeInForce: 'GTC' // GTC, IOC, FOK
});

// Ordem de venda
const sellOrder = await client.trading.sell({
  symbol: 'BTCUSDT',
  quantity: 0.001,
  price: 46000,
  type: 'LIMIT'
});
```

#### Cancelar Ordem
```javascript
await client.trading.cancelOrder('BTCUSDT', orderId);

// Cancelar todas as ordens
await client.trading.cancelAllOrders('BTCUSDT');
```

#### Consultar Ordens
```javascript
// Ordem específica
const order = await client.trading.getOrder('BTCUSDT', orderId);

// Ordens abertas
const openOrders = await client.trading.getOpenOrders('BTCUSDT');

// Histórico de ordens
const orderHistory = await client.trading.getOrderHistory('BTCUSDT', {
  limit: 100,
  startTime: Date.now() - (24 * 60 * 60 * 1000) // últimas 24h
});
```

### Portfolio

#### Saldos
```javascript
// Todos os saldos
const balances = await client.portfolio.getBalances();

// Saldo específico
const btcBalance = await client.portfolio.getBalance('BTC');
```

#### Posições
```javascript
// Posições abertas
const positions = await client.portfolio.getPositions();

// Posição específica
const btcPosition = await client.portfolio.getPosition('BTCUSDT');
```

#### Relatórios
```javascript
// PnL por período
const pnl = await client.portfolio.getPnL({
  startDate: '2024-01-01',
  endDate: '2024-01-31'
});

// Estatísticas de trading
const stats = await client.portfolio.getTradingStats();
```

### Estratégias

#### Listar Estratégias
```javascript
const strategies = await client.strategies.getAll();
```

#### Obter Estratégia
```javascript
const strategy = await client.strategies.get('scalping_conservative');
```

#### Executar Estratégia
```javascript
await client.strategies.execute('scalping_conservative', {
  symbol: 'BTCUSDT',
  amount: 100,
  parameters: {
    rsiPeriod: 14,
    rsiOversold: 30,
    rsiOverbought: 70
  }
});
```

#### Parar Estratégia
```javascript
await client.strategies.stop('scalping_conservative', 'BTCUSDT');
```

## Exemplos de Uso

### Trading Bot Básico

```javascript
const { XBotClient } = require('xbot-v2-sdk');

class TradingBot {
  constructor(apiKey, apiSecret) {
    this.client = new XBotClient({
      apiKey,
      apiSecret,
      testnet: true
    });
  }
  
  async start() {
    try {
      // Verificar conexão
      await this.client.auth.verifyToken();
      console.log('Bot conectado com sucesso!');
      
      // Configurar WebSocket para preços em tempo real
      this.client.websocket.onPrice('BTCUSDT', (data) => {
        this.onPriceUpdate(data);
      });
      
      // Iniciar monitoramento
      this.monitorMarket();
      
    } catch (error) {
      console.error('Erro ao iniciar bot:', error);
    }
  }
  
  onPriceUpdate(data) {
    console.log(`${data.symbol}: $${data.price}`);
    
    // Lógica de trading simples
    if (data.price < 45000) {
      this.considerBuy(data.symbol, data.price);
    } else if (data.price > 47000) {
      this.considerSell(data.symbol, data.price);
    }
  }
  
  async considerBuy(symbol, price) {
    try {
      const balance = await this.client.portfolio.getBalance('USDT');
      
      if (balance.available > 100) {
        const order = await this.client.trading.buy({
          symbol,
          quantity: 100 / price,
          type: 'MARKET'
        });
        
        console.log('Ordem de compra executada:', order);
      }
    } catch (error) {
      console.error('Erro ao comprar:', error);
    }
  }
  
  async considerSell(symbol, price) {
    try {
      const balance = await this.client.portfolio.getBalance('BTC');
      
      if (balance.available > 0.001) {
        const order = await this.client.trading.sell({
          symbol,
          quantity: balance.available,
          type: 'MARKET'
        });
        
        console.log('Ordem de venda executada:', order);
      }
    } catch (error) {
      console.error('Erro ao vender:', error);
    }
  }
  
  async monitorMarket() {
    setInterval(async () => {
      try {
        const positions = await this.client.portfolio.getPositions();
        console.log('Posições atuais:', positions);
      } catch (error) {
        console.error('Erro ao consultar posições:', error);
      }
    }, 30000); // a cada 30 segundos
  }
}

// Uso
const bot = new TradingBot('api-key', 'api-secret');
bot.start();
```

### Monitor de Portfolio

```javascript
class PortfolioMonitor {
  constructor(client) {
    this.client = client;
    this.alerts = [];
  }
  
  addAlert(condition, action) {
    this.alerts.push({ condition, action });
  }
  
  async start() {
    setInterval(async () => {
      await this.checkAlerts();
    }, 5000);
  }
  
  async checkAlerts() {
    try {
      const portfolio = await this.client.portfolio.getBalances();
      const totalValue = await this.calculateTotalValue(portfolio);
      
      for (const alert of this.alerts) {
        if (alert.condition(totalValue, portfolio)) {
          await alert.action(totalValue, portfolio);
        }
      }
    } catch (error) {
      console.error('Erro ao verificar alertas:', error);
    }
  }
  
  async calculateTotalValue(portfolio) {
    let total = 0;
    
    for (const asset of portfolio) {
      if (asset.asset === 'USDT') {
        total += parseFloat(asset.free);
      } else {
        const price = await this.client.market.getPrice(`${asset.asset}USDT`);
        total += parseFloat(asset.free) * parseFloat(price);
      }
    }
    
    return total;
  }
}

// Uso
const monitor = new PortfolioMonitor(client);

// Alerta de perda
monitor.addAlert(
  (totalValue) => totalValue < 5000,
  (totalValue) => {
    console.log(`🚨 Alerta: Portfolio abaixo de $5000 (${totalValue})`);
    // Enviar email, SMS, etc.
  }
);

// Alerta de lucro
monitor.addAlert(
  (totalValue) => totalValue > 10000,
  (totalValue) => {
    console.log(`🎉 Meta atingida: Portfolio acima de $10000 (${totalValue})`);
  }
);

monitor.start();
```

### Análise Técnica

```javascript
class TechnicalAnalysis {
  constructor(client) {
    this.client = client;
  }
  
  async getIndicators(symbol, interval = '1h', limit = 100) {
    const candles = await this.client.market.getHistory(symbol, interval, limit);
    
    return {
      sma: this.calculateSMA(candles, 20),
      ema: this.calculateEMA(candles, 20),
      rsi: this.calculateRSI(candles, 14),
      macd: this.calculateMACD(candles)
    };
  }
  
  calculateSMA(candles, period) {
    const prices = candles.map(c => parseFloat(c.close));
    const sma = [];
    
    for (let i = period - 1; i < prices.length; i++) {
      const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
      sma.push(sum / period);
    }
    
    return sma;
  }
  
  calculateEMA(candles, period) {
    const prices = candles.map(c => parseFloat(c.close));
    const ema = [];
    const k = 2 / (period + 1);
    
    ema[0] = prices[0];
    
    for (let i = 1; i < prices.length; i++) {
      ema[i] = prices[i] * k + ema[i - 1] * (1 - k);
    }
    
    return ema;
  }
  
  calculateRSI(candles, period) {
    const prices = candles.map(c => parseFloat(c.close));
    const rsi = [];
    
    for (let i = period; i < prices.length; i++) {
      const gains = [];
      const losses = [];
      
      for (let j = i - period + 1; j <= i; j++) {
        const diff = prices[j] - prices[j - 1];
        if (diff > 0) {
          gains.push(diff);
          losses.push(0);
        } else {
          gains.push(0);
          losses.push(Math.abs(diff));
        }
      }
      
      const avgGain = gains.reduce((a, b) => a + b, 0) / period;
      const avgLoss = losses.reduce((a, b) => a + b, 0) / period;
      
      const rs = avgGain / avgLoss;
      rsi.push(100 - (100 / (1 + rs)));
    }
    
    return rsi;
  }
  
  async generateSignal(symbol) {
    const indicators = await this.getIndicators(symbol);
    const currentRSI = indicators.rsi[indicators.rsi.length - 1];
    const currentSMA = indicators.sma[indicators.sma.length - 1];
    const currentPrice = await this.client.market.getPrice(symbol);
    
    if (currentRSI < 30 && currentPrice < currentSMA) {
      return { action: 'BUY', confidence: 0.8 };
    } else if (currentRSI > 70 && currentPrice > currentSMA) {
      return { action: 'SELL', confidence: 0.8 };
    }
    
    return { action: 'HOLD', confidence: 0.5 };
  }
}

// Uso
const analysis = new TechnicalAnalysis(client);
const signal = await analysis.generateSignal('BTCUSDT');
console.log('Sinal gerado:', signal);
```

## TypeScript Support

### Tipos e Interfaces

```typescript
import { XBotClient, Order, Balance, Position } from 'xbot-v2-sdk';

interface TradingConfig {
  symbol: string;
  strategy: string;
  amount: number;
  stopLoss: number;
  takeProfit: number;
}

class TypedTradingBot {
  private client: XBotClient;
  
  constructor(apiKey: string, apiSecret: string) {
    this.client = new XBotClient({
      apiKey,
      apiSecret,
      testnet: true
    });
  }
  
  async placeOrder(config: TradingConfig): Promise<Order> {
    return await this.client.trading.buy({
      symbol: config.symbol,
      quantity: config.amount,
      type: 'LIMIT',
      stopPrice: config.stopLoss,
      timeInForce: 'GTC'
    });
  }
  
  async getPortfolio(): Promise<Balance[]> {
    return await this.client.portfolio.getBalances();
  }
}
```

### Tipos Personalizados

```typescript
// types/trading.ts
export interface CustomStrategy {
  name: string;
  parameters: Record<string, any>;
  signals: TradingSignal[];
}

export interface TradingSignal {
  timestamp: Date;
  symbol: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  indicators: {
    rsi?: number;
    macd?: number;
    sma?: number;
  };
}

export interface BacktestResult {
  totalReturn: number;
  maxDrawdown: number;
  sharpeRatio: number;
  winRate: number;
  trades: Trade[];
}
```

## Error Handling

### Tipos de Erro

```javascript
const { XBotError, NetworkError, AuthError, RateLimitError } = require('xbot-v2-sdk');

try {
  await client.trading.buy({
    symbol: 'BTCUSDT',
    quantity: 0.001,
    type: 'MARKET'
  });
} catch (error) {
  if (error instanceof AuthError) {
    console.log('Erro de autenticação - verificar credenciais');
  } else if (error instanceof RateLimitError) {
    console.log('Rate limit excedido - aguardar:', error.retryAfter);
  } else if (error instanceof NetworkError) {
    console.log('Erro de rede - tentar novamente');
  } else {
    console.log('Erro desconhecido:', error.message);
  }
}
```

### Retry Automático

```javascript
async function executeWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      
      const delay = Math.pow(2, i) * 1000; // exponential backoff
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Uso
const order = await executeWithRetry(() => 
  client.trading.buy({
    symbol: 'BTCUSDT',
    quantity: 0.001
  })
);
```

## Monitoramento

### Métricas

```javascript
const monitor = client.monitoring;

// Monitorar latência
monitor.onLatency((metric) => {
  console.log(`Latência: ${metric.duration}ms para ${metric.endpoint}`);
});

// Monitorar rate limits
monitor.onRateLimit((info) => {
  console.log(`Rate limit: ${info.remaining}/${info.limit} requests`);
});

// Monitorar erros
monitor.onError((error) => {
  console.error('Erro capturado:', error);
});
```

### Health Check

```javascript
async function healthCheck() {
  try {
    const status = await client.getStatus();
    
    console.log({
      connected: status.connected,
      latency: status.latency,
      rateLimits: status.rateLimits,
      websocket: status.websocket
    });
    
    return status.connected;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}

// Executar health check periodicamente
setInterval(healthCheck, 30000);
```

## WebSocket Streams

### Preços em Tempo Real

```javascript
// Stream de preços
client.websocket.subscribeToPrice('BTCUSDT', (data) => {
  console.log(`${data.symbol}: $${data.price}`);
});

// Stream de order book
client.websocket.subscribeToOrderBook('BTCUSDT', (data) => {
  console.log('Order Book atualizado:', {
    bids: data.bids.slice(0, 5),
    asks: data.asks.slice(0, 5)
  });
});

// Stream de trades
client.websocket.subscribeToTrades('BTCUSDT', (data) => {
  console.log('Novo trade:', {
    price: data.price,
    quantity: data.quantity,
    side: data.isBuyerMaker ? 'sell' : 'buy'
  });
});
```

### Eventos de Conta

```javascript
// Atualizações de ordens
client.websocket.subscribeToOrders((order) => {
  console.log('Ordem atualizada:', {
    symbol: order.symbol,
    status: order.status,
    executedQty: order.executedQty
  });
});

// Atualizações de saldo
client.websocket.subscribeToBalance((balance) => {
  console.log('Saldo atualizado:', {
    asset: balance.asset,
    free: balance.free,
    locked: balance.locked
  });
});
```

## Configuração Avançada

### Proxy

```javascript
const client = new XBotClient({
  apiKey: 'your-key',
  apiSecret: 'your-secret',
  proxy: {
    host: '127.0.0.1',
    port: 8080,
    auth: {
      username: 'user',
      password: 'pass'
    }
  }
});
```

### SSL/TLS

```javascript
const fs = require('fs');

const client = new XBotClient({
  apiKey: 'your-key',
  apiSecret: 'your-secret',
  https: {
    cert: fs.readFileSync('./certs/client.crt'),
    key: fs.readFileSync('./certs/client.key'),
    ca: fs.readFileSync('./certs/ca.crt')
  }
});
```

### Logging

```javascript
const client = new XBotClient({
  apiKey: 'your-key',
  apiSecret: 'your-secret',
  logging: {
    level: 'debug', // error, warn, info, debug
    file: './logs/xbot-sdk.log',
    maxFiles: 5,
    maxSize: '10m'
  }
});
```