"""
XBot v2 - Domain Interfaces (Contratos/Abstrações)

Interfaces que definem os contratos entre as camadas seguindo Clean Architecture.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, AsyncIterator
from decimal import Decimal
from datetime import datetime

from .entities import (
    TradingBot, Market, Order, Position, Pattern, MarketAnalysis, 
    TradingSignal, Candle, PatternType, RiskProfile, TradingStrategy
)


# ===============================
# Repository Interfaces
# ===============================

class IMarketDataRepository(ABC):
    """Interface para repositório de dados de mercado"""
    
    @abstractmethod
    async def get_market_info(self, symbol: str) -> Optional[Market]:
        """Obtém informações do mercado/símbolo"""
        pass
    
    @abstractmethod
    async def get_current_price(self, symbol: str) -> Optional[Decimal]:
        """Obtém preço atual do símbolo"""
        pass
    
    @abstractmethod
    async def get_candles(
        self, 
        symbol: str, 
        timeframe: str, 
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Candle]:
        """Obtém dados de candlesticks"""
        pass
    
    @abstractmethod
    async def get_24h_stats(self, symbol: str) -> Dict[str, Decimal]:
        """Obtém estatísticas de 24h"""
        pass
    
    @abstractmethod
    async def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, List[Tuple[Decimal, Decimal]]]:
        """Obtém order book (bids/asks)"""
        pass


class ITradingRepository(ABC):
    """Interface para repositório de trading"""
    
    @abstractmethod
    async def place_order(self, order: Order) -> Order:
        """Coloca uma ordem no mercado"""
        pass
    
    @abstractmethod
    async def cancel_order(self, symbol: str, order_id: str) -> bool:
        """Cancela uma ordem"""
        pass
    
    @abstractmethod
    async def get_order_status(self, symbol: str, order_id: str) -> Optional[Order]:
        """Obtém status de uma ordem"""
        pass
    
    @abstractmethod
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Obtém ordens abertas"""
        pass
    
    @abstractmethod
    async def get_order_history(
        self, 
        symbol: str, 
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Order]:
        """Obtém histórico de ordens"""
        pass


class IPortfolioRepository(ABC):
    """Interface para repositório de portfólio"""
    
    @abstractmethod
    async def get_account_balance(self) -> Dict[str, Decimal]:
        """Obtém saldo da conta"""
        pass
    
    @abstractmethod
    async def get_positions(self) -> List[Position]:
        """Obtém posições atuais"""
        pass
    
    @abstractmethod
    async def get_position(self, symbol: str) -> Optional[Position]:
        """Obtém posição específica"""
        pass


class IBotRepository(ABC):
    """Interface para repositório de bots"""
    
    @abstractmethod
    async def save_bot(self, bot: TradingBot) -> bool:
        """Salva configuração do bot"""
        pass
    
    @abstractmethod
    async def load_bot(self, bot_id: str) -> Optional[TradingBot]:
        """Carrega configuração do bot"""
        pass
    
    @abstractmethod
    async def get_all_bots(self) -> List[TradingBot]:
        """Obtém todos os bots"""
        pass
    
    @abstractmethod
    async def update_bot_status(self, bot_id: str, status: str) -> bool:
        """Atualiza status do bot"""
        pass


# ===============================
# Service Interfaces
# ===============================

class IPatternDetectionService(ABC):
    """Interface para serviço de detecção de padrões"""
    
    @abstractmethod
    async def detect_patterns(
        self, 
        candles: List[Candle], 
        pattern_types: Optional[List[PatternType]] = None
    ) -> List[Pattern]:
        """Detecta padrões nos candlesticks"""
        pass
    
    @abstractmethod
    async def analyze_pattern_strength(self, pattern: Pattern) -> Decimal:
        """Analisa força do padrão"""
        pass
    
    @abstractmethod
    async def get_pattern_targets(self, pattern: Pattern) -> Tuple[Optional[Decimal], Optional[Decimal]]:
        """Obtém alvos do padrão (take profit, stop loss)"""
        pass


class ITechnicalAnalysisService(ABC):
    """Interface para análise técnica"""
    
    @abstractmethod
    async def calculate_rsi(self, candles: List[Candle], period: int = 14) -> List[Decimal]:
        """Calcula RSI"""
        pass
    
    @abstractmethod
    async def calculate_macd(
        self, 
        candles: List[Candle], 
        fast_period: int = 12, 
        slow_period: int = 26, 
        signal_period: int = 9
    ) -> Dict[str, List[Decimal]]:
        """Calcula MACD"""
        pass
    
    @abstractmethod
    async def calculate_bollinger_bands(
        self, 
        candles: List[Candle], 
        period: int = 20, 
        std_dev: int = 2
    ) -> Dict[str, List[Decimal]]:
        """Calcula Bollinger Bands"""
        pass
    
    @abstractmethod
    async def calculate_moving_averages(
        self, 
        candles: List[Candle], 
        periods: List[int]
    ) -> Dict[int, List[Decimal]]:
        """Calcula médias móveis"""
        pass
    
    @abstractmethod
    async def find_support_resistance(self, candles: List[Candle]) -> Dict[str, List[Decimal]]:
        """Encontra níveis de suporte e resistência"""
        pass


class IRiskAnalysisService(ABC):
    """Interface para análise de risco"""
    
    @abstractmethod
    async def calculate_position_size(
        self, 
        capital: Decimal, 
        risk_profile: RiskProfile,
        entry_price: Decimal,
        stop_loss: Decimal
    ) -> Decimal:
        """Calcula tamanho da posição"""
        pass
    
    @abstractmethod
    async def assess_market_risk(self, analysis: MarketAnalysis) -> Decimal:
        """Avalia risco do mercado (0.0 a 1.0)"""
        pass
    
    @abstractmethod
    async def calculate_var(self, positions: List[Position], confidence: Decimal = Decimal('0.95')) -> Decimal:
        """Calcula Value at Risk"""
        pass
    
    @abstractmethod
    async def should_close_position(
        self, 
        position: Position, 
        current_analysis: MarketAnalysis
    ) -> Tuple[bool, str]:
        """Determina se deve fechar posição"""
        pass


class ISignalGenerationService(ABC):
    """Interface para geração de sinais"""
    
    @abstractmethod
    async def generate_signal(
        self, 
        market_analysis: MarketAnalysis,
        strategy: TradingStrategy
    ) -> Optional[TradingSignal]:
        """Gera sinal de trading baseado na análise"""
        pass
    
    @abstractmethod
    async def validate_signal(self, signal: TradingSignal) -> bool:
        """Valida sinal antes da execução"""
        pass
    
    @abstractmethod
    async def combine_signals(self, signals: List[TradingSignal]) -> Optional[TradingSignal]:
        """Combina múltiplos sinais em um consenso"""
        pass


class INotificationService(ABC):
    """Interface para notificações"""
    
    @abstractmethod
    async def send_trade_notification(
        self, 
        bot_id: str, 
        order: Order, 
        message: str
    ) -> bool:
        """Envia notificação de trade"""
        pass
    
    @abstractmethod
    async def send_alert(self, title: str, message: str, urgency: str = "normal") -> bool:
        """Envia alerta geral"""
        pass
    
    @abstractmethod
    async def send_performance_report(self, bot: TradingBot) -> bool:
        """Envia relatório de performance"""
        pass
    
    @abstractmethod
    async def send_risk_alert(self, bot: TradingBot, risk_message: str) -> bool:
        """Envia alerta de risco"""
        pass


class IBacktestingService(ABC):
    """Interface para backtesting"""
    
    @abstractmethod
    async def run_backtest(
        self,
        strategy: TradingStrategy,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        initial_capital: Decimal
    ) -> Dict[str, Decimal]:
        """Executa backtest da estratégia"""
        pass
    
    @abstractmethod
    async def optimize_parameters(
        self,
        strategy: TradingStrategy,
        symbol: str,
        parameter_ranges: Dict[str, Tuple[float, float]]
    ) -> Dict[str, float]:
        """Otimiza parâmetros da estratégia"""
        pass


class IMarketDataStream(ABC):
    """Interface para stream de dados em tempo real"""
    
    @abstractmethod
    async def subscribe_ticker(self, symbol: str) -> AsyncIterator[Dict[str, Decimal]]:
        """Subscribe para dados de ticker"""
        pass
    
    @abstractmethod
    async def subscribe_candles(self, symbol: str, timeframe: str) -> AsyncIterator[Candle]:
        """Subscribe para dados de candlesticks"""
        pass
    
    @abstractmethod
    async def subscribe_order_book(self, symbol: str) -> AsyncIterator[Dict]:
        """Subscribe para order book"""
        pass
    
    @abstractmethod
    async def unsubscribe_all(self) -> None:
        """Remove todos os subscribes"""
        pass


class IAIService(ABC):
    """Interface para serviços de AI/ML"""
    
    @abstractmethod
    async def analyze_market_sentiment(
        self, 
        symbol: str,
        news_data: Optional[List[str]] = None,
        social_data: Optional[List[str]] = None
    ) -> Tuple[str, Decimal]:
        """Analisa sentiment do mercado"""
        pass
    
    @abstractmethod
    async def predict_price_movement(
        self,
        candles: List[Candle],
        timeframe: str,
        horizon: int = 24  # hours
    ) -> Dict[str, Decimal]:
        """Prediz movimento de preço"""
        pass
    
    @abstractmethod
    async def optimize_strategy(
        self,
        strategy: TradingStrategy,
        performance_history: List[Dict]
    ) -> TradingStrategy:
        """Otimiza estratégia usando ML"""
        pass
    
    @abstractmethod
    async def detect_anomalies(
        self,
        market_data: Dict,
        threshold: Decimal = Decimal('0.95')
    ) -> List[Dict[str, any]]:
        """Detecta anomalias no mercado"""
        pass


class IComplianceService(ABC):
    """Interface para conformidade e regulamentação"""
    
    @abstractmethod
    async def validate_trade(self, order: Order, current_positions: List[Position]) -> Tuple[bool, str]:
        """Valida trade antes da execução"""
        pass
    
    @abstractmethod
    async def check_position_limits(self, bot: TradingBot) -> Tuple[bool, str]:
        """Verifica limites de posição"""
        pass
    
    @abstractmethod
    async def check_daily_loss_limit(self, bot: TradingBot) -> Tuple[bool, str]:
        """Verifica limite de perda diária"""
        pass
    
    @abstractmethod
    async def generate_audit_log(self, bot: TradingBot, action: str, details: Dict) -> bool:
        """Gera log de auditoria"""
        pass


# ===============================
# Event Interfaces
# ===============================

class IEventBus(ABC):
    """Interface para event bus"""
    
    @abstractmethod
    async def publish(self, event_type: str, data: Dict) -> None:
        """Publica evento"""
        pass
    
    @abstractmethod
    async def subscribe(self, event_type: str, handler) -> None:
        """Subscreve para eventos"""
        pass
    
    @abstractmethod
    async def unsubscribe(self, event_type: str, handler) -> None:
        """Remove subscription"""
        pass


class IEventHandler(ABC):
    """Interface para handlers de eventos"""
    
    @abstractmethod
    async def handle(self, event_data: Dict) -> None:
        """Processa evento"""
        pass