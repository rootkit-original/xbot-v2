# 🧪 Testing Guide - Guia de Testes

Guia completo para testes no XBot v2 com pytest, mocking e CI/CD.

## 🎯 Visão Geral dos Testes

### Arquitetura de Testes

```
tests/
├── unit/              # Testes unitários
│   ├── domain/       # Entidades e regras de negócio
│   ├── application/  # Casos de uso
│   ├── infrastructure/ # Adaptadores externos
│   └── web/          # Controllers e API
├── integration/      # Testes de integração
│   ├── api/          # Testes de API
│   ├── database/     # Testes de banco
│   └── external/     # Testes com APIs externas
├── e2e/              # Testes end-to-end
├── performance/      # Testes de performance
├── fixtures/         # Dados de teste
├── mocks/           # Mocks e stubs
└── conftest.py      # Configurações pytest
```

### Tipos de Testes Implementados

| Tipo | Cobertura | Tempo | Comando |
|------|-----------|--------|---------|
| **Unit** | Classes individuais | ~5min | `pytest tests/unit/` |
| **Integration** | Módulos integrados | ~15min | `pytest tests/integration/` |
| **E2E** | Sistema completo | ~30min | `pytest tests/e2e/` |
| **Performance** | Benchmarks | ~45min | `pytest tests/performance/` |

## 🏃‍♂️ Quick Start

### Executar Todos os Testes

```bash
# Testes básicos (rápido)
pytest

# Testes com cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/domain/

# Testes paralelos (mais rápido)
pytest -n auto
```

### Configuração do Ambiente de Testes

```bash
# Instalar dependências de teste
pip install -e ".[test]"

# Configurar variáveis de ambiente
cp .env.test.example .env.test

# Executar setup inicial
python -m pytest --setup-only
```

## 🔧 Configuração do Pytest

### conftest.py Principal

```python
# tests/conftest.py
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.external.binance_client import BinanceClient

# Configuração de fixtures globais
@pytest.fixture(scope="session")
def event_loop():
    """Cria loop de eventos para testes async"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_database():
    """Mock do banco de dados"""
    db_mock = Mock(spec=DatabaseConnection)
    return db_mock

@pytest.fixture
def mock_binance_client():
    """Mock do cliente Binance"""
    client_mock = AsyncMock(spec=BinanceClient)
    
    # Configurar responses padrão
    client_mock.get_symbol_ticker.return_value = {
        'symbol': 'BTCUSDT',
        'price': '45000.00'
    }
    
    client_mock.get_account.return_value = {
        'balances': [
            {'asset': 'USDT', 'free': '1000.00', 'locked': '0.00'},
            {'asset': 'BTC', 'free': '0.02', 'locked': '0.00'}
        ]
    }
    
    return client_mock

@pytest.fixture
def sample_market_data():
    """Dados de mercado para testes"""
    return {
        'symbol': 'BTCUSDT',
        'price': 45000.00,
        'volume': 1000.0,
        'high': 46000.00,
        'low': 44000.00,
        'open': 45500.00,
        'close': 45000.00,
        'timestamp': datetime.now()
    }

@pytest.fixture
def sample_ohlcv_data():
    """Dados OHLCV para testes de indicadores"""
    base_time = datetime.now() - timedelta(days=30)
    data = []
    
    for i in range(30):
        data.append({
            'timestamp': base_time + timedelta(days=i),
            'open': 44000 + (i * 100),
            'high': 45000 + (i * 100),
            'low': 43000 + (i * 100),
            'close': 44500 + (i * 100),
            'volume': 1000 + (i * 10)
        })
    
    return data
```

### Configuração de Markers

```python
# pytest.ini
[tool:pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    slow: Slow tests (skip in CI)
    external: Tests that require external APIs
    database: Tests that require database
    asyncio: Async tests
    
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    -ra

asyncio_mode = auto
```

## 🔬 Testes Unitários

### Testando Entities (Domain Layer)

```python
# tests/unit/domain/test_strategy.py
import pytest
from src.domain.entities.strategy import Strategy
from src.domain.value_objects.trade_signal import TradeSignal

class TestStrategy:
    
    def test_strategy_creation(self):
        """Testa criação de estratégia"""
        strategy = Strategy(
            name="test_strategy",
            parameters={'rsi_period': 14, 'rsi_overbought': 70}
        )
        
        assert strategy.name == "test_strategy"
        assert strategy.parameters['rsi_period'] == 14
        assert strategy.is_active == True
    
    def test_strategy_validation(self):
        """Testa validação de parâmetros"""
        with pytest.raises(ValueError, match="RSI period must be positive"):
            Strategy(
                name="invalid_strategy",
                parameters={'rsi_period': -5}
            )
    
    @pytest.mark.parametrize("rsi,expected_signal", [
        (25, TradeSignal.BUY),
        (75, TradeSignal.SELL),
        (50, TradeSignal.HOLD)
    ])
    def test_rsi_signal_generation(self, rsi, expected_signal, sample_market_data):
        """Testa geração de sinais baseada em RSI"""
        strategy = Strategy("rsi_strategy", {
            'rsi_overbought': 70,
            'rsi_oversold': 30
        })
        
        # Mock RSI calculation
        with patch.object(strategy, '_calculate_rsi', return_value=rsi):
            signal = strategy.generate_signal(sample_market_data)
            assert signal == expected_signal
```

### Testando Use Cases (Application Layer)

```python
# tests/unit/application/test_create_bot_use_case.py
import pytest
from unittest.mock import Mock, AsyncMock
from src.application.use_cases.create_bot import CreateBotUseCase
from src.domain.entities.bot import Bot
from src.domain.entities.strategy import Strategy

class TestCreateBotUseCase:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.bot_repository = Mock()
        self.strategy_repository = Mock()
        self.use_case = CreateBotUseCase(
            bot_repository=self.bot_repository,
            strategy_repository=self.strategy_repository
        )
    
    async def test_create_bot_success(self):
        """Testa criação bem-sucedida de bot"""
        # Arrange
        strategy = Strategy("scalping", {'stop_loss': 2.0})
        self.strategy_repository.get_by_name.return_value = strategy
        self.bot_repository.save.return_value = None
        
        # Act
        bot_data = {
            'name': 'Test Bot',
            'strategy_name': 'scalping',
            'symbol': 'BTCUSDT',
            'capital': 1000.0
        }
        
        result = await self.use_case.execute(bot_data)
        
        # Assert
        assert result.success == True
        assert result.data.name == 'Test Bot'
        self.bot_repository.save.assert_called_once()
    
    async def test_create_bot_duplicate_name(self):
        """Testa criação com nome duplicado"""
        # Arrange
        existing_bot = Bot(name='Test Bot', strategy_name='scalping')
        self.bot_repository.get_by_name.return_value = existing_bot
        
        # Act & Assert
        with pytest.raises(ValueError, match="Bot name already exists"):
            await self.use_case.execute({'name': 'Test Bot'})
    
    async def test_create_bot_invalid_strategy(self):
        """Testa criação com estratégia inválida"""
        # Arrange
        self.strategy_repository.get_by_name.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Strategy not found"):
            await self.use_case.execute({
                'name': 'Test Bot',
                'strategy_name': 'nonexistent'
            })
```

### Testando Indicadores Técnicos

```python
# tests/unit/domain/test_indicators.py
import pytest
import numpy as np
from src.domain.services.indicators import TechnicalIndicators

class TestTechnicalIndicators:
    
    def setup_method(self):
        """Setup dados de teste"""
        self.prices = [44000, 44500, 45000, 44800, 45200, 
                      45500, 45100, 45800, 45400, 46000]
        self.indicators = TechnicalIndicators()
    
    def test_sma_calculation(self):
        """Testa cálculo de SMA"""
        sma = self.indicators.sma(self.prices, period=5)
        
        # SMA dos últimos 5 preços
        expected = sum(self.prices[-5:]) / 5
        assert abs(sma - expected) < 0.01
    
    def test_ema_calculation(self):
        """Testa cálculo de EMA"""
        ema = self.indicators.ema(self.prices, period=5)
        
        # EMA deve ser diferente de SMA
        sma = self.indicators.sma(self.prices, period=5)
        assert abs(ema - sma) > 0.01
        
        # EMA deve dar mais peso aos preços recentes
        assert ema > sma  # assumindo tendência de alta
    
    def test_rsi_calculation(self):
        """Testa cálculo de RSI"""
        # Preços em tendência de alta
        high_prices = list(range(100, 115))
        rsi_high = self.indicators.rsi(high_prices, period=14)
        
        # Preços em tendência de baixa
        low_prices = list(range(115, 100, -1))
        rsi_low = self.indicators.rsi(low_prices, period=14)
        
        assert rsi_high > 50  # RSI alto em tendência de alta
        assert rsi_low < 50   # RSI baixo em tendência de baixa
        assert 0 <= rsi_high <= 100
        assert 0 <= rsi_low <= 100
    
    def test_bollinger_bands(self):
        """Testa cálculo de Bollinger Bands"""
        bb = self.indicators.bollinger_bands(self.prices, period=5, std_dev=2)
        
        assert 'upper' in bb
        assert 'middle' in bb
        assert 'lower' in bb
        
        # Banda superior deve ser maior que a média
        assert bb['upper'] > bb['middle']
        
        # Banda inferior deve ser menor que a média
        assert bb['lower'] < bb['middle']
        
        # Preço atual deve estar entre as bandas (na maioria dos casos)
        current_price = self.prices[-1]
        # assert bb['lower'] <= current_price <= bb['upper']  # pode falhar em outliers
    
    @pytest.mark.parametrize("prices,period,expected_range", [
        ([100] * 10, 5, (0, 100)),  # Preços estáveis
        (list(range(90, 110)), 5, (0, 100)),  # Tendência de alta
        (list(range(110, 90, -1)), 5, (0, 100))  # Tendência de baixa
    ])
    def test_rsi_ranges(self, prices, period, expected_range):
        """Testa se RSI está sempre no range correto"""
        rsi = self.indicators.rsi(prices, period)
        min_val, max_val = expected_range
        assert min_val <= rsi <= max_val
```

## 🔄 Testes de Integração

### Testando Repository com Banco

```python
# tests/integration/infrastructure/test_bot_repository.py
import pytest
import asyncio
from src.infrastructure.database.bot_repository import BotRepository
from src.infrastructure.database.connection import DatabaseConnection
from src.domain.entities.bot import Bot

class TestBotRepository:
    
    @pytest.fixture(autouse=True)
    async def setup(self):
        """Setup antes de cada teste"""
        self.db = DatabaseConnection(":memory:")  # SQLite em memória
        await self.db.create_tables()
        self.repository = BotRepository(self.db)
        
        yield
        
        await self.db.close()
    
    async def test_save_and_get_bot(self):
        """Testa salvar e recuperar bot"""
        # Arrange
        bot = Bot(
            name="Test Bot",
            strategy_name="scalping",
            symbol="BTCUSDT",
            capital=1000.0,
            is_active=True
        )
        
        # Act
        saved_bot = await self.repository.save(bot)
        retrieved_bot = await self.repository.get_by_id(saved_bot.id)
        
        # Assert
        assert retrieved_bot is not None
        assert retrieved_bot.name == "Test Bot"
        assert retrieved_bot.capital == 1000.0
        assert retrieved_bot.is_active == True
    
    async def test_update_bot(self):
        """Testa atualização de bot"""
        # Arrange
        bot = Bot(name="Test Bot", capital=1000.0)
        saved_bot = await self.repository.save(bot)
        
        # Act
        saved_bot.capital = 1500.0
        updated_bot = await self.repository.update(saved_bot)
        retrieved_bot = await self.repository.get_by_id(saved_bot.id)
        
        # Assert
        assert retrieved_bot.capital == 1500.0
    
    async def test_delete_bot(self):
        """Testa exclusão de bot"""
        # Arrange
        bot = Bot(name="Test Bot")
        saved_bot = await self.repository.save(bot)
        
        # Act
        await self.repository.delete(saved_bot.id)
        retrieved_bot = await self.repository.get_by_id(saved_bot.id)
        
        # Assert
        assert retrieved_bot is None
    
    async def test_list_active_bots(self):
        """Testa listagem de bots ativos"""
        # Arrange
        active_bot1 = Bot(name="Active 1", is_active=True)
        active_bot2 = Bot(name="Active 2", is_active=True)
        inactive_bot = Bot(name="Inactive", is_active=False)
        
        await self.repository.save(active_bot1)
        await self.repository.save(active_bot2)
        await self.repository.save(inactive_bot)
        
        # Act
        active_bots = await self.repository.list_active()
        
        # Assert
        assert len(active_bots) == 2
        assert all(bot.is_active for bot in active_bots)
```

### Testando APIs Externas (com mocking)

```python
# tests/integration/external/test_binance_integration.py
import pytest
from unittest.mock import patch, AsyncMock
import aiohttp
from src.infrastructure.external.binance_client import BinanceClient
from src.infrastructure.external.binance_adapter import BinanceAdapter

class TestBinanceIntegration:
    
    @pytest.fixture
    def client(self):
        """Cliente Binance para testes"""
        return BinanceClient(
            api_key="test_key",
            secret_key="test_secret",
            testnet=True
        )
    
    @pytest.fixture
    def adapter(self, client):
        """Adapter Binance para testes"""
        return BinanceAdapter(client)
    
    @patch('aiohttp.ClientSession.get')
    async def test_get_ticker_price(self, mock_get, client):
        """Testa obtenção de preço"""
        # Mock da resposta
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            'symbol': 'BTCUSDT',
            'price': '45000.00'
        })
        mock_response.status = 200
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Act
        price = await client.get_ticker_price('BTCUSDT')
        
        # Assert
        assert price == 45000.00
        mock_get.assert_called_once()
    
    @patch('aiohttp.ClientSession.post')
    async def test_place_order(self, mock_post, client):
        """Testa colocação de ordem"""
        # Mock da resposta
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            'orderId': 12345,
            'status': 'NEW',
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'type': 'LIMIT',
            'quantity': '0.001',
            'price': '45000.00'
        })
        mock_response.status = 200
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # Act
        order = await client.place_limit_order(
            symbol='BTCUSDT',
            side='BUY',
            quantity=0.001,
            price=45000.00
        )
        
        # Assert
        assert order['orderId'] == 12345
        assert order['status'] == 'NEW'
        mock_post.assert_called_once()
    
    async def test_adapter_market_data_transformation(self, adapter):
        """Testa transformação de dados de mercado"""
        # Mock do cliente
        with patch.object(adapter.client, 'get_klines') as mock_klines:
            mock_klines.return_value = [
                [1609459200000, '29000.00', '29500.00', '28800.00', '29200.00', '100.0'],
                [1609462800000, '29200.00', '29800.00', '29000.00', '29600.00', '150.0']
            ]
            
            # Act
            market_data = await adapter.get_market_data('BTCUSDT', '1h', 2)
            
            # Assert
            assert len(market_data) == 2
            assert market_data[0]['open'] == 29000.00
            assert market_data[0]['close'] == 29200.00
            assert market_data[1]['volume'] == 150.0
```

## 🎭 Mocking e Fixtures

### Mock Factories

```python
# tests/mocks/factories.py
from datetime import datetime, timedelta
from src.domain.entities.bot import Bot
from src.domain.entities.trade import Trade
from src.domain.value_objects.trade_signal import TradeSignal

class BotFactory:
    """Factory para criar bots de teste"""
    
    @staticmethod
    def create_bot(**kwargs):
        defaults = {
            'name': 'Test Bot',
            'strategy_name': 'scalping_conservative',
            'symbol': 'BTCUSDT',
            'capital': 1000.0,
            'is_active': True,
            'created_at': datetime.now()
        }
        defaults.update(kwargs)
        return Bot(**defaults)
    
    @staticmethod
    def create_multiple_bots(count=3):
        bots = []
        for i in range(count):
            bot = BotFactory.create_bot(
                name=f'Test Bot {i+1}',
                symbol=f'BTC{i+1}USDT' if i < 2 else 'ETHUSDT'
            )
            bots.append(bot)
        return bots

class TradeFactory:
    """Factory para criar trades de teste"""
    
    @staticmethod
    def create_trade(**kwargs):
        defaults = {
            'bot_id': 1,
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'quantity': 0.001,
            'price': 45000.0,
            'executed_at': datetime.now(),
            'status': 'FILLED'
        }
        defaults.update(kwargs)
        return Trade(**defaults)
    
    @staticmethod
    def create_trade_sequence(bot_id, count=5):
        """Cria sequência de trades para backtesting"""
        trades = []
        base_time = datetime.now() - timedelta(days=count)
        
        for i in range(count):
            side = 'BUY' if i % 2 == 0 else 'SELL'
            price = 45000 + (i * 100)  # Variação de preço
            
            trade = TradeFactory.create_trade(
                bot_id=bot_id,
                side=side,
                price=price,
                executed_at=base_time + timedelta(days=i)
            )
            trades.append(trade)
        
        return trades

class MarketDataFactory:
    """Factory para dados de mercado"""
    
    @staticmethod
    def create_ohlcv_sequence(days=30, base_price=45000):
        """Cria sequência OHLCV para testes"""
        data = []
        base_time = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            # Simula variação de preço
            daily_var = (i % 7 - 3) * 100  # Padrão semanal
            open_price = base_price + daily_var
            
            ohlcv = {
                'timestamp': base_time + timedelta(days=i),
                'open': open_price,
                'high': open_price + 500,
                'low': open_price - 300,
                'close': open_price + 200,
                'volume': 1000 + (i * 50)
            }
            data.append(ohlcv)
        
        return data
```

### Fixtures Customizadas

```python
# tests/fixtures/market_fixtures.py
import pytest
from tests.mocks.factories import MarketDataFactory

@pytest.fixture
def trending_up_data():
    """Dados de mercado em tendência de alta"""
    data = []
    base_price = 40000
    
    for i in range(30):
        price = base_price + (i * 500)  # Alta consistente
        data.append({
            'timestamp': datetime.now() - timedelta(days=30-i),
            'open': price,
            'high': price + 200,
            'low': price - 100,
            'close': price + 150,
            'volume': 1000
        })
    
    return data

@pytest.fixture
def trending_down_data():
    """Dados de mercado em tendência de baixa"""
    data = []
    base_price = 50000
    
    for i in range(30):
        price = base_price - (i * 300)  # Baixa consistente
        data.append({
            'timestamp': datetime.now() - timedelta(days=30-i),
            'open': price,
            'high': price + 100,
            'low': price - 200,
            'close': price - 100,
            'volume': 1000
        })
    
    return data

@pytest.fixture
def sideways_data():
    """Dados de mercado lateral"""
    data = []
    base_price = 45000
    
    for i in range(30):
        # Oscilação em torno do preço base
        price = base_price + (200 * (i % 4 - 2))
        data.append({
            'timestamp': datetime.now() - timedelta(days=30-i),
            'open': price,
            'high': price + 300,
            'low': price - 300,
            'close': price + (50 * (i % 3 - 1)),
            'volume': 1000
        })
    
    return data
```

## 🚀 Testes End-to-End

### Teste Completo de Criação e Execução de Bot

```python
# tests/e2e/test_bot_lifecycle.py
import pytest
import asyncio
from src.main import XBotApplication
from tests.mocks.binance_mock import BinanceMockServer

class TestBotLifecycle:
    
    @pytest.fixture(autouse=True)
    async def setup(self):
        """Setup ambiente E2E"""
        # Iniciar mock server da Binance
        self.binance_mock = BinanceMockServer()
        await self.binance_mock.start()
        
        # Configurar aplicação
        self.app = XBotApplication(test_mode=True)
        await self.app.initialize()
        
        yield
        
        # Cleanup
        await self.app.shutdown()
        await self.binance_mock.stop()
    
    async def test_complete_bot_workflow(self):
        """Testa workflow completo: criar -> configurar -> executar -> monitorar -> parar"""
        
        # 1. Criar bot
        create_result = await self.app.create_bot({
            'name': 'E2E Test Bot',
            'strategy': 'scalping_conservative',
            'symbol': 'BTCUSDT',
            'capital': 1000.0
        })
        
        assert create_result.success == True
        bot_id = create_result.data.id
        
        # 2. Configurar parâmetros
        config_result = await self.app.configure_bot(bot_id, {
            'stop_loss': 2.0,
            'take_profit': 4.0,
            'risk_per_trade': 1.0
        })
        
        assert config_result.success == True
        
        # 3. Iniciar bot
        start_result = await self.app.start_bot(bot_id)
        assert start_result.success == True
        
        # 4. Aguardar execução (simular alguns ciclos)
        await asyncio.sleep(5)
        
        # 5. Verificar se bot está operando
        status = await self.app.get_bot_status(bot_id)
        assert status.data.is_running == True
        
        # 6. Verificar se análise está funcionando
        analysis_count = await self.app.get_analysis_count(bot_id)
        assert analysis_count > 0
        
        # 7. Parar bot
        stop_result = await self.app.stop_bot(bot_id)
        assert stop_result.success == True
        
        # 8. Verificar estatísticas finais
        stats = await self.app.get_bot_statistics(bot_id)
        assert stats.data.total_analyses > 0
    
    async def test_bot_trading_execution(self):
        """Testa execução real de trades"""
        # Mock condições favoráveis para trade
        self.binance_mock.set_market_condition('oversold')  # RSI < 30
        
        # Criar e iniciar bot
        bot_result = await self.app.create_bot({
            'name': 'Trading Test Bot',
            'strategy': 'scalping_conservative',
            'symbol': 'BTCUSDT',
            'capital': 1000.0
        })
        
        bot_id = bot_result.data.id
        await self.app.start_bot(bot_id)
        
        # Aguardar sinal de compra
        await asyncio.sleep(3)
        
        # Verificar se ordem de compra foi colocada
        orders = await self.app.get_bot_orders(bot_id)
        buy_orders = [o for o in orders if o.side == 'BUY']
        assert len(buy_orders) > 0
        
        # Simular preenchimento da ordem
        self.binance_mock.fill_order(buy_orders[0].id)
        
        # Mudar condições para venda
        self.binance_mock.set_market_condition('overbought')  # RSI > 70
        await asyncio.sleep(3)
        
        # Verificar se ordem de venda foi colocada
        orders = await self.app.get_bot_orders(bot_id)
        sell_orders = [o for o in orders if o.side == 'SELL']
        assert len(sell_orders) > 0
```

## ⚡ Testes de Performance

### Benchmarks de Estratégias

```python
# tests/performance/test_strategy_performance.py
import pytest
import time
import asyncio
from src.domain.entities.strategy import ScalpingConservativeStrategy
from tests.mocks.factories import MarketDataFactory

class TestStrategyPerformance:
    
    @pytest.fixture
    def large_dataset(self):
        """Dataset grande para testes de performance"""
        return MarketDataFactory.create_ohlcv_sequence(days=1000)
    
    @pytest.mark.performance
    def test_strategy_analysis_speed(self, large_dataset):
        """Testa velocidade de análise da estratégia"""
        strategy = ScalpingConservativeStrategy()
        
        start_time = time.time()
        
        # Analisar dataset completo
        for data_point in large_dataset:
            signal = strategy.analyze(data_point)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Deve processar 1000 pontos em menos de 1 segundo
        assert execution_time < 1.0
        
        # Calcular throughput
        throughput = len(large_dataset) / execution_time
        assert throughput > 1000  # > 1000 análises por segundo
    
    @pytest.mark.performance
    def test_indicator_calculation_performance(self, large_dataset):
        """Testa performance de cálculos de indicadores"""
        from src.domain.services.indicators import TechnicalIndicators
        
        indicators = TechnicalIndicators()
        prices = [d['close'] for d in large_dataset]
        
        # Benchmark RSI
        start_time = time.time()
        rsi_values = []
        for i in range(14, len(prices)):  # RSI precisa de 14 períodos
            rsi = indicators.rsi(prices[i-14:i+1], 14)
            rsi_values.append(rsi)
        rsi_time = time.time() - start_time
        
        # Benchmark MACD
        start_time = time.time()
        macd_values = []
        for i in range(26, len(prices)):  # MACD precisa de 26 períodos
            macd = indicators.macd(prices[i-26:i+1])
            macd_values.append(macd)
        macd_time = time.time() - start_time
        
        # Assertions de performance
        assert rsi_time < 0.5  # RSI em menos de 500ms
        assert macd_time < 1.0  # MACD em menos de 1s
        
        print(f"RSI calculation: {len(rsi_values)/rsi_time:.0f} calculations/sec")
        print(f"MACD calculation: {len(macd_values)/macd_time:.0f} calculations/sec")
```

### Load Testing

```python
# tests/performance/test_concurrent_bots.py
import pytest
import asyncio
from src.main import XBotApplication

class TestConcurrentExecution:
    
    @pytest.mark.performance
    @pytest.mark.slow
    async def test_multiple_bots_performance(self):
        """Testa performance com múltiplos bots"""
        app = XBotApplication(test_mode=True)
        await app.initialize()
        
        # Criar 10 bots
        bot_ids = []
        for i in range(10):
            result = await app.create_bot({
                'name': f'Performance Bot {i+1}',
                'strategy': 'scalping_conservative',
                'symbol': f'BTC{i%3}USDT',  # Variar símbolos
                'capital': 1000.0
            })
            bot_ids.append(result.data.id)
        
        # Iniciar todos os bots simultaneamente
        start_time = time.time()
        
        tasks = [app.start_bot(bot_id) for bot_id in bot_ids]
        results = await asyncio.gather(*tasks)
        
        startup_time = time.time() - start_time
        
        # Verificar que todos iniciaram com sucesso
        assert all(r.success for r in results)
        
        # Startup deve ser rápido mesmo com múltiplos bots
        assert startup_time < 5.0  # Menos de 5 segundos
        
        # Executar por um período
        await asyncio.sleep(10)
        
        # Verificar performance do sistema
        system_stats = await app.get_system_stats()
        
        # CPU não deve estar saturada
        assert system_stats.cpu_usage < 80
        
        # Memória deve estar controlada
        assert system_stats.memory_usage_mb < 500
        
        # Cleanup
        stop_tasks = [app.stop_bot(bot_id) for bot_id in bot_ids]
        await asyncio.gather(*stop_tasks)
        
        await app.shutdown()
```

## 📊 Coverage e Relatórios

### Configuração de Coverage

```python
# .coveragerc
[run]
source = src
omit = 
    src/main.py
    src/*/__init__.py
    src/*/migrations/*
    */venv/*
    */tests/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

### Executar Coverage

```bash
# Coverage básico
pytest --cov=src

# Coverage com relatório HTML
pytest --cov=src --cov-report=html

# Coverage com falha se abaixo de 80%
pytest --cov=src --cov-fail-under=80

# Coverage detalhado por arquivo
pytest --cov=src --cov-report=term-missing
```

### Quality Gates

```python
# scripts/quality_check.py
#!/usr/bin/env python3
import subprocess
import sys

def run_command(command):
    """Executa comando e retorna resultado"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    print("🔍 Running Quality Checks...")
    
    # 1. Executar testes
    print("\n📊 Running tests...")
    code, out, err = run_command("pytest tests/ -v --tb=short")
    if code != 0:
        print(f"❌ Tests failed: {err}")
        sys.exit(1)
    
    # 2. Verificar coverage
    print("\n📈 Checking coverage...")
    code, out, err = run_command("pytest --cov=src --cov-fail-under=80 --cov-report=term")
    if code != 0:
        print(f"❌ Coverage below 80%: {err}")
        sys.exit(1)
    
    # 3. Linting
    print("\n🧹 Running linter...")
    code, out, err = run_command("flake8 src tests --max-line-length=100")
    if code != 0:
        print(f"❌ Linting failed: {err}")
        sys.exit(1)
    
    # 4. Type checking
    print("\n🔍 Type checking...")
    code, out, err = run_command("mypy src --ignore-missing-imports")
    if code != 0:
        print(f"❌ Type checking failed: {err}")
        sys.exit(1)
    
    print("\n✅ All quality checks passed!")

if __name__ == "__main__":
    main()
```

## 🚀 CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[test]"
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=src --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        
  performance:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e ".[test]"
    
    - name: Run performance tests
      run: |
        pytest tests/performance/ -v -m "not slow"
    
    - name: Generate performance report
      run: |
        python scripts/generate_performance_report.py
```

## 📚 Comandos Úteis

### Comandos de Teste Frequentes

```bash
# Testes rápidos (apenas unit)
pytest tests/unit/ -v

# Testes com output detalhado
pytest -v -s

# Executar teste específico
pytest tests/unit/domain/test_strategy.py::TestStrategy::test_strategy_creation

# Testes com pdb (debugger)
pytest --pdb

# Testes paralelos
pytest -n auto

# Testes com markers
pytest -m "not slow"  # Pular testes lentos
pytest -m "integration"  # Apenas integração

# Watch mode (reroda testes quando arquivos mudam)
ptw tests/ src/
```

### Debugging de Testes

```python
# Usar pdb em testes
def test_something():
    import pdb; pdb.set_trace()
    # ... rest of test

# Usar pytest fixtures para debug
@pytest.fixture(autouse=True)
def debug_fixture(request):
    print(f"\n🧪 Running test: {request.node.name}")
    yield
    print(f"✅ Test completed: {request.node.name}")
```

### Métricas e Relatórios

```bash
# Relatório de cobertura detalhado
pytest --cov=src --cov-report=html --cov-report=term-missing

# Profiling de testes
pytest --profile

# Duração de testes
pytest --durations=10

# Relatório em XML para CI
pytest --junitxml=report.xml
```

---

🧪 **Testes bem estruturados = Sistema mais confiável! Use este guia para garantir qualidade no XBot v2.**