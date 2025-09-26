# XBot v2 - Sistema Completo de Trading Bot

Um sistema avançado de trading bot desenvolvido com Clean Architecture para negociação automatizada na Binance.

## 🚀 Características Principais

- **Detecção de Padrões Avançada**: Identifica padrões de candlesticks, tendências e breakouts
- **Análise de Risco Sofisticada**: Gerenciamento de risco com Kelly Criterion, VaR e análise de volatilidade
- **Compliance e Auditoria**: Sistema completo de validação e logs de auditoria
- **Notificações Telegram**: Alertas em tempo real sobre trades e performance
- **Clean Architecture**: Código organizado, testável e maintível
- **Interface CLI**: Comando line interface completa para gerenciamento dos bots

## 📁 Estrutura do Projeto

```
xBotv2/
├── src/
│   ├── domain/
│   │   ├── entities.py          # Entidades de negócio (TradingBot, Order, Position, etc.)
│   │   └── interfaces.py        # Interfaces e contratos
│   ├── application/
│   │   └── use_cases.py         # Casos de uso da aplicação
│   ├── infrastructure/
│   │   ├── binance_service.py   # Integração com Binance API
│   │   ├── pattern_detection_service.py  # Detecção de padrões técnicos
│   │   ├── risk_analysis_service.py      # Análise de risco
│   │   ├── signal_generation_service.py  # Geração de sinais
│   │   ├── compliance_service.py         # Validação e compliance
│   │   ├── telegram_service.py           # Notificações Telegram
│   │   ├── bot_repository.py             # Armazenamento de bots
│   │   └── config.py                     # Configurações
│   └── main.py                  # Ponto de entrada da aplicação
├── requirements.txt
└── README.md
```

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd xBotv2
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:

```env
# Binance API Configuration
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
BINANCE_TESTNET=true  # Use testnet for testing

# Telegram Configuration (Opcional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Bot Configuration
BOT_DATA_DIR=./data
MAX_CONCURRENT_BOTS=5
DEFAULT_RISK_LEVEL=MODERATE
```

## 🎯 Uso Básico

### Interface de Linha de Comando

```bash
# Iniciar a aplicação
python src/main.py

# Criar um novo bot
python src/main.py create-bot "MeuBot" --capital 1000 --symbols BTCUSDT,ETHUSDT

# Listar bots
python src/main.py list-bots

# Iniciar um bot
python src/main.py start-bot bot-id

# Parar um bot
python src/main.py stop-bot bot-id

# Ver performance
python src/main.py show-performance bot-id

# Dashboard completo
python src/main.py dashboard
```

### Uso Programático

```python
from src.main import XBotApplication
from src.domain.entities import TradingStrategy, RiskProfile, RiskLevel

# Inicializar aplicação
app = XBotApplication()

# Criar estratégia personalizada
strategy = TradingStrategy(
    name="Scalping Strategy",
    target_symbols=["BTCUSDT", "ETHUSDT"],
    risk_profile=RiskProfile(
        risk_level=RiskLevel.MODERATE,
        max_position_size=10.0,
        stop_loss_percentage=2.0,
        take_profit_percentage=4.0
    )
)

# Criar e executar bot
bot_id = await app.create_trading_bot(
    name="Meu Bot Scalping",
    strategy=strategy,
    initial_capital=1000
)

await app.start_bot(bot_id)
```

## 📊 Funcionalidades Avançadas

### Detecção de Padrões

O sistema identifica automaticamente:
- **Padrões de Candlestick**: Engulfing, Hammer, Doji, Shooting Star
- **Padrões de Tendência**: Triângulos, Flags, Pennants
- **Suporte e Resistência**: Níveis chave de preço
- **Breakouts**: Rompimentos de níveis importantes

### Análise de Risco

- **Kelly Criterion**: Cálculo otimizado do tamanho da posição
- **Value at Risk (VaR)**: Estimativa de perdas potenciais
- **Sharpe Ratio**: Análise de retorno ajustado ao risco
- **Drawdown Control**: Controle de perdas máximas

### Compliance e Auditoria

- **Validação de Trades**: Verificação antes da execução
- **Limites de Posição**: Controle de exposição
- **Audit Trail**: Log completo de todas as operações
- **Emergency Stop**: Parada automática em condições críticas

## 🔧 Configuração Avançada

### Personalização de Estratégias

```python
# Criar estratégia personalizada
strategy = TradingStrategy(
    name="Custom Strategy",
    target_symbols=["BTCUSDT"],
    indicators={
        "rsi_period": 14,
        "ema_short": 9,
        "ema_long": 21,
        "bb_period": 20
    },
    risk_profile=RiskProfile(
        risk_level=RiskLevel.CONSERVATIVE,
        max_position_size=5.0,
        max_concurrent_positions=3,
        stop_loss_percentage=1.5,
        take_profit_percentage=3.0,
        max_daily_loss=5.0
    )
)
```

### Configuração de Notificações

```python
# Configurar notificações Telegram
telegram_config = {
    "enabled": True,
    "bot_token": "your_token",
    "chat_id": "your_chat_id",
    "notifications": {
        "trades": True,
        "signals": True,
        "errors": True,
        "performance": True
    }
}
```

## 📈 Monitoramento e Performance

### Métricas Disponíveis

- **P&L Realizado/Não Realizado**
- **Taxa de Acerto (Win Rate)**
- **Profit Factor**
- **Maximum Drawdown**
- **Sharpe Ratio**
- **Número de Trades**
- **Tempo Médio por Trade**

### Dashboard em Tempo Real

O comando `dashboard` fornece:
- Status de todos os bots
- Performance em tempo real
- Posições abertas
- Alertas de risco
- Logs de auditoria

## ⚠️ Importantes Considerações de Segurança

1. **Use o Testnet primeiro**: Sempre teste suas estratégias no testnet da Binance
2. **Proteja suas chaves**: Nunca commite chaves de API no código
3. **Monitore constantemente**: Bots automatizados requerem supervisão
4. **Limite o capital**: Nunca arrisque mais do que pode perder
5. **Backup regular**: Faça backup das configurações e logs

## 🧪 Testes

```bash
# Executar testes (quando implementados)
python -m pytest tests/

# Executar em modo dry-run (simulação)
python src/main.py start-bot bot-id --dry-run
```

## 📚 Documentação da API

### Principais Classes

- **TradingBot**: Bot principal com lógica de trading
- **TradingStrategy**: Estratégia de negociação
- **Order**: Representação de uma ordem
- **Position**: Posição aberta no mercado
- **Pattern**: Padrão técnico detectado
- **RiskProfile**: Perfil de risco do bot

### Serviços

- **BinanceService**: Integração com Binance
- **PatternDetectionService**: Detecção de padrões
- **RiskAnalysisService**: Análise de risco
- **ComplianceService**: Validação e compliance
- **TelegramService**: Notificações

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ⚖️ Disclaimer

Este software é fornecido apenas para fins educacionais. Trading de criptomoedas envolve riscos significativos. O usuário é totalmente responsável por suas decisões de investimento. Os desenvolvedores não se responsabilizam por perdas financeiras.

## 🔗 Links Úteis

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Python-Binance Library](https://python-binance.readthedocs.io/)
- [TA-Lib Documentation](https://ta-lib.org/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

**Desenvolvido com ❤️ para a comunidade de trading algorítmico**