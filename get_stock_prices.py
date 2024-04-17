import yfinance as yf
from tqdm import tqdm
import os
import pandas as pd

START_DATE = "2002-01-01"
END_DATE = "2024-04-12"


# Getting all the Adjacent Closing Price and other necessary information
# for every stock from Yahoo Finance
def get_stock_prices():
    with open("temp.txt") as l:
        stocks = l.read().split("\n")

    folder_path = "Historic_Prices"

    # Create the directory if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    os.chdir(folder_path)

    for stock in tqdm(stocks, desc='Downloading', unit='stock'):
        yf.download(stock, start=START_DATE, end=END_DATE, rounding=False, timeout=2, progress=False).to_csv(
            f"{stock}.csv")

        """
        Because there are some days that are missing (weekends, holidays, etc.),
        we are going to fill it with previous data. Of course, this is going to
        impact the data in some way. You are more than welcome to change its setting.
        """

        stock_raw = pd.read_csv(f"{stock}.csv", index_col="Date", parse_dates=True)
        start_date = str(stock_raw.index[0])
        end_date = str(stock_raw.index[-1])
        idx = pd.date_range(start_date, end_date)
        stock_raw = stock_raw.reindex(idx)
        stock_raw.ffill(inplace=True)

        stock_raw.to_csv(f"{stock}.csv", index_label="Date")

# If for some reason you couldn't download a specific stock info, please use this line below
# yf.download("stock", start=START_DATE, end=END_DATE, rounding=False).to_csv("stock.csv")
# Getting SPY data to compare the performance of each stock

def get_SPY():
    yf.download("SPY", start=START_DATE, end=END_DATE, rounding=False).to_csv("sp500_df.csv")
    sp500_raw = pd.read_csv("sp500_df.csv", index_col="Date", parse_dates=True)

    # Same situation as get_stock_prices(). Filling in the missing dates.
    start_date = str(sp500_raw.index[0])
    end_date = str(sp500_raw.index[-1])
    idx = pd.date_range(start_date, end_date)
    sp500_raw = sp500_raw.reindex(idx)
    sp500_raw.ffill(inplace=True)

    sp500_raw.to_csv("sp500_df.csv", index_label="Date")


if __name__ == "__main__":
    get_stock_prices()
    get_SPY()
