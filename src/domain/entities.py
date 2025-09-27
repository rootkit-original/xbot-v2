"""
XBfrom typing import List, Dict, Optional, Any
from decimal import Decimal
from datetime import datetime
from enum import Enum - Trading Bot Entities (Domain Layer)

Entidades principais do domínio de trading seguindo Clean Architecture.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from enum import Enum
from pathlib import Path


class OrderType(Enum):
    """Tipos de ordem"""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    OCO = "OCO"


class OrderSide(Enum):
    """Lado da ordem"""

    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    """Status da ordem"""

    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class BotStatus(Enum):
    """Status do bot"""

    IDLE = "IDLE"
    ANALYZING = "ANALYZING"
    TRADING = "TRADING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
    STOPPED = "STOPPED"


class PatternType(Enum):
    """Tipos de padrões detectados"""

    BULLISH_ENGULFING = "BULLISH_ENGULFING"
    BEARISH_ENGULFING = "BEARISH_ENGULFING"
    HAMMER = "HAMMER"
    DOJI = "DOJI"
    SUPPORT_RESISTANCE = "SUPPORT_RESISTANCE"
    TREND_REVERSAL = "TREND_REVERSAL"
    BREAKOUT = "BREAKOUT"
    GOLDEN_CROSS = "GOLDEN_CROSS"
    DEATH_CROSS = "DEATH_CROSS"


class RiskLevel(Enum):
    """Níveis de risco"""

    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Market:
    """Informações do mercado/símbolo"""

    symbol: str
    base_asset: str
    quote_asset: str
    status: str
    is_spot_trading_allowed: bool = True
    is_margin_trading_allowed: bool = False
    min_qty: Decimal = Decimal("0.0")
    max_qty: Decimal = Decimal("0.0")
    step_size: Decimal = Decimal("0.0")
    min_notional: Decimal = Decimal("0.0")

    @property
    def trading_pair(self) -> str:
        return f"{self.base_asset}/{self.quote_asset}"


@dataclass
class Candle:
    """Candlestick data"""

    timestamp: datetime
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal
    symbol: str

    @property
    def is_bullish(self) -> bool:
        return self.close_price > self.open_price

    @property
    def is_bearish(self) -> bool:
        return self.close_price < self.open_price

    @property
    def body_size(self) -> Decimal:
        return abs(self.close_price - self.open_price)

    @property
    def upper_shadow(self) -> Decimal:
        return self.high_price - max(self.open_price, self.close_price)

    @property
    def lower_shadow(self) -> Decimal:
        return min(self.open_price, self.close_price) - self.low_price


@dataclass
class Order:
    """Ordem de trading"""

    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None
    time_in_force: str = "GTC"

    # Status info
    order_id: Optional[str] = None
    client_order_id: Optional[str] = None
    status: OrderStatus = OrderStatus.NEW
    executed_qty: Decimal = Decimal("0.0")
    executed_value: Decimal = Decimal("0.0")

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def is_filled(self) -> bool:
        return self.status == OrderStatus.FILLED

    @property
    def fill_percentage(self) -> Decimal:
        if self.quantity == 0:
            return Decimal("0.0")
        return (self.executed_qty / self.quantity) * 100


@dataclass
class Position:
    """Posição atual no mercado"""

    symbol: str
    side: OrderSide
    quantity: Decimal
    entry_price: Decimal
    current_price: Decimal
    unrealized_pnl: Decimal = Decimal("0.0")
    realized_pnl: Decimal = Decimal("0.0")

    # Risk management
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None

    # Timestamps
    opened_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def market_value(self) -> Decimal:
        return self.quantity * self.current_price

    @property
    def pnl_percentage(self) -> Decimal:
        if self.entry_price == 0:
            return Decimal("0.0")
        return ((self.current_price - self.entry_price) / self.entry_price) * 100

    @property
    def is_profitable(self) -> bool:
        return self.unrealized_pnl > 0


@dataclass
class Pattern:
    """Padrão detectado no mercado"""

    pattern_type: PatternType
    symbol: str
    timeframe: str
    confidence: Decimal  # 0.0 to 1.0
    detected_at: datetime

    # Pattern specific data
    candles_analyzed: int
    key_levels: List[Decimal] = field(default_factory=list)
    indicators: Dict[str, Decimal] = field(default_factory=dict)

    # Signal information
    is_bullish: bool = False
    is_bearish: bool = False
    target_price: Optional[Decimal] = None
    stop_loss_price: Optional[Decimal] = None

    @property
    def is_high_confidence(self) -> bool:
        return self.confidence >= Decimal("0.8")

    @property
    def signal_strength(self) -> str:
        if self.confidence >= Decimal("0.9"):
            return "STRONG"
        elif self.confidence >= Decimal("0.7"):
            return "MODERATE"
        else:
            return "WEAK"


@dataclass
class RiskProfile:
    """Perfil de risco para o bot"""

    max_position_size: Decimal  # Porcentagem do capital
    max_daily_loss: Decimal  # Porcentagem do capital
    max_concurrent_positions: int
    min_risk_reward_ratio: Decimal = Decimal("2.0")  # Mínimo 1:2

    # Stop loss settings
    stop_loss_percentage: Decimal = Decimal("2.0")
    take_profit_percentage: Decimal = Decimal("4.0")
    trailing_stop_enabled: bool = False
    trailing_stop_percentage: Decimal = Decimal("0.02")

    # Position sizing
    use_kelly_criterion: bool = False
    fixed_position_size: Optional[Decimal] = None

    # Risk level (for backward compatibility)
    risk_level: RiskLevel = RiskLevel.MODERATE

    @property
    def calculated_risk_level(self) -> RiskLevel:
        """Calcula nível de risco baseado nos parâmetros"""
        if self.max_daily_loss <= Decimal("0.02"):
            return RiskLevel.CONSERVATIVE
        elif self.max_daily_loss <= Decimal("0.05"):
            return RiskLevel.MODERATE
        elif self.max_daily_loss <= Decimal("0.10"):
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL


@dataclass
class TradingStrategy:
    """Estratégia de trading"""

    name: str
    description: str = ""
    enabled: bool = True

    # Target symbols
    target_symbols: List[str] = field(default_factory=list)

    # Pattern preferences
    preferred_patterns: List[PatternType] = field(default_factory=list)
    min_pattern_confidence: Decimal = Decimal("0.7")

    # Timeframes
    analysis_timeframes: List[str] = field(default_factory=lambda: ["1h", "4h", "1d"])
    entry_timeframe: str = "1h"

    # Risk management
    risk_profile: Optional[RiskProfile] = None

    # Technical indicators
    indicators: Dict[str, any] = field(default_factory=dict)
    indicators_config: Dict[str, Dict] = field(default_factory=dict)

    # Entry conditions
    entry_conditions: Dict[str, any] = field(default_factory=dict)

    # Backtesting results
    win_rate: Optional[Decimal] = None
    profit_factor: Optional[Decimal] = None
    max_drawdown: Optional[Decimal] = None

    def __post_init__(self):
        """Initialize defaults after creation"""
        if self.risk_profile is None:
            self.risk_profile = RiskProfile(
                max_position_size=Decimal("10.0"),
                max_daily_loss=Decimal("5.0"),
                max_concurrent_positions=3,
            )

    @property
    def is_conservative(self) -> bool:
        return self.risk_profile.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]


@dataclass
class TradingBot:
    """Bot de trading principal"""

    id: str
    name: str
    strategy: TradingStrategy
    initial_capital: Decimal
    status: BotStatus = BotStatus.IDLE

    # Capital management
    current_capital: Optional[Decimal] = None
    available_capital: Optional[Decimal] = None

    # Trading state
    active_positions: List[Position] = field(default_factory=list)
    pending_orders: List[Order] = field(default_factory=list)
    order_history: List[Order] = field(default_factory=list)

    # Performance tracking
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_profit: Decimal = Decimal("0.0")
    max_drawdown: Decimal = Decimal("0.0")

    # Additional attributes for compatibility
    description: str = ""

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_analysis_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize defaults after creation"""
        if self.current_capital is None:
            self.current_capital = self.initial_capital
        if self.available_capital is None:
            self.available_capital = self.initial_capital
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    last_trade_at: Optional[datetime] = None
    last_analysis_at: Optional[datetime] = None

    @property
    def win_rate(self) -> Decimal:
        if self.total_trades == 0:
            return Decimal("0.0")
        return (Decimal(self.winning_trades) / Decimal(self.total_trades)) * 100

    @property
    def profit_percentage(self) -> Decimal:
        if self.initial_capital == 0:
            return Decimal("0.0")
        return ((self.current_capital - self.initial_capital) / self.initial_capital) * 100

    @property
    def is_active(self) -> bool:
        return self.status in [BotStatus.ANALYZING, BotStatus.TRADING]

    @property
    def position_count(self) -> int:
        return len(self.active_positions)

    @property
    def total_position_value(self) -> Decimal:
        return sum(pos.market_value for pos in self.active_positions)


@dataclass
class MarketAnalysis:
    """Análise completa do mercado"""

    symbol: str
    timestamp: datetime

    # Price data
    current_price: Decimal
    price_change_24h: Decimal
    volume_24h: Decimal

    # Technical analysis
    detected_patterns: List[Pattern]
    support_levels: List[Decimal]
    resistance_levels: List[Decimal]

    # Indicators
    rsi: Optional[Decimal] = None
    macd_signal: Optional[str] = None  # 'BUY', 'SELL', 'NEUTRAL'
    moving_averages: Dict[str, Decimal] = field(default_factory=dict)
    bollinger_bands: Dict[str, Decimal] = field(default_factory=dict)

    # Sentiment
    market_sentiment: str = "NEUTRAL"  # 'BULLISH', 'BEARISH', 'NEUTRAL'
    sentiment_score: Decimal = Decimal("0.5")  # 0.0 to 1.0

    # Risk assessment
    volatility: Decimal = Decimal("0.0")
    liquidity_score: Decimal = Decimal("0.0")

    @property
    def is_bullish(self) -> bool:
        return self.market_sentiment == "BULLISH"

    @property
    def is_bearish(self) -> bool:
        return self.market_sentiment == "BEARISH"

    @property
    def has_strong_patterns(self) -> bool:
        return any(p.is_high_confidence for p in self.detected_patterns)


@dataclass
class TradingSignal:
    """Sinal de trading gerado"""

    symbol: str
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    confidence: Decimal
    generated_at: datetime

    # Entry/Exit points
    entry_price: Optional[Decimal] = None
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None

    # Signal source
    source_patterns: List[Pattern] = field(default_factory=list)
    source_analysis: Optional[MarketAnalysis] = None

    # Risk assessment
    risk_score: Decimal = Decimal("0.5")  # 0.0 to 1.0
    position_size_suggestion: Optional[Decimal] = None

    @property
    def is_actionable(self) -> bool:
        return self.confidence >= Decimal("0.7") and self.signal_type != "HOLD"

    @property
    def risk_reward_ratio(self) -> Optional[Decimal]:
        if not all([self.entry_price, self.stop_loss, self.take_profit]):
            return None

        risk = abs(self.entry_price - self.stop_loss)
        reward = abs(self.take_profit - self.entry_price)

        if risk == 0:
            return None

        return reward / risk
