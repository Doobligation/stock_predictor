import os
import time
from tqdm import tqdm
import requests
import SECRET
import json

"""
We are going to use API from financialmodelingprep.com
Get the free API Key from them! Now, you still have to pay for quarterly announcements
If this is a problem, we will get them from yfinance again.
"""

# stocks = ["AAPL", "MSFT"] # testing purpose
days = ["annual"]
#"quarter",
statements = ["income-statement"]
#, "balance-sheet-statement", "cash-flow-statement"


def make_folders():
    for day in days:
        for statement in statements:
            os.makedirs(f"Financial_Data/{day}/{statement}", exist_ok=True)


def get_financial_data():
    with open("stock_list.txt", "r") as f1:
        stocks = f1.read().split()

    for stock in tqdm(stocks, desc='Downloading', unit='stock'):
        for day in days:
            for statement in statements:
                response = requests.get(
                    f"https://financialmodelingprep.com/api/v3/{statement}/{stock}?period={day}&apikey={SECRET.YOUR_API_KEY}")
                folder_path = f"Financial_Data/{day}/{statement}"
                filename = os.path.join(folder_path, f"{stock}.json")

                with open(filename, "w") as f2:
                    json.dump(response.json(), f2, indent=4)

                time.sleep(2)

                # Figuring out where it went wrong!
                # print(day, statement, stock)


def testing():
    response2 = requests.get("https://api.artic.edu/api/v1/artworks/129884")

    folder_path = "Financial_Data/quarter/income-statement"

    filename = os.path.join(folder_path, "test.json")

    with open(filename, "w") as f:
        json.dump(response2.json(), f, indent=4)


if __name__ == "__main__":
    make_folders()
    get_financial_data()
    # testing()
