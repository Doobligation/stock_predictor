import yfinance as yf
from tqdm import tqdm
import os

START_DATE = "2002-01-01"
END_DATE = "2024-04-12"

# Getting All The Adjacent Closing Price for All the stocks from Yahoo Finance
def get_stock_prices():
    with open("stock_list.txt") as l:
        stocks = l.read().split("\n")

    folder_path = "Historic_Prices"

    # Create the directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    os.chdir(folder_path)

    for stock in tqdm(stocks, desc='Downloading', unit='stock'):
        yf.download(stock, start=START_DATE, end=END_DATE, rounding=False, timeout=2, progress=False).to_csv(f"{stock}.csv")

# If for some reason you couldn't download a specific stock info, please use this line below
# yf.download("stock", start=START_DATE, end=END_DATE, rounding=False).to_csv("stock.csv")

# Getting SPY data to compare the perfomance of each stock
def get_SPY():
    yf.download("SPY", start=START_DATE, end=END_DATE, rounding=False).to_csv("SPY.csv")

if __name__ == "__main__":
    get_stock_prices()
    get_SPY()


