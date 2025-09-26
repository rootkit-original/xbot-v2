# 🏗️ Arquitetura do Sistema

Guia completo da arquitetura do XBot v2, padrões utilizados e estrutura do código.

## 🎯 Visão Geral Arquitetural

O XBot v2 foi construído seguindo os princípios da **Clean Architecture** (Arquitetura Limpa), garantindo:

- ✅ **Separação de responsabilidades**
- ✅ **Baixo acoplamento entre camadas**
- ✅ **Alta coesão interna**
- ✅ **Testabilidade e manutenibilidade**
- ✅ **Independência de frameworks externos**
- ✅ **Flexibilidade para mudanças**

## 📊 Diagrama da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │     CLI     │  │  Web API    │  │   Telegram Bot      │  │
│  │ Interface   │  │ Interface   │  │    Interface        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  APPLICATION LAYER                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Trading   │  │ Portfolio   │  │   Notification      │  │
│  │ Use Cases   │  │ Use Cases   │  │    Use Cases        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   DOMAIN LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Entities   │  │ Value       │  │   Domain            │  │
│  │   (Models)  │  │ Objects     │  │   Services          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                INFRASTRUCTURE LAYER                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Binance    │  │  Database   │  │    External         │  │
│  │    API      │  │  Services   │  │    Services         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🏛️ Camadas da Arquitetura

### 1. Domain Layer (Camada de Domínio)

**Localização:** `src/domain/`

A camada mais interna e importante do sistema, contém:

#### Entidades (`src/domain/entities/`)

```python
# trading_bot.py - Entidade principal do bot de trading
class TradingBot:
    def __init__(self, bot_id: str, name: str, strategy: str):
        self._id = bot_id
        self._name = name
        self._strategy = strategy
        self._status = BotStatus.STOPPED
        self._positions = []
        self._balance = 0.0
    
    def start_trading(self) -> None:
        """Inicia o bot de trading"""
        if self._status == BotStatus.STOPPED:
            self._status = BotStatus.RUNNING
    
    def stop_trading(self) -> None:
        """Para o bot de trading"""
        self._status = BotStatus.STOPPED

# position.py - Entidade de posição
class Position:
    def __init__(self, symbol: str, side: str, quantity: float, price: float):
        self._id = str(uuid.uuid4())
        self._symbol = symbol
        self._side = side
        self._quantity = quantity
        self._entry_price = price
        self._created_at = datetime.now()
```

#### Value Objects (`src/domain/value_objects/`)

```python
# trading_signal.py
class TradingSignal:
    def __init__(self, action: str, symbol: str, price: float, confidence: float):
        self._action = action  # BUY, SELL, HOLD
        self._symbol = symbol
        self._price = price
        self._confidence = confidence
        self._timestamp = datetime.now()

# money.py
class Money:
    def __init__(self, amount: float, currency: str = "USDT"):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self._amount = amount
        self._currency = currency
```

#### Domain Services (`src/domain/services/`)

```python
# signal_generator.py
class SignalGeneratorService:
    def generate_signal(self, market_data: MarketData, strategy: str) -> TradingSignal:
        """Gera sinais de trading baseado nos dados de mercado"""
        pass

# risk_calculator.py
class RiskCalculatorService:
    def calculate_position_size(self, account_balance: float, risk_percent: float) -> float:
        """Calcula o tamanho da posição baseado no risco"""
        pass
```

### 2. Application Layer (Camada de Aplicação)

**Localização:** `src/application/`

Contém os casos de uso (use cases) da aplicação:

#### Use Cases (`src/application/use_cases/`)

```python
# create_trading_bot.py
class CreateTradingBotUseCase:
    def __init__(self, bot_repository: TradingBotRepository):
        self._bot_repository = bot_repository
    
    def execute(self, request: CreateTradingBotRequest) -> CreateTradingBotResponse:
        # Validar dados de entrada
        if not request.name or not request.strategy:
            raise ValidationError("Name and strategy are required")
        
        # Criar entidade do bot
        bot = TradingBot(
            bot_id=str(uuid.uuid4()),
            name=request.name,
            strategy=request.strategy
        )
        
        # Salvar no repositório
        self._bot_repository.save(bot)
        
        return CreateTradingBotResponse(bot_id=bot.id, success=True)

# start_trading_bot.py
class StartTradingBotUseCase:
    def __init__(self, bot_repository: TradingBotRepository,
                 market_service: MarketDataService):
        self._bot_repository = bot_repository
        self._market_service = market_service
    
    def execute(self, bot_id: str) -> StartTradingResponse:
        # Buscar bot
        bot = self._bot_repository.find_by_id(bot_id)
        if not bot:
            raise BotNotFoundError(f"Bot {bot_id} not found")
        
        # Iniciar trading
        bot.start_trading()
        
        # Salvar estado
        self._bot_repository.save(bot)
        
        return StartTradingResponse(success=True)
```

#### DTOs (`src/application/dtos/`)

```python
# create_bot_dto.py
@dataclass
class CreateTradingBotRequest:
    name: str
    strategy: str
    capital: float
    symbols: List[str]
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

@dataclass
class CreateTradingBotResponse:
    bot_id: str
    success: bool
    message: Optional[str] = None
```

### 3. Infrastructure Layer (Camada de Infraestrutura)

**Localização:** `src/infrastructure/`

Implementa interfaces definidas nas camadas superiores:

#### Repositories (`src/infrastructure/repositories/`)

```python
# sqlite_trading_bot_repository.py
class SQLiteTradingBotRepository(TradingBotRepository):
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._init_db()
    
    def save(self, bot: TradingBot) -> None:
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO trading_bots 
                (id, name, strategy, status, balance, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bot.id, bot.name, bot.strategy, bot.status.value, 
                  bot.balance, bot.created_at))
            conn.commit()
    
    def find_by_id(self, bot_id: str) -> Optional[TradingBot]:
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, strategy, status, balance, created_at
                FROM trading_bots WHERE id = ?
            """, (bot_id,))
            row = cursor.fetchone()
            
            if row:
                return TradingBot(
                    bot_id=row[0],
                    name=row[1],
                    strategy=row[2]
                )
            return None
```

#### External Services (`src/infrastructure/services/`)

```python
# binance_market_service.py
class BinanceMarketService(MarketDataService):
    def __init__(self, api_key: str, secret_key: str):
        self._client = Client(api_key, secret_key)
    
    def get_price(self, symbol: str) -> float:
        ticker = self._client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    
    def get_klines(self, symbol: str, interval: str, limit: int) -> List[Kline]:
        klines = self._client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        return [self._convert_to_kline(kline) for kline in klines]

# telegram_notification_service.py
class TelegramNotificationService(NotificationService):
    def __init__(self, bot_token: str, chat_id: str):
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._bot = telebot.TeleBot(bot_token)
    
    def send_message(self, message: str) -> None:
        self._bot.send_message(self._chat_id, message)
```

### 4. Presentation Layer (Camada de Apresentação)

**Localização:** `src/presentation/`

Interface com o usuário:

#### CLI (`src/presentation/cli/`)

```python
# main_cli.py
class MainCLI:
    def __init__(self):
        self._create_bot_use_case = CreateTradingBotUseCase(
            bot_repository=SQLiteTradingBotRepository("bots.db")
        )
    
    def create_bot_command(self, name: str, strategy: str, capital: float):
        try:
            request = CreateTradingBotRequest(
                name=name,
                strategy=strategy,
                capital=capital,
                symbols=["BTCUSDT"]
            )
            response = self._create_bot_use_case.execute(request)
            
            if response.success:
                print(f"✅ Bot '{name}' criado com sucesso!")
            else:
                print(f"❌ Erro ao criar bot: {response.message}")
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
```

## 🔗 Interfaces e Contratos

### Repository Interfaces

```python
# src/domain/repositories/trading_bot_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.trading_bot import TradingBot

class TradingBotRepository(ABC):
    @abstractmethod
    def save(self, bot: TradingBot) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, bot_id: str) -> Optional[TradingBot]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[TradingBot]:
        pass
    
    @abstractmethod
    def delete(self, bot_id: str) -> None:
        pass
```

### Service Interfaces

```python
# src/domain/services/market_data_service.py
class MarketDataService(ABC):
    @abstractmethod
    def get_price(self, symbol: str) -> float:
        pass
    
    @abstractmethod
    def get_klines(self, symbol: str, interval: str, limit: int) -> List[Kline]:
        pass
    
    @abstractmethod
    def get_order_book(self, symbol: str) -> OrderBook:
        pass

# src/domain/services/notification_service.py
class NotificationService(ABC):
    @abstractmethod
    def send_message(self, message: str) -> None:
        pass
    
    @abstractmethod
    def send_alert(self, alert: Alert) -> None:
        pass
```

## 🏗️ Padrões de Design Utilizados

### 1. Repository Pattern

Abstrai o acesso aos dados, permitindo trocar implementações:

```python
# Interface
class TradingBotRepository(ABC):
    @abstractmethod
    def save(self, bot: TradingBot) -> None:
        pass

# Implementações
class SQLiteTradingBotRepository(TradingBotRepository):
    # Implementação SQLite
    pass

class MongoTradingBotRepository(TradingBotRepository):
    # Implementação MongoDB
    pass
```

### 2. Strategy Pattern

Para diferentes estratégias de trading:

```python
# src/domain/strategies/trading_strategy.py
class TradingStrategy(ABC):
    @abstractmethod
    def generate_signal(self, market_data: MarketData) -> TradingSignal:
        pass

# Implementações
class ScalpingStrategy(TradingStrategy):
    def generate_signal(self, market_data: MarketData) -> TradingSignal:
        # Lógica de scalping
        pass

class SwingTradingStrategy(TradingStrategy):
    def generate_signal(self, market_data: MarketData) -> TradingSignal:
        # Lógica de swing trading
        pass
```

### 3. Factory Pattern

Para criar objetos complexos:

```python
# src/infrastructure/factories/strategy_factory.py
class StrategyFactory:
    @staticmethod
    def create_strategy(strategy_name: str) -> TradingStrategy:
        strategies = {
            "scalping_conservative": ScalpingStrategy,
            "swing_trading_moderate": SwingTradingStrategy,
            "trend_following_aggressive": TrendFollowingStrategy
        }
        
        strategy_class = strategies.get(strategy_name)
        if not strategy_class:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        return strategy_class()
```

### 4. Observer Pattern

Para notificações e eventos:

```python
# src/domain/events/event_dispatcher.py
class EventDispatcher:
    def __init__(self):
        self._listeners = {}
    
    def subscribe(self, event_type: str, listener: callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
    
    def dispatch(self, event: Event):
        listeners = self._listeners.get(event.type, [])
        for listener in listeners:
            listener(event)
```

### 5. Dependency Injection

Para inversão de dependências:

```python
# src/infrastructure/di/container.py
class DIContainer:
    def __init__(self):
        self._services = {}
    
    def register(self, interface: type, implementation: type):
        self._services[interface] = implementation
    
    def get(self, interface: type):
        implementation = self._services.get(interface)
        if not implementation:
            raise ValueError(f"Service {interface} not registered")
        return implementation()
```

## 📁 Estrutura de Pastas

```
src/
├── domain/                     # Camada de domínio
│   ├── entities/              # Entidades de negócio
│   │   ├── trading_bot.py
│   │   ├── position.py
│   │   └── order.py
│   ├── value_objects/         # Objetos de valor
│   │   ├── money.py
│   │   ├── trading_signal.py
│   │   └── market_data.py
│   ├── services/              # Serviços de domínio
│   │   ├── signal_generator.py
│   │   └── risk_calculator.py
│   ├── repositories/          # Interfaces de repositório
│   │   └── trading_bot_repository.py
│   └── events/               # Eventos de domínio
│       └── trading_events.py
├── application/               # Camada de aplicação
│   ├── use_cases/            # Casos de uso
│   │   ├── create_trading_bot.py
│   │   ├── start_trading_bot.py
│   │   └── stop_trading_bot.py
│   └── dtos/                 # Data Transfer Objects
│       ├── create_bot_dto.py
│       └── trading_dto.py
├── infrastructure/            # Camada de infraestrutura
│   ├── repositories/         # Implementações de repositório
│   │   ├── sqlite_bot_repository.py
│   │   └── memory_bot_repository.py
│   ├── services/            # Serviços externos
│   │   ├── binance_service.py
│   │   └── telegram_service.py
│   ├── database/            # Configuração de banco
│   │   └── sqlite_config.py
│   └── config/              # Configurações
│       └── settings.py
├── presentation/             # Camada de apresentação
│   ├── cli/                 # Interface CLI
│   │   └── main_cli.py
│   └── web/                 # Interface Web (futuro)
│       └── api.py
└── shared/                  # Utilitários compartilhados
    ├── exceptions/          # Exceções customizadas
    ├── logging/            # Configuração de logs
    └── utils/              # Utilitários gerais
```

## 🔄 Fluxo de Execução

### 1. Criação de Bot

```
CLI Input → CreateBotUseCase → TradingBot Entity → Repository → Database
```

### 2. Execução de Trading

```
Market Data → Strategy → Signal → Use Case → Bot Entity → Order → Binance API
```

### 3. Notificação

```
Trading Event → EventDispatcher → NotificationService → Telegram API
```

## 🧪 Testabilidade

A arquitetura limpa facilita muito os testes:

### Testes Unitários

```python
# test_create_trading_bot_use_case.py
class TestCreateTradingBotUseCase:
    def test_should_create_bot_successfully(self):
        # Arrange
        mock_repository = Mock(spec=TradingBotRepository)
        use_case = CreateTradingBotUseCase(mock_repository)
        request = CreateTradingBotRequest(
            name="Test Bot",
            strategy="scalping",
            capital=1000.0,
            symbols=["BTCUSDT"]
        )
        
        # Act
        response = use_case.execute(request)
        
        # Assert
        assert response.success is True
        mock_repository.save.assert_called_once()
```

### Testes de Integração

```python
# test_binance_integration.py
class TestBinanceIntegration:
    def test_should_get_real_price(self):
        # Arrange
        service = BinanceMarketService(api_key, secret_key)
        
        # Act
        price = service.get_price("BTCUSDT")
        
        # Assert
        assert isinstance(price, float)
        assert price > 0
```

## 🚀 Benefícios da Arquitetura

### 1. **Manutenibilidade**
- Código bem organizado e separado por responsabilidades
- Fácil localizar e modificar funcionalidades específicas
- Reduz o acoplamento entre componentes

### 2. **Testabilidade**
- Cada camada pode ser testada independentemente
- Uso de mocks e stubs para testes isolados
- Cobertura de testes mais abrangente

### 3. **Flexibilidade**
- Troca de implementações sem afetar outras camadas
- Fácil adição de novas funcionalidades
- Suporte a múltiplas interfaces (CLI, Web, API)

### 4. **Escalabilidade**
- Estrutura preparada para crescimento
- Facilita o trabalho em equipe
- Permite distribuição de responsabilidades

### 5. **Independência de Frameworks**
- Core business logic independente de tecnologias externas
- Facilita migrações e upgrades
- Reduz vendor lock-in

## 📚 Próximos Passos

### Melhorias Planejadas

1. **Event Sourcing**: Implementar histórico completo de eventos
2. **CQRS**: Separar comandos de consultas
3. **Microservices**: Dividir em serviços menores
4. **GraphQL**: API mais flexível
5. **WebSockets**: Comunicação em tempo real
6. **Message Queue**: Processamento assíncrono robusto

---

🏗️ **Uma arquitetura sólida é a base para um sistema de trading confiável e evolutivo!**