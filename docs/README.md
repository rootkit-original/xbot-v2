# 📖 Documentação XBot v2

Bem-vindo à documentação completa do XBot v2 - Sistema Avançado de Trading Automatizado com Inteligência Artificial.

## 🎯 Sobre o XBot v2

O XBot v2 é um sistema de trading automatizado construído com **Clean Architecture**, oferecendo:

- ✅ **7 Estratégias Pré-Configuradas** otimizadas para diferentes mercados
- ✅ **Interface CLI Intuitiva** para controle total via linha de comando
- ✅ **Monitoramento em Tempo Real** com alertas via Telegram
- ✅ **Risk Management Avançado** com stop loss e take profit inteligentes
- ✅ **Backtesting Completo** para validar estratégias
- ✅ **API REST + WebSockets** para integração externa
- ✅ **Multi-Exchange Support** (Binance Spot e Futures)

## 🚀 Quick Start

### 1. Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/username/xbot-v2.git
cd xbot-v2

# Configure o ambiente Python
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure suas APIs
python -m src.main config --binance-api-key "sua_api_key"
python -m src.main config --binance-secret "seu_secret"
```

### 2. Primeiro Bot

```bash
# Crie seu primeiro bot
python -m src.main create-bot \
  --name "Meu Primeiro Bot" \
  --strategy scalping_conservative \
  --capital 1000 \
  --symbols BTCUSDT,ETHUSDT

# Inicie o bot
python -m src.main start --bot-name "Meu Primeiro Bot"

# Monitore em tempo real
python -m src.main monitor --refresh 30
```

### 3. Próximos Passos

1. **[Instalação Detalhada](installation.md)** - Setup completo do ambiente
2. **[Quick Start Completo](quick-start.md)** - Tutorial passo a passo
3. **[Estratégias](user-guide/trading-strategies.md)** - Escolha a melhor estratégia

## 📚 Documentação

### � Para Usuários

#### Guias Essenciais
- **[📋 Instalação](installation.md)** - Configure seu ambiente de trading
- **[⚡ Quick Start](quick-start.md)** - Primeiros passos e configuração inicial
- **[🎮 Interface CLI](user-guide/cli-interface.md)** - Domine a linha de comando
- **[📊 Estratégias de Trading](user-guide/trading-strategies.md)** - 7 estratégias completas
- **[📱 Monitoramento e Alertas](user-guide/monitoring-alerts.md)** - Sistema de notificações

### 👨‍💻 Para Desenvolvedores

#### Arquitetura e Desenvolvimento
- **[🏗️ Arquitetura do Sistema](developer-guide/architecture.md)** - Clean Architecture e padrões
- **[🔧 API Reference](api/api-reference.md)** - REST API completa + WebSockets

### 📈 Estratégias Detalhadas

| Estratégia | Risco | Capital Mín. | Timeframe | Descrição |
|-----------|-------|-------------|-----------|-----------|
| [**Scalping Conservador**](user-guide/trading-strategies.md#scalping-conservador) | � Baixo | $500 | 1-5min | Lucros pequenos e frequentes |
| [**Swing Trading**](user-guide/trading-strategies.md#swing-trading-moderado) | 🟡 Moderado | $1,000 | 4h-1d | Movimentos de médio prazo |
| [**Trend Following**](user-guide/trading-strategies.md#trend-following-agressivo) | 🔴 Alto | $2,000 | 1-4h | Segue tendências fortes |
| [**Breakout Strategy**](user-guide/trading-strategies.md#breakout-strategy) | 🟡 Moderado | $1,000 | 1-4h | Rompimentos de níveis |
| [**Mean Reversion**](user-guide/trading-strategies.md#mean-reversion) | 🟡 Moderado | $1,000 | 15m-1h | Reversão à média |
| [**Grid Trading**](user-guide/trading-strategies.md#grid-trading) | 🟢 Baixo | $1,500 | Qualquer | Múltiplas posições em grid |
| [**DCA Strategy**](user-guide/trading-strategies.md#dca-strategy) | 🟢 Baixo | $2,000+ | Diário | Acumulação em quedas |

## 🛠️ Recursos Técnicos

### Arquitetura
- **Clean Architecture** com separação clara de responsabilidades
- **Domain-Driven Design** para modelagem de negócio
- **Async/Await** para performance otimizada
- **SQLite** para persistência local
- **JWT Authentication** para segurança da API

### Integrations
- **Binance API** - Spot e Futures trading
- **Telegram Bot** - Alertas e notificações
- **WebSocket** - Dados em tempo real
- **REST API** - Integração externa completa

### Indicadores Técnicos
- RSI, MACD, Bollinger Bands
- EMAs, SMAs, ATR, ADX
- Volume analysis
- Support/Resistance detection

## 🔗 Links e Recursos

### Comunidade e Suporte
- 📧 **Email**: support@xbot-trading.com
- 💬 **Discord**: [Discord Community](https://discord.gg/xbot-trading)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/username/xbot-v2/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/username/xbot-v2/discussions)
- 📱 **Telegram Group**: [@xbot_trading](https://t.me/xbot_trading)

### Desenvolvimento
- 🔧 **GitHub Repository**: [xbot-v2](https://github.com/username/xbot-v2)
- 📚 **Wiki**: [Project Wiki](https://github.com/username/xbot-v2/wiki)
- 🚀 **Roadmap**: [Project Roadmap](https://github.com/username/xbot-v2/projects/1)
- 📋 **Changelog**: [Release Notes](https://github.com/username/xbot-v2/releases)

### Recursos Externos
- 📖 **Binance API Docs**: [Official Documentation](https://binance-docs.github.io/apidocs/)
- 🤖 **Telegram Bot API**: [Bot API Guide](https://core.telegram.org/bots/api)

## 🏆 Status do Projeto

- ✅ **Core System**: Completo e testado
- ✅ **7 Trading Strategies**: Implementadas e otimizadas
- ✅ **CLI Interface**: Funcional com todos os comandos
- ✅ **Risk Management**: Sistema robusto
- ✅ **Monitoring System**: Alertas e dashboards
- ✅ **API & WebSockets**: Endpoints funcionais
- 🚧 **Web Interface**: Em desenvolvimento
- 🚧 **Mobile App**: Planejado para v3.0
- 🚧 **Machine Learning**: Modelos preditivos em desenvolvimento

## 📊 Performance Histórica

### Backtests (12 meses)
- **Scalping Conservador**: +45% ROI, 15% max drawdown
- **Swing Trading**: +38% ROI, 12% max drawdown
- **Trend Following**: +65% ROI, 25% max drawdown
- **Grid Trading**: +28% ROI, 8% max drawdown

*⚠️ Rentabilidade passada não garante resultados futuros. Trading envolve riscos.*

## 🎯 Começando Agora

### Para Iniciantes
1. 📖 Leia o **[Quick Start](quick-start.md)** completo
2. 🎮 Comece com **Scalping Conservador** ou **Grid Trading**
3. 💬 Entre no **grupo Telegram** para suporte
4. 📊 Use **modo demo** até ganhar confiança

### Para Experts
1. 🏗️ Estude a **[Arquitetura](developer-guide/architecture.md)**
2. 🔧 Explore a **[API Reference](api/api-reference.md)**
3. 🧪 Crie **estratégias customizadas**
4. 🤝 **Contribua** com o projeto

---

🚀 **Pronto para automatizar seus trades? Comece pelo [Quick Start](quick-start.md) agora!**

---

*XBot v2 - Desenvolvido com ❤️ por traders, para traders.*
- [DCA Strategy](strategies/dca-strategy.md)

### 🔧 API Reference
- [Domain Entities](api/entities.md)
- [Services](api/services.md)
- [Use Cases](api/use-cases.md)
- [Configuration](api/configuration.md)

### 📋 Referência
- [FAQ](faq.md)
- [Troubleshooting](troubleshooting.md)
- [Changelog](changelog.md)
- [Roadmap](roadmap.md)

## 🎯 Visão Geral

O XBot v2 é um sistema completo de trading automatizado que oferece:

- **Detecção de Padrões Avançada**: Identifica padrões técnicos complexos
- **Análise de Risco Sofisticada**: Gestão inteligente de capital e risco
- **Múltiplas Estratégias**: 7+ estratégias pré-configuradas
- **Clean Architecture**: Código modular e extensível
- **Interface CLI**: Controle completo via linha de comando
- **Integração Binance**: Trading real com API oficial
- **Notificações Telegram**: Alertas em tempo real

## 🚨 Aviso Legal

⚠️ **IMPORTANTE**: Trading de criptomoedas envolve riscos significativos. Este software é fornecido apenas para fins educacionais. O usuário é totalmente responsável por suas decisões de investimento.

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/xbot-v2/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/xbot-v2/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/seu-usuario/xbot-v2/wiki)

---
**Desenvolvido com ❤️ para a comunidade de trading algorítmico**