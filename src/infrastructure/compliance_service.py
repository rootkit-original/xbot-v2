"""
XBot v2 - Compliance Service (Infrastructure Layer)

Serviço para validação de compliance e conformidade regulatória.
"""

from typing import Dict, List, Tuple, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import logging

from ..domain.entities import Order, Position, TradingBot, RiskLevel
from ..domain.interfaces import IComplianceService, IRiskAnalysisService


logger = logging.getLogger(__name__)


class ComplianceService(IComplianceService):
    """Serviço de compliance e conformidade"""
    
    def __init__(self, risk_analyzer: IRiskAnalysisService):
        self.risk_analyzer = risk_analyzer
        self.audit_logs = []
    
    async def validate_trade(
        self, 
        order: Order, 
        current_positions: List[Position]
    ) -> Tuple[bool, str]:
        """Valida trade antes da execução"""
        
        # 1. Validate order parameters
        if order.quantity <= 0:
            return False, "Quantidade inválida"
        
        if order.price and order.price <= 0:
            return False, "Preço inválido"
        
        # 2. Check for conflicting positions
        existing_position = next(
            (pos for pos in current_positions if pos.symbol == order.symbol), 
            None
        )
        
        if existing_position:
            # Check if trying to open opposite position
            if existing_position.side != order.side:
                logger.warning(f"Posição conflitante detectada para {order.symbol}")
                # This could be allowed for hedging in advanced strategies
        
        # 3. Minimum order value check
        if order.price:
            order_value = order.quantity * order.price
            min_order_value = Decimal('10')  # $10 minimum
            
            if order_value < min_order_value:
                return False, f"Valor da ordem muito baixo: ${order_value} < ${min_order_value}"
        
        # 4. Symbol validation (basic)
        if not order.symbol or len(order.symbol) < 6:
            return False, "Símbolo inválido"
        
        logger.info(f"Trade validado: {order.symbol} {order.side.value}")
        return True, "Trade válido"
    
    async def check_position_limits(self, bot: TradingBot) -> Tuple[bool, str]:
        """Verifica limites de posição"""
        
        # 1. Maximum concurrent positions
        max_positions = bot.strategy.risk_profile.max_concurrent_positions
        current_positions = len(bot.active_positions)
        
        if current_positions >= max_positions:
            return False, f"Limite de posições excedido: {current_positions}/{max_positions}"
        
        # 2. Position size limits
        for position in bot.active_positions:
            position_percentage = (position.market_value / bot.current_capital) * 100
            max_position_size = bot.strategy.risk_profile.max_position_size
            
            if position_percentage > max_position_size:
                return False, f"Posição {position.symbol} excede limite: {position_percentage:.1f}% > {max_position_size}%"
        
        # 3. Total exposure
        total_exposure = sum(pos.market_value for pos in bot.active_positions)
        max_total_exposure = bot.current_capital * Decimal('0.95')  # 95% max exposure
        
        if total_exposure > max_total_exposure:
            return False, f"Exposição total excede limite: ${total_exposure} > ${max_total_exposure}"
        
        return True, "Limites de posição OK"
    
    async def check_daily_loss_limit(self, bot: TradingBot) -> Tuple[bool, str]:
        """Verifica limite de perda diária"""
        
        # Calculate daily P&L (simplified - should track from start of day)
        daily_loss_limit = bot.strategy.risk_profile.max_daily_loss
        
        # Simplified calculation using current profit/loss
        current_loss_percentage = abs(min(bot.profit_percentage, Decimal('0')))
        
        if current_loss_percentage > daily_loss_limit:
            return False, f"Limite de perda diária excedido: {current_loss_percentage:.2f}% > {daily_loss_limit:.2f}%"
        
        # Check unrealized losses
        unrealized_loss = sum(
            min(pos.unrealized_pnl, Decimal('0')) 
            for pos in bot.active_positions
        )
        
        if unrealized_loss != 0:
            unrealized_loss_percentage = abs(unrealized_loss / bot.current_capital * 100)
            
            if unrealized_loss_percentage > daily_loss_limit:
                return False, f"Perdas não realizadas excedem limite: {unrealized_loss_percentage:.2f}% > {daily_loss_limit:.2f}%"
        
        return True, "Limite de perda diária OK"
    
    async def generate_audit_log(
        self, 
        bot: TradingBot, 
        action: str, 
        details: Dict
    ) -> bool:
        """Gera log de auditoria"""
        
        audit_entry = {
            'timestamp': datetime.now(),
            'bot_id': bot.id,
            'bot_name': bot.name,
            'action': action,
            'details': details,
            'bot_status': bot.status.value,
            'current_capital': float(bot.current_capital),
            'profit_percentage': float(bot.profit_percentage)
        }
        
        self.audit_logs.append(audit_entry)
        
        # Log to file/database in production
        logger.info(f"Audit Log: {action} - Bot {bot.id} - {details}")
        
        # Keep only last 1000 entries in memory
        if len(self.audit_logs) > 1000:
            self.audit_logs = self.audit_logs[-1000:]
        
        return True
    
    async def check_risk_management_rules(self, bot: TradingBot) -> List[str]:
        """Verifica regras de gestão de risco"""
        violations = []
        
        # 1. Check if bot has been running too long without review
        if bot.last_analysis_at:
            hours_since_analysis = (datetime.now() - bot.last_analysis_at).total_seconds() / 3600
            if hours_since_analysis > 24:  # 24 hours
                violations.append(f"Bot sem análise há {hours_since_analysis:.1f} horas")
        
        # 2. Check maximum drawdown
        if bot.max_drawdown > Decimal('20'):  # 20% max drawdown
            violations.append(f"Drawdown máximo excedido: {bot.max_drawdown:.1f}%")
        
        # 3. Check for excessive losses
        if bot.profit_percentage < Decimal('-10'):  # -10% total loss
            violations.append(f"Perda total excessiva: {bot.profit_percentage:.1f}%")
        
        # 4. Check win rate (if enough trades)
        if bot.total_trades > 20 and bot.win_rate < Decimal('30'):  # 30% minimum win rate
            violations.append(f"Taxa de acerto baixa: {bot.win_rate:.1f}% ({bot.total_trades} trades)")
        
        # 5. Check position concentration
        if bot.active_positions:
            total_value = sum(pos.market_value for pos in bot.active_positions)
            for position in bot.active_positions:
                if total_value > 0:
                    concentration = (position.market_value / total_value) * 100
                    if concentration > 50:  # No single position > 50% of portfolio
                        violations.append(f"Concentração excessiva em {position.symbol}: {concentration:.1f}%")
        
        return violations
    
    async def calculate_compliance_score(self, bot: TradingBot) -> Dict[str, any]:
        """Calcula score de compliance"""
        
        violations = await self.check_risk_management_rules(bot)
        position_check = await self.check_position_limits(bot)
        daily_loss_check = await self.check_daily_loss_limit(bot)
        
        # Calculate score (100 = perfect compliance)
        base_score = 100
        
        # Deduct points for violations
        base_score -= len(violations) * 10
        
        if not position_check[0]:
            base_score -= 15
        
        if not daily_loss_check[0]:
            base_score -= 20
        
        # Risk level adjustment
        risk_level = bot.strategy.risk_profile.risk_level
        if risk_level == RiskLevel.HIGH:
            base_score -= 5
        elif risk_level == RiskLevel.CRITICAL:
            base_score -= 15
        
        compliance_score = max(0, min(100, base_score))
        
        # Determine compliance status
        if compliance_score >= 90:
            status = "EXCELLENT"
        elif compliance_score >= 75:
            status = "GOOD"
        elif compliance_score >= 60:
            status = "ADEQUATE"
        elif compliance_score >= 40:
            status = "POOR"
        else:
            status = "CRITICAL"
        
        return {
            'score': compliance_score,
            'status': status,
            'violations': violations,
            'position_limits_ok': position_check[0],
            'daily_loss_ok': daily_loss_check[0],
            'risk_level': risk_level.value,
            'last_check': datetime.now()
        }
    
    async def get_audit_logs(
        self, 
        bot_id: Optional[str] = None,
        hours: int = 24
    ) -> List[Dict]:
        """Obtém logs de auditoria"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_logs = [
            log for log in self.audit_logs
            if log['timestamp'] >= cutoff_time
        ]
        
        if bot_id:
            filtered_logs = [
                log for log in filtered_logs
                if log['bot_id'] == bot_id
            ]
        
        # Sort by timestamp (most recent first)
        filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return filtered_logs
    
    async def emergency_stop_conditions(self, bot: TradingBot) -> Tuple[bool, str]:
        """Verifica condições de parada de emergência"""
        
        # 1. Excessive losses
        if bot.profit_percentage < Decimal('-25'):  # 25% total loss
            return True, f"Perda total crítica: {bot.profit_percentage:.1f}%"
        
        # 2. Too many consecutive losses
        if bot.total_trades > 10:
            recent_loss_rate = (bot.total_trades - bot.winning_trades) / bot.total_trades
            if recent_loss_rate > 0.8:  # 80% loss rate
                return True, f"Taxa de perda crítica: {recent_loss_rate:.1%}"
        
        # 3. API/Connection issues (simplified)
        # This would normally check for API rate limits, connection failures, etc.
        
        # 4. Unusual market conditions
        # This could include high volatility, low liquidity, etc.
        
        return False, "Condições normais"