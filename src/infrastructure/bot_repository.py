"""
XBot v2 - Bot Repository (Infrastructure Layer)

Repositório para armazenamento e persistência de bots de trading.
"""

from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path

from ..domain.entities import TradingBot, BotStatus, Order, Position, Pattern
from ..domain.interfaces import IBotRepository


logger = logging.getLogger(__name__)


class InMemoryBotRepository(IBotRepository):
    """Repositório em memória para bots de trading"""

    def __init__(self, persistence_dir: Optional[str] = None):
        self._bots: Dict[str, TradingBot] = {}
        self._persistence_dir = Path(persistence_dir) if persistence_dir else None

        if self._persistence_dir:
            self._persistence_dir.mkdir(parents=True, exist_ok=True)
            self._load_persisted_bots()

    async def create_bot(self, bot: TradingBot) -> TradingBot:
        """Cria um novo bot"""
        if bot.id in self._bots:
            raise ValueError(f"Bot com ID {bot.id} já existe")

        bot.created_at = datetime.now()
        bot.updated_at = datetime.now()

        self._bots[bot.id] = bot
        await self._persist_bot(bot)

        logger.info(f"Bot criado: {bot.id} - {bot.name}")
        return bot

    async def get_bot(self, bot_id: str) -> Optional[TradingBot]:
        """Obtém bot por ID"""
        return self._bots.get(bot_id)

    async def update_bot(self, bot: TradingBot) -> TradingBot:
        """Atualiza bot existente"""
        if bot.id not in self._bots:
            raise ValueError(f"Bot {bot.id} não encontrado")

        bot.updated_at = datetime.now()
        self._bots[bot.id] = bot
        await self._persist_bot(bot)

        logger.debug(f"Bot atualizado: {bot.id}")
        return bot

    async def delete_bot(self, bot_id: str) -> bool:
        """Remove bot"""
        if bot_id not in self._bots:
            return False

        del self._bots[bot_id]

        # Remove persisted file
        if self._persistence_dir:
            bot_file = self._persistence_dir / f"bot_{bot_id}.json"
            if bot_file.exists():
                bot_file.unlink()

        logger.info(f"Bot removido: {bot_id}")
        return True

    async def list_bots(self) -> List[TradingBot]:
        """Lista todos os bots"""
        return list(self._bots.values())

    async def get_active_bots(self) -> List[TradingBot]:
        """Obtém bots ativos"""
        return [bot for bot in self._bots.values() if bot.status == BotStatus.RUNNING]

    async def get_bots_by_symbol(self, symbol: str) -> List[TradingBot]:
        """Obtém bots que negociam um símbolo específico"""
        return [
            bot
            for bot in self._bots.values()
            if any(symbol.upper() in pos.symbol.upper() for pos in bot.active_positions)
            or symbol.upper() in [s.upper() for s in bot.strategy.target_symbols]
        ]

    async def get_bots_by_status(self, status: BotStatus) -> List[TradingBot]:
        """Obtém bots por status"""
        return [bot for bot in self._bots.values() if bot.status == status]

    async def update_bot_positions(self, bot_id: str, positions: List[Position]) -> bool:
        """Atualiza posições do bot"""
        bot = await self.get_bot(bot_id)
        if not bot:
            return False

        bot.active_positions = positions
        bot.updated_at = datetime.now()

        await self._persist_bot(bot)
        return True

    async def add_bot_order(self, bot_id: str, order: Order) -> bool:
        """Adiciona ordem ao histórico do bot"""
        bot = await self.get_bot(bot_id)
        if not bot:
            return False

        bot.order_history.append(order)
        bot.total_trades += 1
        bot.updated_at = datetime.now()

        # Update statistics
        if order.status and "FILLED" in order.status.upper():
            if order.realized_pnl and order.realized_pnl > 0:
                bot.winning_trades += 1

        await self._persist_bot(bot)
        return True

    async def get_bot_performance(self, bot_id: str, days: int = 30) -> Dict:
        """Obtém performance do bot"""
        bot = await self.get_bot(bot_id)
        if not bot:
            return {}

        cutoff_date = datetime.now() - timedelta(days=days)

        # Filter recent orders
        recent_orders = [order for order in bot.order_history if order.timestamp >= cutoff_date]

        # Calculate metrics
        total_trades = len(recent_orders)
        winning_trades = sum(
            1 for order in recent_orders if order.realized_pnl and order.realized_pnl > 0
        )

        total_pnl = sum(order.realized_pnl for order in recent_orders if order.realized_pnl)

        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        return {
            "bot_id": bot_id,
            "period_days": days,
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "win_rate": round(win_rate, 2),
            "total_pnl": float(total_pnl),
            "avg_pnl_per_trade": float(total_pnl / total_trades) if total_trades > 0 else 0,
            "current_capital": float(bot.current_capital),
            "profit_percentage": float(bot.profit_percentage),
            "active_positions": len(bot.active_positions),
            "last_trade": recent_orders[-1].timestamp if recent_orders else None,
        }

    async def get_portfolio_summary(self) -> Dict:
        """Obtém resumo do portfólio"""
        active_bots = await self.get_active_bots()

        total_capital = sum(bot.current_capital for bot in active_bots)
        total_positions = sum(len(bot.active_positions) for bot in active_bots)

        # Calculate total unrealized P&L
        total_unrealized_pnl = sum(
            sum(pos.unrealized_pnl for pos in bot.active_positions) for bot in active_bots
        )

        # Get symbol exposure
        symbol_exposure = {}
        for bot in active_bots:
            for position in bot.active_positions:
                symbol = position.symbol
                if symbol not in symbol_exposure:
                    symbol_exposure[symbol] = {"value": 0, "bots": set()}

                symbol_exposure[symbol]["value"] += position.market_value
                symbol_exposure[symbol]["bots"].add(bot.id)

        # Convert sets to counts
        for symbol in symbol_exposure:
            symbol_exposure[symbol]["bot_count"] = len(symbol_exposure[symbol]["bots"])
            del symbol_exposure[symbol]["bots"]

        return {
            "total_bots": len(self._bots),
            "active_bots": len(active_bots),
            "total_capital": float(total_capital),
            "total_positions": total_positions,
            "total_unrealized_pnl": float(total_unrealized_pnl),
            "symbol_exposure": {
                symbol: {"value": float(data["value"]), "bot_count": data["bot_count"]}
                for symbol, data in symbol_exposure.items()
            },
            "last_updated": datetime.now(),
        }

    async def backup_bots(self, backup_path: str) -> bool:
        """Cria backup de todos os bots"""
        try:
            backup_dir = Path(backup_path)
            backup_dir.mkdir(parents=True, exist_ok=True)

            backup_data = {"timestamp": datetime.now().isoformat(), "bots": {}}

            for bot_id, bot in self._bots.items():
                backup_data["bots"][bot_id] = self._serialize_bot(bot)

            backup_file = (
                backup_dir / f"xbot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)

            logger.info(f"Backup criado: {backup_file}")
            return True

        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return False

    async def restore_bots(self, backup_path: str) -> bool:
        """Restaura bots do backup"""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                logger.error(f"Arquivo de backup não encontrado: {backup_path}")
                return False

            with open(backup_file, "r", encoding="utf-8") as f:
                backup_data = json.load(f)

            restored_count = 0
            for bot_id, bot_data in backup_data.get("bots", {}).items():
                try:
                    bot = self._deserialize_bot(bot_data)
                    self._bots[bot_id] = bot
                    await self._persist_bot(bot)
                    restored_count += 1
                except Exception as e:
                    logger.error(f"Erro ao restaurar bot {bot_id}: {e}")

            logger.info(f"Bots restaurados: {restored_count}")
            return True

        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {e}")
            return False

    def _serialize_bot(self, bot: TradingBot) -> Dict:
        """Serializa bot para JSON"""
        return {
            "id": bot.id,
            "name": bot.name,
            "description": bot.description,
            "status": bot.status.value,
            "initial_capital": float(bot.initial_capital),
            "current_capital": float(bot.current_capital),
            "profit_percentage": float(bot.profit_percentage),
            "max_drawdown": float(bot.max_drawdown),
            "total_trades": bot.total_trades,
            "winning_trades": bot.winning_trades,
            "win_rate": float(bot.win_rate),
            "created_at": bot.created_at.isoformat() if bot.created_at else None,
            "updated_at": bot.updated_at.isoformat() if bot.updated_at else None,
            "last_analysis_at": bot.last_analysis_at.isoformat() if bot.last_analysis_at else None,
            # Note: This is a simplified serialization
            # In production, you'd need to serialize strategy, positions, etc.
        }

    def _deserialize_bot(self, data: Dict) -> TradingBot:
        """Deserializa bot do JSON"""
        # This is a simplified deserialization
        # In production, you'd need to reconstruct all complex objects
        bot = TradingBot(
            id=data["id"],
            name=data["name"],
            strategy=None,  # Would need to reconstruct
            initial_capital=data["initial_capital"],
        )

        bot.description = data.get("description", "")
        bot.status = BotStatus(data["status"])
        bot.current_capital = data["current_capital"]
        bot.profit_percentage = data["profit_percentage"]
        bot.max_drawdown = data["max_drawdown"]
        bot.total_trades = data["total_trades"]
        bot.winning_trades = data["winning_trades"]

        if data.get("created_at"):
            bot.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            bot.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("last_analysis_at"):
            bot.last_analysis_at = datetime.fromisoformat(data["last_analysis_at"])

        return bot

    async def _persist_bot(self, bot: TradingBot):
        """Persiste bot em arquivo"""
        if not self._persistence_dir:
            return

        try:
            bot_file = self._persistence_dir / f"bot_{bot.id}.json"
            bot_data = self._serialize_bot(bot)

            with open(bot_file, "w", encoding="utf-8") as f:
                json.dump(bot_data, f, indent=2, ensure_ascii=False, default=str)

        except Exception as e:
            logger.error(f"Erro ao persistir bot {bot.id}: {e}")

    def _load_persisted_bots(self):
        """Carrega bots persistidos"""
        if not self._persistence_dir or not self._persistence_dir.exists():
            return

        for bot_file in self._persistence_dir.glob("bot_*.json"):
            try:
                with open(bot_file, "r", encoding="utf-8") as f:
                    bot_data = json.load(f)

                bot = self._deserialize_bot(bot_data)
                self._bots[bot.id] = bot

            except Exception as e:
                logger.error(f"Erro ao carregar bot de {bot_file}: {e}")

        logger.info(f"Bots carregados: {len(self._bots)}")


class FileBotRepository(InMemoryBotRepository):
    """Repositório baseado em arquivos com melhor persistência"""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        super().__init__(str(self.data_dir))

    async def create_bot(self, bot: TradingBot) -> TradingBot:
        """Cria bot com persistência imediata"""
        result = await super().create_bot(bot)
        await self._full_persist_bot(bot)
        return result

    async def _full_persist_bot(self, bot: TradingBot):
        """Persistência completa do bot (incluindo estratégia, posições, etc.)"""
        # This would implement full serialization of all bot components
        # Including strategy, positions, order history, etc.
        pass
