import MetaTrader5 as mt5
import pandas as pd

# Connect to MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5")
    quit()

# Define symbol and parameters
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_H1  # 1-hour timeframe
ma_period = 14  # Period for MA14

# Ensure the symbol is available in the market watch
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select symbol {symbol}")
    mt5.shutdown()
    quit()

# Retrieve historical price data (e.g., last 100 candles)
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)

# Check if rates were retrieved successfully
if rates is None:
    print("Failed to retrieve rates")
    mt5.shutdown()
    quit()

# Convert the data to a Pandas DataFrame for easier manipulation
data = pd.DataFrame(rates)

# Convert the time in seconds to a datetime format for better readability
data['time'] = pd.to_datetime(data['time'], unit='s')

# Calculate MA14 using Pandas rolling mean
data['MA14'] = data['close'].rolling(window=ma_period).mean()

# Print the most recent MA14 value
print(f"Most recent MA14 value: {data['MA14'].iloc[-1]}")

# Shutdown MetaTrader 5 connection
mt5.shutdown()
