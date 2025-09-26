"""
XBot v2 - Binance Service (Infrastructure Layer)

Implementação do serviço da Binance para operações de trading e dados de mercado.
"""

import aiohttp
import asyncio
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Tuple, AsyncIterator
from decimal import Decimal
from datetime import datetime
import json
import logging

from ..domain.entities import Market, Order, Position, Candle, OrderStatus, OrderSide, OrderType
from ..domain.interfaces import IMarketDataRepository, ITradingRepository, IPortfolioRepository, IMarketDataStream


logger = logging.getLogger(__name__)


class BinanceService(IMarketDataRepository, ITradingRepository, IPortfolioRepository, IMarketDataStream):
    """Serviço integrado da Binance"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # URLs
        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.ws_url = "wss://testnet.binance.vision/ws"
        else:
            self.base_url = "https://api.binance.com"
            self.ws_url = "wss://stream.binance.com:9443/ws"
        
        # Session HTTP
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws_connection: Optional[aiohttp.ClientWebSocketResponse] = None
        
        # Cache para evitar rate limiting
        self._symbol_cache = {}
        self._cache_ttl = 300  # 5 minutos
        
    async def _ensure_session(self):
        """Garante que a sessão HTTP está ativa"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def _sign_request(self, params: Dict) -> Dict:
        """Assina requisição para endpoints autenticados"""
        params['timestamp'] = int(time.time() * 1000)
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        params['signature'] = signature
        return params
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Dict = None, 
        signed: bool = False
    ) -> Dict:
        """Faz requisição HTTP para a API"""
        await self._ensure_session()
        
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if self.api_key:
            headers['X-MBX-APIKEY'] = self.api_key
        
        if params is None:
            params = {}
        
        if signed:
            params = await self._sign_request(params)
        
        try:
            if method.upper() == 'GET':
                async with self.session.get(url, params=params, headers=headers) as response:
                    return await self._handle_response(response)
            elif method.upper() == 'POST':
                async with self.session.post(url, data=params, headers=headers) as response:
                    return await self._handle_response(response)
            elif method.upper() == 'DELETE':
                async with self.session.delete(url, params=params, headers=headers) as response:
                    return await self._handle_response(response)
                    
        except aiohttp.ClientError as e:
            logger.error(f"Erro de conexão com Binance: {e}")
            raise
    
    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """Trata resposta da API"""
        try:
            data = await response.json()
            
            if response.status == 200:
                return data
            else:
                error_msg = data.get('msg', 'Unknown error')
                logger.error(f"Erro da API Binance: {response.status} - {error_msg}")
                raise Exception(f"Binance API Error: {error_msg}")
                
        except json.JSONDecodeError:
            text = await response.text()
            logger.error(f"Resposta inválida da API: {text}")
            raise Exception(f"Invalid API response: {text}")
    
    # ========================================
    # IMarketDataRepository Implementation
    # ========================================
    
    async def get_market_info(self, symbol: str) -> Optional[Market]:
        """Obtém informações do mercado"""
        try:
            # Cache check
            cache_key = f"symbol_{symbol}"
            if cache_key in self._symbol_cache:
                cached_data, timestamp = self._symbol_cache[cache_key]
                if time.time() - timestamp < self._cache_ttl:
                    return cached_data
            
            data = await self._make_request('GET', '/api/v3/exchangeInfo')
            
            for symbol_info in data.get('symbols', []):
                if symbol_info['symbol'] == symbol:
                    # Extrai filtros
                    lot_size_filter = next(
                        (f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'), 
                        {}
                    )
                    min_notional_filter = next(
                        (f for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 
                        {}
                    )
                    
                    market = Market(
                        symbol=symbol_info['symbol'],
                        base_asset=symbol_info['baseAsset'],
                        quote_asset=symbol_info['quoteAsset'],
                        status=symbol_info['status'],
                        is_spot_trading_allowed=symbol_info.get('isSpotTradingAllowed', True),
                        is_margin_trading_allowed=symbol_info.get('isMarginTradingAllowed', False),
                        min_qty=Decimal(lot_size_filter.get('minQty', '0')),
                        max_qty=Decimal(lot_size_filter.get('maxQty', '0')),
                        step_size=Decimal(lot_size_filter.get('stepSize', '0')),
                        min_notional=Decimal(min_notional_filter.get('minNotional', '0'))
                    )
                    
                    # Cache
                    self._symbol_cache[cache_key] = (market, time.time())
                    return market
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do mercado {symbol}: {e}")
            return None
    
    async def get_current_price(self, symbol: str) -> Optional[Decimal]:
        """Obtém preço atual"""
        try:
            data = await self._make_request('GET', '/api/v3/ticker/price', {'symbol': symbol})
            return Decimal(data['price'])
        except Exception as e:
            logger.error(f"Erro ao obter preço de {symbol}: {e}")
            return None
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Candle]:
        """Obtém candlesticks"""
        try:
            params = {
                'symbol': symbol,
                'interval': timeframe,
                'limit': min(limit, 1000)  # Limite da API
            }
            
            if start_time:
                params['startTime'] = int(start_time.timestamp() * 1000)
            if end_time:
                params['endTime'] = int(end_time.timestamp() * 1000)
            
            data = await self._make_request('GET', '/api/v3/klines', params)
            
            candles = []
            for kline in data:
                candle = Candle(
                    timestamp=datetime.fromtimestamp(kline[0] / 1000),
                    open_price=Decimal(kline[1]),
                    high_price=Decimal(kline[2]),
                    low_price=Decimal(kline[3]),
                    close_price=Decimal(kline[4]),
                    volume=Decimal(kline[5]),
                    symbol=symbol
                )
                candles.append(candle)
            
            return candles
            
        except Exception as e:
            logger.error(f"Erro ao obter candles de {symbol}: {e}")
            return []
    
    async def get_24h_stats(self, symbol: str) -> Dict[str, Decimal]:
        """Obtém estatísticas de 24h"""
        try:
            data = await self._make_request('GET', '/api/v3/ticker/24hr', {'symbol': symbol})
            
            return {
                'priceChange': Decimal(data['priceChange']),
                'priceChangePercent': Decimal(data['priceChangePercent']),
                'weightedAvgPrice': Decimal(data['weightedAvgPrice']),
                'prevClosePrice': Decimal(data['prevClosePrice']),
                'lastPrice': Decimal(data['lastPrice']),
                'lastQty': Decimal(data['lastQty']),
                'bidPrice': Decimal(data['bidPrice']),
                'askPrice': Decimal(data['askPrice']),
                'openPrice': Decimal(data['openPrice']),
                'highPrice': Decimal(data['highPrice']),
                'lowPrice': Decimal(data['lowPrice']),
                'volume': Decimal(data['volume']),
                'quoteVolume': Decimal(data['quoteVolume']),
                'count': Decimal(data['count'])
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas 24h de {symbol}: {e}")
            return {}
    
    async def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, List[Tuple[Decimal, Decimal]]]:
        """Obtém order book"""
        try:
            params = {'symbol': symbol, 'limit': min(limit, 5000)}
            data = await self._make_request('GET', '/api/v3/depth', params)
            
            bids = [(Decimal(price), Decimal(qty)) for price, qty in data['bids']]
            asks = [(Decimal(price), Decimal(qty)) for price, qty in data['asks']]
            
            return {'bids': bids, 'asks': asks}
            
        except Exception as e:
            logger.error(f"Erro ao obter order book de {symbol}: {e}")
            return {'bids': [], 'asks': []}
    
    # ========================================
    # ITradingRepository Implementation
    # ========================================
    
    async def place_order(self, order: Order) -> Order:
        """Coloca ordem no mercado"""
        try:
            params = {
                'symbol': order.symbol,
                'side': order.side.value,
                'type': order.order_type.value,
                'quantity': str(order.quantity)
            }
            
            if order.price:
                params['price'] = str(order.price)
            if order.stop_price:
                params['stopPrice'] = str(order.stop_price)
            if order.time_in_force:
                params['timeInForce'] = order.time_in_force
            if order.client_order_id:
                params['newClientOrderId'] = order.client_order_id
            
            data = await self._make_request('POST', '/api/v3/order', params, signed=True)
            
            # Atualiza ordem com dados da resposta
            order.order_id = str(data['orderId'])
            order.client_order_id = data.get('clientOrderId')
            order.status = OrderStatus(data['status'])
            order.executed_qty = Decimal(data['executedQty'])
            order.created_at = datetime.fromtimestamp(data['transactTime'] / 1000)
            
            if 'fills' in data:
                executed_value = sum(Decimal(fill['price']) * Decimal(fill['qty']) for fill in data['fills'])
                order.executed_value = executed_value
            
            logger.info(f"Ordem colocada: {order.order_id} - {order.symbol} {order.side.value}")
            return order
            
        except Exception as e:
            logger.error(f"Erro ao colocar ordem: {e}")
            raise
    
    async def cancel_order(self, symbol: str, order_id: str) -> bool:
        """Cancela ordem"""
        try:
            params = {'symbol': symbol, 'orderId': order_id}
            await self._make_request('DELETE', '/api/v3/order', params, signed=True)
            
            logger.info(f"Ordem cancelada: {order_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao cancelar ordem {order_id}: {e}")
            return False
    
    async def get_order_status(self, symbol: str, order_id: str) -> Optional[Order]:
        """Obtém status de ordem"""
        try:
            params = {'symbol': symbol, 'orderId': order_id}
            data = await self._make_request('GET', '/api/v3/order', params, signed=True)
            
            order = Order(
                symbol=data['symbol'],
                side=OrderSide(data['side']),
                order_type=OrderType(data['type']),
                quantity=Decimal(data['origQty']),
                price=Decimal(data['price']) if data['price'] != '0.00000000' else None,
                order_id=str(data['orderId']),
                client_order_id=data.get('clientOrderId'),
                status=OrderStatus(data['status']),
                executed_qty=Decimal(data['executedQty']),
                time_in_force=data.get('timeInForce'),
                created_at=datetime.fromtimestamp(data['time'] / 1000),
                updated_at=datetime.fromtimestamp(data['updateTime'] / 1000)
            )
            
            return order
            
        except Exception as e:
            logger.error(f"Erro ao obter status da ordem {order_id}: {e}")
            return None
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Obtém ordens abertas"""
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            
            data = await self._make_request('GET', '/api/v3/openOrders', params, signed=True)
            
            orders = []
            for order_data in data:
                order = Order(
                    symbol=order_data['symbol'],
                    side=OrderSide(order_data['side']),
                    order_type=OrderType(order_data['type']),
                    quantity=Decimal(order_data['origQty']),
                    price=Decimal(order_data['price']) if order_data['price'] != '0.00000000' else None,
                    order_id=str(order_data['orderId']),
                    client_order_id=order_data.get('clientOrderId'),
                    status=OrderStatus(order_data['status']),
                    executed_qty=Decimal(order_data['executedQty']),
                    time_in_force=order_data.get('timeInForce'),
                    created_at=datetime.fromtimestamp(order_data['time'] / 1000),
                    updated_at=datetime.fromtimestamp(order_data['updateTime'] / 1000)
                )
                orders.append(order)
            
            return orders
            
        except Exception as e:
            logger.error(f"Erro ao obter ordens abertas: {e}")
            return []
    
    async def get_order_history(
        self,
        symbol: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Order]:
        """Obtém histórico de ordens"""
        try:
            params = {'symbol': symbol}
            if start_time:
                params['startTime'] = int(start_time.timestamp() * 1000)
            if end_time:
                params['endTime'] = int(end_time.timestamp() * 1000)
            
            data = await self._make_request('GET', '/api/v3/allOrders', params, signed=True)
            
            orders = []
            for order_data in data[-100:]:  # Últimas 100 ordens
                order = Order(
                    symbol=order_data['symbol'],
                    side=OrderSide(order_data['side']),
                    order_type=OrderType(order_data['type']),
                    quantity=Decimal(order_data['origQty']),
                    price=Decimal(order_data['price']) if order_data['price'] != '0.00000000' else None,
                    order_id=str(order_data['orderId']),
                    client_order_id=order_data.get('clientOrderId'),
                    status=OrderStatus(order_data['status']),
                    executed_qty=Decimal(order_data['executedQty']),
                    time_in_force=order_data.get('timeInForce'),
                    created_at=datetime.fromtimestamp(order_data['time'] / 1000),
                    updated_at=datetime.fromtimestamp(order_data['updateTime'] / 1000)
                )
                orders.append(order)
            
            return orders
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico de ordens de {symbol}: {e}")
            return []
    
    # ========================================
    # IPortfolioRepository Implementation
    # ========================================
    
    async def get_account_balance(self) -> Dict[str, Decimal]:
        """Obtém saldo da conta"""
        try:
            data = await self._make_request('GET', '/api/v3/account', {}, signed=True)
            
            balances = {}
            for balance in data['balances']:
                asset = balance['asset']
                free = Decimal(balance['free'])
                locked = Decimal(balance['locked'])
                total = free + locked
                
                if total > 0:  # Apenas assets com saldo
                    balances[asset] = {
                        'free': free,
                        'locked': locked,
                        'total': total
                    }
            
            return balances
            
        except Exception as e:
            logger.error(f"Erro ao obter saldo da conta: {e}")
            return {}
    
    async def get_positions(self) -> List[Position]:
        """Obtém posições atuais (simuladas baseadas em trades)"""
        # Nota: Binance Spot não tem posições como futures
        # Simula baseado nos saldos
        try:
            balances = await self.get_account_balance()
            positions = []
            
            for asset, balance_info in balances.items():
                if asset != 'USDT' and balance_info['total'] > 0:
                    # Simula posição para assets que não sejam USDT
                    symbol = f"{asset}USDT"
                    current_price = await self.get_current_price(symbol)
                    
                    if current_price:
                        position = Position(
                            symbol=symbol,
                            side=OrderSide.BUY,
                            quantity=balance_info['total'],
                            entry_price=current_price,  # Simplificação
                            current_price=current_price,
                            unrealized_pnl=Decimal('0')  # Requer cálculo mais complexo
                        )
                        positions.append(position)
            
            return positions
            
        except Exception as e:
            logger.error(f"Erro ao obter posições: {e}")
            return []
    
    async def get_position(self, symbol: str) -> Optional[Position]:
        """Obtém posição específica"""
        positions = await self.get_positions()
        return next((pos for pos in positions if pos.symbol == symbol), None)
    
    # ========================================
    # IMarketDataStream Implementation
    # ========================================
    
    async def subscribe_ticker(self, symbol: str) -> AsyncIterator[Dict[str, Decimal]]:
        """Subscribe para dados de ticker"""
        stream = f"{symbol.lower()}@ticker"
        
        async for message in self._ws_stream([stream]):
            if message.get('e') == '24hrTicker':
                yield {
                    'symbol': message['s'],
                    'price': Decimal(message['c']),
                    'price_change': Decimal(message['P']),
                    'volume': Decimal(message['v'])
                }
    
    async def subscribe_candles(self, symbol: str, timeframe: str) -> AsyncIterator[Candle]:
        """Subscribe para candlesticks"""
        stream = f"{symbol.lower()}@kline_{timeframe}"
        
        async for message in self._ws_stream([stream]):
            if message.get('e') == 'kline':
                k = message['k']
                if k['x']:  # Candle fechado
                    candle = Candle(
                        timestamp=datetime.fromtimestamp(k['t'] / 1000),
                        open_price=Decimal(k['o']),
                        high_price=Decimal(k['h']),
                        low_price=Decimal(k['l']),
                        close_price=Decimal(k['c']),
                        volume=Decimal(k['v']),
                        symbol=k['s']
                    )
                    yield candle
    
    async def subscribe_order_book(self, symbol: str) -> AsyncIterator[Dict]:
        """Subscribe para order book"""
        stream = f"{symbol.lower()}@depth"
        
        async for message in self._ws_stream([stream]):
            if 'b' in message and 'a' in message:
                yield {
                    'symbol': symbol,
                    'bids': [(Decimal(price), Decimal(qty)) for price, qty in message['b']],
                    'asks': [(Decimal(price), Decimal(qty)) for price, qty in message['a']]
                }
    
    async def _ws_stream(self, streams: List[str]) -> AsyncIterator[Dict]:
        """Stream genérico do WebSocket"""
        url = f"{self.ws_url}/{'/'.join(streams)}"
        
        try:
            session = aiohttp.ClientSession()
            async with session.ws_connect(url) as ws:
                self.ws_connection = ws
                
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        try:
                            data = json.loads(msg.data)
                            yield data
                        except json.JSONDecodeError:
                            continue
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f'WebSocket error: {ws.exception()}')
                        break
                        
        except Exception as e:
            logger.error(f"Erro no WebSocket: {e}")
        finally:
            await session.close()
    
    async def unsubscribe_all(self) -> None:
        """Remove todos os subscribes"""
        if self.ws_connection and not self.ws_connection.closed:
            await self.ws_connection.close()
    
    async def close(self):
        """Fecha conexões"""
        if self.session and not self.session.closed:
            await self.session.close()
        
        if self.ws_connection and not self.ws_connection.closed:
            await self.ws_connection.close()