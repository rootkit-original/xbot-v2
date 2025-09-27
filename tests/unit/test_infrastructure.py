"""
XBot v2 - Infrastructure Services Unit Tests
Testes unitários para serviços da infraestrutura
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
from datetime import datetime
from typing import List, Dict

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.config import XBotConfig, BinanceConfig, TelegramConfig
from src.infrastructure.risk_analysis_service import RiskAnalysisService
from src.infrastructure.pattern_detection_service import PatternDetectionService


class TestXBotConfig:
    """Testes para configuração do XBot"""

    def test_config_initialization(self):
        """Testa inicialização da configuração"""
        config = XBotConfig()
        
        assert config is not None
        assert hasattr(config, 'binance')
        assert hasattr(config, 'telegram')
        assert hasattr(config, 'risk')

    def test_binance_config(self):
        """Testa configuração da Binance"""
        config = XBotConfig()
        
        assert hasattr(config.binance, 'api_key')
        assert hasattr(config.binance, 'api_secret')
        assert hasattr(config.binance, 'testnet')

    def test_telegram_config(self):
        """Testa configuração do Telegram"""
        config = XBotConfig()
        
        assert hasattr(config.telegram, 'bot_token')
        assert hasattr(config.telegram, 'chat_id')

    def test_risk_config(self):
        """Testa configuração de risco"""
        config = XBotConfig()
        
        assert hasattr(config.risk, 'max_position_size')
        assert hasattr(config.risk, 'risk_percentage')

    def test_config_methods(self):
        """Testa métodos da configuração"""
        config = XBotConfig()
        
        # Test available strategies method
        strategies = config.get_available_strategies()
        assert isinstance(strategies, list)
        
        # Test validation method
        is_valid = config.validate_api_credentials()
        assert isinstance(is_valid, bool)


class TestRiskAnalysisService:
    """Testes para serviço de análise de risco"""

    @pytest.fixture
    def risk_service(self):
        """Fixture do serviço de risco"""
        return RiskAnalysisService()

    @pytest.fixture
    def mock_risk_profile(self):
        """Mock do perfil de risco"""
        from src.domain.entities import RiskProfile
        return RiskProfile(
            max_risk_percentage=2.0,
            max_daily_loss=500.0,
            max_open_positions=5,
            stop_loss_percentage=2.0,
            take_profit_percentage=4.0
        )

    def test_calculate_position_size(self, risk_service, mock_risk_profile):
        """Testa cálculo do tamanho da posição"""
        balance = Decimal("1000.00")
        price = Decimal("50000.00")
        
        position_size = risk_service.calculate_position_size(
            balance, price, mock_risk_profile
        )
        
        assert isinstance(position_size, Decimal)
        assert position_size > 0
        
        # Position size should respect risk percentage
        max_risk = balance * (mock_risk_profile.max_risk_percentage / 100)
        assert position_size * price <= max_risk * 10  # Some buffer for calculations

    def test_assess_market_risk(self, risk_service):
        """Testa avaliação de risco do mercado"""
        # Mock market data
        mock_candles = []
        for i in range(100):
            price_base = Decimal("50000.00")
            price_variation = Decimal(str(i * 10))
            mock_candles.append({
                'open': price_base + price_variation,
                'high': price_base + price_variation + Decimal("100"),
                'low': price_base + price_variation - Decimal("100"),
                'close': price_base + price_variation + Decimal("50"),
                'volume': Decimal("10.0")
            })
        
        risk_level = risk_service.assess_market_risk(mock_candles)
        
        from src.domain.entities import RiskLevel
        assert risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.EXTREME]

    def test_calculate_stop_loss(self, risk_service, mock_risk_profile):
        """Testa cálculo do stop loss"""
        entry_price = Decimal("50000.00")
        side = "BUY"
        
        stop_loss = risk_service.calculate_stop_loss(
            entry_price, side, mock_risk_profile
        )
        
        assert isinstance(stop_loss, Decimal)
        
        # For BUY orders, stop loss should be below entry price
        if side == "BUY":
            assert stop_loss < entry_price
        
        # Stop loss should respect the risk profile percentage
        expected_sl_distance = entry_price * (mock_risk_profile.stop_loss_percentage / 100)
        actual_sl_distance = abs(entry_price - stop_loss)
        assert abs(actual_sl_distance - expected_sl_distance) < Decimal("1.0")

    def test_calculate_take_profit(self, risk_service, mock_risk_profile):
        """Testa cálculo do take profit"""
        entry_price = Decimal("50000.00")
        side = "BUY"
        
        take_profit = risk_service.calculate_take_profit(
            entry_price, side, mock_risk_profile
        )
        
        assert isinstance(take_profit, Decimal)
        
        # For BUY orders, take profit should be above entry price
        if side == "BUY":
            assert take_profit > entry_price
        
        # Take profit should respect the risk profile percentage
        expected_tp_distance = entry_price * (mock_risk_profile.take_profit_percentage / 100)
        actual_tp_distance = abs(take_profit - entry_price)
        assert abs(actual_tp_distance - expected_tp_distance) < Decimal("1.0")

    def test_validate_trade_risk(self, risk_service, mock_risk_profile):
        """Testa validação de risco da operação"""
        trade_params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'quantity': Decimal('0.01'),
            'price': Decimal('50000.00'),
            'balance': Decimal('1000.00')
        }
        
        is_valid = risk_service.validate_trade_risk(trade_params, mock_risk_profile)
        assert isinstance(is_valid, bool)

    def test_portfolio_risk_assessment(self, risk_service):
        """Testa avaliação de risco do portfolio"""
        # Mock positions
        mock_positions = [
            {
                'symbol': 'BTCUSDT',
                'side': 'BUY',
                'quantity': Decimal('0.1'),
                'unrealized_pnl': Decimal('100.0')
            },
            {
                'symbol': 'ETHUSDT',
                'side': 'SELL',
                'quantity': Decimal('1.0'),
                'unrealized_pnl': Decimal('-50.0')
            }
        ]
        
        portfolio_risk = risk_service.assess_portfolio_risk(mock_positions)
        
        assert isinstance(portfolio_risk, dict)
        assert 'total_exposure' in portfolio_risk
        assert 'risk_level' in portfolio_risk
        assert 'diversification_score' in portfolio_risk


class TestPatternDetectionService:
    """Testes para serviço de detecção de padrões"""

    @pytest.fixture
    def pattern_service(self):
        """Fixture do serviço de padrões"""
        return PatternDetectionService()

    @pytest.fixture
    def mock_candles(self):
        """Mock de candles para testes"""
        candles = []
        base_price = Decimal("50000.00")
        
        for i in range(50):
            # Create trending pattern
            trend_factor = i * 10
            candles.append({
                'open': base_price + Decimal(str(trend_factor)),
                'high': base_price + Decimal(str(trend_factor + 200)),
                'low': base_price + Decimal(str(trend_factor - 100)),
                'close': base_price + Decimal(str(trend_factor + 100)),
                'volume': Decimal("10.0"),
                'timestamp': datetime.now()
            })
        
        return candles

    def test_detect_support_resistance(self, pattern_service, mock_candles):
        """Testa detecção de suporte e resistência"""
        from src.domain.entities import PatternType
        
        patterns = pattern_service.detect_patterns(mock_candles, PatternType.SUPPORT_RESISTANCE)
        
        assert isinstance(patterns, list)
        # Should find at least some support/resistance levels
        for pattern in patterns:
            assert hasattr(pattern, 'pattern_type')
            assert hasattr(pattern, 'confidence')
            assert 0.0 <= pattern.confidence <= 1.0

    def test_detect_breakout_patterns(self, pattern_service, mock_candles):
        """Testa detecção de padrões de rompimento"""
        from src.domain.entities import PatternType
        
        patterns = pattern_service.detect_patterns(mock_candles, PatternType.BREAKOUT)
        
        assert isinstance(patterns, list)
        for pattern in patterns:
            assert pattern.pattern_type == PatternType.BREAKOUT
            assert isinstance(pattern.confidence, float)

    def test_detect_reversal_patterns(self, pattern_service, mock_candles):
        """Testa detecção de padrões de reversão"""
        from src.domain.entities import PatternType
        
        patterns = pattern_service.detect_patterns(mock_candles, PatternType.REVERSAL)
        
        assert isinstance(patterns, list)
        for pattern in patterns:
            assert pattern.pattern_type == PatternType.REVERSAL

    def test_calculate_pattern_confidence(self, pattern_service):
        """Testa cálculo de confiança do padrão"""
        # Mock pattern data
        pattern_data = {
            'strength': 0.8,
            'volume_confirmation': 0.9,
            'time_consistency': 0.7,
            'market_context': 0.85
        }
        
        confidence = pattern_service.calculate_pattern_confidence(pattern_data)
        
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_trend_analysis(self, pattern_service, mock_candles):
        """Testa análise de tendência"""
        trend_info = pattern_service.analyze_trend(mock_candles)
        
        assert isinstance(trend_info, dict)
        assert 'direction' in trend_info
        assert 'strength' in trend_info
        assert 'duration' in trend_info
        
        # Direction should be up, down, or sideways
        assert trend_info['direction'] in ['up', 'down', 'sideways']
        
        # Strength should be between 0 and 1
        assert 0.0 <= trend_info['strength'] <= 1.0

    def test_volume_analysis(self, pattern_service, mock_candles):
        """Testa análise de volume"""
        volume_info = pattern_service.analyze_volume(mock_candles)
        
        assert isinstance(volume_info, dict)
        assert 'average_volume' in volume_info
        assert 'volume_trend' in volume_info
        assert 'volume_spikes' in volume_info

    def test_volatility_calculation(self, pattern_service, mock_candles):
        """Testa cálculo de volatilidade"""
        volatility = pattern_service.calculate_volatility(mock_candles)
        
        assert isinstance(volatility, (float, Decimal))
        assert volatility >= 0

    def test_pattern_filtering(self, pattern_service):
        """Testa filtragem de padrões"""
        # Mock patterns with different confidence levels
        mock_patterns = [
            Mock(confidence=0.95, pattern_type='BREAKOUT'),
            Mock(confidence=0.60, pattern_type='REVERSAL'),
            Mock(confidence=0.85, pattern_type='SUPPORT_RESISTANCE'),
            Mock(confidence=0.45, pattern_type='CONTINUATION')
        ]
        
        filtered_patterns = pattern_service.filter_patterns_by_confidence(
            mock_patterns, min_confidence=0.7
        )
        
        assert len(filtered_patterns) == 2  # Only patterns with confidence >= 0.7
        assert all(p.confidence >= 0.7 for p in filtered_patterns)


class TestIntegrationScenarios:
    """Testes de cenários integrados"""

    def test_complete_risk_analysis_workflow(self):
        """Testa workflow completo de análise de risco"""
        from src.domain.entities import RiskProfile
        from infrastructure.risk_analysis_service import RiskAnalysisService
        
        # Setup
        risk_service = RiskAnalysisService()
        risk_profile = RiskProfile(1.5, 300.0, 3, 2.0, 3.5)
        
        # Test workflow
        balance = Decimal("1000.00")
        price = Decimal("45000.00")
        
        # 1. Calculate position size
        position_size = risk_service.calculate_position_size(balance, price, risk_profile)
        assert position_size > 0
        
        # 2. Calculate stop loss
        stop_loss = risk_service.calculate_stop_loss(price, "BUY", risk_profile)
        assert stop_loss < price
        
        # 3. Calculate take profit
        take_profit = risk_service.calculate_take_profit(price, "BUY", risk_profile)
        assert take_profit > price
        
        # 4. Validate trade
        trade_params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'quantity': position_size,
            'price': price,
            'balance': balance
        }
        
        is_valid = risk_service.validate_trade_risk(trade_params, risk_profile)
        assert isinstance(is_valid, bool)

    def test_pattern_and_risk_integration(self):
        """Testa integração entre detecção de padrões e análise de risco"""
        from src.infrastructure.pattern_detection_service import PatternDetectionService
        from infrastructure.risk_analysis_service import RiskAnalysisService
        
        pattern_service = PatternDetectionService()
        risk_service = RiskAnalysisService()
        
        # Mock data
        mock_candles = [
            {'open': Decimal('50000'), 'high': Decimal('51000'), 
             'low': Decimal('49500'), 'close': Decimal('50800'), 'volume': Decimal('10')}
        ] * 20
        
        # 1. Analyze market trend
        trend_info = pattern_service.analyze_trend(mock_candles)
        assert isinstance(trend_info, dict)
        
        # 2. Assess market risk
        risk_level = risk_service.assess_market_risk(mock_candles)
        assert risk_level is not None
        
        # Integration should work without errors
        assert True


if __name__ == "__main__":
    pytest.main([__file__])
