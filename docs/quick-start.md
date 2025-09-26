# 🚀 Guia de Início Rápido

Comece a usar o XBot v2 em poucos minutos!

## ⚡ Setup em 5 Minutos

### 1. Instalar o Sistema
```bash
git clone https://github.com/seu-usuario/xbot-v2.git
cd xbot-v2
python setup.py
```

### 2. Configurar Credenciais
```bash
cp .env.example .env
# Edite .env com suas chaves da Binance
```

### 3. Testar o Sistema
```bash
python test_xbot.py --demo
```

### 4. Criar Seu Primeiro Bot
```bash
python -m src.main create-bot "MeuPrimeiroBot" --capital 1000 --strategy scalping_conservative
```

### 5. Iniciar o Bot
```bash
python -m src.main start-bot <bot-id>
```

## 🎯 Primeiro Bot Passo a Passo

### Cenário: Bot Conservador com $1000

```bash
# 1. Criar bot com estratégia conservadora
python -m src.main create-bot \
  --name "Scalping BTCUSDT" \
  --strategy scalping_conservative \
  --capital 1000 \
  --symbols BTCUSDT

# 2. Verificar configuração
python -m src.main list-bots

# 3. Analisar mercado primeiro
python -m src.main analyze BTCUSDT

# 4. Iniciar em modo simulação (recomendado)
python -m src.main start-bot <bot-id> --dry-run

# 5. Monitorar performance
python -m src.main dashboard
```

## 📊 Dashboard em Tempo Real

O dashboard mostra:

```
┌─ XBot v2 Dashboard ─────────────────────────────┐
│ Status: 3 bots ativos | Capital Total: $5,000   │
├─────────────────────────────────────────────────┤
│ Bot               Status    P&L      Trades      │
│ Scalping BTCUSDT  RUNNING   +2.5%   15/12       │
│ Swing ETHUSDT     RUNNING   +1.8%   8/7         │
│ Grid ADAUSDT      PAUSED    -0.5%   22/18       │
└─────────────────────────────────────────────────┘
```

## ⚙️ Configurações Essenciais

### Configuração Mínima (.env)
```env
BINANCE_API_KEY=sua_api_key
BINANCE_SECRET_KEY=sua_secret_key
BINANCE_TESTNET=true
DEFAULT_INITIAL_CAPITAL=1000
MAX_CONCURRENT_BOTS=3
```

### Configuração com Telegram
```env
TELEGRAM_BOT_TOKEN=seu_bot_token
TELEGRAM_CHAT_ID=seu_chat_id
TELEGRAM_NOTIFICATIONS_ENABLED=true
```

## 🛡️ Primeiras Configurações de Segurança

### 1. Sempre Use Testnet Primeiro
```env
BINANCE_TESTNET=true
```

### 2. Configure Limites Conservadores
```env
MAX_POSITION_SIZE=5.0
MAX_DAILY_LOSS=2.0
MAX_CONCURRENT_POSITIONS=2
```

### 3. Habilite Stop Loss
```env
DEFAULT_STOP_LOSS=1.5
DEFAULT_TAKE_PROFIT=3.0
```

## 📈 Estratégias Recomendadas para Iniciantes

### 1. Scalping Conservador
- **Capital**: $500 - $2,000
- **Risco**: Baixo
- **Tempo**: Trading ativo
- **Símbolos**: BTCUSDT, ETHUSDT

```bash
python -m src.main create-bot \
  --strategy scalping_conservative \
  --capital 1000 \
  --symbols BTCUSDT,ETHUSDT
```

### 2. Grid Trading
- **Capital**: $1,000 - $5,000
- **Risco**: Baixo a Moderado
- **Tempo**: Mercados laterais
- **Símbolos**: BTCUSDT, ETHUSDT

```bash
python -m src.main create-bot \
  --strategy grid_trading \
  --capital 2000 \
  --symbols BTCUSDT
```

### 3. DCA Strategy
- **Capital**: $2,000+
- **Risco**: Moderado
- **Tempo**: Long term
- **Símbolos**: Principais cryptos

```bash
python -m src.main create-bot \
  --strategy dca_strategy \
  --capital 3000 \
  --symbols BTCUSDT,ETHUSDT
```

## 🔍 Comandos Essenciais

### Gerenciamento de Bots
```bash
# Listar todos os bots
python -m src.main list-bots

# Status de um bot específico
python -m src.main bot-status <bot-id>

# Parar um bot
python -m src.main stop-bot <bot-id>

# Remover um bot
python -m src.main remove-bot <bot-id>
```

### Análise de Mercado
```bash
# Analisar símbolo específico
python -m src.main analyze BTCUSDT

# Detectar padrões
python -m src.main patterns ETHUSDT

# Verificar sinais
python -m src.main signals
```

### Monitoramento
```bash
# Dashboard completo
python -m src.main dashboard

# Performance de um bot
python -m src.main performance <bot-id>

# Histórico de trades
python -m src.main history <bot-id>
```

## 📱 Notificações Telegram

Configure para receber alertas:

```bash
# Teste de notificação
python -m src.main test-telegram

# Configurar alertas
python -m src.main configure-alerts \
  --trades true \
  --signals true \
  --errors true
```

Tipos de notificação:
- 📈 **Trade executado**
- 🎯 **Novo sinal detectado**
- ⚠️ **Alerta de risco**
- 📊 **Relatório de performance**
- ❌ **Erros do sistema**

## ⚠️ Checklist de Segurança

Antes de usar dinheiro real:

- [ ] ✅ Testei no testnet por pelo menos 1 semana
- [ ] ✅ Configurei stop loss apropriado
- [ ] ✅ Limitei o capital de risco (máximo 5% do total)
- [ ] ✅ Configurei notificações de alerta
- [ ] ✅ Entendo a estratégia escolhida
- [ ] ✅ Configurei backup automático
- [ ] ✅ Testei recuperação de falhas

## 🆘 Problemas Comuns

### Bot não inicia
```bash
# Verificar configuração
python -m src.main validate-config

# Verificar conexão com Binance
python -m src.main test-connection
```

### Erro de API
- Verifique se as chaves estão corretas
- Confirme permissões de trading
- Verifique se não atingiu rate limits

### Performance ruim
- Revise a estratégia escolhida
- Ajuste parâmetros de risco
- Considere mudar timeframe

## 📚 Próximos Passos

1. 📖 Leia sobre [Estratégias](user-guide/trading-strategies.md)
2. 🛡️ Configure [Gestão de Risco](user-guide/risk-management.md)
3. 📊 Aprenda sobre [Monitoramento](user-guide/monitoring.md)
4. ⚙️ Personalize [Configurações](configuration.md)

---

🎉 **Pronto para começar! Boa sorte com seus trades!** 🚀