import pandas as pd
import PythonMetaTrader5 as mt
from MetaTrader5 import *
import numpy as np


def initialize():
    if mt.initialize():
        return True

    raise Exception(f"Failed to check initialization: {last_error()}")


def login(login, password, server):
    if mt.login(login, password, server):
        return True

    raise Exception(f"Failed to login {login}: {last_error()}")


def shutdown():
    mt.shutdown()


def version():
    v = mt.version()
    if v is None:
        raise Exception(f"Failed to get version: {last_error()}")
    return v


def last_error():
    return mt.last_error()


def account_info():
    info = mt.account_info()
    if info is None:
        raise Exception(f"Failed to get account info: {last_error()}")
    return info


def terminal_info():
    info = mt.terminal_info()
    if info is None:
        raise Exception(f"Failed to get terminal info: {last_error()}")
    return info


def symbols_total():
    total = mt.symbols_total()
    if total is None:
        raise Exception(f"Failed to get symbols total: {last_error()}")
    return total


def symbol_info(symbol):
    if not symbol_select(symbol, True):
        raise Exception(f"Failed to select {symbol}: {last_error()}")

    info = mt.symbol_info(symbol)
    if info is None:
        raise Exception(f"Failed to get info {symbol}: {last_error()}")

    return info


def symbol_info_tick(symbol):
    info_tick = mt.symbol_info_tick(symbol)
    if info_tick is None:
        raise Exception(f"Failed to get info tick {symbol}: {last_error()}")

    return info_tick


def symbol_select(symbol, enable=None):
    return mt.symbol_select(symbol, enable)


def copy_rates_from(symbol, timeframe, date_from, count):
    arr = mt.copy_rates_from(symbol, timeframe, date_from, count)
    if arr is None:
        raise Exception(f"Failed to get copy rates from {symbol}: {last_error()}")
    return arr


def copy_rates_from_pos(symbol, timeframe, shift, period):
    arr = mt.copy_rates_from_pos(symbol, timeframe, shift, period)
    if arr is None:
        raise Exception(f"Failed to get copy rates from pos {symbol}: {last_error()}")
    return arr


def copy_rates_range(symbol, timeframe, date_from, date_to):
    arr = mt.copy_rates_range(symbol, timeframe, date_from, date_to)
    if arr is None:
        raise Exception(f"Failed to get copy rates range {symbol}: {last_error()}")
    return arr


def copy_ticks_from(symbol, date_from, count, flags):
    arr = mt.copy_ticks_from(symbol, date_from, count, flags)
    if arr is None:
        raise Exception(f"Failed to get copy ticks from {symbol}: {last_error()}")
    return arr


def copy_ticks_range(symbol, date_from, date_to, flags):
    arr = mt.copy_ticks_range(symbol, date_from, date_to, flags)
    if arr is None:
        raise Exception(f"Failed to get copy ticks range {symbol}: {last_error()}")
    return arr


def orders_total():
    total = mt.orders_total()
    if total is None:
        raise Exception(f"Failed to get orders total: {last_error()}")
    return total


def orders_get(**kwargs):
    order = mt.orders_get(**kwargs)
    if order is None:
        raise Exception(f"Failed to get orders: {last_error()}")
    return order


def order_calc_margin(action, symbol, volume, price):
    margin = mt.order_calc_margin(action, symbol, volume, price)
    if margin is None:
        raise Exception(f"Failed to get order margin: {last_error()}")
    return margin


def order_calc_profit(action, symbol, volume, price_open, price_close):
    profit = mt.order_calc_profit(action, symbol, volume, price_open, price_close)
    if profit is None:
        raise Exception(f"Failed to get order profit: {last_error()}")
    return profit


def order_check(request):
    return mt.order_check(request)


def order_send(request):
    result = mt.order_send(request)

    if result is None:
        raise Exception(f"Failed to send order {request}: {last_error()}")

    if result.retcode == mt.TRADE_RETCODE_DONE:
        return result

    raise Exception(f"Failed to send order {request}: {last_error()}: {result}")


def positions_total():
    total = mt.positions_total()
    if total is None:
        raise Exception(f"Failed to get positions total: {last_error()}")
    return total


def positions_get(**kwargs):
    positions = mt.positions_get(**kwargs)
    if positions is None:
        raise Exception(f"Failed to get positions: {last_error()}")
    return positions


def history_orders_total(date_from, date_to):
    total = mt.history_orders_total(date_from, date_to)
    if total is None:
        raise Exception(f"Failed to get history orders total: {last_error()}")
    return total


def history_orders_get(**kwargs):
    orders = mt.history_orders_get(**kwargs)
    if orders is None:
        raise Exception(f"Failed to get history orders: {last_error()}")
    return orders


def history_deals_total(date_from, date_to):
    total = mt.history_deals_total(date_from, date_to)
    if total is None:
        raise Exception(f"Failed to get history deals total: {last_error()}")
    return total


def history_deals_get(**kwargs):
    orders = mt.history_deals_get(**kwargs)
    if orders is None:
        raise Exception(f"Failed to get history orders: {last_error()}")
    return orders


def buy(symbol, volume):
    order = mt.Buy(symbol, volume)
    if order is None:
        raise Exception(f"Failed to buy {symbol}: {last_error()}")

    if order.retcode == mt.TRADE_RETCODE_DONE:
        return order

    raise Exception(f"Failed to buy {symbol}: {order}: {last_error()}")


def sell(symbol, volume):
    order = mt.Sell(symbol, volume)
    if order is None:
        raise Exception(f"Failed to sell {symbol}: {last_error()}")

    if order.retcode == mt.TRADE_RETCODE_DONE:
        return order

    raise Exception(f"Failed to sell {symbol}: {order}: {last_error()}")


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
        "price": symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }

    return order_send(request)


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
