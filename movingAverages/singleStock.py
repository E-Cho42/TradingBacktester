# Imports
import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt

# Define ticker and date range
ticker = "FDX" #<------ Ticker 
start_date = "2010-01-01"
end_date = "2025-9-22"

# Download data
df = yf.download(ticker, start_date, end_date)

# --------------------------------- Begin define trading logic ------------------------------------- #
# Define moving average window sizes
short_w = 20
long_w = 50

# Calculate the moving averages
df["SMA_short"] = df["Close"].rolling(short_w).mean()
df["SMA_long"] = df["Close"].rolling(long_w).mean()


# Create a signal
df['Signal'] = 0  # initialize the column

# Create trading logic()
df['Signal'] = 0
df['Signal'] = (df['SMA_short'] > df['SMA_long']).astype(int)

# New column that tracks the **change** in signal (difference between today and yesterday)
df['Position'] = df['Signal'].diff()

# Create the position column (buy/sell signal)
df['Position'] = df['Signal'].diff()

# --------------------------------- End define trading logic ------------------------------------- #
#intializes cash
initial_cash = 100  # starting money
cash = initial_cash
shares = 0
portfolio_values = []

for i in range(1, len(df)):
    if df['Position'].iloc[i] == 1.0:
        price = df['Close'][ticker].iloc[i]  
        amount_of_shares = cash / price
        cash = 0 
        portfolio_values.append([ticker, amount_of_shares])
    if df['Position'].iloc[i] == -1.0:
        price = df['Close'][ticker].iloc[i] 
        amount_made = portfolio_values[0][1] * price
        cash += amount_made
        portfolio_values.pop()

last_price = df['Close'][ticker].iloc[-1]
print("Cash: " +str(cash))
print("Portfolio: "+ str(portfolio_values))
print("Amount started with: "+ str(initial_cash))
try:
    print("Profit made if you sold: " + str((portfolio_values[0][1]* last_price) - initial_cash))
except:
    print("Profit made: " + str(cash-initial_cash))

# --------------------------------- Begin Graphing ------------------------------------- #
# Plot the closing prices
plt.figure(figsize=(14,7))
plt.plot(df.index, df['Close'], label='Close Price', alpha=0.7)

# Mark buy signals
buy_signals = df[df['Position'] == 1.0]
plt.scatter(buy_signals.index, df.loc[buy_signals.index, 'Close'], marker='^', color='g', label='Buy', s=100)

# Mark sell signals
sell_signals = df[df['Position'] == -1.0]
plt.scatter(sell_signals.index, df.loc[sell_signals.index, 'Close'], marker='v', color='r', label='Sell', s=100)

plt.title(f"{ticker} Price with Buy and Sell Signals")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.show()

    




