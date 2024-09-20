import MetaTrader5 as mt5


def initialize_mt5(account_id, password, server):
    if not mt5.initialize(login=account_id, password=password, server=server):
        print(f"Failed to connect to MetaTrader 5, error: {mt5.last_error()}")
        return False
    return True


def place_trade(symbol, volume, trade_type):
    # Ensure the symbol is available
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found")
        return

    # Ensure the symbol is visible in the Market Watch
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select symbol {symbol}")
            return

    # Get the current price (ask for buy, bid for sell)
    tick = mt5.symbol_info_tick(symbol)

    # Set up the order type and price based on buy or sell
    if trade_type == "buy":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask  # Buy at the ask price
    elif trade_type == "sell":
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid  # Sell at the bid price
    else:
        print("Invalid trade type. Use 'buy' or 'sell'.")
        return

    # Calculate Stop Loss and Take Profit based on current price and point value
    point = symbol_info.point
    sl = price - 100 * point if trade_type == "buy" else price + 100 * point  # 100 points stop loss
    tp = price + 100 * point if trade_type == "buy" else price - 100 * point  # 100 points take profit

    # Set the allowed slippage (in points)
    deviation = 50  # Allow up to 20 points of slippage

    # Ensure the volume is within the broker's limits
    if volume < symbol_info.volume_min or volume > symbol_info.volume_max or volume % symbol_info.volume_step != 0:
        print(
            f"Invalid volume {volume}. Must be between {symbol_info.volume_min} and {symbol_info.volume_max}, in steps of {symbol_info.volume_step}.")
        return

    # Create the trade request dictionary
    request = {
        "action": mt5.TRADE_ACTION_DEAL,  # Market order
        "symbol": symbol,  # Trading symbol (EURUSD)
        "volume": volume,  # Volume in lots (e.g., 0.01)
        "type": order_type,  # Buy or Sell
        "price": price,  # Execution price (ask for buy, bid for sell)
        "sl": sl,  # Stop Loss (100 points below/above the entry price)
        "tp": tp,  # Take Profit (100 points above/below the entry price)
        "deviation": deviation,  # Maximum price deviation allowed
        "magic": 234000,  # Unique identifier for the trade
        "comment": "Python script trade",  # Optional comment for the trade
        "type_time": mt5.ORDER_TIME_GTC,  # Good Till Canceled (order stays open until filled or manually closed)
        "type_filling": mt5.ORDER_FILLING_IOC,  # Immediate or Cancel filling policy
    }

    # Send the trade request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Trade failed, error: {result.retcode}, description: {mt5.last_error()}")
    else:
        print(f"Trade placed successfully: {result}")


def shutdown_mt5():
    mt5.shutdown()
