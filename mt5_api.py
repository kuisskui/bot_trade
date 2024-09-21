import MetaTrader5 as mt5
import pandas as pd


def initialize_mt5(account_id, password, server):
    if mt5.initialize(login=account_id, password=password, server=server):
        return True
    return False


def shutdown_mt5():
    mt5.shutdown()


def check_initialize_mt5():
    if not mt5.initialize():
        print(f"Failed to initialize MetaTrader 5: {mt5.last_error()}")
        return False
    return True


def place_trade(symbol, volume, trade_type):
    if not check_initialize_mt5():
        return
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found")
        return

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select symbol {symbol}")
            return

    if trade_type == "buy":
        order_type = mt5.ORDER_TYPE_BUY
    elif trade_type == "sell":
        order_type = mt5.ORDER_TYPE_SELL
    else:
        print("Invalid trade type. Use 'buy' or 'sell'.")
        return

    deviation = 20

    request = {
        "action": mt5.TRADE_ACTION_DEAL,  # Market order
        "symbol": symbol,  # Trading symbol (EURUSD)
        "volume": volume,  # Volume in lots (e.g., 0.01)
        "type": order_type,  # Buy or Sell
        "price": mt5.symbol_info_tick(symbol).ask,  # Execution price (ask for buy, bid for sell)
        "sl": 0.0,  # Stop Loss (100 points below/above the entry price)
        "tp": 0.0,  # Take Profit (100 points above/below the entry price)
        "deviation": deviation,  # Maximum price deviation allowed
        "magic": 234000,  # Unique identifier for the trade
        "comment": "Python script trade",  # Optional comment for the trade
        "type_time": mt5.ORDER_TIME_GTC,  # Good Till Canceled (order stays open until filled or manually closed)
        "type_filling": mt5.ORDER_FILLING_IOC,  # Immediate or Cancel filling policy
    }

    # Send the trade request
    result = mt5.order_send(request)
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Trade failed, error: {result.retcode}, description: {mt5.last_error()}")
    else:
        print(f"Trade placed successfully: {result}")


def iMA(symbol, timeframe, period, shift=0):
    # Connect to MetaTrader 5 if not already connected
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5")
        return None

    # Ensure the symbol is available in the market watch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select symbol {symbol}")
        mt5.shutdown()
        return None

    # Get the required amount of historical data (at least `period + shift` candles)
    rates = mt5.copy_rates_from_pos(symbol, timeframe, shift, period + shift)

    # Check if rates were retrieved successfully
    if rates is None or len(rates) == 0:
        print(f"Failed to retrieve rates for {symbol}")
        mt5.shutdown()
        return None

    # Convert the data to a Pandas DataFrame for easier manipulation
    data = pd.DataFrame(rates)

    # Convert the time in seconds to a datetime format
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate the Simple Moving Average (SMA) on the closing price
    ma = data['close'].rolling(window=period).mean().iloc[-1 - shift]

    # Shutdown the connection
    mt5.shutdown()

    return ma


def close_all_orders():
    # Initialize MetaTrader 5 connection
    if not mt5.initialize():
        print(f"Failed to initialize MetaTrader 5: {mt5.last_error()}")
        return

    # Get all open positions
    positions = mt5.positions_get()

    if positions is None or len(positions) == 0:
        print("No open positions found")
        mt5.shutdown()
        return

    # Close each position
    for position in positions:
        print(f"Closing position: {position.ticket}, {position.symbol}, {position.volume} lots")
        close_order(position)

    # Shutdown MetaTrader 5 connection
    mt5.shutdown()


def close_order(position):
    symbol = position.symbol
    volume = position.volume
    position_type = position.type
    ticket = position.ticket

    # Get the latest price data for the symbol
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Failed to get symbol info for {symbol}")
        return

    # Ensure the symbol is selected
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select symbol {symbol}")
            return

    # Get the current price to close the order
    if position_type == mt5.POSITION_TYPE_BUY:
        price = mt5.symbol_info_tick(symbol).bid  # Close buy at the bid price
        order_type = mt5.ORDER_TYPE_SELL  # Closing a buy order requires a sell
    elif position_type == mt5.POSITION_TYPE_SELL:
        price = mt5.symbol_info_tick(symbol).ask  # Close sell at the ask price
        order_type = mt5.ORDER_TYPE_BUY  # Closing a sell order requires a buy
    else:
        print(f"Unknown position type for {ticket}")
        return

    # Prepare the close request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,  # Position ticket
        "price": price,
        "deviation": 20,
        "magic": 234000,  # Arbitrary identifier for the trade
        "comment": "Python script close order",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,  # Immediate or cancel
    }

    # Send the close order request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to close order {ticket}, error: {result.retcode}, description: {mt5.last_error()}")
    else:
        print(f"Order {ticket} closed successfully")


def orders_get(symbol=None):
    if not check_initialize_mt5():
        return

    # Retrieve pending orders for the symbol
    order = mt5.orders_get(symbol=symbol)

    if order is None:
        print(f"No pending orders found for symbol {symbol}")
    else:
        print(f"Pending orders for {symbol}: {order}")

    return order


def get_active_positions(symbol=None):
    if not check_initialize_mt5():
        return

    # Retrieve active buy/sell positions for the symbol
    positions = mt5.positions_get(symbol=symbol)

    if positions is None or len(positions) == 0:
        print(f"No active positions found for symbol {symbol}")
    else:
        for position in positions:
            print(
                f"Position ticket: {position.ticket}, Symbol: {position.symbol}, Volume: {position.volume}, Type: {'Buy' if position.type == 0 else 'Sell'}")

    return positions


def close_position(position):
    symbol = position.symbol
    volume = position.volume
    position_type = position.type
    ticket = position.ticket

    # Get the latest price data for the symbol
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Failed to get symbol info for {symbol}")
        return

    # Ensure the symbol is selected
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select symbol {symbol}")
            return

    # Get the current price to close the order
    if position_type == mt5.POSITION_TYPE_BUY:
        price = mt5.symbol_info_tick(symbol).bid  # Close buy at the bid price
        order_type = mt5.ORDER_TYPE_SELL  # To close a buy order, we send a sell order
    elif position_type == mt5.POSITION_TYPE_SELL:
        price = mt5.symbol_info_tick(symbol).ask  # Close sell at the ask price
        order_type = mt5.ORDER_TYPE_BUY  # To close a sell order, we send a buy order
    else:
        print(f"Unknown position type for {ticket}")
        return

    # Prepare the close request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,  # Close the full volume
        "type": order_type,  # Opposite order to close the position
        "position": ticket,  # Ticket number of the position to close
        "price": price,
        "deviation": 20,
        "magic": 234000,  # Arbitrary identifier for the trade
        "comment": "Python script close order",
        "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,  # Immediate or cancel
    }

    # Send the close order request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Failed to close position {ticket}, error: {result.retcode}, description: {mt5.last_error()}")
    else:
        print(f"Position {ticket} closed successfully")
