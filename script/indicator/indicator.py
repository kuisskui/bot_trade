from api.mt5_api import *

import pandas as pd


def get_moving_average(symbol, timeframe, shift, period):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period)

    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    ma = data['close'].rolling(window=period).mean().iloc[-1]

    return ma


def get_exponential_moving_average(symbol, timeframe, shift, period):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period)

    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Calculate EMA using the Pandas ewm() function
    ema = data['close'].ewm(span=period, adjust=False).mean().iloc[-1]

    return ema


def get_relative_strength_index(symbol, timeframe, shift, period):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period)

    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    delta = data['close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    data['rsi'] = 100 - (100 / (1 + rs))

    return data['rsi'].iloc[-1]


def get_bollinger_bands(symbol, timeframe, shift, period, std_dev):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period)

    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    data['sma'] = data['close'].rolling(window=period).mean()
    data['std'] = data['close'].rolling(window=period).std()

    data['upper_band'] = data['sma'] + (data['std'] * std_dev)
    data['lower_band'] = data['sma'] - (data['std'] * std_dev)

    latest_data = data.iloc[-1]
    return latest_data['upper_band'], latest_data['sma'], latest_data['lower_band']


def get_ema(data, period):
    """Helper function to calculate the Exponential Moving Average (EMA)"""
    return data.ewm(span=period, adjust=False).mean()


def get_moving_average_convergence_divergence(symbol, timeframe, shift, short_period=12, long_period=26, signal_period=9):
    rates = copy_rates_from_pos(symbol, timeframe, shift, long_period)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')

    data['short_ema'] = get_ema(data['close'], short_period)
    data['long_ema'] = get_ema(data['close'], long_period)

    data['macd_line'] = data['short_ema'] - data['long_ema']
    data['signal_line'] = get_ema(data['macd_line'], signal_period)

    data['macd_histogram'] = data['macd_line'] - data['signal_line']

    # Return the latest MACD line, Signal line, and MACD histogram values
    latest_data = data.iloc[-1]
    return latest_data['macd_line'], latest_data['signal_line'], latest_data['macd_histogram']
