# 📊 Monitoramento e Alertas

Sistema completo de monitoramento em tempo real e notificações inteligentes.

## 🎯 Visão Geral do Sistema

O XBot v2 oferece um sistema de monitoramento robusto que inclui:

- ✅ Dashboard em tempo real
- ✅ Alertas por Telegram
- ✅ Métricas de performance
- ✅ Logs detalhados
- ✅ Alertas de risk management
- ✅ Notificações de sistema

## 📱 Dashboard de Monitoramento

### Interface Principal

```bash
# Iniciar monitor geral
python -m src.main monitor

# Monitor com refresh automático
python -m src.main monitor --refresh 15

# Monitor específico de um bot
python -m src.main monitor --bot-name "Scalping BTC"

# Monitor com alertas ativos
python -m src.main monitor --alerts --refresh 30
```

### Layout do Dashboard

```
╔══════════════════════════════════════════════════════════════╗
║                        XBot v2 Monitor                       ║
╠══════════════════════════════════════════════════════════════╣
║ Status: ✅ Online  │ Bots Ativos: 3  │ PnL: +$245.67        ║
╠══════════════════════════════════════════════════════════════╣
║ Bot Name         │ Strategy    │ Status │ PnL    │ Trades    ║
║ Scalping BTC     │ Scalping    │ 🟢     │ +$89.23│ 24        ║
║ Swing ETH        │ Swing       │ 🟡     │ -$12.45│ 3         ║
║ Grid Master      │ Grid        │ 🟢     │ +$168.89│ 15       ║
╠══════════════════════════════════════════════════════════════╣
║ Posições Abertas: 5  │ Capital Total: $8,432.11            ║
║ Drawdown Atual: -2.3%│ Win Rate: 68.4%                     ║
╚══════════════════════════════════════════════════════════════╝
```

### Indicadores de Status

| Símbolo | Status | Descrição |
|---------|--------|-----------|
| 🟢 | Online | Bot ativo e operando |
| 🟡 | Warning | Avisos ou atenção necessária |
| 🔴 | Error | Erro crítico ou parado |
| 🟠 | Paused | Bot pausado pelo usuário |
| ⚪ | Offline | Bot desconectado |

## 🔔 Sistema de Alertas

### Configuração do Telegram

```bash
# Configurar bot do Telegram
python -m src.main config --telegram-token "SEU_BOT_TOKEN"

# Configurar chat ID
python -m src.main config --telegram-chat-id "SEU_CHAT_ID"

# Testar configuração
python -m src.main test-telegram
```

**Como obter as credenciais:**

1. **Bot Token:**
   - Fale com @BotFather no Telegram
   - Digite `/newbot` e siga as instruções
   - Copie o token fornecido

2. **Chat ID:**
   - Adicione seu bot a um grupo/chat
   - Envie uma mensagem no grupo
   - Acesse: `https://api.telegram.org/bot[TOKEN]/getUpdates`
   - Encontre o "chat":{"id": valor}

### Tipos de Alertas

#### 1. Alertas de Trading

```json
{
  "trade_alerts": {
    "new_position": true,
    "position_closed": true,
    "stop_loss_hit": true,
    "take_profit_hit": true,
    "large_trades": {
      "enabled": true,
      "threshold_usd": 100
    }
  }
}
```

**Exemplo de notificação:**
```
🚀 XBot v2 - Nova Posição
Bot: Scalping BTC
Símbolo: BTCUSDT
Lado: LONG
Preço: $43,250.00
Quantidade: 0.0232 BTC
Valor: $1,003.40
Stop Loss: $42,817.50
Take Profit: $44,115.00
```

#### 2. Alertas de Risk Management

```json
{
  "risk_alerts": {
    "daily_loss_limit": {
      "enabled": true,
      "threshold_percent": 5.0
    },
    "drawdown_alert": {
      "enabled": true,
      "threshold_percent": 10.0
    },
    "low_balance": {
      "enabled": true,
      "threshold_usd": 500
    }
  }
}
```

**Exemplo de notificação:**
```
⚠️ XBot v2 - Alerta de Risco
Drawdown atual: -8.5%
Limite configurado: -10.0%
Bot: Swing ETH
Ação: Reduzir exposição
Tempo: 2024-03-15 14:30:15
```

#### 3. Alertas de Sistema

```json
{
  "system_alerts": {
    "connection_error": true,
    "api_error": true,
    "low_disk_space": true,
    "high_cpu_usage": {
      "enabled": true,
      "threshold_percent": 80
    }
  }
}
```

### Configuração Personalizada

```bash
# Configurar alertas por categoria
python -m src.main config --alerts-trading on
python -m src.main config --alerts-risk on
python -m src.main config --alerts-system on

# Configurar thresholds
python -m src.main config --daily-loss-alert 3.0
python -m src.main config --drawdown-alert 8.0
python -m src.main config --large-trade-alert 500
```

## 📈 Métricas de Performance

### Dashboard de Performance

```bash
# Performance geral
python -m src.main performance

# Performance detalhada por bot
python -m src.main performance --bot-name "Scalping BTC"

# Performance por período
python -m src.main performance --period 7d

# Performance com gráficos
python -m src.main performance --charts
```

### Métricas Principais

#### 1. Métricas de Retorno

```
Profit & Loss (PnL)
├── PnL Total: $1,234.56
├── PnL Diário: $89.23
├── PnL Semanal: $456.78
├── ROI Total: 12.34%
├── ROI Anualizado: 45.67%
└── Sharpe Ratio: 1.89

Drawdown
├── Drawdown Atual: -2.3%
├── Drawdown Máximo: -8.9%
├── Período de Drawdown: 5 dias
└── Recovery Time: 3 dias
```

#### 2. Métricas de Trading

```
Estatísticas de Trades
├── Trades Totais: 145
├── Trades Vencedores: 98 (67.6%)
├── Trades Perdedores: 47 (32.4%)
├── Win Rate: 67.6%
├── Profit Factor: 1.85
├── Trade Médio: $8.52
├── Maior Ganho: $89.34
└── Maior Perda: -$43.21

Frequência
├── Trades/Dia: 12.3
├── Holding Time Médio: 2h 15m
├── Trades Ativos: 3
└── Máximo Simultâneo: 5
```

#### 3. Métricas de Risco

```
Risk Management
├── Volatilidade: 15.8%
├── VaR (95%): -$67.89
├── Sortino Ratio: 2.15
├── Calmar Ratio: 1.42
├── Max Position Size: 5.2%
├── Correlation BTCUSD: 0.78
└── Risk Score: Medium (6/10)
```

## 📊 Logs e Auditoria

### Sistema de Logs

```bash
# Ver logs em tempo real
tail -f logs/xbot.log

# Logs específicos por nível
grep "ERROR" logs/xbot.log
grep "TRADE" logs/xbot.log
grep "WARNING" logs/xbot.log

# Logs por bot
grep "Scalping BTC" logs/xbot.log

# Logs por período
grep "2024-03-15" logs/xbot.log
```

### Estrutura dos Logs

```
2024-03-15 14:30:15,123 [INFO] [TradingBot:Scalping BTC] Starting analysis for BTCUSDT
2024-03-15 14:30:15,156 [DEBUG] [Indicators] RSI: 42.3, EMA5: 43250.5, EMA13: 43180.2
2024-03-15 14:30:15,189 [INFO] [SignalGenerator] BUY signal generated for BTCUSDT
2024-03-15 14:30:15,234 [INFO] [OrderManager] Placing BUY order: 0.0232 BTC @ $43,250.00
2024-03-15 14:30:15,267 [SUCCESS] [TradingBot:Scalping BTC] Position opened: LONG BTCUSDT
2024-03-15 14:30:15,298 [INFO] [NotificationService] Telegram alert sent
```

### Níveis de Log

| Nível | Descrição | Arquivo |
|-------|-----------|---------|
| DEBUG | Detalhes técnicos | debug.log |
| INFO | Informações gerais | info.log |
| WARNING | Avisos importantes | warning.log |
| ERROR | Erros críticos | error.log |
| TRADE | Atividade de trading | trades.log |

### Configuração de Logs

```bash
# Configurar nível de log
python -m src.main config --log-level INFO

# Configurar rotação de logs
python -m src.main config --log-rotation daily

# Configurar retenção
python -m src.main config --log-retention 30

# Logs personalizados
python -m src.main config --log-format detailed
```

## 🎛️ Alertas Customizados

### Criação de Alertas Personalizados

```python
# custom_alerts.py
from src.core.notification_service import NotificationService

class CustomAlerts:
    def __init__(self):
        self.notification_service = NotificationService()
    
    def volume_spike_alert(self, symbol, current_volume, avg_volume):
        """Alerta para picos de volume"""
        if current_volume > avg_volume * 3:
            message = f"""
🔥 VOLUME SPIKE ALERT
Symbol: {symbol}
Current Volume: {current_volume:,.0f}
Average Volume: {avg_volume:,.0f}
Spike: {(current_volume/avg_volume):.1f}x
Time: {datetime.now().strftime('%H:%M:%S')}
            """
            self.notification_service.send_telegram(message)
    
    def correlation_alert(self, correlation_change):
        """Alerta para mudanças de correlação"""
        if abs(correlation_change) > 0.3:
            message = f"""
📊 CORRELATION ALERT
Market correlation changed by {correlation_change:.1f}
This may affect strategy performance
Consider adjusting position sizes
            """
            self.notification_service.send_telegram(message)
```

### Alertas Baseados em Indicadores

```bash
# Configurar alertas técnicos
python -m src.main alerts add \
  --name "RSI Oversold" \
  --condition "RSI < 25" \
  --symbols "BTCUSDT,ETHUSDT" \
  --timeframe "1h"

python -m src.main alerts add \
  --name "Volume Spike" \
  --condition "VOLUME > SMA(VOLUME,20) * 2" \
  --symbols "BTCUSDT" \
  --timeframe "5m"

python -m src.main alerts add \
  --name "Price Breakout" \
  --condition "CLOSE > BOLLINGER_UPPER" \
  --symbols "ETHUSDT" \
  --timeframe "15m"
```

### Alertas de Portfolio

```bash
# Alertas de exposição
python -m src.main alerts add \
  --name "High Exposure" \
  --condition "PORTFOLIO_EXPOSURE > 80%" \
  --frequency "daily"

# Alertas de concentração
python -m src.main alerts add \
  --name "Symbol Concentration" \
  --condition "SYMBOL_WEIGHT > 40%" \
  --frequency "hourly"

# Alertas de correlação
python -m src.main alerts add \
  --name "High Correlation" \
  --condition "AVG_CORRELATION > 0.8" \
  --frequency "daily"
```

## 📱 Interface Mobile (WebApp)

### Acesso via Navegador

```bash
# Iniciar web interface
python -m src.main web --port 8080

# Interface segura (HTTPS)
python -m src.main web --port 8080 --ssl

# Acesso externo
python -m src.main web --host 0.0.0.0 --port 8080
```

### Recursos Mobile

- 📱 Dashboard responsivo
- 📊 Gráficos interativos
- 🔔 Push notifications
- ⚡ Controles rápidos
- 📈 Performance metrics
- 🚨 Alertas em tempo real

### URL de Acesso

```
Local: http://localhost:8080
Rede: http://[seu-ip]:8080
HTTPS: https://localhost:8443
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Alertas não chegam

```bash
# Verificar configuração
python -m src.main config --show | grep telegram

# Testar conexão
python -m src.main test-telegram

# Verificar logs
grep "telegram" logs/xbot.log
```

#### 2. Monitor não atualiza

```bash
# Verificar status dos bots
python -m src.main status

# Reiniciar serviço de monitoramento
python -m src.main restart-monitor

# Verificar recursos do sistema
python -m src.main system-info
```

#### 3. Métricas incorretas

```bash
# Recalcular métricas
python -m src.main recalculate-metrics

# Verificar integridade dos dados
python -m src.main validate-data

# Limpar cache
python -m src.main clear-cache
```

## 🎯 Boas Práticas

### 1. Configuração de Alertas

```bash
# Configure apenas alertas essenciais
python -m src.main config --essential-alerts-only

# Use thresholds apropriados
python -m src.main config --risk-alerts-conservative
```

### 2. Monitoramento Eficiente

```bash
# Use refresh adequado ao timeframe
python -m src.main monitor --refresh 60  # Para swing trading
python -m src.main monitor --refresh 15  # Para scalping
```

### 3. Gestão de Logs

```bash
# Configure rotação automática
python -m src.main config --log-rotation daily --log-retention 30
```

### 4. Backup de Configurações

```bash
# Backup regular das configurações
python -m src.main backup-config --destination backup/
```

---

📊 **Monitore seus bots 24/7 com inteligência e receba alertas precisos em tempo real!**