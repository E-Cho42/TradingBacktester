# Imports
import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt

#User inputs
print("Welcome to Ethan's Trading Backtester. Please input the stock tickers you want to invest in, separated by a comma:")
stockString = input()
stockToInvest = stockString.strip(" ").split(",")
print("Thank you. Could you now input a start and end date, in year-month-date seperated by a comma:")
yearSting = input()
dates = yearSting.strip(" ").split(",")
print(" *********************** Crunching numbers *********************** ")

#class stock
class stock():
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.df = yf.download(ticker, start_date, end_date)
        self.short_w = 10
        self.long_w = 50
        self.profit = 0
    

        # Calculate the moving averages
        self.df["SMA_short"] = self.df["Close"].rolling(self.short_w).mean()
        self.df["SMA_long"] = self.df["Close"].rolling(self.long_w).mean()


        # Create a signal
        self.df['Signal'] = 0  # initialize the column

        # Create trading logic()
        self.df['Signal'] = 0
        self.df['Signal'] = (self.df['SMA_short'] > self.df['SMA_long']).astype(int)

        # New column that tracks the **change** in signal (difference between today and yesterday)
        self.df['Position'] = self.df['Signal'].diff()

        # Create the position column (buy/sell signal)
        self.df['Position'] = self.df['Signal'].diff()
        
    def backtest(self):
        initial_cash = 10000  # starting money
        cash = initial_cash
        shares = 0
        portfolio_values = []
        for i in range(1, len(self.df)):
            if self.df['Position'].iloc[i] == 1.0:
                price = self.df['Close'][self.ticker].iloc[i]  
                amount_of_shares = cash / price
                cash = 0 
                portfolio_values.append([self.ticker, amount_of_shares])
            elif self.df['Position'].iloc[i] == -1.0:
                price = self.df['Close'][self.ticker].iloc[i] 
                amount_made = portfolio_values[0][1] * price
                cash += amount_made
                portfolio_values.pop()
        last_price = self.df['Close'][self.ticker].iloc[-1]
        print("Cash: " +str(cash))
        print("Portfolio: "+ str(portfolio_values))
        print("Amount started with: "+ str(initial_cash))
        try:
            print("Profit made if you sold: " + str((portfolio_values[0][1]* last_price) - initial_cash))
            self.profit = (portfolio_values[0][1]* last_price) - initial_cash
        except:
            print("Profit made: " + str(cash-initial_cash))
            self.profit = cash-initial_cash
    def graph(self):
        plt.figure(figsize=(14,7))
        plt.plot(self.df.index, self.df['Close'], label='Close Price', alpha=0.7)

        # Mark buy signals
        buy_signals = self.df[self.df['Position'] == 1.0]
        plt.scatter(buy_signals.index, self.df.loc[buy_signals.index, 'Close'], marker='^', color='g', label='Buy', s=100)

        # Mark sell signals
        sell_signals = self.df[self.df['Position'] == -1.0]
        plt.scatter(sell_signals.index, self.df.loc[sell_signals.index, 'Close'], marker='v', color='r', label='Sell', s=100)

        plt.title(f"{self.ticker} Price with Buy and Sell Signals")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"Charts/{self.ticker} Price with Buy and Sell Signals")
               
print(" *********************** Finished crunching numbers *********************** ")
#creating portfolio 
portfolio = []
for i in stockToInvest:
    portfolio.append(stock(i,dates[0],dates[1]))

profits = []    

for i in portfolio:
    i.backtest()
    i.graph()
    profits.append(float(i.profit))
    