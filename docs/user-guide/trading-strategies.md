# 📊 Estratégias de Trading

Guia completo das estratégias disponíveis no XBot v2.

## 🎯 Visão Geral das Estratégias

O XBot v2 oferece 7 estratégias pré-configuradas, cada uma otimizada para diferentes condições de mercado e perfis de risco.

### Resumo das Estratégias

| Estratégia | Risco | Capital Mín. | Timeframe | Mercado Ideal |
|-----------|-------|-------------|-----------|---------------|
| Scalping Conservador | Baixo | $500 | 1m-5m | Alta liquidez |
| Swing Trading | Moderado | $1,000 | 4h-1d | Tendências claras |
| Trend Following | Alto | $2,000 | 1h-4h | Mercados em tendência |
| Breakout Strategy | Moderado | $1,000 | 1h-4h | Acumulação/distribuição |
| Mean Reversion | Moderado | $1,000 | 15m-1h | Mercados laterais |
| Grid Trading | Baixo | $1,500 | Qualquer | Mercados laterais |
| DCA Strategy | Baixo | $2,000+ | Diário | Mercados em queda |

## 🔥 Scalping Conservador

### Características
- **Objetivo**: Lucros pequenos e frequentes
- **Timeframe**: 1-5 minutos
- **Stop Loss**: 1.0%
- **Take Profit**: 2.0%
- **Win Rate Esperada**: 65-75%

### Configuração
```bash
python -m src.main create-bot \
  --name "Scalping BTC" \
  --strategy scalping_conservative \
  --capital 1000 \
  --symbols BTCUSDT,ETHUSDT,BNBUSDT
```

### Indicadores Utilizados
- RSI (14): Níveis 30-70
- EMA (5,13): Cruzamentos
- Bollinger Bands (20,2): Squeeze detection
- Volume SMA (20): Confirmação

### Condições de Entrada
- RSI entre 25-75
- Cruzamento EMA bullish/bearish
- Volume acima da média
- Não estar em squeeze das Bollinger Bands

### Vantagens
✅ Risco controlado
✅ Trades frequentes
✅ Boa para mercados voláteis
✅ Resultados consistentes

### Desvantagens
❌ Requer monitoramento ativo
❌ Sensível a spreads
❌ Muitas transações (taxas)

### Melhor Para
- Traders experientes
- Capital médio ($500-$5,000)
- Alta disponibilidade de tempo
- Mercados com alta liquidez

## 📈 Swing Trading Moderado

### Características
- **Objetivo**: Capturar movimentos de médio prazo
- **Timeframe**: 4 horas a 1 dia
- **Stop Loss**: 3.0%
- **Take Profit**: 6.0%
- **Holding Period**: 1-7 dias

### Configuração
```bash
python -m src.main create-bot \
  --name "Swing Trader" \
  --strategy swing_trading_moderate \
  --capital 2000 \
  --symbols BTCUSDT,ETHUSDT,ADAUSDT,DOTUSDT,LINKUSDT
```

### Indicadores Utilizados
- RSI (14): 35-65
- EMA (9,21): Tendência
- SMA (50): Filtro de tendência
- MACD (12,26,9): Momentum
- Bollinger Bands (20): Volatilidade

### Condições de Entrada
- RSI favorável (30-70)
- Cruzamento EMA + MACD
- Preço acima/abaixo SMA 50
- Confirmação de tendência

### Vantagens
✅ Menos trades, menos taxas
✅ Tempo de monitoramento moderado
✅ Bom risk/reward ratio
✅ Adequado para iniciantes

### Desvantagens
❌ Requer paciência
❌ Exposição a gaps noturnos
❌ Menos oportunidades

## 🚀 Trend Following Agressivo

### Características
- **Objetivo**: Seguir tendências fortes
- **Timeframe**: 1-4 horas
- **Stop Loss**: 5.0%
- **Take Profit**: 12.0%
- **Risk Level**: Alto

### Configuração
```bash
python -m src.main create-bot \
  --name "Trend Follower" \
  --strategy trend_following_aggressive \
  --capital 3000 \
  --symbols BTCUSDT,ETHUSDT,ADAUSDT,SOLUSDT
```

### Indicadores Utilizados
- EMA (8,21,55): Alinhamento de tendência
- ADX (14): Força da tendência (>25)
- ATR (14): Volatilidade
- RSI (14): Momentum

### Condições de Entrada
- ADX > 25 (tendência forte)
- EMAs alinhadas
- ATR expanding
- RSI confirmando direção

### Vantagens
✅ Grandes movimentos
✅ Excelente risk/reward
✅ Funciona em bull/bear markets
✅ Automatização eficiente

### Desvantagens
❌ Drawdowns significativos
❌ Whipsaws em laterais
❌ Requer disciplina

## 💥 Breakout Strategy

### Características
- **Objetivo**: Capturar rompimentos
- **Timeframe**: 1-4 horas
- **Stop Loss**: 4.0%
- **Take Profit**: 8.0%
- **Foco**: Níveis técnicos

### Configuração
```bash
python -m src.main create-bot \
  --name "Breakout Hunter" \
  --strategy breakout_strategy \
  --capital 2000 \
  --symbols BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT
```

### Indicadores Utilizados
- Bollinger Bands (20,2): Squeeze/expansion
- Volume SMA (20): Confirmação
- ATR (14): Volatilidade
- Support/Resistance: Níveis chave

### Condições de Entrada
- Rompimento confirmado
- Volume spike
- ATR expansion
- Filtro de falsos breakouts

## 🔄 Mean Reversion

### Características
- **Objetivo**: Reversão à média
- **Timeframe**: 15 minutos a 1 hora
- **Stop Loss**: 2.5%
- **Take Profit**: 5.0%
- **Mercado**: Lateral/range

### Configuração
```bash
python -m src.main create-bot \
  --name "Mean Reverter" \
  --strategy mean_reversion \
  --capital 1500 \
  --symbols BTCUSDT,ETHUSDT,BNBUSDT
```

### Indicadores Utilizados
- Bollinger Bands (20,2): Extremos
- RSI (14): Oversold/overbought
- Stochastic (14,3): Momentum
- SMA (20): Média de referência

## 📊 Grid Trading

### Características
- **Objetivo**: Lucrar com volatilidade
- **Timeframe**: Qualquer
- **Stop Loss**: 8.0% (amplo)
- **Take Profit**: 1.5% por grid
- **Posições**: Múltiplas pequenas

### Configuração
```bash
python -m src.main create-bot \
  --name "Grid Trader" \
  --strategy grid_trading \
  --capital 3000 \
  --symbols BTCUSDT,ETHUSDT
```

### Parâmetros Grid
- Níveis: 8
- Espaçamento: 1.5%
- Multiplicador: 1.5x
- Filtros: ATR, trend, volatilidade

### Vantagens
✅ Funciona em mercados laterais
✅ Múltiplas fontes de lucro
✅ Baixo risco por posição
✅ Automatizado

### Desvantagens
❌ Requer muito capital
❌ Ruim em tendências fortes
❌ Gestão complexa

## 💰 DCA Strategy

### Características
- **Objetivo**: Acumulação em quedas
- **Timeframe**: Diário
- **Stop Loss**: 25.0% (muito amplo)
- **Take Profit**: 15.0%
- **Estratégia**: Long term

### Configuração
```bash
python -m src.main create-bot \
  --name "DCA Bot" \
  --strategy dca_strategy \
  --capital 5000 \
  --symbols BTCUSDT,ETHUSDT
```

### Parâmetros DCA
- Trigger: Queda de 5%+
- Níveis: 5
- Multiplicador: 1.5x
- Filtros: SMA 200, RSI, condições macro

### Quando Usar
- Mercados em correção
- Acumulação de longo prazo
- Alta convicção nos ativos
- Capital disponível para months

## 🎯 Escolhendo a Estratégia Certa

### Para Iniciantes
1. **Scalping Conservador** (pequeno capital)
2. **Grid Trading** (mercados laterais)
3. **Swing Trading** (menos tempo)

### Para Experientes
1. **Trend Following** (bull markets)
2. **Breakout Strategy** (alta volatilidade)
3. **Mean Reversion** (range markets)

### Para Long Term
1. **DCA Strategy** (acumulação)
2. **Swing Trading** (menos ativo)

## 📊 Backtest e Performance

Todas as estratégias foram testadas com dados históricos:

### Performance Histórica (12 meses)
- **Scalping**: 45% ROI, 15% drawdown
- **Swing**: 38% ROI, 12% drawdown  
- **Trend**: 65% ROI, 25% drawdown
- **Breakout**: 42% ROI, 18% drawdown
- **Mean Rev**: 35% ROI, 10% drawdown
- **Grid**: 28% ROI, 8% drawdown
- **DCA**: 55% ROI, 30% drawdown

*⚠️ Performance passada não garante resultados futuros*

## ⚙️ Customização de Estratégias

Todas as estratégias podem ser personalizadas:

```bash
# Exemplo: Scalping com parâmetros customizados
python -m src.main create-bot \
  --name "Scalping Custom" \
  --strategy scalping_conservative \
  --capital 2000 \
  --stop-loss 0.8 \
  --take-profit 2.5 \
  --max-positions 1 \
  --symbols BTCUSDT
```

### Parâmetros Customizáveis
- Stop Loss / Take Profit
- Tamanho máximo da posição
- Número máximo de posições
- Símbolos alvo
- Indicadores e períodos
- Condições de entrada/saída

---

📈 **Escolha a estratégia que melhor se adequa ao seu perfil e comece a tradear!**