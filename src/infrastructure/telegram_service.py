"""
XBot v2 - Telegram Notification Service (Infrastructure Layer)

Serviço para envio de notificações via Telegram Bot.
"""

import aiohttp
import asyncio
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
import json
import logging

from ..domain.entities import TradingBot, Order, Position
from ..domain.interfaces import INotificationService


logger = logging.getLogger(__name__)


class TelegramNotificationService(INotificationService):
    """Serviço de notificações via Telegram"""
    
    def __init__(self, bot_token: str, admin_chat_id: str, group_chat_id: Optional[str] = None):
        self.bot_token = bot_token
        self.admin_chat_id = admin_chat_id
        self.group_chat_id = group_chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
        # Rate limiting
        self.last_message_time = {}
        self.min_interval = 5  # Seconds between messages
        
        # Message templates
        self.emoji_map = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️',
            'money': '💰',
            'chart_up': '📈',
            'chart_down': '📉',
            'robot': '🤖',
            'fire': '🔥',
            'target': '🎯',
            'shield': '🛡️'
        }
    
    async def send_trade_notification(
        self, 
        bot_id: str, 
        order: Order, 
        message: str
    ) -> bool:
        """Envia notificação de trade"""
        logger.info(f"Enviando notificação de trade: {order.order_id}")
        
        # Rate limiting check
        if not self._can_send_message(f"trade_{bot_id}"):
            return False
        
        emoji = self.emoji_map['chart_up'] if order.side.value == 'BUY' else self.emoji_map['chart_down']
        status_emoji = self.emoji_map['success'] if order.is_filled else self.emoji_map['info']
        
        text = f"""
{status_emoji} **TRADE EXECUTADO**

{emoji} **{order.symbol}** - {order.side.value}
{self.emoji_map['money']} Quantidade: `{order.quantity}`
{self.emoji_map['target']} Preço: `{order.price or 'MARKET'}`
{self.emoji_map['info']} Status: {order.status.value}

{self.emoji_map['robot']} Bot: `{bot_id}`
📊 Order ID: `{order.order_id}`

{message}
        """.strip()
        
        success = await self._send_message(self.admin_chat_id, text)
        
        # Also send to group if configured
        if self.group_chat_id and success:
            await self._send_message(self.group_chat_id, text)
        
        return success
    
    async def send_alert(self, title: str, message: str, urgency: str = "normal") -> bool:
        """Envia alerta geral"""
        logger.info(f"Enviando alerta: {title}")
        
        if not self._can_send_message(f"alert_{urgency}"):
            return False
        
        # Choose emoji based on urgency
        urgency_emojis = {
            'low': self.emoji_map['info'],
            'normal': self.emoji_map['warning'],
            'high': self.emoji_map['error'],
            'critical': self.emoji_map['fire']
        }
        
        emoji = urgency_emojis.get(urgency, self.emoji_map['info'])
        
        text = f"""
{emoji} **{title.upper()}**

{message}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_performance_report(self, bot: TradingBot) -> bool:
        """Envia relatório de performance"""
        logger.info(f"Enviando relatório de performance: {bot.name}")
        
        if not self._can_send_message(f"report_{bot.id}"):
            return False
        
        profit_emoji = self.emoji_map['chart_up'] if bot.profit_percentage > 0 else self.emoji_map['chart_down']
        
        text = f"""
📊 **RELATÓRIO DIÁRIO - {bot.name}**

{self.emoji_map['money']} **Capital**
• Inicial: `{bot.initial_capital:.2f} USDT`
• Atual: `{bot.current_capital:.2f} USDT`
• Lucro: `{profit_emoji} {bot.profit_percentage:.2f}%`

📈 **Performance**
• Total de Trades: `{bot.total_trades}`
• Trades Ganhos: `{bot.winning_trades}`
• Taxa de Acerto: `{bot.win_rate:.1f}%`

💼 **Posições**
• Ativas: `{bot.position_count}`
• Valor Total: `{bot.total_position_value:.2f} USDT`

🛡️ **Risco**
• Drawdown Máximo: `{bot.max_drawdown:.2f}%`
• Última Análise: `{bot.last_analysis_at.strftime('%H:%M') if bot.last_analysis_at else 'N/A'}`

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_risk_alert(self, bot: TradingBot, risk_message: str) -> bool:
        """Envia alerta de risco"""
        logger.warning(f"Enviando alerta de risco: {bot.name}")
        
        text = f"""
🚨 **ALERTA DE RISCO**

{self.emoji_map['shield']} **Bot:** {bot.name}
⚠️ **Problema:** {risk_message}

💰 **Capital Atual:** `{bot.current_capital:.2f} USDT`
📉 **Profit/Loss:** `{bot.profit_percentage:.2f}%`
📊 **Posições Ativas:** `{bot.position_count}`

🤖 **Status:** {bot.status.value}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Ação recomendada:** Verificar configurações do bot imediatamente!
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_pattern_alert(
        self, 
        symbol: str, 
        patterns: List, 
        confidence: Decimal
    ) -> bool:
        """Envia alerta de padrão detectado"""
        if not patterns:
            return False
        
        logger.info(f"Enviando alerta de padrão: {symbol}")
        
        pattern_names = [p.pattern_type.value.replace('_', ' ').title() for p in patterns]
        pattern_list = '\n'.join([f"• {name}" for name in pattern_names])
        
        text = f"""
🔍 **PADRÃO DETECTADO**

📊 **Símbolo:** {symbol}
🎯 **Confiança:** `{confidence:.1%}`

📈 **Padrões:**
{pattern_list}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_market_summary(
        self, 
        symbol: str, 
        analysis_data: Dict
    ) -> bool:
        """Envia resumo de análise de mercado"""
        logger.info(f"Enviando resumo de mercado: {symbol}")
        
        sentiment_emoji = {
            'BULLISH': self.emoji_map['chart_up'],
            'BEARISH': self.emoji_map['chart_down'],
            'NEUTRAL': self.emoji_map['info']
        }
        
        sentiment = analysis_data.get('sentiment', 'NEUTRAL')
        
        text = f"""
📊 **ANÁLISE DE MERCADO - {symbol}**

{sentiment_emoji.get(sentiment, self.emoji_map['info'])} **Sentiment:** {sentiment}
📈 **Preço:** `{analysis_data.get('price', 'N/A')}`
📊 **Volatilidade:** `{analysis_data.get('volatility', 'N/A')}`

🔍 **Indicadores:**
• RSI: `{analysis_data.get('rsi', 'N/A')}`
• MACD: `{analysis_data.get('macd_signal', 'N/A')}`

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_position_update(
        self, 
        position: Position, 
        action: str, 
        reason: str = ""
    ) -> bool:
        """Envia atualização de posição"""
        logger.info(f"Enviando atualização de posição: {position.symbol}")
        
        action_emojis = {
            'opened': self.emoji_map['chart_up'],
            'closed': self.emoji_map['money'],
            'updated': self.emoji_map['info']
        }
        
        pnl_emoji = self.emoji_map['chart_up'] if position.pnl_percentage > 0 else self.emoji_map['chart_down']
        
        text = f"""
{action_emojis.get(action, self.emoji_map['info'])} **POSIÇÃO {action.upper()}**

📊 **{position.symbol}** - {position.side.value}
💰 **Quantidade:** `{position.quantity}`
🎯 **Preço de Entrada:** `{position.entry_price}`
📈 **Preço Atual:** `{position.current_price}`

{pnl_emoji} **P&L:** `{position.pnl_percentage:.2f}%`
💵 **Valor:** `{position.unrealized_pnl:.2f} USDT`

{f"📝 **Motivo:** {reason}" if reason else ""}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_system_status(
        self, 
        active_bots: int, 
        total_positions: int, 
        system_health: str
    ) -> bool:
        """Envia status do sistema"""
        logger.info("Enviando status do sistema")
        
        health_emojis = {
            'healthy': self.emoji_map['success'],
            'warning': self.emoji_map['warning'],
            'critical': self.emoji_map['error']
        }
        
        text = f"""
🤖 **STATUS DO SISTEMA XBOT**

{health_emojis.get(system_health, self.emoji_map['info'])} **Saúde:** {system_health.upper()}

📊 **Estatísticas:**
• Bots Ativos: `{active_bots}`
• Posições Totais: `{total_positions}`

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_custom_message(self, message: str, chat_id: Optional[str] = None) -> bool:
        """Envia mensagem customizada"""
        target_chat = chat_id or self.admin_chat_id
        return await self._send_message(target_chat, message)
    
    # ========================================
    # Private Helper Methods
    # ========================================
    
    async def _send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        """Envia mensagem via API do Telegram"""
        url = f"{self.base_url}/sendMessage"
        
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.debug("Mensagem enviada com sucesso")
                        return True
                    else:
                        error_data = await response.json()
                        logger.error(f"Erro ao enviar mensagem: {error_data}")
                        return False
                        
        except aiohttp.ClientError as e:
            logger.error(f"Erro de conexão ao Telegram: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar mensagem: {e}")
            return False
    
    def _can_send_message(self, message_key: str) -> bool:
        """Verifica se pode enviar mensagem (rate limiting)"""
        current_time = datetime.now().timestamp()
        last_time = self.last_message_time.get(message_key, 0)
        
        if current_time - last_time >= self.min_interval:
            self.last_message_time[message_key] = current_time
            return True
        
        logger.debug(f"Rate limit ativo para {message_key}")
        return False
    
    async def test_connection(self) -> bool:
        """Testa conexão com o Telegram"""
        url = f"{self.base_url}/getMe"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        bot_info = data.get('result', {})
                        logger.info(f"Conexão Telegram OK. Bot: {bot_info.get('first_name', 'Unknown')}")
                        return True
                    else:
                        logger.error(f"Erro na conexão Telegram: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Erro ao testar conexão Telegram: {e}")
            return False
    
    async def send_startup_message(self) -> bool:
        """Envia mensagem de inicialização"""
        text = f"""
🚀 **XBOT INICIADO**

{self.emoji_map['robot']} Sistema de trading ativo
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Status: **OPERACIONAL** ✅
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)
    
    async def send_shutdown_message(self) -> bool:
        """Envia mensagem de desligamento"""
        text = f"""
🛑 **XBOT PARADO**

{self.emoji_map['warning']} Sistema de trading desativado
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Status: **PARADO** ⏹️
        """.strip()
        
        return await self._send_message(self.admin_chat_id, text)