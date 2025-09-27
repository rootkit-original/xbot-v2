# 💼 Gestão de Portfolio

Guia completo para gerenciamento de portfolio, diversificação e otimização de capital no XBot v2.

## 🎯 Visão Geral

O sistema de gestão de portfolio do XBot v2 oferece ferramentas avançadas para:

- ✅ **Diversificação inteligente** de ativos
- ✅ **Controle de risco** por portfolio
- ✅ **Rebalanceamento automático**
- ✅ **Análise de correlação** entre ativos
- ✅ **Otimização de alocação** de capital
- ✅ **Monitoramento de performance** consolidada

## 📊 Dashboard do Portfolio

### Visualizar Portfolio Atual

```bash
# Portfolio geral
python -m src.main portfolio

# Portfolio detalhado
python -m src.main portfolio --detailed

# Portfolio por período
python -m src.main portfolio --period 30d

# Exportar para análise
python -m src.main portfolio --export portfolio_report.csv
```

### Métricas Principais

```
┌─────────────────────────────────────────────────────────────┐
│                    PORTFOLIO OVERVIEW                       │
├─────────────────────────────────────────────────────────────┤
│ Total Balance:     $15,234.56  │ Available: $3,456.78      │
│ Total PnL:         +$2,184.23  │ Invested:  $11,777.78     │
│ ROI Total:         +16.74%     │ Daily PnL: +$89.34        │
│ Max Drawdown:      -8.5%       │ Sharpe:    1.85           │
├─────────────────────────────────────────────────────────────┤
│ Asset Allocation:                                           │
│ BTC: 45.2% │ ETH: 28.5% │ BNB: 15.8% │ Others: 10.5%      │
│ ████████████████████████████████████████████████████████████│
├─────────────────────────────────────────────────────────────┤
│ Active Bots: 5     │ Positions: 12    │ Strategies: 4     │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Estratégia de Diversificação

### 1. Diversificação por Ativo

```bash
# Configurar limites por símbolo
python -m src.main config --symbol-limit BTCUSDT 40.0
python -m src.main config --symbol-limit ETHUSDT 30.0
python -m src.main config --symbol-limit BNBUSDT 20.0
python -m src.main config --symbol-limit OTHERS 10.0

# Verificar alocação atual
python -m src.main portfolio --allocation
```

**Exemplo de Alocação Recomendada:**

| Ativo | Alocação | Risco | Liquidez | Correlação BTC |
|-------|----------|-------|----------|----------------|
| BTC | 40-50% | Médio | Alta | 1.00 |
| ETH | 25-35% | Médio-Alto | Alta | 0.85 |
| BNB | 10-20% | Alto | Média | 0.75 |
| Altcoins | 5-15% | Muito Alto | Baixa | 0.60 |
| Stablecoins | 5-10% | Baixo | Alta | -0.10 |

### 2. Diversificação por Estratégia

```bash
# Portfolio multi-estratégia
python -m src.main create-bot --name "Conservative" --strategy scalping_conservative --capital 3000
python -m src.main create-bot --name "Aggressive" --strategy trend_following_aggressive --capital 2000
python -m src.main create-bot --name "Stable" --strategy grid_trading --capital 4000
python -m src.main create-bot --name "Long-term" --strategy dca_strategy --capital 6000

# Verificar diversificação
python -m src.main portfolio --by-strategy
```

**Alocação por Estratégia Recomendada:**

```
Conservative Strategies (40-50%):
├── Scalping Conservative: 20%
├── Grid Trading: 15%
└── Mean Reversion: 10%

Moderate Strategies (30-40%):
├── Swing Trading: 20%
└── Breakout Strategy: 15%

Aggressive Strategies (15-25%):
├── Trend Following: 15%
└── DCA Strategy: 10%
```

### 3. Diversificação Temporal

```bash
# Diferentes timeframes
python -m src.main create-bot --name "Scalper" --strategy scalping_conservative --timeframe 1m
python -m src.main create-bot --name "Day Trader" --strategy breakout_strategy --timeframe 15m
python -m src.main create-bot --name "Swing Trader" --strategy swing_trading_moderate --timeframe 4h
python -m src.main create-bot --name "Position Trader" --strategy trend_following_aggressive --timeframe 1d
```

## ⚖️ Gestão de Risco por Portfolio

### Configuração de Limites Globais

```bash
# Limite de drawdown do portfolio
python -m src.main config --portfolio-max-drawdown 15.0

# Limite de perda diária
python -m src.main config --daily-loss-limit 5.0

# Limite de exposição total
python -m src.main config --max-portfolio-exposure 80.0

# Correlação máxima permitida
python -m src.main config --max-correlation 0.85
```

### Risk Budgeting

```python
# Exemplo de configuração de risk budget
{
  "portfolio_risk_budget": {
    "conservative_strategies": {
      "allocation": 40,
      "max_drawdown": 8.0,
      "var_limit": 2.0
    },
    "moderate_strategies": {
      "allocation": 35,
      "max_drawdown": 12.0,
      "var_limit": 3.5
    },
    "aggressive_strategies": {
      "allocation": 25,
      "max_drawdown": 20.0,
      "var_limit": 5.0
    }
  }
}
```

### Kelly Criterion para Position Sizing

```bash
# Ativar Kelly Criterion
python -m src.main config --position-sizing kelly

# Configurar parâmetros
python -m src.main config --kelly-lookback 100
python -m src.main config --kelly-multiplier 0.25
```

## 📈 Rebalanceamento de Portfolio

### Rebalanceamento Automático

```bash
# Configurar rebalanceamento
python -m src.main config --auto-rebalance true
python -m src.main config --rebalance-frequency weekly
python -m src.main config --rebalance-threshold 10.0

# Executar rebalanceamento manual
python -m src.main rebalance --dry-run
python -m src.main rebalance --execute
```

### Estratégias de Rebalanceamento

#### 1. **Threshold Rebalancing**
Rebalanceia quando alocação desvia mais que X% do target:

```bash
python -m src.main config --rebalance-method threshold --threshold 15.0
```

#### 2. **Time-based Rebalancing**
Rebalanceia em intervalos fixos:

```bash
python -m src.main config --rebalance-method time --frequency monthly
```

#### 3. **Volatility-based Rebalancing**
Rebalanceia baseado na volatilidade:

```bash
python -m src.main config --rebalance-method volatility --vol-threshold 25.0
```

## 🔍 Análise de Correlação

### Matriz de Correlação

```bash
# Analisar correlações
python -m src.main analyze correlation --period 90d

# Alertas de alta correlação
python -m src.main config --correlation-alert 0.9
```

**Exemplo de Matriz:**

```
Correlation Matrix (90 days):
         BTC    ETH    BNB    ADA    DOT
BTC     1.00   0.85   0.75   0.68   0.72
ETH     0.85   1.00   0.78   0.71   0.74
BNB     0.75   0.78   1.00   0.65   0.69
ADA     0.68   0.71   0.65   1.00   0.82
DOT     0.72   0.74   0.69   0.82   1.00

⚠️ High correlation detected: ADA-DOT (0.82)
```

### Diversificação Score

```bash
# Calcular score de diversificação
python -m src.main analyze diversification

# Sugestões de melhoria
python -m src.main analyze diversification --suggestions
```

## 📊 Performance Analytics

### Análise Consolidada

```bash
# Relatório completo de performance
python -m src.main analyze performance --comprehensive

# Performance por estratégia
python -m src.main analyze performance --by-strategy

# Performance ajustada ao risco
python -m src.main analyze performance --risk-adjusted
```

### Métricas Avançadas

#### 1. **Sharpe Ratio**
Retorno ajustado ao risco:
```
Sharpe = (Return - Risk_free_rate) / Volatility
```

#### 2. **Sortino Ratio**
Foco no downside risk:
```
Sortino = (Return - Target) / Downside_deviation
```

#### 3. **Maximum Drawdown**
Maior queda peak-to-trough:
```
MDD = (Peak_value - Trough_value) / Peak_value
```

#### 4. **Calmar Ratio**
Retorno anualizado / Max Drawdown:
```
Calmar = Annual_return / Max_drawdown
```

### Dashboard de Performance

```
Performance Analytics (30 days):
┌─────────────────────────────────────────────────────────────┐
│ Return Metrics:                                             │
│ Total Return:      +12.45%    │ Annualized:    +156.8%     │
│ Volatility:        18.5%      │ Risk-free:     2.5%        │
│ Sharpe Ratio:      1.85       │ Sortino:       2.34        │
│ Max Drawdown:      -8.5%      │ Calmar:        18.4        │
├─────────────────────────────────────────────────────────────┤
│ Risk Metrics:                                               │
│ VaR (95%):         -2.1%      │ CVaR:          -3.4%       │
│ Beta (vs BTC):     0.85       │ Alpha:         +2.3%       │
│ Information Ratio: 1.42       │ Tracking Err:  4.2%        │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Otimização de Portfolio

### Mean-Variance Optimization

```bash
# Otimizar alocação usando Markowitz
python -m src.main optimize markowitz --target-return 15.0
python -m src.main optimize markowitz --min-variance

# Aplicar otimização
python -m src.main optimize apply --method markowitz
```

### Risk Parity

```bash
# Alocar capital por paridade de risco
python -m src.main optimize risk-parity

# Configurar limites
python -m src.main config --min-allocation 5.0
python -m src.main config --max-allocation 40.0
```

### Black-Litterman Model

```bash
# Incorporar views do mercado
python -m src.main optimize black-litterman \
  --view "BTC:bullish:0.8" \
  --view "ETH:neutral:0.5" \
  --confidence 0.7
```

## 💰 Gestão de Capital

### Capital Allocation

```bash
# Alocar capital novo
python -m src.main capital allocate 5000 --strategy proportional

# Retirar capital
python -m src.main capital withdraw 2000 --strategy conservative

# Reserva de emergência
python -m src.main config --emergency-reserve 10.0
```

### Dynamic Position Sizing

```bash
# Position sizing baseado em volatilidade
python -m src.main config --position-sizing volatility-target
python -m src.main config --volatility-target 10.0

# Position sizing baseado em Kelly
python -m src.main config --position-sizing kelly
python -m src.main config --kelly-fraction 0.25
```

## 📱 Monitoramento e Alertas

### Alertas de Portfolio

```bash
# Configurar alertas críticos
python -m src.main alerts add --name "Portfolio Drawdown" \
  --condition "portfolio_drawdown > 10.0" \
  --priority high

python -m src.main alerts add --name "Concentration Risk" \
  --condition "max_allocation > 50.0" \
  --priority medium

python -m src.main alerts add --name "Low Diversification" \
  --condition "diversification_score < 0.6" \
  --priority medium
```

### Dashboard em Tempo Real

```bash
# Monitor de portfolio
python -m src.main monitor portfolio --refresh 60

# Monitor de risco
python -m src.main monitor risk --refresh 300

# Monitor de correlação
python -m src.main monitor correlation --refresh 3600
```

## 📊 Relatórios Personalizados

### Relatório Diário

```bash
# Gerar relatório automático
python -m src.main report daily --email your@email.com
python -m src.main report daily --telegram @your_user
```

### Relatório Semanal

```bash
# Relatório completo semanal
python -m src.main report weekly --format pdf
python -m src.main report weekly --format html --send-email
```

### Relatório Mensal

```bash
# Análise profunda mensal
python -m src.main report monthly --comprehensive
python -m src.main report monthly --benchmark BTCUSDT
```

## 🎯 Estratégias Avançadas

### Portfolio Multi-Timeframe

```python
# Configuração de portfolio multi-timeframe
portfolio_config = {
    "short_term": {
        "allocation": 30,
        "strategies": ["scalping", "mean_reversion"],
        "timeframes": ["1m", "5m", "15m"]
    },
    "medium_term": {
        "allocation": 50,
        "strategies": ["swing", "breakout"],
        "timeframes": ["1h", "4h"]
    },
    "long_term": {
        "allocation": 20,
        "strategies": ["trend_following", "dca"],
        "timeframes": ["1d", "1w"]
    }
}
```

### Regime-Based Allocation

```bash
# Detectar regime de mercado
python -m src.main analyze regime --method hmm

# Ajustar alocação por regime
python -m src.main config --regime-allocation bull:aggressive
python -m src.main config --regime-allocation bear:conservative
python -m src.main config --regime-allocation sideways:neutral
```

## 🔍 Backtesting de Portfolio

### Teste Histórico Completo

```bash
# Backtest do portfolio completo
python -m src.main backtest portfolio \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --initial-capital 50000

# Comparar com benchmark
python -m src.main backtest portfolio \
  --benchmark BTCUSDT \
  --benchmark SPY \
  --report detailed_backtest.html
```

### Walk-Forward Analysis

```bash
# Análise walk-forward
python -m src.main backtest walk-forward \
  --window 90 \
  --step 30 \
  --optimization-period 180
```

## 🏆 Boas Práticas

### 1. **Diversificação Eficiente**
```bash
# Manter correlação baixa
python -m src.main config --max-correlation 0.7

# Balancear por setor
python -m src.main config --sector-limits true
```

### 2. **Gestão de Risco Rigorosa**
```bash
# Limites por categoria
python -m src.main config --large-cap-limit 60.0
python -m src.main config --mid-cap-limit 30.0
python -m src.main config --small-cap-limit 10.0
```

### 3. **Rebalanceamento Disciplinado**
```bash
# Rebalanceamento automático
python -m src.main config --auto-rebalance true
python -m src.main config --rebalance-threshold 15.0
```

### 4. **Monitoramento Contínuo**
```bash
# Alertas proativos
python -m src.main monitor portfolio --alerts all
python -m src.main monitor risk --continuous
```

---

💼 **Domine a gestão de portfolio e maximize seus retornos com risco controlado!**