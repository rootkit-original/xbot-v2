# Tutoriais Avançados - XBot v2

## Índice
- [Introdução](#introdução)
- [Setup do Ambiente](#setup-do-ambiente)
- [Análise Técnica Avançada](#análise-técnica-avançada)
- [Algoritmos de Machine Learning](#algoritmos-de-machine-learning)
- [Backtesting Avançado](#backtesting-avançado)
- [Otimização de Parâmetros](#otimização-de-parâmetros)
- [Trading Multi-Exchange](#trading-multi-exchange)
- [Gestão de Risco Avançada](#gestão-de-risco-avançada)

## Introdução

Este guia apresenta tutoriais avançados para usuários experientes que desejam maximizar o potencial do XBot v2. Inclui técnicas de análise quantitativa, machine learning e otimização algorítmica.

### Pré-requisitos
- ✅ Conhecimento básico do XBot v2
- ✅ Experiência em programação (JavaScript/Python)
- ✅ Fundamentos de análise técnica
- ✅ Conceitos básicos de estatística
- ✅ Experiência com APIs de trading

## Setup do Ambiente

### Ambiente de Desenvolvimento

```bash
# Clonar repositório de exemplos
git clone https://github.com/xbot-v2/advanced-tutorials.git
cd advanced-tutorials

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env
```

### Configuração Avançada

```javascript
// config/advanced.js
module.exports = {
  trading: {
    maxConcurrentPositions: 5,
    riskPerTrade: 0.02,
    maxDailyLoss: 0.1,
    slippage: 0.001
  },
  analysis: {
    lookbackPeriod: 1000,
    indicators: {
      rsi: { period: 14, overbought: 70, oversold: 30 },
      macd: { fast: 12, slow: 26, signal: 9 },
      bollinger: { period: 20, stdDev: 2 }
    }
  },
  ml: {
    modelPath: './models/price_prediction.json',
    features: ['price', 'volume', 'rsi', 'macd', 'bb_position'],
    predictionHorizon: 24
  }
};
```

## Análise Técnica Avançada

### Indicadores Personalizados

```javascript
class AdvancedIndicators {
  constructor() {
    this.cache = new Map();
  }
  
  // Ichimoku Kinko Hyo
  calculateIchimoku(candles, periods = { tenkan: 9, kijun: 26, senkou: 52 }) {
    const highs = candles.map(c => c.high);
    const lows = candles.map(c => c.low);
    const closes = candles.map(c => c.close);
    
    const tenkanSen = this.calculateKijunSen(highs, lows, periods.tenkan);
    const kijunSen = this.calculateKijunSen(highs, lows, periods.kijun);
    const senkouSpanA = tenkanSen.map((t, i) => (t + kijunSen[i]) / 2);
    const senkouSpanB = this.calculateKijunSen(highs, lows, periods.senkou);
    const chikouSpan = closes.map((c, i) => i >= 26 ? closes[i - 26] : null);
    
    return {
      tenkanSen,
      kijunSen,
      senkouSpanA,
      senkouSpanB,
      chikouSpan
    };
  }
  
  calculateKijunSen(highs, lows, period) {
    const result = [];
    for (let i = period - 1; i < highs.length; i++) {
      const periodHighs = highs.slice(i - period + 1, i + 1);
      const periodLows = lows.slice(i - period + 1, i + 1);
      const highest = Math.max(...periodHighs);
      const lowest = Math.min(...periodLows);
      result.push((highest + lowest) / 2);
    }
    return result;
  }
  
  // Volume Profile
  calculateVolumeProfile(candles, bins = 20) {
    const prices = candles.map(c => c.close);
    const volumes = candles.map(c => c.volume);
    
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const priceRange = maxPrice - minPrice;
    const binSize = priceRange / bins;
    
    const profile = Array(bins).fill(0).map((_, i) => ({
      price: minPrice + (i * binSize),
      volume: 0
    }));
    
    candles.forEach(candle => {
      const binIndex = Math.min(
        Math.floor((candle.close - minPrice) / binSize),
        bins - 1
      );
      profile[binIndex].volume += candle.volume;
    });
    
    return profile.sort((a, b) => b.volume - a.volume);
  }
  
  // Market Regime Detection
  detectMarketRegime(candles, lookback = 50) {
    const returns = this.calculateReturns(candles);
    const volatility = this.calculateVolatility(returns, lookback);
    const trend = this.calculateTrend(candles, lookback);
    
    if (volatility > 0.03 && Math.abs(trend) < 0.01) {
      return 'HIGH_VOLATILITY';
    } else if (trend > 0.02) {
      return 'BULL_TREND';
    } else if (trend < -0.02) {
      return 'BEAR_TREND';
    } else if (volatility < 0.01) {
      return 'LOW_VOLATILITY';
    }
    
    return 'SIDEWAYS';
  }
  
  calculateReturns(candles) {
    return candles.slice(1).map((candle, i) => 
      (candle.close - candles[i].close) / candles[i].close
    );
  }
  
  calculateVolatility(returns, period) {
    const mean = returns.slice(-period).reduce((sum, r) => sum + r, 0) / period;
    const variance = returns.slice(-period).reduce((sum, r) => 
      sum + Math.pow(r - mean, 2), 0) / period;
    return Math.sqrt(variance * 252); // Anualizada
  }
  
  calculateTrend(candles, period) {
    const prices = candles.slice(-period).map(c => c.close);
    const n = prices.length;
    const x = Array.from({length: n}, (_, i) => i);
    
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = prices.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * prices[i], 0);
    const sumXX = x.reduce((sum, xi) => sum + xi * xi, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    return slope / prices[prices.length - 1]; // Normalizado
  }
}

// Uso
const indicators = new AdvancedIndicators();
const ichimoku = indicators.calculateIchimoku(candles);
const volumeProfile = indicators.calculateVolumeProfile(candles);
const regime = indicators.detectMarketRegime(candles);
```

### Pattern Recognition

```javascript
class PatternRecognition {
  constructor() {
    this.patterns = {
      HAMMER: this.isHammer.bind(this),
      DOJI: this.isDoji.bind(this),
      ENGULFING: this.isEngulfing.bind(this),
      MORNING_STAR: this.isMorningStar.bind(this),
      EVENING_STAR: this.isEveningStar.bind(this)
    };
  }
  
  findPatterns(candles, lookback = 100) {
    const results = [];
    
    for (let i = lookback; i < candles.length; i++) {
      const current = candles[i];
      const previous = candles.slice(i - 2, i + 1);
      
      for (const [pattern, detector] of Object.entries(this.patterns)) {
        if (detector(previous, current)) {
          results.push({
            pattern,
            timestamp: current.timestamp,
            price: current.close,
            confidence: this.calculateConfidence(pattern, previous)
          });
        }
      }
    }
    
    return results;
  }
  
  isHammer(candles) {
    const candle = candles[candles.length - 1];
    const body = Math.abs(candle.close - candle.open);
    const totalRange = candle.high - candle.low;
    const lowerShadow = Math.min(candle.open, candle.close) - candle.low;
    const upperShadow = candle.high - Math.max(candle.open, candle.close);
    
    return (
      lowerShadow >= 2 * body &&
      upperShadow <= body * 0.1 &&
      body <= totalRange * 0.3
    );
  }
  
  isDoji(candles) {
    const candle = candles[candles.length - 1];
    const body = Math.abs(candle.close - candle.open);
    const totalRange = candle.high - candle.low;
    
    return body <= totalRange * 0.1;
  }
  
  isEngulfing(candles) {
    if (candles.length < 2) return false;
    
    const prev = candles[candles.length - 2];
    const curr = candles[candles.length - 1];
    
    const prevBullish = prev.close > prev.open;
    const currBullish = curr.close > curr.open;
    
    return (
      prevBullish !== currBullish &&
      curr.open < Math.min(prev.open, prev.close) &&
      curr.close > Math.max(prev.open, prev.close)
    );
  }
  
  calculateConfidence(pattern, candles) {
    // Implementar lógica de confiança baseada em contexto
    const volume = candles[candles.length - 1].volume;
    const avgVolume = candles.slice(0, -1).reduce((sum, c) => sum + c.volume, 0) / (candles.length - 1);
    
    let confidence = 0.5;
    
    // Aumentar confiança com volume acima da média
    if (volume > avgVolume * 1.5) {
      confidence += 0.2;
    }
    
    // Ajustar baseado no padrão específico
    switch (pattern) {
      case 'HAMMER':
        confidence += 0.1;
        break;
      case 'ENGULFING':
        confidence += 0.15;
        break;
    }
    
    return Math.min(confidence, 1.0);
  }
}
```

## Algoritmos de Machine Learning

### Modelo de Predição de Preços

```javascript
const tf = require('@tensorflow/tfjs-node');

class PricePredictionModel {
  constructor(config) {
    this.config = config;
    this.model = null;
    this.scaler = {
      mean: {},
      std: {}
    };
  }
  
  async buildModel(inputShape) {
    this.model = tf.sequential({
      layers: [
        tf.layers.lstm({
          units: 128,
          returnSequences: true,
          inputShape: [inputShape, this.config.features.length]
        }),
        tf.layers.dropout({ rate: 0.2 }),
        tf.layers.lstm({
          units: 64,
          returnSequences: true
        }),
        tf.layers.dropout({ rate: 0.2 }),
        tf.layers.lstm({
          units: 32,
          returnSequences: false
        }),
        tf.layers.dropout({ rate: 0.1 }),
        tf.layers.dense({ units: 16, activation: 'relu' }),
        tf.layers.dense({ units: 1, activation: 'linear' })
      ]
    });
    
    this.model.compile({
      optimizer: tf.train.adam(0.001),
      loss: 'meanSquaredError',
      metrics: ['mae']
    });
  }
  
  prepareData(candles, indicators) {
    const features = [];
    
    for (let i = 0; i < candles.length; i++) {
      const candle = candles[i];
      const feature = [
        candle.close,
        candle.volume,
        indicators.rsi[i] || 50,
        indicators.macd[i] || 0,
        indicators.bb_position[i] || 0.5
      ];
      features.push(feature);
    }
    
    return this.normalizeData(features);
  }
  
  normalizeData(data) {
    const normalized = [];
    const features = data[0].length;
    
    // Calcular média e desvio padrão para cada feature
    for (let f = 0; f < features; f++) {
      const values = data.map(row => row[f]);
      this.scaler.mean[f] = values.reduce((a, b) => a + b) / values.length;
      this.scaler.std[f] = Math.sqrt(
        values.reduce((sum, val) => sum + Math.pow(val - this.scaler.mean[f], 2), 0) / values.length
      );
    }
    
    // Normalizar dados
    for (let row of data) {
      const normalizedRow = row.map((val, f) => 
        (val - this.scaler.mean[f]) / this.scaler.std[f]
      );
      normalized.push(normalizedRow);
    }
    
    return normalized;
  }
  
  createSequences(data, sequenceLength = 60) {
    const sequences = [];
    const targets = [];
    
    for (let i = sequenceLength; i < data.length; i++) {
      const sequence = data.slice(i - sequenceLength, i);
      const target = data[i][0]; // Predizer o preço (primeira feature)
      
      sequences.push(sequence);
      targets.push(target);
    }
    
    return {
      sequences: tf.tensor3d(sequences),
      targets: tf.tensor2d(targets, [targets.length, 1])
    };
  }
  
  async train(candles, indicators, epochs = 100) {
    const data = this.prepareData(candles, indicators);
    const { sequences, targets } = this.createSequences(data);
    
    await this.buildModel(60);
    
    const history = await this.model.fit(sequences, targets, {
      epochs,
      batchSize: 32,
      validationSplit: 0.2,
      callbacks: {
        onEpochEnd: (epoch, logs) => {
          console.log(`Epoch ${epoch + 1}: loss = ${logs.loss.toFixed(4)}, val_loss = ${logs.val_loss.toFixed(4)}`);
        }
      }
    });
    
    return history;
  }
  
  async predict(recentData) {
    if (!this.model) {
      throw new Error('Model not trained yet');
    }
    
    const normalizedData = this.normalizeData(recentData);
    const inputTensor = tf.tensor3d([normalizedData]);
    
    const prediction = await this.model.predict(inputTensor);
    const denormalizedPrediction = prediction.dataSync()[0] * this.scaler.std[0] + this.scaler.mean[0];
    
    return denormalizedPrediction;
  }
  
  async saveModel(path) {
    await this.model.save(`file://${path}`);
  }
  
  async loadModel(path) {
    this.model = await tf.loadLayersModel(`file://${path}`);
  }
}

// Uso
const mlModel = new PricePredictionModel(config.ml);
await mlModel.train(historicalCandles, indicators);
const prediction = await mlModel.predict(recentData);
```

### Clustering de Padrões

```javascript
class PatternClustering {
  constructor(k = 5) {
    this.k = k;
    this.centroids = [];
    this.clusters = [];
  }
  
  extractPatterns(candles, patternLength = 20) {
    const patterns = [];
    
    for (let i = patternLength; i < candles.length; i++) {
      const pattern = candles.slice(i - patternLength, i).map(c => ({
        priceChange: (c.close - candles[i - patternLength].close) / candles[i - patternLength].close,
        volumeRatio: c.volume / candles.slice(i - patternLength, i).reduce((sum, c) => sum + c.volume, 0) * patternLength,
        highLowRatio: (c.high - c.low) / c.close
      }));
      
      patterns.push({
        index: i,
        pattern: this.flattenPattern(pattern),
        outcome: this.calculateOutcome(candles, i)
      });
    }
    
    return patterns;
  }
  
  flattenPattern(pattern) {
    return pattern.reduce((flat, p) => [
      ...flat,
      p.priceChange,
      p.volumeRatio,
      p.highLowRatio
    ], []);
  }
  
  calculateOutcome(candles, index, horizon = 5) {
    if (index + horizon >= candles.length) return 0;
    
    const currentPrice = candles[index].close;
    const futurePrice = candles[index + horizon].close;
    
    return (futurePrice - currentPrice) / currentPrice;
  }
  
  kMeansCluster(patterns) {
    // Inicializar centroides aleatoriamente
    this.centroids = this.initializeCentroids(patterns);
    
    let converged = false;
    let iterations = 0;
    const maxIterations = 100;
    
    while (!converged && iterations < maxIterations) {
      const newClusters = this.assignToClusters(patterns);
      const newCentroids = this.updateCentroids(newClusters);
      
      converged = this.hasConverged(newCentroids);
      this.centroids = newCentroids;
      this.clusters = newClusters;
      iterations++;
    }
    
    return this.clusters;
  }
  
  initializeCentroids(patterns) {
    const centroids = [];
    const patternLength = patterns[0].pattern.length;
    
    for (let i = 0; i < this.k; i++) {
      const randomPattern = patterns[Math.floor(Math.random() * patterns.length)];
      centroids.push([...randomPattern.pattern]);
    }
    
    return centroids;
  }
  
  assignToClusters(patterns) {
    const clusters = Array(this.k).fill().map(() => []);
    
    patterns.forEach(pattern => {
      let minDistance = Infinity;
      let closestCluster = 0;
      
      this.centroids.forEach((centroid, i) => {
        const distance = this.euclideanDistance(pattern.pattern, centroid);
        if (distance < minDistance) {
          minDistance = distance;
          closestCluster = i;
        }
      });
      
      clusters[closestCluster].push(pattern);
    });
    
    return clusters;
  }
  
  euclideanDistance(a, b) {
    return Math.sqrt(a.reduce((sum, val, i) => sum + Math.pow(val - b[i], 2), 0));
  }
  
  updateCentroids(clusters) {
    return clusters.map(cluster => {
      if (cluster.length === 0) return this.centroids[0]; // Manter centroide atual se cluster vazio
      
      const patternLength = cluster[0].pattern.length;
      const newCentroid = Array(patternLength).fill(0);
      
      cluster.forEach(pattern => {
        pattern.pattern.forEach((val, i) => {
          newCentroid[i] += val;
        });
      });
      
      return newCentroid.map(sum => sum / cluster.length);
    });
  }
  
  hasConverged(newCentroids) {
    const threshold = 0.001;
    
    return this.centroids.every((centroid, i) => 
      this.euclideanDistance(centroid, newCentroids[i]) < threshold
    );
  }
  
  analyzeClusterPerformance() {
    const analysis = [];
    
    this.clusters.forEach((cluster, i) => {
      if (cluster.length === 0) return;
      
      const outcomes = cluster.map(p => p.outcome);
      const avgOutcome = outcomes.reduce((sum, o) => sum + o, 0) / outcomes.length;
      const winRate = outcomes.filter(o => o > 0).length / outcomes.length;
      const maxGain = Math.max(...outcomes);
      const maxLoss = Math.min(...outcomes);
      
      analysis.push({
        cluster: i,
        size: cluster.length,
        avgOutcome,
        winRate,
        maxGain,
        maxLoss,
        sharpeRatio: this.calculateSharpeRatio(outcomes)
      });
    });
    
    return analysis.sort((a, b) => b.avgOutcome - a.avgOutcome);
  }
  
  calculateSharpeRatio(returns) {
    const mean = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);
    
    return stdDev === 0 ? 0 : mean / stdDev;
  }
}

// Uso
const clustering = new PatternClustering(8);
const patterns = clustering.extractPatterns(candles);
const clusters = clustering.kMeansCluster(patterns);
const performance = clustering.analyzeClusterPerformance();
```

## Backtesting Avançado

### Framework de Backtesting

```javascript
class AdvancedBacktester {
  constructor(config) {
    this.config = config;
    this.portfolio = {
      balance: config.initialBalance,
      positions: new Map(),
      orders: [],
      trades: []
    };
    this.metrics = {
      totalReturn: 0,
      maxDrawdown: 0,
      sharpeRatio: 0,
      calmarRatio: 0,
      winRate: 0,
      profitFactor: 0
    };
  }
  
  async runBacktest(strategy, data, startDate, endDate) {
    console.log(`Iniciando backtest: ${startDate} até ${endDate}`);
    
    const filteredData = this.filterDataByDate(data, startDate, endDate);
    const results = [];
    
    for (let i = 0; i < filteredData.length; i++) {
      const currentData = filteredData.slice(0, i + 1);
      const signals = await strategy.generateSignals(currentData);
      
      for (const signal of signals) {
        await this.processSignal(signal, filteredData[i]);
      }
      
      const portfolioValue = this.calculatePortfolioValue(filteredData[i]);
      results.push({
        timestamp: filteredData[i].timestamp,
        portfolioValue,
        balance: this.portfolio.balance,
        positions: Array.from(this.portfolio.positions.values())
      });
      
      // Atualizar drawdown
      this.updateDrawdown(portfolioValue);
    }
    
    this.calculateMetrics(results);
    return {
      results,
      metrics: this.metrics,
      trades: this.portfolio.trades
    };
  }
  
  async processSignal(signal, marketData) {
    switch (signal.action) {
      case 'BUY':
        await this.executeBuy(signal, marketData);
        break;
      case 'SELL':
        await this.executeSell(signal, marketData);
        break;
      case 'CLOSE':
        await this.closePosition(signal.symbol, marketData);
        break;
    }
  }
  
  async executeBuy(signal, marketData) {
    const price = this.getExecutionPrice(signal, marketData, 'BUY');
    const quantity = this.calculatePositionSize(signal, price);
    const cost = quantity * price * (1 + this.config.fees);
    
    if (cost > this.portfolio.balance) {
      console.log(`Saldo insuficiente para compra: ${cost} > ${this.portfolio.balance}`);
      return;
    }
    
    // Executar ordem
    this.portfolio.balance -= cost;
    
    if (this.portfolio.positions.has(signal.symbol)) {
      const existing = this.portfolio.positions.get(signal.symbol);
      existing.quantity += quantity;
      existing.avgPrice = (existing.avgPrice * existing.quantity + price * quantity) / (existing.quantity + quantity);
    } else {
      this.portfolio.positions.set(signal.symbol, {
        symbol: signal.symbol,
        quantity,
        avgPrice: price,
        side: 'LONG',
        timestamp: marketData.timestamp
      });
    }
    
    this.portfolio.trades.push({
      symbol: signal.symbol,
      side: 'BUY',
      quantity,
      price,
      timestamp: marketData.timestamp,
      strategy: signal.strategy
    });
  }
  
  calculatePositionSize(signal, price) {
    const riskAmount = this.portfolio.balance * this.config.riskPerTrade;
    const stopLossDistance = signal.stopLoss ? Math.abs(price - signal.stopLoss) : price * 0.02;
    
    return Math.min(
      riskAmount / stopLossDistance,
      this.portfolio.balance * 0.1 / price // Max 10% do portfolio por posição
    );
  }
  
  getExecutionPrice(signal, marketData, side) {
    const basePrice = marketData.close;
    const slippage = this.config.slippage || 0.001;
    
    if (side === 'BUY') {
      return basePrice * (1 + slippage);
    } else {
      return basePrice * (1 - slippage);
    }
  }
  
  calculatePortfolioValue(marketData) {
    let totalValue = this.portfolio.balance;
    
    for (const [symbol, position] of this.portfolio.positions) {
      const currentPrice = marketData.close; // Assumindo que marketData é do símbolo da posição
      totalValue += position.quantity * currentPrice;
    }
    
    return totalValue;
  }
  
  updateDrawdown(currentValue) {
    if (!this.peakValue || currentValue > this.peakValue) {
      this.peakValue = currentValue;
    }
    
    const drawdown = (this.peakValue - currentValue) / this.peakValue;
    if (drawdown > this.metrics.maxDrawdown) {
      this.metrics.maxDrawdown = drawdown;
    }
  }
  
  calculateMetrics(results) {
    const returns = this.calculateReturns(results);
    
    this.metrics.totalReturn = (results[results.length - 1].portfolioValue - this.config.initialBalance) / this.config.initialBalance;
    this.metrics.sharpeRatio = this.calculateSharpeRatio(returns);
    this.metrics.calmarRatio = this.metrics.totalReturn / this.metrics.maxDrawdown;
    this.metrics.winRate = this.calculateWinRate();
    this.metrics.profitFactor = this.calculateProfitFactor();
    
    console.log('Métricas do Backtest:');
    console.log(`Total Return: ${(this.metrics.totalReturn * 100).toFixed(2)}%`);
    console.log(`Max Drawdown: ${(this.metrics.maxDrawdown * 100).toFixed(2)}%`);
    console.log(`Sharpe Ratio: ${this.metrics.sharpeRatio.toFixed(2)}`);
    console.log(`Win Rate: ${(this.metrics.winRate * 100).toFixed(2)}%`);
  }
  
  calculateReturns(results) {
    return results.slice(1).map((result, i) => 
      (result.portfolioValue - results[i].portfolioValue) / results[i].portfolioValue
    );
  }
  
  calculateSharpeRatio(returns) {
    const mean = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / returns.length;
    const stdDev = Math.sqrt(variance);
    
    return stdDev === 0 ? 0 : (mean * 252) / (stdDev * Math.sqrt(252)); // Anualizado
  }
  
  calculateWinRate() {
    const completedTrades = this.getCompletedTrades();
    const winningTrades = completedTrades.filter(trade => trade.pnl > 0);
    
    return completedTrades.length > 0 ? winningTrades.length / completedTrades.length : 0;
  }
  
  calculateProfitFactor() {
    const completedTrades = this.getCompletedTrades();
    const grossProfit = completedTrades.filter(t => t.pnl > 0).reduce((sum, t) => sum + t.pnl, 0);
    const grossLoss = Math.abs(completedTrades.filter(t => t.pnl < 0).reduce((sum, t) => sum + t.pnl, 0));
    
    return grossLoss === 0 ? Infinity : grossProfit / grossLoss;
  }
  
  getCompletedTrades() {
    // Lógica para identificar trades completos (compra + venda)
    const completed = [];
    const trades = [...this.portfolio.trades].sort((a, b) => a.timestamp - b.timestamp);
    
    let position = 0;
    let avgPrice = 0;
    
    for (const trade of trades) {
      if (trade.side === 'BUY') {
        if (position === 0) {
          avgPrice = trade.price;
        } else {
          avgPrice = (avgPrice * position + trade.price * trade.quantity) / (position + trade.quantity);
        }
        position += trade.quantity;
      } else { // SELL
        if (position > 0) {
          const soldQuantity = Math.min(trade.quantity, position);
          const pnl = (trade.price - avgPrice) * soldQuantity;
          
          completed.push({
            symbol: trade.symbol,
            entryPrice: avgPrice,
            exitPrice: trade.price,
            quantity: soldQuantity,
            pnl,
            entryTime: trade.timestamp,
            exitTime: trade.timestamp
          });
          
          position -= soldQuantity;
        }
      }
    }
    
    return completed;
  }
}

// Uso
const backtester = new AdvancedBacktester({
  initialBalance: 10000,
  riskPerTrade: 0.02,
  fees: 0.001,
  slippage: 0.001
});

const results = await backtester.runBacktest(
  strategy,
  historicalData,
  '2023-01-01',
  '2023-12-31'
);
```

## Otimização de Parâmetros

### Algoritmo Genético

```javascript
class ParameterOptimizer {
  constructor(config) {
    this.config = config;
    this.population = [];
    this.generation = 0;
  }
  
  async optimize(strategy, data, parameterRanges) {
    console.log('Iniciando otimização de parâmetros...');
    
    // Inicializar população
    this.initializePopulation(parameterRanges);
    
    for (let gen = 0; gen < this.config.maxGenerations; gen++) {
      this.generation = gen;
      console.log(`Geração ${gen + 1}/${this.config.maxGenerations}`);
      
      // Avaliar fitness de cada indivíduo
      await this.evaluatePopulation(strategy, data);
      
      // Selecionar os melhores
      this.selection();
      
      // Crossover e mutação
      this.reproduction(parameterRanges);
      
      const bestIndividual = this.getBestIndividual();
      console.log(`Melhor fitness: ${bestIndividual.fitness.toFixed(4)}`);
    }
    
    return this.getBestIndividual();
  }
  
  initializePopulation(parameterRanges) {
    this.population = [];
    
    for (let i = 0; i < this.config.populationSize; i++) {
      const individual = {};
      
      for (const [param, range] of Object.entries(parameterRanges)) {
        individual[param] = this.randomInRange(range.min, range.max, range.type);
      }
      
      this.population.push({
        parameters: individual,
        fitness: 0,
        metrics: {}
      });
    }
  }
  
  randomInRange(min, max, type = 'float') {
    const random = Math.random() * (max - min) + min;
    return type === 'int' ? Math.floor(random) : random;
  }
  
  async evaluatePopulation(strategy, data) {
    const evaluations = this.population.map(async (individual, index) => {
      try {
        const backtester = new AdvancedBacktester(this.config.backtest);
        const strategyWithParams = { ...strategy, parameters: individual.parameters };
        
        const results = await backtester.runBacktest(strategyWithParams, data, this.config.startDate, this.config.endDate);
        
        individual.fitness = this.calculateFitness(results.metrics);
        individual.metrics = results.metrics;
        
        console.log(`Indivíduo ${index + 1}: fitness = ${individual.fitness.toFixed(4)}`);
      } catch (error) {
        console.error(`Erro ao avaliar indivíduo ${index + 1}:`, error);
        individual.fitness = -Infinity;
      }
    });
    
    await Promise.all(evaluations);
  }
  
  calculateFitness(metrics) {
    // Função de fitness multi-objetivo
    const returnWeight = 0.4;
    const drawdownWeight = 0.3;
    const sharpeWeight = 0.2;
    const winRateWeight = 0.1;
    
    const normalizedReturn = Math.max(0, metrics.totalReturn);
    const normalizedDrawdown = Math.max(0, 1 - metrics.maxDrawdown);
    const normalizedSharpe = Math.max(0, metrics.sharpeRatio / 3); // Assuming max reasonable Sharpe is 3
    const normalizedWinRate = metrics.winRate;
    
    return (
      normalizedReturn * returnWeight +
      normalizedDrawdown * drawdownWeight +
      normalizedSharpe * sharpeWeight +
      normalizedWinRate * winRateWeight
    );
  }
  
  selection() {
    // Selecão por torneio
    const selected = [];
    const tournamentSize = Math.max(2, Math.floor(this.config.populationSize * 0.1));
    
    for (let i = 0; i < this.config.populationSize; i++) {
      const tournament = [];
      
      for (let j = 0; j < tournamentSize; j++) {
        const randomIndex = Math.floor(Math.random() * this.population.length);
        tournament.push(this.population[randomIndex]);
      }
      
      const winner = tournament.reduce((best, current) => 
        current.fitness > best.fitness ? current : best
      );
      
      selected.push({ ...winner });
    }
    
    this.population = selected;
  }
  
  reproduction(parameterRanges) {
    const newPopulation = [];
    
    // Manter os melhores (elitismo)
    const eliteCount = Math.floor(this.config.populationSize * 0.1);
    const elite = [...this.population]
      .sort((a, b) => b.fitness - a.fitness)
      .slice(0, eliteCount);
    
    newPopulation.push(...elite);
    
    // Criar nova geração através de crossover e mutação
    while (newPopulation.length < this.config.populationSize) {
      const parent1 = this.selectParent();
      const parent2 = this.selectParent();
      
      const child = this.crossover(parent1, parent2);
      this.mutate(child, parameterRanges);
      
      newPopulation.push(child);
    }
    
    this.population = newPopulation;
  }
  
  selectParent() {
    // Seleção por roleta
    const totalFitness = this.population.reduce((sum, ind) => sum + Math.max(0, ind.fitness), 0);
    
    if (totalFitness === 0) {
      return this.population[Math.floor(Math.random() * this.population.length)];
    }
    
    let random = Math.random() * totalFitness;
    
    for (const individual of this.population) {
      random -= Math.max(0, individual.fitness);
      if (random <= 0) {
        return individual;
      }
    }
    
    return this.population[this.population.length - 1];
  }
  
  crossover(parent1, parent2) {
    const child = {
      parameters: {},
      fitness: 0,
      metrics: {}
    };
    
    for (const param of Object.keys(parent1.parameters)) {
      // Crossover uniforme
      child.parameters[param] = Math.random() < 0.5 ? 
        parent1.parameters[param] : 
        parent2.parameters[param];
    }
    
    return child;
  }
  
  mutate(individual, parameterRanges) {
    for (const [param, range] of Object.entries(parameterRanges)) {
      if (Math.random() < this.config.mutationRate) {
        // Mutação gaussiana
        const currentValue = individual.parameters[param];
        const mutationStrength = (range.max - range.min) * 0.1;
        const mutation = (Math.random() - 0.5) * 2 * mutationStrength;
        
        individual.parameters[param] = Math.max(
          range.min,
          Math.min(range.max, currentValue + mutation)
        );
        
        if (range.type === 'int') {
          individual.parameters[param] = Math.round(individual.parameters[param]);
        }
      }
    }
  }
  
  getBestIndividual() {
    return this.population.reduce((best, current) => 
      current.fitness > best.fitness ? current : best
    );
  }
}

// Uso
const optimizer = new ParameterOptimizer({
  populationSize: 50,
  maxGenerations: 20,
  mutationRate: 0.1,
  backtest: {
    initialBalance: 10000,
    riskPerTrade: 0.02,
    fees: 0.001
  },
  startDate: '2023-01-01',
  endDate: '2023-12-31'
});

const parameterRanges = {
  rsiPeriod: { min: 5, max: 30, type: 'int' },
  rsiOversold: { min: 20, max: 40, type: 'float' },
  rsiOverbought: { min: 60, max: 80, type: 'float' },
  macdFast: { min: 8, max: 16, type: 'int' },
  macdSlow: { min: 20, max: 35, type: 'int' }
};

const bestParameters = await optimizer.optimize(strategy, data, parameterRanges);
console.log('Melhores parâmetros encontrados:', bestParameters);
```

Este tutorial avançado oferece ferramentas poderosas para análise técnica sofisticada, machine learning aplicado ao trading, backtesting robusto e otimização de parâmetros usando algoritmos genéticos. Cada seção pode ser expandida e personalizada conforme suas necessidades específicas.