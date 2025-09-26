# 🎮 Interface de Linha de Comando (CLI)

Guia completo da interface de linha de comando do XBot v2.

## 🚀 Visão Geral

O XBot v2 oferece uma interface CLI intuitiva e poderosa que permite:

- ✅ Criar e gerenciar bots de trading
- ✅ Monitorar performance em tempo real  
- ✅ Configurar alertas e notificações
- ✅ Executar backtests e análises
- ✅ Gerenciar portfólio e posições

## 📋 Comandos Principais

### help - Ajuda e Documentação

```bash
# Ajuda geral
python -m src.main --help

# Ajuda específica de um comando
python -m src.main create-bot --help
python -m src.main start --help
python -m src.main monitor --help
```

### create-bot - Criar Novo Bot

```bash
# Sintaxe básica
python -m src.main create-bot \
  --name "Nome do Bot" \
  --strategy [estratégia] \
  --capital [valor] \
  [opções]

# Exemplo completo
python -m src.main create-bot \
  --name "Scalping BTC" \
  --strategy scalping_conservative \
  --capital 1000 \
  --symbols BTCUSDT,ETHUSDT \
  --stop-loss 1.0 \
  --take-profit 2.0 \
  --max-positions 2
```

**Parâmetros Obrigatórios:**
- `--name`: Nome único para identificar o bot
- `--strategy`: Estratégia de trading a ser utilizada
- `--capital`: Capital inicial em USDT

**Parâmetros Opcionais:**
- `--symbols`: Lista de símbolos (padrão: BTCUSDT)
- `--stop-loss`: Stop loss em % (padrão: estratégia)
- `--take-profit`: Take profit em % (padrão: estratégia)
- `--max-positions`: Máximo de posições simultâneas
- `--testnet`: Usar Binance Testnet para testes

**Estratégias Disponíveis:**
- `scalping_conservative`
- `swing_trading_moderate`  
- `trend_following_aggressive`
- `breakout_strategy`
- `mean_reversion`
- `grid_trading`
- `dca_strategy`

### start - Iniciar Bot

```bash
# Iniciar bot específico
python -m src.main start --bot-name "Scalping BTC"

# Iniciar múltiplos bots
python -m src.main start --bot-name "Bot1,Bot2,Bot3"

# Iniciar todos os bots
python -m src.main start --all

# Iniciar em modo de demonstração
python -m src.main start --bot-name "Demo" --demo-mode
```

### stop - Parar Bot

```bash
# Parar bot específico
python -m src.main stop --bot-name "Scalping BTC"

# Parar todos os bots
python -m src.main stop --all

# Parada de emergência (fecha posições)
python -m src.main stop --bot-name "Bot1" --emergency
```

### monitor - Monitoramento

```bash
# Monitor geral
python -m src.main monitor

# Monitor específico
python -m src.main monitor --bot-name "Scalping BTC"

# Monitor com refresh automático
python -m src.main monitor --refresh 10

# Monitor com alertas
python -m src.main monitor --alerts
```

### status - Status dos Bots

```bash
# Status de todos os bots
python -m src.main status

# Status detalhado
python -m src.main status --detailed

# Status em JSON
python -m src.main status --format json

# Status específico
python -m src.main status --bot-name "Bot1"
```

### portfolio - Gestão de Portfólio

```bash
# Visão geral do portfólio
python -m src.main portfolio

# Relatório detalhado
python -m src.main portfolio --detailed

# Performance histórica
python -m src.main portfolio --history 30

# Exportar para CSV
python -m src.main portfolio --export portfolio.csv
```

### backtest - Testes Históricos

```bash
# Backtest básico
python -m src.main backtest \
  --strategy scalping_conservative \
  --symbols BTCUSDT \
  --start-date 2024-01-01 \
  --end-date 2024-03-01

# Backtest avançado
python -m src.main backtest \
  --strategy swing_trading_moderate \
  --symbols BTCUSDT,ETHUSDT \
  --capital 10000 \
  --start-date 2024-01-01 \
  --end-date 2024-03-01 \
  --report backtest_report.html
```

### config - Configuração

```bash
# Visualizar configuração atual
python -m src.main config --show

# Configurar API Binance
python -m src.main config --binance-api-key [sua_key]
python -m src.main config --binance-secret [seu_secret]

# Configurar Telegram
python -m src.main config --telegram-token [bot_token]
python -m src.main config --telegram-chat-id [chat_id]

# Configurar risk management
python -m src.main config --max-drawdown 10.0
python -m src.main config --daily-loss-limit 5.0
```

## 🎛️ Opções Globais

Estas opções podem ser usadas com qualquer comando:

```bash
# Modo verboso (logs detalhados)
python -m src.main [comando] --verbose

# Modo silencioso (apenas erros)
python -m src.main [comando] --quiet

# Arquivo de log personalizado
python -m src.main [comando] --log-file custom.log

# Formato de saída
python -m src.main [comando] --output-format [table|json|csv]

# Arquivo de configuração customizado
python -m src.main [comando] --config-file custom_config.json
```

## 💡 Exemplos Práticos

### 1. Setup Inicial Completo

```bash
# 1. Configurar APIs
python -m src.main config --binance-api-key "sua_api_key"
python -m src.main config --binance-secret "seu_secret"
python -m src.main config --telegram-token "bot_token"
python -m src.main config --telegram-chat-id "chat_id"

# 2. Criar bot de scalping
python -m src.main create-bot \
  --name "Scalping Principal" \
  --strategy scalping_conservative \
  --capital 2000 \
  --symbols BTCUSDT,ETHUSDT,BNBUSDT

# 3. Iniciar bot
python -m src.main start --bot-name "Scalping Principal"

# 4. Monitorar
python -m src.main monitor --refresh 30
```

### 2. Portfolio Diversificado

```bash
# Bot 1: Scalping
python -m src.main create-bot \
  --name "Scalper" \
  --strategy scalping_conservative \
  --capital 1000 \
  --symbols BTCUSDT,ETHUSDT

# Bot 2: Swing Trading  
python -m src.main create-bot \
  --name "Swing Trader" \
  --strategy swing_trading_moderate \
  --capital 2000 \
  --symbols BTCUSDT,ETHUSDT,ADAUSDT,DOTUSDT

# Bot 3: Grid Trading
python -m src.main create-bot \
  --name "Grid Master" \
  --strategy grid_trading \
  --capital 3000 \
  --symbols BTCUSDT,ETHUSDT

# Iniciar todos
python -m src.main start --all
```

### 3. Análise e Backtesting

```bash
# Backtest de diferentes estratégias
for strategy in scalping_conservative swing_trading_moderate trend_following_aggressive; do
  python -m src.main backtest \
    --strategy $strategy \
    --symbols BTCUSDT \
    --start-date 2024-01-01 \
    --end-date 2024-06-01 \
    --capital 10000 \
    --report "backtest_${strategy}.html"
done

# Comparar resultados
python -m src.main portfolio --history 180 --detailed
```

### 4. Monitoramento Avançado

```bash
# Terminal 1: Monitor geral
python -m src.main monitor --refresh 15 --alerts

# Terminal 2: Logs em tempo real
tail -f logs/xbot.log | grep -E "(ERROR|WARNING|TRADE)"

# Terminal 3: Portfolio tracking
watch -n 30 "python -m src.main portfolio"
```

## 🔧 Scripts PowerShell Úteis

### Inicialização Rápida

```powershell
# quick_start.ps1
Write-Host "🚀 Iniciando XBot v2..." -ForegroundColor Green

# Verificar se bots existem
$bots = python -m src.main status --format json | ConvertFrom-Json

if ($bots.Count -eq 0) {
    Write-Host "⚠️  Nenhum bot encontrado. Criando bot padrão..." -ForegroundColor Yellow
    
    python -m src.main create-bot `
        --name "Bot Principal" `
        --strategy scalping_conservative `
        --capital 1000 `
        --symbols BTCUSDT,ETHUSDT
}

# Iniciar bots
python -m src.main start --all

# Abrir monitor
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m src.main monitor --refresh 20"
```

### Backup e Restauração

```powershell
# backup.ps1
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backup_$timestamp"

Write-Host "📦 Criando backup: $backupDir" -ForegroundColor Blue

# Criar diretório de backup
New-Item -ItemType Directory -Path $backupDir -Force

# Copiar arquivos importantes
Copy-Item "config.json" "$backupDir/" -ErrorAction SilentlyContinue
Copy-Item "bots.db" "$backupDir/" -ErrorAction SilentlyContinue
Copy-Item "logs/" "$backupDir/" -Recurse -ErrorAction SilentlyContinue

Write-Host "✅ Backup concluído!" -ForegroundColor Green
```

### Relatório Diário

```powershell
# daily_report.ps1
$today = Get-Date -Format "yyyy-MM-dd"
$reportFile = "reports/daily_$today.html"

Write-Host "📊 Gerando relatório diário..." -ForegroundColor Cyan

# Portfolio status
python -m src.main portfolio --detailed --export "reports/portfolio_$today.csv"

# Bot status
python -m src.main status --detailed --format json | Out-File "reports/status_$today.json"

Write-Host "✅ Relatório salvo em: $reportFile" -ForegroundColor Green
```

## 🎨 Customização da Interface

### Cores e Temas

```bash
# Configurar tema escuro
python -m src.main config --theme dark

# Configurar cores personalizadas
python -m src.main config --colors profit:green,loss:red,warning:yellow
```

### Formato de Saída

```bash
# Saída em tabela (padrão)
python -m src.main status --format table

# Saída em JSON
python -m src.main status --format json

# Saída em CSV
python -m src.main status --format csv
```

## 🚨 Tratamento de Erros

### Códigos de Erro Comuns

| Código | Descrição | Solução |
|--------|-----------|---------|
| 1 | Erro de configuração | Verificar `config.json` |
| 2 | API Key inválida | Reconfigurar Binance API |
| 3 | Capital insuficiente | Aumentar capital do bot |
| 4 | Bot não encontrado | Verificar nome do bot |
| 5 | Erro de conexão | Verificar internet/proxy |

### Depuração

```bash
# Modo debug
python -m src.main [comando] --debug

# Logs detalhados
python -m src.main [comando] --verbose --log-file debug.log

# Verificar configuração
python -m src.main config --validate

# Testar conexão
python -m src.main test-connection
```

## 🎯 Dicas e Boas Práticas

### 1. Organização de Bots

```bash
# Use nomes descritivos
python -m src.main create-bot --name "BTC-Scalp-1min" ...
python -m src.main create-bot --name "ETH-Swing-4h" ...
python -m src.main create-bot --name "Multi-Grid-Range" ...
```

### 2. Monitoramento Eficiente

```bash
# Use refresh otimizado
python -m src.main monitor --refresh 30  # Para scalping
python -m src.main monitor --refresh 300 # Para swing trading
```

### 3. Backup Regular

```bash
# Backup automatizado (cron/task scheduler)
python -m src.main config --backup-interval 1440  # Daily
```

### 4. Testing Seguro

```bash
# Sempre teste primeiro
python -m src.main create-bot \
  --name "Test Bot" \
  --strategy scalping_conservative \
  --capital 100 \
  --testnet \
  --demo-mode
```

---

🎮 **Domine a CLI do XBot v2 e tenha controle total sobre seus bots de trading!**