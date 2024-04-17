import pandas as pd

# Download the recent S&P 500 stocks from here:
# https://topforeignstocks.com/wp-content/uploads/2024/04/Complete-List-of-SP-500-Index-Constituents-Apr-3-2024.csv

# Read the CSV file and extract the 'Ticker' column
ls = pd.read_csv("stock_list.csv", usecols=["Ticker"])

# Convert the 'Ticker' column to a string, remove extra whitespace
ticker_str = ls.to_string(index=False, header=False).strip()

# Split the string by newline character to get individual ticker symbols
ticker_symbols = ticker_str.split()
ticker_symbols_sorted = sorted(ticker_symbols)

# Write the ticker symbols to a text file, each on a separate line
with open("stock_list.txt", 'w') as kongs:
    for ticker in ticker_symbols_sorted:
        kongs.write(ticker + '\n')

