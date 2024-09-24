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

    return 100 - (100 / (1 + rs))
