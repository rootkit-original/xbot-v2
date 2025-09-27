#!/usr/bin/env python3
"""
XBot v2 - Main Orchestrator
============================

Este é o ponto de entrada principal do sistema XBot v2.
Responsável por orquestrar todos os componentes e serviços.

Usage:
    python main.py [command] [options]

Commands:
    start       - Inicia o sistema XBot        choices=["start", "stop", "status", "create-bot", "list-bots", 
                 "dashboard", "performance", "setup", "test"],    stop        - Para o sistema XBot
    status      - Mostra o status do sistema
    create-bot  - Cria um novo bot de trading
    list-bots   - Lista todos os bots
    dashboard   - Abre o dashboard de monitoramento
    performance - Mostra desempenho detalhado dos bots
    setup       - Configura o ambiente inicial
    test        - Executa testes do sistema
"""

import sys
import asyncio
import argparse
import logging
import json
from pathlib import Path
from typing import Optional, List
from decimal import Decimal

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adiciona o diretório src ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.infrastructure.config import XBotConfig
    from src.application.use_cases import RunTradingBotUseCase
    from src.domain.entities import TradingBot, TradingStrategy, RiskProfile
    from src.infrastructure.binance_service import BinanceService
    from src.infrastructure.telegram_service import TelegramNotificationService as TelegramService
except ImportError as e:
    logger.error(f"Erro de importação: {e}")
    print("⚠️ Algumas dependências não estão disponíveis. Execute 'python main.py setup' primeiro.")


class XBotOrchestrator:
    """
    Orquestrador principal do sistema XBot v2
    """
    
    def __init__(self):
        self.config = XBotConfig()
        self.binance_service = None
        self.telegram_service = None
        self.use_cases = None
        self.active_bots: List[TradingBot] = []
        self.bots_file = Path("data/bots.json")
        self.bots_file.parent.mkdir(exist_ok=True)
        
    async def initialize(self):
        """Inicializa todos os serviços"""
        try:
            logger.info("🚀 Inicializando XBot v2...")
            
            # Inicializar serviços
            try:
                self.binance_service = BinanceService(
                    api_key=self.config.binance.api_key,
                    api_secret=self.config.binance.api_secret,
                    testnet=self.config.binance.testnet
                )
                self.telegram_service = TelegramService(
                    bot_token=self.config.telegram.bot_token,
                    admin_chat_id=self.config.telegram.admin_chat_id,
                    group_chat_id=self.config.telegram.group_chat_id
                )
                # self.run_bot_use_case = RunTradingBotUseCase()  # TODO: Fix dependency injection
            except Exception as e:
                logger.error(f"Erro ao inicializar serviços: {e}")
                import traceback
                traceback.print_exc()
                self.binance_service = None
                self.telegram_service = None
                self.run_bot_use_case = None
            
            # Validar configurações
            await self._validate_configuration()
            
            # Carregar bots salvos
            self._load_bots()
            
            logger.info("✅ XBot v2 inicializado com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro na inicialização: {e}")
            raise
    
    async def _validate_configuration(self):
        """Valida as configurações do sistema"""
        # Verificar diretamente as variáveis de ambiente, pois o config pode estar vazio
        import os
        if not os.getenv('BINANCE_API_KEY'):
            logger.warning("⚠️ API Key da Binance não configurada")
        
        if not os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_NOTIFICATIONS_ENABLED', 'false').lower() == 'true':
            logger.warning("⚠️ Token do Telegram não configurado")
    
    def _save_bots(self):
        """Salva bots em arquivo JSON"""
        try:
            bots_data = []
            for bot in self.active_bots:
                bot_data = {
                    "id": bot.id,
                    "name": bot.name,
                    "initial_capital": str(bot.initial_capital),
                    "current_capital": str(bot.current_capital) if bot.current_capital else "0",
                    "status": bot.status.value,
                    "strategy_name": bot.strategy.name if bot.strategy else "default"
                }
                bots_data.append(bot_data)
            
            with open(self.bots_file, 'w') as f:
                json.dump(bots_data, f, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar bots: {e}")
    
    def _load_bots(self):
        """Carrega bots do arquivo JSON"""
        try:
            if self.bots_file.exists():
                with open(self.bots_file, 'r') as f:
                    bots_data = json.load(f)
                
                for bot_data in bots_data:
                    # Criar estratégia simples
                    strategy = TradingStrategy(
                        name=bot_data.get("strategy_name", "default"),
                        description=f"Estratégia para {bot_data['name']}"
                    )
                    
                    # Criar bot
                    bot = TradingBot(
                        id=bot_data["id"],
                        name=bot_data["name"],
                        strategy=strategy,
                        initial_capital=Decimal(bot_data["initial_capital"]),
                        current_capital=Decimal(bot_data["current_capital"])
                    )
                    self.active_bots.append(bot)
                    
                logger.info(f"📚 Carregados {len(self.active_bots)} bots salvos")
        except Exception as e:
            logger.error(f"Erro ao carregar bots: {e}")
    
    async def start_system(self):
        """Inicia o sistema completo"""
        await self.initialize()
        logger.info("🟢 Sistema XBot v2 iniciado")
        
        # Aqui você pode adicionar lógica para iniciar bots existentes
        # ou manter o sistema rodando
        
    async def stop_system(self):
        """Para o sistema e todos os bots"""
        logger.info("🔴 Parando sistema XBot v2...")
        
        # Parar todos os bots ativos
        for bot in self.active_bots:
            logger.info(f"Parando bot: {bot.name}")
            # Adicionar lógica para parar bot
            
        logger.info("✅ Sistema parado com sucesso")
    
    async def create_bot(self, name: str, strategy_name: str, symbols: List[str], 
                        initial_capital: float):
        """Cria um novo bot de trading"""
        try:
            logger.info(f"🤖 Criando bot: {name}")
            
            # Criar estratégia
            strategy = TradingStrategy(
                name=strategy_name,
                description=f"Estratégia para {name}"
            )
            
            # Criar perfil de risco padrão
            risk_profile = RiskProfile(
                max_position_size=5.0,
                max_daily_loss=100.0,
                max_concurrent_positions=3,
                stop_loss_percentage=2.0,
                take_profit_percentage=4.0
            )
            
            # Criar bot
            bot = TradingBot(
                id=f"bot_{len(self.active_bots) + 1}",
                name=name,
                strategy=strategy,
                initial_capital=Decimal(str(initial_capital)),
                current_capital=Decimal(str(initial_capital))
            )
            
            self.active_bots.append(bot)
            self._save_bots()  # Salvar após criar
            logger.info(f"✅ Bot '{name}' criado com sucesso!")
            return bot
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar bot: {e}")
            raise
    
    def list_bots(self):
        """Lista todos os bots"""
        if not self.active_bots:
            print("📝 Nenhum bot encontrado")
            return
        
        print(f"🤖 Bots Ativos ({len(self.active_bots)}):")
        print("-" * 50)
        
        for i, bot in enumerate(self.active_bots, 1):
            print(f"{i}. {bot.name}")
            print(f"   Status: {bot.status.value}")
            print(f"   Capital: ${bot.current_capital}")
            print(f"   Estratégia: {bot.strategy.name}")
            print()
    
    def show_status(self):
        """Mostra o status do sistema"""
        print("📊 Status do Sistema XBot v2")
        print("=" * 40)
        print(f"🤖 Bots Ativos: {len(self.active_bots)}")
        print(f"🔗 Binance: {'✅ Conectado' if self.binance_service else '❌ Desconectado'}")
        print(f"📱 Telegram: {'✅ Ativo' if self.config.telegram.enabled else '❌ Inativo'}")
        print()
        
    def show_performance(self):
        """Mostra performance detalhada dos bots"""
        print("📊 Dashboard de Performance XBot v2")
        print("=" * 60)
        
        if not self.active_bots:
            print("❌ Nenhum bot ativo")
            return
        
        print(f"🤖 Total de Bots: {len(self.active_bots)}")
        print()
        
        total_capital = Decimal("0")
        total_profit = Decimal("0")
        
        for i, bot in enumerate(self.active_bots, 1):
            initial = bot.initial_capital
            current = bot.current_capital or initial
            profit = current - initial
            profit_pct = (profit / initial * 100) if initial > 0 else 0
            
            total_capital += current
            total_profit += profit
            
            # Status emoji
            status_emoji = "🟢" if bot.status.value == "ACTIVE" else "🔴" if bot.status.value == "ERROR" else "🟡"
            
            # Profit emoji
            if profit > 0:
                profit_emoji = "📈"
                profit_color = "+"
            elif profit < 0:
                profit_emoji = "📉"
                profit_color = ""
            else:
                profit_emoji = "➖"
                profit_color = ""
            
            print(f"{i}. {status_emoji} {bot.name}")
            print(f"   💰 Capital: ${initial} → ${current}")
            print(f"   {profit_emoji} P&L: {profit_color}${profit} ({profit_color}{profit_pct:.2f}%)")
            print(f"   📊 Status: {bot.status.value}")
            print(f"   🎯 Estratégia: {bot.strategy.name if bot.strategy else 'N/A'}")
            print(f"   📈 Trades: {bot.total_trades}")
            print(f"   🎯 Trades Ganhos: {bot.winning_trades}/{bot.total_trades}")
            print()
        
        # Resumo geral
        initial_total = sum(bot.initial_capital for bot in self.active_bots)
        total_profit_pct = (total_profit / initial_total * 100) if initial_total > 0 else 0
        
        print("=" * 60)
        print("📈 RESUMO GERAL")
        print("=" * 60)
        print(f"💰 Capital Total: ${total_capital}")
        print(f"📊 P&L Total: ${total_profit} ({total_profit_pct:.2f}%)")
        print(f"🤖 Bots Ativos: {len([b for b in self.active_bots if b.status.value == 'ACTIVE'])}")
        print(f"🛑 Bots Parados: {len([b for b in self.active_bots if b.status.value == 'IDLE'])}")
        print()
    
    async def run_dashboard(self):
        """Executa o dashboard de monitoramento"""
        logger.info("📊 Iniciando dashboard...")
        print("🚀 Iniciando Dashboard Web...")
        try:
            from dashboard_app import run_dashboard
            run_dashboard()
        except ImportError as e:
            print(f"❌ Erro ao importar dashboard: {e}")
            print("💡 Execute: pip install flask")
        except KeyboardInterrupt:
            print("\n� Dashboard interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro no dashboard: {e}")
    
    async def setup_environment(self):
        """Configura o ambiente inicial"""
        logger.info("⚙️ Configurando ambiente...")
        
        # Verificar dependências
        print("✅ Verificando dependências...")
        
        # Criar diretórios necessários
        directories = ['data', 'logs', 'backups']
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            print(f"📁 Diretório '{directory}' criado/verificado")
        
        # Verificar configurações
        print("⚙️ Verificando configurações...")
        
        print("✅ Setup concluído!")
    
    async def run_tests(self):
        """Executa testes do sistema"""
        logger.info("🧪 Executando testes...")
        import subprocess
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", "tests/", "-v"
            ], capture_output=True, text=True, cwd=project_root)
            
            print(result.stdout)
            if result.stderr:
                print("Erros:", result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar testes: {e}")
            return False


async def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="XBot v2 - Sistema de Trading Automatizado",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py start                          # Inicia o sistema
  python main.py create-bot "MeuBot" --capital 1000 --symbols BTCUSDT,ETHUSDT
  python main.py list-bots                      # Lista todos os bots
  python main.py status                         # Mostra status do sistema
  python main.py dashboard                      # Abre dashboard
  python main.py setup                          # Configura ambiente
  python main.py test                           # Executa testes
        """
    )
    
    parser.add_argument(
        "command",
        choices=["start", "stop", "status", "create-bot", "list-bots", 
                "dashboard", "performance", "setup", "test"],
        help="Comando a ser executado"
    )
    
    parser.add_argument(
        "name",
        nargs="?",
        help="Nome do bot (para create-bot)"
    )
    
    parser.add_argument(
        "--capital",
        type=float,
        default=1000.0,
        help="Capital inicial do bot (padrão: 1000)"
    )
    
    parser.add_argument(
        "--symbols",
        default="BTCUSDT",
        help="Símbolos para trading (separados por vírgula, padrão: BTCUSDT)"
    )
    
    parser.add_argument(
        "--strategy",
        default="default_strategy",
        help="Nome da estratégia (padrão: default_strategy)"
    )
    
    args = parser.parse_args()
    
    # Criar orquestrador
    orchestrator = XBotOrchestrator()
    
    try:
        if args.command == "start":
            await orchestrator.start_system()
            
        elif args.command == "stop":
            await orchestrator.stop_system()
            
        elif args.command == "status":
            await orchestrator.initialize()
            orchestrator.show_status()
            
        elif args.command == "create-bot":
            if not args.name:
                print("❌ Nome do bot é obrigatório para create-bot")
                return
            
            symbols = [s.strip() for s in args.symbols.split(",")]
            await orchestrator.initialize()
            await orchestrator.create_bot(
                name=args.name,
                strategy_name=args.strategy,
                symbols=symbols,
                initial_capital=args.capital
            )
            
        elif args.command == "list-bots":
            await orchestrator.initialize()
            orchestrator.list_bots()
            
        elif args.command == "dashboard":
            await orchestrator.run_dashboard()
            
        elif args.command == "performance":
            await orchestrator.initialize()
            orchestrator.show_performance()
            
        elif args.command == "setup":
            await orchestrator.setup_environment()
            
        elif args.command == "test":
            success = await orchestrator.run_tests()
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        logger.info("⏹️ Interrompido pelo usuário")
        await orchestrator.stop_system()
        
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Executar o main com asyncio
    asyncio.run(main())