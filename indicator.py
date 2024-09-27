from mt5_api import *

import MetaTrader5 as mt5
import pandas as pd


def get_moving_average(symbol, timeframe, shift=0, period=14):
    # Fetch historical price data from MetaTrader 5
    rates = copy_rates_from_pos(symbol, timeframe, shift, period + shift)

    # Check if the data is valid
    if rates is None or len(rates) == 0:
        print(f"Failed to retrieve historical data for {symbol}")
        return None

    # Convert rates to a Pandas DataFrame for easier manipulation
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate the moving average on the 'close' prices
    if len(data) < period:
        print(f"Not enough data to calculate the moving average for {symbol}")
        return None

    ma = data['close'].rolling(window=period).mean().iloc[-1 - shift]

    return ma


def get_exponential_moving_average(symbol, timeframe, shift=0, period=14):
    # Fetch historical price data from MetaTrader 5
    rates = copy_rates_from_pos(symbol, timeframe, shift, period + shift)

    # Check if the data is valid
    if rates is None or len(rates) == 0:
        print(f"Failed to retrieve historical data for {symbol}")
        return None

    # Convert rates to a Pandas DataFrame for easier manipulation
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate the exponential moving average (EMA) on the 'close' prices
    if len(data) < period:
        print(f"Not enough data to calculate the moving average for {symbol}")
        return None

    # Calculate EMA using the Pandas ewm() function
    ema = data['close'].ewm(span=period, adjust=False).mean().iloc[-1 - shift]

    return ema


def get_relative_strength_index(symbol, timeframe, shift=0, period=14):
    # Get historical data
    rates = copy_rates_from_pos(symbol, timeframe, shift, period)
    if rates is None or len(rates) == 0:
        print(f"Failed to retrieve historical data for {symbol}")
        return None

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    delta = df['close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    # Calculate the RSI
    df['rsi'] = 100 - (100 / (1 + rs))

    # Return the last RSI value as an integer
    return int(df['rsi'].iloc[-1])


def get_bollinger_bands(symbol, timeframe, period=20, std_dev=2):
    # Get historical rates for the symbol
    rates = copy_rates_from_pos(symbol, timeframe, 0, period + 100)

    # Convert rates to a DataFrame for easier manipulation
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate the Middle Band (SMA)
    data['SMA'] = data['close'].rolling(window=period).mean()

    # Calculate the standard deviation
    data['STD'] = data['close'].rolling(window=period).std()

    # Calculate Upper and Lower Bands
    data['Upper_Band'] = data['SMA'] + (data['STD'] * std_dev)
    data['Lower_Band'] = data['SMA'] - (data['STD'] * std_dev)

    # Return the latest Bollinger Band values
    latest_data = data.iloc[-1]
    return latest_data['Upper_Band'], latest_data['Lower_Band'], latest_data['SMA']


def get_ema(data, period):
    """Helper function to calculate the Exponential Moving Average (EMA)"""
    return data.ewm(span=period, adjust=False).mean()


def get_macd(symbol, timeframe, short_period=12, long_period=26, signal_period=9):
    # Fetch historical data for the symbol
    rates = copy_rates_from_pos(symbol, timeframe, 0, long_period + signal_period + 100)
    # Convert the historical data into a Pandas DataFrame
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate the short-term EMA (12 periods) and long-term EMA (26 periods)
    data['EMA_12'] = get_ema(data['close'], short_period)
    data['EMA_26'] = get_ema(data['close'], long_period)

    # Calculate the MACD line (EMA_12 - EMA_26)
    data['MACD_Line'] = data['EMA_12'] - data['EMA_26']

    # Calculate the Signal Line (9-period EMA of MACD Line)
    data['Signal_Line'] = get_ema(data['MACD_Line'], signal_period)

    # Calculate the MACD Histogram (MACD Line - Signal Line)
    data['MACD_Histogram'] = data['MACD_Line'] - data['Signal_Line']

    # Return the latest MACD line, Signal line, and MACD histogram values
    latest_data = data.iloc[-1]
    return latest_data['MACD_Line'], latest_data['Signal_Line'], latest_data['MACD_Histogram']
