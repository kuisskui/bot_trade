import MetaTrader5 as mt5


def initialize_mt5(account_id, password, server):
    if not mt5.initialize(login=account_id, password=password, server=server):
        print(f"Failed to connect to MetaTrader 5, error: {mt5.last_error()}")
        return False
    return True


def place_trade(symbol, volume, trade_type):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found")
        return

    if trade_type == "buy":
        order_type = mt5.ORDER_TYPE_BUY
    elif trade_type == "sell":
        order_type = mt5.ORDER_TYPE_SELL
    else:
        print("Invalid trade type")
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 20,
        "magic": 234000,
        "comment": "Python script trade",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till cancel order
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Trade failed, error: {result.retcode}")
    else:
        print(f"Trade placed successfully: {result}")


def shutdown_mt5():
    mt5.shutdown()
