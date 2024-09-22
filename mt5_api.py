from MetaTrader5 import *
import pandas as pd
from MetaTrader5._core import *


def check_initialization():
    if not initialize():
        raise Exception(f"Failed to check initialization: {last_error()}")
    return True


def check_symbol(symbol):
    # Ensure the symbol is visible in the Market Watch
    symbol = symbol_info(symbol)
    if not symbol.visible:
        if not symbol_select(symbol, True):
            raise Exception(f"Failed to check symbol: {symbol}")

    return True


def place_trade(symbol, volume, trade_type, sl=0.0, tp=0.0, deviation=20, magic=234000, comment="Python trade script"):
    check_initialization()
    check_symbol(symbol)

    if trade_type == "buy":
        order_type = ORDER_TYPE_BUY
    elif trade_type == "sell":
        order_type = ORDER_TYPE_SELL
    else:
        raise Exception(f"Invalid trade type. Use 'buy' or 'sell'.: {trade_type}")

    request = {
        "action": TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": ORDER_TIME_GTC,
        "type_filling": ORDER_FILLING_IOC,
    }

    order_send(request)

    return True


def get_moving_average(symbol, timeframe, period, shift=0):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period + shift)

    if rates is None or len(rates) == 0:
        raise Exception(f"Failed to copy rates from {symbol}")

    data = pd.DataFrame(rates)

    data['time'] = pd.to_datetime(data['time'], unit='s')
    ma = data['close'].rolling(window=period).mean().iloc[-1 - shift]
    return ma


def close_all_orders():
    check_initialization()

    positions = positions_get()

    if positions is None or len(positions) == 0:
        for position in positions:
            print(f"Closing position: {position.ticket}, {position.symbol}, {position.volume} lots")
            close_order(position)
        return True
    print("No open positions found")


def close_order(position):
    symbol = position.symbol
    volume = position.volume
    position_type = position.type
    ticket = position.ticket

    # Get the latest price data for the symbol
    symbol_info = symbol_info(symbol)
    if symbol_info is None:
        print(f"Failed to get symbol info for {symbol}")
        return

    # Ensure the symbol is selected
    if not symbol_info.visible:
        if not symbol_select(symbol, True):
            print(f"Failed to select symbol {symbol}")
            return

    # Get the current price to close the order
    if position_type == POSITION_TYPE_BUY:
        price = symbol_info_tick(symbol).bid  # Close buy at the bid price
        order_type = ORDER_TYPE_SELL  # Closing a buy order requires a sell
    elif position_type == POSITION_TYPE_SELL:
        price = symbol_info_tick(symbol).ask  # Close sell at the ask price
        order_type = ORDER_TYPE_BUY  # Closing a sell order requires a buy
    else:
        print(f"Unknown position type for {ticket}")
        return

    # Prepare the close request
    request = {
        "action": TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,  # Position ticket
        "price": price,
        "deviation": 20,
        "magic": 234000,  # Arbitrary identifier for the trade
        "comment": "Python script close order",
        "type_time": ORDER_TIME_GTC,  # Good till canceled
        "type_filling": ORDER_FILLING_IOC,  # Immediate or cancel
    }

    # Send the close order request
    result = order_send(request)
    if result.retcode != TRADE_RETCODE_DONE:
        print(f"Failed to close order {ticket}, error: {result.retcode}, description: {last_error()}")
    else:
        print(f"Order {ticket} closed successfully")


def get_active_positions(symbol):
    check_initialization()
    positions = positions_get(symbol=symbol)

    if positions is None or len(positions) == 0:
        print(f"No active positions found for symbol {symbol}")
    else:
        for position in positions:
            print(
                f"Position ticket: {position.ticket}, "
                f"Symbol: {position.symbol}, "
                f"Volume: {position.volume}, "
                f"Type: {'Buy' if position.type == 0 else 'Sell'}"
            )
    return positions

