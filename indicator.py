from mt5_api import *


def get_moving_average(symbol, timeframe, shift=0, period=14):
    rates = copy_rates_from_pos(symbol, timeframe, shift, period)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
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
