"""
XBot v2 - Main Application (Entry Point)

Aplicação principal com dependency injection e comandos CLI.
"""

import asyncio
import sys
import argparse
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import signal

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from domain.entities import TradingBot, BotStatus, TradingStrategy
from application.use_cases import (
    AnalyzeMarketUseCase,
    DetectPatternsUseCase,
    ExecuteTradeUseCase,
    RunTradingBotUseCase,
)
from infrastructure.binance_service import BinanceService
from infrastructure.pattern_detection_service import PatternDetectionService
from infrastructure.risk_analysis_service import RiskAnalysisService
from infrastructure.signal_generation_service import SignalGenerationService
from infrastructure.compliance_service import ComplianceService
from infrastructure.telegram_service import TelegramService
from infrastructure.bot_repository import InMemoryBotRepository
from infrastructure.config import XBotConfig
from strategies.predefined_strategies import TradingStrategies


logger = logging.getLogger(__name__)


class XBotApplication:
    """Aplicação principal do XBot"""

    def __init__(self, config: XBotConfig):
        self.config = config
        self.running = False
        self.active_bots: Dict[str, TradingBot] = {}

        # Dependency injection setup
        self._setup_dependencies()

        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _setup_dependencies(self):
        """Configura injeção de dependência"""
        logger.info("Configurando dependências...")

        # Infrastructure Services
        self.binance_service = BinanceService(
            api_key=self.config.binance.api_key,
            api_secret=self.config.binance.api_secret,
            testnet=self.config.binance.testnet,
        )

        self.pattern_detector = PatternDetectionService()
        self.risk_analyzer = RiskAnalysisService()

        # Notification service (optional)
        self.notification_service = None
        if self.config.telegram.enabled and self.config.telegram.bot_token:
            self.notification_service = TelegramService(
                bot_token=self.config.telegram.bot_token,
                admin_chat_id=self.config.telegram.admin_chat_id,
                group_chat_id=self.config.telegram.group_chat_id,
            )

        # Technical Analysis Service (using pattern detector for now)
        self.technical_analysis = self.pattern_detector  # Simplified

        # Signal Generation Service (simplified implementation)
        self.signal_generator = SignalGenerationService(
            pattern_detector=self.pattern_detector, technical_analysis=self.technical_analysis
        )

        # Compliance Service (simplified implementation)
        self.compliance_service = ComplianceService(risk_analyzer=self.risk_analyzer)

        # Bot Repository (in-memory for now)
        self.bot_repository = InMemoryBotRepository()

        # Use Cases
        self.analyze_market = AnalyzeMarketUseCase(
            market_data_repo=self.binance_service,
            pattern_detector=self.pattern_detector,
            technical_analysis=self.technical_analysis,
        )

        self.detect_patterns = DetectPatternsUseCase(
            market_data_repo=self.binance_service, pattern_detector=self.pattern_detector
        )

        self.execute_trade = ExecuteTradeUseCase(
            trading_repo=self.binance_service,
            portfolio_repo=self.binance_service,
            compliance_service=self.compliance_service,
            notification_service=self.notification_service,
        )

        self.run_trading_bot = RunTradingBotUseCase(
            analyze_market=self.analyze_market,
            detect_patterns=self.detect_patterns,
            generate_signal=self.generate_signal,
            execute_trade=self.execute_trade,
            monitor_positions=self.monitor_positions,
            bot_repo=self.bot_repository,
            notification_service=self.notification_service,
        )

        logger.info("Dependências configuradas com sucesso")

    async def start(self):
        """Inicia a aplicação"""
        logger.info("🚀 Iniciando XBot v2...")

        try:
            # Test connections
            await self._test_connections()

            # Send startup notification
            if self.notification_service:
                await self.notification_service.send_startup_message()

            self.running = True
            logger.info("✅ XBot iniciado com sucesso!")

        except Exception as e:
            logger.error(f"❌ Erro ao iniciar XBot: {e}")
            raise

    async def stop(self):
        """Para a aplicação"""
        logger.info("🛑 Parando XBot...")

        self.running = False

        # Stop all active bots
        for bot_id in list(self.active_bots.keys()):
            await self.stop_bot(bot_id)

        # Send shutdown notification
        if self.notification_service:
            await self.notification_service.send_shutdown_message()

        # Close connections
        await self.binance_service.close()

        logger.info("✅ XBot parado com sucesso!")

    async def create_bot(
        self, name: str, strategy_name: str, initial_capital: float, symbols: List[str] = None
    ) -> str:
        """Cria um novo bot de trading"""
        logger.info(f"Criando bot: {name}")

        strategy = self.config.get_strategy(strategy_name)
        if not strategy:
            raise ValueError(f"Estratégia '{strategy_name}' não encontrada")

        # Set default symbols if not provided
        if not symbols:
            symbols = ["BTCUSDT", "ETHUSDT"]

        # Add symbols to strategy (simplified)
        strategy.symbols = symbols

        bot = TradingBot(
            id=f"bot_{int(datetime.now().timestamp())}",
            name=name,
            strategy=strategy,
            status=BotStatus.IDLE,
            initial_capital=float(initial_capital),
            current_capital=float(initial_capital),
            available_capital=float(initial_capital),
        )

        # Save bot
        await self.bot_repository.save_bot(bot)

        logger.info(f"✅ Bot criado: {bot.id}")
        return bot.id

    async def start_bot(self, bot_id: str) -> bool:
        """Inicia um bot"""
        logger.info(f"Iniciando bot: {bot_id}")

        bot = await self.bot_repository.load_bot(bot_id)
        if not bot:
            logger.error(f"Bot {bot_id} não encontrado")
            return False

        if bot.id in self.active_bots:
            logger.warning(f"Bot {bot_id} já está ativo")
            return False

        bot.status = BotStatus.IDLE
        await self.bot_repository.save_bot(bot)

        self.active_bots[bot_id] = bot

        # Start bot loop
        asyncio.create_task(self._bot_loop(bot_id))

        logger.info(f"✅ Bot {bot_id} iniciado")
        return True

    async def stop_bot(self, bot_id: str) -> bool:
        """Para um bot"""
        logger.info(f"Parando bot: {bot_id}")

        if bot_id not in self.active_bots:
            logger.warning(f"Bot {bot_id} não está ativo")
            return False

        bot = self.active_bots[bot_id]
        bot.status = BotStatus.STOPPED
        await self.bot_repository.save_bot(bot)

        del self.active_bots[bot_id]

        logger.info(f"✅ Bot {bot_id} parado")
        return True

    async def list_bots(self) -> List[TradingBot]:
        """Lista todos os bots"""
        return await self.bot_repository.get_all_bots()

    async def get_bot_status(self, bot_id: str) -> Optional[dict]:
        """Obtém status de um bot"""
        bot = await self.bot_repository.load_bot(bot_id)
        if not bot:
            return None

        return {
            "id": bot.id,
            "name": bot.name,
            "status": bot.status.value,
            "strategy": bot.strategy.name,
            "profit_percentage": float(bot.profit_percentage),
            "active_positions": bot.position_count,
            "total_trades": bot.total_trades,
            "win_rate": float(bot.win_rate),
            "last_analysis": bot.last_analysis_at.isoformat() if bot.last_analysis_at else None,
        }

    async def analyze_symbol(self, symbol: str) -> dict:
        """Analisa um símbolo específico"""
        logger.info(f"Analisando símbolo: {symbol}")

        analysis = await self.analyze_market.execute(symbol)

        return {
            "symbol": analysis.symbol,
            "current_price": float(analysis.current_price),
            "sentiment": analysis.market_sentiment,
            "volatility": float(analysis.volatility),
            "patterns_found": len(analysis.detected_patterns),
            "patterns": [
                {
                    "type": p.pattern_type.value,
                    "confidence": float(p.confidence),
                    "direction": (
                        "bullish" if p.is_bullish else "bearish" if p.is_bearish else "neutral"
                    ),
                }
                for p in analysis.detected_patterns
            ],
        }

    async def _bot_loop(self, bot_id: str):
        """Loop principal do bot"""
        logger.info(f"Iniciando loop do bot {bot_id}")

        while self.running and bot_id in self.active_bots:
            try:
                # Execute bot cycle
                results = await self.run_trading_bot.execute(bot_id)

                if results.get("status") == "inactive":
                    logger.info(f"Bot {bot_id} inativo, parando loop")
                    break

                # Log results
                logger.info(f"Bot {bot_id} - Cycle completed: {results.get('duration', 0):.2f}s")

                # Wait for next cycle
                await asyncio.sleep(self.config.system.analysis_interval)

            except Exception as e:
                logger.error(f"Erro no loop do bot {bot_id}: {e}")

                # Notify error
                if self.notification_service:
                    await self.notification_service.send_alert(
                        "Bot Error", f"Erro no bot {bot_id}: {str(e)}", "high"
                    )

                # Wait before retrying
                await asyncio.sleep(60)

        logger.info(f"Loop do bot {bot_id} finalizado")

    async def _test_connections(self):
        """Testa conexões com serviços externos"""
        logger.info("Testando conexões...")

        # Test Binance connection
        try:
            test_price = await self.binance_service.get_current_price("BTCUSDT")
            if test_price:
                logger.info(f"✅ Conexão Binance OK - BTC: ${test_price}")
            else:
                raise Exception("Não foi possível obter preço do BTC")
        except Exception as e:
            logger.error(f"❌ Erro na conexão Binance: {e}")
            raise

        # Test Telegram connection
        if self.notification_service:
            try:
                connection_ok = await self.notification_service.test_connection()
                if connection_ok:
                    logger.info("✅ Conexão Telegram OK")
                else:
                    logger.warning("⚠️ Erro na conexão Telegram - Notificações desabilitadas")
                    self.notification_service = None
            except Exception as e:
                logger.warning(f"⚠️ Erro Telegram: {e} - Continuando sem notificações")
                self.notification_service = None

    def _signal_handler(self, signum, frame):
        """Handler para sinais do sistema"""
        logger.info(f"Sinal recebido: {signum}")
        if self.running:
            asyncio.create_task(self.stop())


def setup_logging(config: XBotConfig):
    """Configura sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format=config.logging.format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Add file handler if configured
    if config.logging.file_path:
        log_file = Path(config.logging.file_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            log_file, maxBytes=config.logging.max_bytes, backupCount=config.logging.backup_count
        )
        file_handler.setFormatter(logging.Formatter(config.logging.format))
        logging.getLogger().addHandler(file_handler)


async def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="XBot v2 - Sistema de Trading Automatizado")
    parser.add_argument("--config", type=str, help="Caminho para arquivo de configuração")
    parser.add_argument(
        "--create-config", action="store_true", help="Cria template de configuração"
    )
    parser.add_argument("--validate-config", action="store_true", help="Valida configuração")
    parser.add_argument(
        "--list-strategies", action="store_true", help="Lista estratégias disponíveis"
    )

    # Bot management commands
    parser.add_argument("--create-bot", type=str, help="Cria novo bot com nome especificado")
    parser.add_argument(
        "--strategy", type=str, default="conservative", help="Estratégia para o bot"
    )
    parser.add_argument("--capital", type=float, default=1000.0, help="Capital inicial em USDT")
    parser.add_argument("--symbols", nargs="+", help="Símbolos para trading")
    parser.add_argument("--start-bot", type=str, help="Inicia bot por ID")
    parser.add_argument("--stop-bot", type=str, help="Para bot por ID")
    parser.add_argument("--list-bots", action="store_true", help="Lista todos os bots")
    parser.add_argument("--bot-status", type=str, help="Status de um bot específico")
    parser.add_argument("--analyze", type=str, help="Analisa um símbolo específico")

    args = parser.parse_args()

    # Load configuration
    config = XBotConfig()

    if args.create_config:
        print("✅ Para criar configuração, copie .env.example para .env")
        print("Configure suas chaves de API no arquivo .env")
        return
        return

    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if args.validate_config:
        print("✅ Configuração OK (validação simplificada)")
        return

    if args.list_strategies:
        print("📊 Estratégias disponíveis:")
        for name, strategy in config.default_strategies.items():
            print(f"  • {name}: {strategy.description}")
        return

    # Create application
    app = XBotApplication(config)

    try:
        await app.start()

        # Handle specific commands
        if args.create_bot:
            bot_id = await app.create_bot(
                name=args.create_bot,
                strategy_name=args.strategy,
                initial_capital=args.capital,
                symbols=args.symbols,
            )
            print(f"✅ Bot criado: {bot_id}")

        elif args.start_bot:
            success = await app.start_bot(args.start_bot)
            if success:
                print(f"✅ Bot {args.start_bot} iniciado")
            else:
                print(f"❌ Erro ao iniciar bot {args.start_bot}")

        elif args.stop_bot:
            success = await app.stop_bot(args.stop_bot)
            if success:
                print(f"✅ Bot {args.stop_bot} parado")
            else:
                print(f"❌ Erro ao parar bot {args.stop_bot}")

        elif args.list_bots:
            bots = await app.list_bots()
            if bots:
                print("🤖 Bots cadastrados:")
                for bot in bots:
                    status_emoji = (
                        "🟢"
                        if bot.status == BotStatus.IDLE
                        else "🔴" if bot.status == BotStatus.ERROR else "🟡"
                    )
                    print(f"  {status_emoji} {bot.id}: {bot.name} ({bot.status.value})")
            else:
                print("Nenhum bot encontrado")

        elif args.bot_status:
            status = await app.get_bot_status(args.bot_status)
            if status:
                print(f"📊 Status do bot {args.bot_status}:")
                for key, value in status.items():
                    print(f"  • {key}: {value}")
            else:
                print(f"❌ Bot {args.bot_status} não encontrado")

        elif args.analyze:
            analysis = await app.analyze_symbol(args.analyze)
            print(f"📈 Análise de {args.analyze}:")
            print(f"  • Preço: ${analysis['current_price']:.2f}")
            print(f"  • Sentiment: {analysis['sentiment']}")
            print(f"  • Volatilidade: {analysis['volatility']:.2f}%")
            print(f"  • Padrões encontrados: {analysis['patterns_found']}")
            if analysis["patterns"]:
                for pattern in analysis["patterns"]:
                    print(
                        f"    - {pattern['type']}: {pattern['confidence']:.1%} ({pattern['direction']})"
                    )

        else:
            # Run in continuous mode
            print("🚀 XBot rodando em modo contínuo...")
            print("Pressione Ctrl+C para parar")

            try:
                while app.running:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Parando XBot...")

    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
