import pandas as pd
import PythonMetaTrader5 as mt
from MetaTrader5 import *


def initialize():
    if mt.initialize():
        return True

    raise Exception(f"Failed to check initialization: {last_error()}")


def shutdown():
    mt.shutdown()


def last_error():
    return mt.last_error()


def login(login, password, server):
    if mt.login(login, password, server):
        return True

    raise Exception(f"Failed to login {login}: {last_error()}")


def symbol_info(symbol):
    if not mt.symbol_select(symbol, True):
        raise Exception(f"Failed to select {symbol}: {last_error()}")

    info = mt.symbol_info(symbol)
    if not info:
        raise Exception(f"Failed to select {symbol}: {last_error()}")

    return info


def buy(symbol, volume):
    order = mt.Buy(symbol, volume)
    if not order:
        raise Exception(f"Failed to buy {symbol}: {last_error()}")

    if order.retcode == mt.TRADE_RETCODE_DONE:
        return order

    raise Exception(f"Failed to buy {symbol}: {order}: {last_error()}")


def sell(symbol, volume):
    order = mt.Sell(symbol, volume)
    if not order:
        raise Exception(f"Failed to sell {symbol}: {last_error()}")

    if order.retcode == mt.TRADE_RETCODE_DONE:
        return order

    raise Exception(f"Failed to sell {symbol}: {order}: {last_error()}")


def order_send(request):
    result = mt.order_send(request)

    if not result:
        raise Exception(f"Failed to send order {request}: {last_error()}")

    if result.retcode == mt.TRADE_RETCODE_DONE:
        return result

    raise Exception(f"Failed to send order {request}: {last_error()}: {result}")


def copy_rates_from_pos(symbol, timeframe, shift, period):
    rates = mt.copy_rates_from_pos(symbol, timeframe, shift, period)
    if not rates:
        raise Exception(f"Failed to copy rates from {symbol}: {last_error()}")

    return rates


def positions_get(**kwargs):
    positions = mt.positions_get(**kwargs)
    if not positions:
        return tuple()
    return positions


def place_trade(symbol, volume, trade_type, sl=0.0, tp=0.0, deviation=20, magic=234000, comment="Python trade script"):
    if trade_type == "buy":
        order_type = mt.ORDER_TYPE_BUY
    elif trade_type == "sell":
        order_type = mt.ORDER_TYPE_SELL
    elif trade_type == mt.ORDER_TYPE_BUY or trade_type == mt.ORDER_TYPE_SELL:
        order_type = trade_type
    else:
        raise Exception(f"Invalid trade type. Use 'buy' or 'sell'.: {trade_type}")

    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": mt.symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }

    return order_send(request)


def get_moving_average(symbol, timeframe, period, shift=0):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period + shift)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    ma = data['close'].rolling(window=period).mean().iloc[-1 - shift]
    return ma


def close_all_orders():
    positions = positions_get()

    for position in positions:
        close_order(position)


def close_order(position):
    symbol = position.symbol
    volume = position.volume
    position_type = position.type
    ticket = position.ticket

    # Get the current price to close the order
    if position_type == mt.POSITION_TYPE_BUY:
        price = mt.symbol_info_tick(symbol).bid  # Close buy at the bid price
        order_type = mt.ORDER_TYPE_SELL  # Closing a buy order requires a sell
    elif position_type == mt.POSITION_TYPE_SELL:
        price = mt.symbol_info_tick(symbol).ask  # Close sell at the ask price
        order_type = mt.ORDER_TYPE_BUY  # Closing a sell order requires a buy
    else:
        raise Exception(f"Invalid position type. : {position_type}")

    # Prepare the close request
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,  # Position ticket
        "price": price,
        "deviation": 20,
        "magic": 234000,  # Arbitrary identifier for the trade
        "comment": "Python script close order",
        "type_time": mt.ORDER_TIME_GTC,  # Good till canceled
        "type_filling": mt.ORDER_FILLING_IOC,  # Immediate or cancel
    }

    # Send the close order request
    return order_send(request)
