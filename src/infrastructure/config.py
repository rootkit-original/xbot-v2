"""
XBot v2 - Configuration Management

Sistema centralizado de configuração usando environment variables e arquivos de config.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from decimal import Decimal
from pathlib import Path
import json
import logging
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain.entities import RiskProfile, TradingStrategy, PatternType, RiskLevel


logger = logging.getLogger(__name__)


@dataclass
class BinanceConfig:
    """Configurações da Binance"""
    api_key: str = ""
    api_secret: str = ""
    testnet: bool = True
    base_url: Optional[str] = None
    ws_url: Optional[str] = None
    
    def __post_init__(self):
        if not self.base_url:
            self.base_url = "https://testnet.binance.vision" if self.testnet else "https://api.binance.com"
        if not self.ws_url:
            self.ws_url = "wss://testnet.binance.vision/ws" if self.testnet else "wss://stream.binance.com:9443/ws"


@dataclass
class TelegramConfig:
    """Configurações do Telegram"""
    bot_token: str = ""
    admin_chat_id: str = ""
    group_chat_id: Optional[str] = None
    enabled: bool = False  # Disabled by default


@dataclass
class AIConfig:
    """Configurações de AI/ML"""
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    enabled: bool = False
    model_name: str = "gemini-pro"
    max_tokens: int = 1000


@dataclass
class DatabaseConfig:
    """Configurações do banco de dados"""
    url: str = "sqlite:///xbot.db"
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


@dataclass
class LoggingConfig:
    """Configurações de logging"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class SystemConfig:
    """Configurações do sistema"""
    environment: str = "development"  # development, production
    debug: bool = False
    max_concurrent_bots: int = 5
    analysis_interval: int = 300  # seconds
    data_retention_days: int = 90
    timezone: str = "UTC"


@dataclass
class XBotConfig:
    """Configuração principal do XBot"""
    binance: BinanceConfig = None
    telegram: TelegramConfig = None
    ai: AIConfig = field(default_factory=AIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    
    # Default strategies
    default_strategies: Dict[str, TradingStrategy] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize defaults after creation"""
        if self.binance is None:
            self.binance = BinanceConfig()
        if self.telegram is None:
            self.telegram = TelegramConfig()
    
    @property
    def binance_testnet(self) -> bool:
        """Convenience property for testnet flag"""
        return self.binance.testnet if self.binance else True
    
    @classmethod
    def from_environment(cls) -> 'XBotConfig':
        """Carrega configuração das environment variables"""
        
        # Binance Config
        binance_config = BinanceConfig(
            api_key=os.getenv('BINANCE_API_KEY', ''),
            api_secret=os.getenv('BINANCE_API_SECRET', ''),
            testnet=os.getenv('BINANCE_TESTNET', 'true').lower() == 'true'
        )
        
        # Telegram Config
        telegram_config = TelegramConfig(
            bot_token=os.getenv('TELEGRAM_BOT_TOKEN', ''),
            admin_chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID', ''),
            group_chat_id=os.getenv('TELEGRAM_GROUP_CHAT_ID'),
            enabled=os.getenv('TELEGRAM_ENABLED', 'true').lower() == 'true'
        )
        
        # AI Config
        ai_config = AIConfig(
            gemini_api_key=os.getenv('GEMINI_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            enabled=os.getenv('AI_ENABLED', 'false').lower() == 'true',
            model_name=os.getenv('AI_MODEL_NAME', 'gemini-pro'),
            max_tokens=int(os.getenv('AI_MAX_TOKENS', '1000'))
        )
        
        # Database Config
        database_config = DatabaseConfig(
            url=os.getenv('DATABASE_URL', 'sqlite:///xbot.db'),
            echo=os.getenv('DATABASE_ECHO', 'false').lower() == 'true',
            pool_size=int(os.getenv('DATABASE_POOL_SIZE', '10')),
            max_overflow=int(os.getenv('DATABASE_MAX_OVERFLOW', '20'))
        )
        
        # Logging Config
        logging_config = LoggingConfig(
            level=os.getenv('LOG_LEVEL', 'INFO').upper(),
            format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            file_path=os.getenv('LOG_FILE_PATH'),
            max_bytes=int(os.getenv('LOG_MAX_BYTES', str(10 * 1024 * 1024))),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', '5'))
        )
        
        # System Config
        system_config = SystemConfig(
            environment=os.getenv('ENVIRONMENT', 'development'),
            debug=os.getenv('DEBUG', 'false').lower() == 'true',
            max_concurrent_bots=int(os.getenv('MAX_CONCURRENT_BOTS', '5')),
            analysis_interval=int(os.getenv('ANALYSIS_INTERVAL', '300')),
            data_retention_days=int(os.getenv('DATA_RETENTION_DAYS', '90')),
            timezone=os.getenv('TIMEZONE', 'UTC')
        )
        
        config = cls(
            binance=binance_config,
            telegram=telegram_config,
            ai=ai_config,
            database=database_config,
            logging=logging_config,
            system=system_config
        )
        
        # Load default strategies
        config.default_strategies = config._load_default_strategies()
        
        return config
    
    @classmethod
    def from_file(cls, config_path: Path) -> 'XBotConfig':
        """Carrega configuração de arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Convert to config objects
            binance_config = BinanceConfig(**config_data.get('binance', {}))
            telegram_config = TelegramConfig(**config_data.get('telegram', {}))
            ai_config = AIConfig(**config_data.get('ai', {}))
            database_config = DatabaseConfig(**config_data.get('database', {}))
            logging_config = LoggingConfig(**config_data.get('logging', {}))
            system_config = SystemConfig(**config_data.get('system', {}))
            
            return cls(
                binance=binance_config,
                telegram=telegram_config,
                ai=ai_config,
                database=database_config,
                logging=logging_config,
                system=system_config
            )
            
        except Exception as e:
            logger.error(f"Erro ao carregar configuração do arquivo: {e}")
            # Fallback to environment
            return cls.from_environment()
    
    def save_to_file(self, config_path: Path) -> bool:
        """Salva configuração em arquivo JSON"""
        try:
            config_data = {
                'binance': {
                    'api_key': '***',  # Don't save sensitive data
                    'api_secret': '***',
                    'testnet': self.binance.testnet
                },
                'telegram': {
                    'bot_token': '***',
                    'admin_chat_id': self.telegram.admin_chat_id,
                    'group_chat_id': self.telegram.group_chat_id,
                    'enabled': self.telegram.enabled
                },
                'ai': {
                    'enabled': self.ai.enabled,
                    'model_name': self.ai.model_name,
                    'max_tokens': self.ai.max_tokens
                },
                'database': {
                    'url': self.database.url,
                    'echo': self.database.echo,
                    'pool_size': self.database.pool_size,
                    'max_overflow': self.database.max_overflow
                },
                'logging': {
                    'level': self.logging.level,
                    'format': self.logging.format,
                    'file_path': self.logging.file_path,
                    'max_bytes': self.logging.max_bytes,
                    'backup_count': self.logging.backup_count
                },
                'system': {
                    'environment': self.system.environment,
                    'debug': self.system.debug,
                    'max_concurrent_bots': self.system.max_concurrent_bots,
                    'analysis_interval': self.system.analysis_interval,
                    'data_retention_days': self.system.data_retention_days,
                    'timezone': self.system.timezone
                }
            }
            
            # Ensure directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuração salva em: {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def validate(self) -> List[str]:
        """Valida configuração e retorna lista de erros"""
        errors = []
        
        # Binance validation
        if not self.binance.api_key:
            errors.append("BINANCE_API_KEY não configurado")
        if not self.binance.api_secret:
            errors.append("BINANCE_API_SECRET não configurado")
        
        # Telegram validation (opcional se disabled)
        if self.telegram.enabled:
            if not self.telegram.bot_token:
                errors.append("TELEGRAM_BOT_TOKEN não configurado")
            if not self.telegram.admin_chat_id:
                errors.append("TELEGRAM_ADMIN_CHAT_ID não configurado")
        
        # AI validation (opcional se disabled)
        if self.ai.enabled:
            if not self.ai.gemini_api_key and not self.ai.openai_api_key:
                errors.append("Nenhuma chave de API de AI configurada")
        
        # System validation
        if self.system.max_concurrent_bots <= 0:
            errors.append("MAX_CONCURRENT_BOTS deve ser maior que 0")
        
        if self.system.analysis_interval < 60:
            errors.append("ANALYSIS_INTERVAL deve ser pelo menos 60 segundos")
        
        return errors
    
    def _load_default_strategies(self) -> Dict[str, TradingStrategy]:
        """Carrega estratégias padrão"""
        strategies = {}
        
        # Conservative Strategy
        conservative_risk = RiskProfile(
            max_position_size=Decimal('2.0'),  # 2% per position
            max_daily_loss=Decimal('1.0'),     # 1% daily loss
            max_concurrent_positions=2,
            min_risk_reward_ratio=Decimal('3.0'),  # 1:3 risk/reward
            default_stop_loss_percentage=Decimal('2.0'),
            trailing_stop_enabled=True,
            trailing_stop_percentage=Decimal('1.0')
        )
        
        strategies['conservative'] = TradingStrategy(
            name='Conservative',
            description='Estratégia conservadora com baixo risco',
            enabled=True,
            preferred_patterns=[
                PatternType.GOLDEN_CROSS,
                PatternType.BULLISH_ENGULFING,
                PatternType.SUPPORT_RESISTANCE
            ],
            min_pattern_confidence=Decimal('0.8'),
            analysis_timeframes=['4h', '1d'],
            entry_timeframe='1h',
            risk_profile=conservative_risk
        )
        
        # Aggressive Strategy
        aggressive_risk = RiskProfile(
            max_position_size=Decimal('5.0'),  # 5% per position
            max_daily_loss=Decimal('3.0'),     # 3% daily loss
            max_concurrent_positions=5,
            min_risk_reward_ratio=Decimal('2.0'),  # 1:2 risk/reward
            default_stop_loss_percentage=Decimal('3.0'),
            trailing_stop_enabled=True,
            trailing_stop_percentage=Decimal('1.5')
        )
        
        strategies['aggressive'] = TradingStrategy(
            name='Aggressive',
            description='Estratégia agressiva para maior retorno',
            enabled=True,
            preferred_patterns=[
                PatternType.BREAKOUT,
                PatternType.TREND_REVERSAL,
                PatternType.BULLISH_ENGULFING,
                PatternType.BEARISH_ENGULFING
            ],
            min_pattern_confidence=Decimal('0.7'),
            analysis_timeframes=['1h', '4h'],
            entry_timeframe='15m',
            risk_profile=aggressive_risk
        )
        
        # Scalping Strategy
        scalping_risk = RiskProfile(
            max_position_size=Decimal('1.0'),  # 1% per position
            max_daily_loss=Decimal('2.0'),     # 2% daily loss
            max_concurrent_positions=10,
            min_risk_reward_ratio=Decimal('1.5'),  # 1:1.5 risk/reward
            default_stop_loss_percentage=Decimal('0.5'),
            trailing_stop_enabled=False
        )
        
        strategies['scalping'] = TradingStrategy(
            name='Scalping',
            description='Estratégia de scalping para trades rápidos',
            enabled=False,  # Requires low latency
            preferred_patterns=[
                PatternType.BREAKOUT,
                PatternType.SUPPORT_RESISTANCE
            ],
            min_pattern_confidence=Decimal('0.6'),
            analysis_timeframes=['5m', '15m'],
            entry_timeframe='1m',
            risk_profile=scalping_risk
        )
        
        return strategies
    
    def get_strategy(self, name: str) -> Optional[TradingStrategy]:
        """Obtém estratégia por nome"""
        return self.default_strategies.get(name)
    
    def is_production(self) -> bool:
        """Verifica se está em produção"""
        return self.system.environment == 'production'
    
    def is_testnet(self) -> bool:
        """Verifica se está usando testnet"""
        return self.binance.testnet


class ConfigManager:
    """Gerenciador de configuração"""
    
    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or Path.home() / '.xbot'
        self.config_file = self.config_dir / 'config.json'
        self.env_file = self.config_dir / '.env'
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self._config: Optional[XBotConfig] = None
    
    def load_config(self, force_reload: bool = False) -> XBotConfig:
        """Carrega configuração"""
        if self._config is None or force_reload:
            # Try to load from file first, fallback to environment
            if self.config_file.exists():
                logger.info(f"Carregando configuração de: {self.config_file}")
                self._config = XBotConfig.from_file(self.config_file)
            else:
                logger.info("Carregando configuração das environment variables")
                self._config = XBotConfig.from_environment()
            
            # Validate configuration
            errors = self._config.validate()
            if errors:
                logger.warning(f"Erros de configuração encontrados: {errors}")
                # In production, you might want to raise an exception
                if self._config.is_production():
                    raise ValueError(f"Configuração inválida: {errors}")
        
        return self._config
    
    def save_config(self, config: XBotConfig) -> bool:
        """Salva configuração"""
        success = config.save_to_file(self.config_file)
        if success:
            self._config = config
        return success
    
    def create_env_template(self) -> bool:
        """Cria template de .env"""
        env_template = """
# XBot v2 Configuration Template
# Copy this file to .env and fill in your values

# Binance API Configuration
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_secret_here
BINANCE_TESTNET=true

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_ADMIN_CHAT_ID=your_telegram_chat_id
TELEGRAM_GROUP_CHAT_ID=optional_group_chat_id
TELEGRAM_ENABLED=true

# AI Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
AI_ENABLED=false
AI_MODEL_NAME=gemini-pro
AI_MAX_TOKENS=1000

# Database Configuration
DATABASE_URL=sqlite:///xbot.db
DATABASE_ECHO=false
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/xbot.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5

# System Configuration
ENVIRONMENT=development
DEBUG=false
MAX_CONCURRENT_BOTS=5
ANALYSIS_INTERVAL=300
DATA_RETENTION_DAYS=90
TIMEZONE=UTC
        """.strip()
        
        try:
            env_template_file = self.config_dir / '.env.template'
            with open(env_template_file, 'w', encoding='utf-8') as f:
                f.write(env_template)
            
            logger.info(f"Template .env criado em: {env_template_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar template .env: {e}")
            return False
    
    def load_env_file(self) -> bool:
        """Carrega arquivo .env"""
        if not self.env_file.exists():
            return False
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            
            logger.info(f"Arquivo .env carregado: {self.env_file}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar .env: {e}")
            return False