# XBot v2 - Professional Cryptocurrency Trading Bot System

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://pytest.org/)
[![VS Code](https://img.shields.io/badge/VS%20Code-Ready-blue.svg)](https://code.visualstudio.com/)

An enterprise-grade automated cryptocurrency trading system built with Clean Architecture principles, featuring advanced pattern recognition, sophisticated risk management, and comprehensive monitoring capabilities for Binance exchange integration.

## 🌟 Key Features

### 🎯 Advanced Trading Capabilities
- **Multi-Strategy Support**: Scalping, swing trading, grid trading, and custom strategies
- **Pattern Recognition**: Advanced candlestick patterns, trend analysis, and breakout detection
- **Smart Signal Generation**: ML-powered technical indicators and market sentiment analysis
- **Multi-Exchange Ready**: Primary Binance integration with extensible architecture

### 🛡️ Risk Management & Compliance
- **Sophisticated Risk Analysis**: Kelly Criterion, VaR calculations, volatility-adjusted position sizing
- **Real-time Monitoring**: Continuous risk assessment and automatic position adjustments
- **Compliance Framework**: Built-in validation, audit trails, and regulatory compliance tools
- **Emergency Controls**: Circuit breakers, kill switches, and automated risk mitigation

### 🏗️ Enterprise Architecture
- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **100% Test Coverage**: Comprehensive unit and integration testing suite
- **Professional Documentation**: Complete API documentation and usage examples
- **VS Code Integration**: Pre-configured development environment with 18+ tasks

## 📁 Project Structure

```
xBotv2/
├── src/                         # Core application source code
│   ├── domain/                  # Business logic and entities
│   │   ├── entities.py          # Core business entities (TradingBot, Order, Position)
│   │   └── interfaces.py        # Domain service contracts and interfaces
│   ├── application/             # Application layer and use cases
│   │   └── use_cases.py         # Business use cases and workflows
│   ├── infrastructure/          # External integrations and services
│   │   ├── binance_service.py   # Binance API integration
│   │   ├── pattern_detection_service.py  # Technical pattern recognition
│   │   ├── risk_analysis_service.py      # Risk management algorithms
│   │   ├── signal_generation_service.py  # Trading signal generation
│   │   ├── compliance_service.py         # Compliance and validation
│   │   ├── telegram_service.py           # Real-time notifications
│   │   ├── bot_repository.py     # Bot persistence and state management
│   │   └── config.py            # Configuration management
│   ├── strategies/              # Trading strategy implementations
│   │   ├── scalping_strategy.py       # High-frequency scalping strategy
│   │   ├── swing_trading_strategy.py  # Medium-term swing trading
│   │   └── grid_trading_strategy.py   # Grid trading implementation
│   └── main.py                  # Application entry point and CLI
├── scripts/                     # Utility and setup scripts
│   ├── install.py              # Professional installation script
│   ├── setup.py                # Development environment setup
│   ├── quick_test.py           # Quick system validation
│   ├── run_xbot.py             # Production bot runner
│   └── test_installation.py    # Installation verification
├── examples/                    # Usage examples and demos
│   ├── basic/                  # Basic usage examples
│   │   ├── configuration_example.py   # Basic configuration setup
│   │   └── simple_bot_example.py      # Simple bot implementation
│   ├── advanced/               # Advanced usage examples
│   │   ├── custom_strategy_example.py # Custom trading strategy
│   │   └── multi_bot_example.py       # Multiple bot management
│   └── configurations/         # Sample configuration files
│       ├── conservative_config.py     # Conservative trading setup
│       └── aggressive_config.py       # Aggressive trading setup
├── tests/                       # Comprehensive testing suite
│   ├── unit/                   # Unit tests (100% coverage)
│   │   ├── test_entities.py           # Domain entity tests
│   │   ├── test_use_cases.py          # Application logic tests
│   │   └── test_infrastructure.py     # Service integration tests
│   ├── integration/            # Integration tests
│   │   ├── test_binance_integration.py # Binance API tests
│   │   └── test_end_to_end.py          # Full system tests
│   └── fixtures/               # Test data and mocks
├── docs/                       # Documentation
│   ├── api/                    # API documentation
│   ├── architecture/           # Architecture diagrams and docs
│   └── user_guide/            # User guides and tutorials
├── .vscode/                    # VS Code configuration
│   ├── tasks.json             # Pre-configured development tasks
│   ├── settings.json          # Project-specific settings
│   └── launch.json            # Debug configurations
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── pytest.ini                 # Test configuration
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## � Quick Start

### Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd xBotv2
```

2. **Run the professional installer:**

```bash
python scripts/install.py
```

The installer will:
- Create and configure virtual environment
- Install all dependencies (production and development)
- Set up VS Code workspace with pre-configured tasks
- Validate installation and run quick tests
- Generate example configuration files

### Manual Installation (Alternative)

1. **Create virtual environment:**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

3. **Configure environment variables:**

Create a `.env` file in the project root (use `.env.example` as template):

```env
# Binance API Configuration
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
BINANCE_TESTNET=true  # Use testnet for testing

# Telegram Configuration (Optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Bot Configuration
BOT_DATA_DIR=./data
MAX_CONCURRENT_BOTS=5
DEFAULT_RISK_LEVEL=MODERATE
LOG_LEVEL=INFO
```

## 💻 Usage

### Command Line Interface

```bash
# Run the main application
python src/main.py

# Create a new trading bot
python src/main.py create-bot "MyBot" --capital 1000 --symbols BTCUSDT,ETHUSDT

# List all bots
python src/main.py list-bots

# Start a specific bot
python src/main.py start-bot bot-id

# Stop a bot
python src/main.py stop-bot bot-id

# View bot performance
python src/main.py show-performance bot-id

# Launch comprehensive dashboard
python src/main.py dashboard
```

### Programmatic Usage

```python
from src.main import XBotApplication
from src.domain.entities import TradingStrategy, RiskProfile, RiskLevel

# Initialize application
app = XBotApplication()

# Create custom trading strategy
strategy = TradingStrategy(
    name="Professional Scalping Strategy",
    target_symbols=["BTCUSDT", "ETHUSDT"],
    risk_profile=RiskProfile(
        risk_level=RiskLevel.MODERATE,
        max_position_size=10.0,
        stop_loss_percentage=2.0,
        take_profit_percentage=4.0
    )
)

# Create and start bot
bot_id = await app.create_trading_bot(
    name="My Professional Bot",
    strategy=strategy,
    initial_capital=1000
)

await app.start_bot(bot_id)
```

### Using Examples

Explore the `examples/` directory for comprehensive usage examples:

```bash
# Basic configuration example
python examples/basic/configuration_example.py

# Advanced custom strategy
python examples/advanced/custom_strategy_example.py

# Multiple bot management
python examples/advanced/multi_bot_example.py
```

## � Advanced Features

### Pattern Detection & Technical Analysis

- **Candlestick Patterns**: Engulfing, Hammer, Doji, Shooting Star, and 20+ more patterns
- **Trend Analysis**: Triangle formations, flags, pennants, and breakout detection
- **Support & Resistance**: Dynamic level identification and validation
- **Volume Analysis**: Volume-weighted indicators and anomaly detection

### Risk Management Suite

- **Kelly Criterion**: Optimal position sizing based on historical performance
- **Value at Risk (VaR)**: Monte Carlo simulation for risk assessment
- **Sharpe Ratio**: Risk-adjusted return optimization
- **Dynamic Stop-Loss**: Volatility-adjusted stop-loss levels
- **Drawdown Control**: Maximum drawdown limits and recovery strategies

### Compliance & Auditing

- **Pre-Trade Validation**: Comprehensive checks before order execution
- **Position Limits**: Real-time position size and exposure monitoring
- **Audit Trail**: Complete logging of all trading decisions and actions
- **Emergency Controls**: Circuit breakers and emergency stop mechanisms
- **Regulatory Compliance**: Built-in compliance checks for various jurisdictions

## 🧪 Testing & Quality Assurance

### Running Tests

```bash
# Run all tests with coverage
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run specific test categories
python -m pytest tests/unit/          # Unit tests only
python -m pytest tests/integration/  # Integration tests only

# Run tests with VS Code tasks
# Ctrl+Shift+P -> "Tasks: Run Task" -> "Run All Tests"
```

### Test Coverage

The project maintains **100% test coverage** across all modules:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions and external services
- **End-to-End Tests**: Complete workflow testing from API to execution
- **Mock Services**: Comprehensive mocking for external dependencies

### VS Code Integration

Pre-configured VS Code environment with 18+ development tasks:

```bash
# Available VS Code tasks (Ctrl+Shift+P -> Tasks: Run Task)
- Install Dependencies
- Run All Tests
- Run Tests with Coverage
- Format Code (Black)
- Lint Code (Flake8)
- Type Check (mypy)
- Start Development Server
- Build Documentation
- Run Security Scan
- Performance Profiling
- Database Migration
- Clean Build Files
- Generate API Docs
- Run Benchmark Tests
- Quick System Check
- Deploy to Production
- Start Monitoring
- Backup Data
```

### Development Workflow

1. **Setup**: Run `python scripts/install.py` for complete environment setup
2. **Code**: Use VS Code with pre-configured settings and extensions
3. **Test**: Continuous testing with `pytest-watch` for TDD workflow
4. **Quality**: Automatic code formatting with Black and linting with Flake8
5. **Deploy**: Professional deployment scripts with health checks

## � Performance Monitoring

### Available Metrics

- **Realized/Unrealized P&L**: Real-time profit and loss tracking
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Trade Statistics**: Count, duration, and success rates
- **Risk Metrics**: VaR, volatility, and exposure analysis

### Real-Time Dashboard

The dashboard command provides comprehensive monitoring:

- Live bot status and performance
- Open positions and pending orders
- Risk alerts and compliance status
- Audit logs and trade history
- Market data and technical indicators

## ⚠️ Security & Risk Considerations

### Security Best Practices

1. **API Security**: Store API keys securely, never in source code
2. **Testnet First**: Always test strategies on Binance testnet
3. **Regular Monitoring**: Automated trading requires constant oversight
4. **Capital Limits**: Never risk more than you can afford to lose
5. **Regular Backups**: Maintain backups of configurations and data

### Risk Management

- **Position Sizing**: Sophisticated algorithms for optimal position sizing
- **Stop-Loss Orders**: Dynamic stop-loss based on volatility
- **Correlation Analysis**: Monitor correlation between positions
- **Emergency Controls**: Immediate stop mechanisms for critical situations

## 🏗️ Architecture & Documentation

### Clean Architecture Implementation

- **Domain Layer**: Business entities and core logic
- **Application Layer**: Use cases and application services
- **Infrastructure Layer**: External service integrations
- **Presentation Layer**: CLI and API interfaces

### API Documentation

Comprehensive documentation available for all major components:

- **TradingBot**: Core bot functionality and lifecycle management
- **TradingStrategy**: Strategy implementation and customization
- **Order Management**: Order creation, modification, and tracking
- **Position Management**: Position monitoring and risk assessment
- **Pattern Detection**: Technical analysis and signal generation

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Maintain 100% test coverage
- Follow Clean Architecture principles
- Use Black for code formatting
- Write comprehensive documentation
- Follow semantic versioning

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## ⚖️ Disclaimer

This software is provided for educational and research purposes only. Cryptocurrency trading involves significant financial risks. Users are solely responsible for their trading decisions and any resulting financial losses. The developers assume no responsibility for financial losses incurred through the use of this software.

**Always:**
- Test thoroughly on paper trading or testnet
- Start with small amounts
- Understand the risks involved
- Comply with local regulations
- Seek professional financial advice

## 🔗 Resources

### Documentation & Guides

- [Complete User Guide](docs/user_guide/)
- [API Documentation](docs/api/)
- [Architecture Overview](docs/architecture/)
- [Development Setup](docs/development/)

### External Resources

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Python-Binance Library](https://python-binance.readthedocs.io/)
- [TA-Lib Documentation](https://ta-lib.org/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 🆘 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions
- **Documentation**: Comprehensive docs in the `docs/` directory
- **Examples**: Practical examples in the `examples/` directory

---

Built with ❤️ for the algorithmic trading community