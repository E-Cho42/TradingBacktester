# Moving Average Crossover Backtest

This Python script backtests a simple moving average crossover strategy using historical NVIDIA (NVDA) stock data from Yahoo Finance. It simulates trades, tracks profit, and visualizes buy/sell signals on a price chart.

## Features
- Fetches real stock data with yfinance
- Calculates short-term and long-term simple moving averages (SMA)
- Generates buy and sell signals when SMAs cross
- Simulates portfolio performance starting with $10,000
- Plots closing prices with visual buy/sell markers

## Requirements
Install dependencies with:
```bash
pip install yfinance pandas matplotlib
```

## Usage
Run the script:
```bash
python moving_average_backtest.py
```

You can modify:
- `ticker` → stock symbol (default: "NVDA")
- `short_w` and `long_w` → SMA window sizes
- `start_date` and `end_date` → backtest period

## How It Works
- Buy when the short-term SMA crosses above the long-term SMA
- Sell when it crosses below
- Tracks your cash and shares through time and reports profit/loss

## Output
- Console output showing final portfolio and profit
- A plotted chart of price history with buy/sell markers