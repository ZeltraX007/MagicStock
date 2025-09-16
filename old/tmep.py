import pandas as pd

# URL for the official NSE stock list
nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

# Read CSV file directly from NSE website
df = pd.read_csv(nse_url)

# Extract stock symbols
stock_symbols = [symbol + ".NS" for symbol in df["SYMBOL"].tolist()]

print(stock_symbols)  # Print first 10 stocks as an example
