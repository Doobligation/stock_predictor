import os
import json
import math

import pandas as pd

"""
This python file is for filtering certain stocks that you may not want to
add in the database. For example, we may find that certain stocks doesn't
qualify to be fit as value stocks.
"""

# Directory files for you to access and control
balance_sheet = f"Financial_Data/annual/balance-sheet-statement"  # check shareholders' equity
income_statement = f"Financial_Data/annual/income-statement"  # check eps, shares outstanding
cash_flow = f"Financial_data/annual/cash_flow_statement"

historic_prices = f"Historic_Prices/"

fin_df = pd.read_csv("fin_data.csv")  # To access fin_data.csv
cur_df = pd.read_csv("current_data.csv")  # To access current_data.csv


# For easy access of file path and its json files
def return_files(stock):
    file_name = f"{stock}.json"
    balance = os.path.join(balance_sheet, file_name)
    income = os.path.join(income_statement, file_name)
    cash = os.path.join(cash_flow, file_name)

    return balance, income, cash


# This function is to check for Graham Number. This has been set as an example to what to expect from this file.
def check_graham_number(stock, x):
    # balance, income, cash = return_files(stock)
    global fin_df, cur_df

    location = fin_df[fin_df['symbol'] == stock]

    eps = location['eps'].values[x]
    shares_outstanding = location['weightedAverageShsOut'].values[x]
    equity = location['totalStockholdersEquity'].values[x]

    graham_number = math.sqrt(22.5 * eps * equity / shares_outstanding)
    stock_price = location['stock_price'].values[x]

    print(graham_number)
    print(stock_price)

    if graham_number < stock_price:
        fin_df = fin_df.drop(location.index)
        cur_df = cur_df.drop(location.index)


if __name__ == "__main__":
    check_graham_number("AAPL", -1)
