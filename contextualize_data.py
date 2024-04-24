import json
from datetime import datetime
import pandas as pd
import os
import time
from collections import defaultdict
import warnings

from tqdm import tqdm

# Ignore FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

with open("stock_list.txt", "r") as r:
    stocks = r.read().split()

spy = pd.read_csv("sp500_df.csv", index_col="Date", parse_dates=True)

features = [  # income statement
    'date', 'symbol', 'stock_price', 'stock_change', 'sp500_price', 'sp500_change',
    'revenue', 'costOfRevenue', 'grossProfit', 'grossProfitRatio', 'researchAndDevelopmentExpenses',
    'generalAndAdministrativeExpenses', 'sellingAndMarketingExpenses',
    'sellingGeneralAndAdministrativeExpenses', 'otherExpenses', 'operatingExpenses', 'costAndExpenses',
    'interestIncome', 'interestExpense', 'depreciationAndAmortization', 'ebitda', 'ebitdaratio',
    'operatingIncome', 'operatingIncomeRatio', 'totalOtherIncomeExpensesNet', 'incomeBeforeTax',
    'incomeBeforeTaxRatio', 'incomeTaxExpense', 'netIncome', 'netIncomeRatio', 'eps', 'epsdiluted',
    'weightedAverageShsOut', 'weightedAverageShsOutDil',

    # cash-flow-statement
    'cashAndCashEquivalents', 'shortTermInvestments', 'cashAndShortTermInvestments', 'netReceivables',
    'inventory', 'otherCurrentAssets', 'totalCurrentAssets', 'propertyPlantEquipmentNet', 'goodwill',
    'intangibleAssets', 'goodwillAndIntangibleAssets', 'longTermInvestments', 'taxAssets',
    'otherNonCurrentAssets', 'totalNonCurrentAssets', 'otherAssets', 'totalAssets', 'accountPayables',
    'shortTermDebt', 'taxPayables', 'deferredRevenue', 'otherCurrentLiabilities', 'totalCurrentLiabilities',
    'longTermDebt', 'deferredRevenueNonCurrent', 'deferredTaxLiabilitiesNonCurrent',
    'otherNonCurrentLiabilities', 'totalNonCurrentLiabilities', 'otherLiabilities', 'capitalLeaseObligations',
    'totalLiabilities', 'preferredStock', 'commonStock', 'retainedEarnings',
    'accumulatedOtherComprehensiveIncomeLoss', 'othertotalStockholdersEquity', 'totalStockholdersEquity',
    'totalEquity', 'totalLiabilitiesAndStockholdersEquity', 'minorityInterest',
    'totalLiabilitiesAndTotalEquity', 'totalInvestments', 'totalDebt', 'netDebt',

    # balance-sheet-statement
    'netIncome', 'depreciationAndAmortization', 'deferredIncomeTax', 'stockBasedCompensation',
    'changeInWorkingCapital', 'accountsReceivables', 'inventory', 'accountsPayables', 'otherWorkingCapital',
    'otherNonCashItems', 'netCashProvidedByOperatingActivities', 'investmentsInPropertyPlantAndEquipment',
    'acquisitionsNet', 'purchasesOfInvestments', 'salesMaturitiesOfInvestments', 'otherInvestingActivites',
    'netCashUsedForInvestingActivites', 'debtRepayment', 'commonStockIssued', 'commonStockRepurchased',
    'dividendsPaid', 'otherFinancingActivites', 'netCashUsedProvidedByFinancingActivities',
    'effectOfForexChangesOnCash', 'netChangeInCash', 'cashAtEndOfPeriod', 'cashAtBeginningOfPeriod',
    'operatingCashFlow', 'capitalExpenditure', 'freeCashFlow'

]
features1 = ['date', 'symbol', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'period',
             'revenue', 'costOfRevenue', 'grossProfit', 'grossProfitRatio', 'researchAndDevelopmentExpenses',
             'generalAndAdministrativeExpenses', 'sellingAndMarketingExpenses',
             'sellingGeneralAndAdministrativeExpenses', 'otherExpenses', 'operatingExpenses', 'costAndExpenses',
             'interestIncome', 'interestExpense', 'depreciationAndAmortization', 'ebitda', 'ebitdaratio',
             'operatingIncome', 'operatingIncomeRatio', 'totalOtherIncomeExpensesNet', 'incomeBeforeTax',
             'incomeBeforeTaxRatio', 'incomeTaxExpense', 'netIncome', 'netIncomeRatio', 'eps', 'epsdiluted',
             'weightedAverageShsOut', 'weightedAverageShsOutDil', 'link', 'finalLink']
features2 = ['date', 'symbol', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'period',
             'cashAndCashEquivalents', 'shortTermInvestments', 'cashAndShortTermInvestments', 'netReceivables',
             'inventory', 'otherCurrentAssets', 'totalCurrentAssets', 'propertyPlantEquipmentNet', 'goodwill',
             'intangibleAssets', 'goodwillAndIntangibleAssets', 'longTermInvestments', 'taxAssets',
             'otherNonCurrentAssets', 'totalNonCurrentAssets', 'otherAssets', 'totalAssets', 'accountPayables',
             'shortTermDebt', 'taxPayables', 'deferredRevenue', 'otherCurrentLiabilities', 'totalCurrentLiabilities',
             'longTermDebt', 'deferredRevenueNonCurrent', 'deferredTaxLiabilitiesNonCurrent',
             'otherNonCurrentLiabilities', 'totalNonCurrentLiabilities', 'otherLiabilities', 'capitalLeaseObligations',
             'totalLiabilities', 'preferredStock', 'commonStock', 'retainedEarnings',
             'accumulatedOtherComprehensiveIncomeLoss', 'othertotalStockholdersEquity', 'totalStockholdersEquity',
             'totalEquity', 'totalLiabilitiesAndStockholdersEquity', 'minorityInterest',
             'totalLiabilitiesAndTotalEquity', 'totalInvestments', 'totalDebt', 'netDebt', 'link', 'finalLink']
features3 = ['date', 'symbol', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'period',
             'netIncome', 'depreciationAndAmortization', 'deferredIncomeTax', 'stockBasedCompensation',
             'changeInWorkingCapital', 'accountsReceivables', 'inventory', 'accountsPayables', 'otherWorkingCapital',
             'otherNonCashItems', 'netCashProvidedByOperatingActivities', 'investmentsInPropertyPlantAndEquipment',
             'acquisitionsNet', 'purchasesOfInvestments', 'salesMaturitiesOfInvestments', 'otherInvestingActivites',
             'netCashUsedForInvestingActivites', 'debtRepayment', 'commonStockIssued', 'commonStockRepurchased',
             'dividendsPaid', 'otherFinancingActivites', 'netCashUsedProvidedByFinancingActivities',
             'effectOfForexChangesOnCash', 'netChangeInCash', 'cashAtEndOfPeriod', 'cashAtBeginningOfPeriod',
             'operatingCashFlow', 'capitalExpenditure', 'freeCashFlow', 'link', 'finalLink']

statements = ["income-statement", "balance-sheet-statement", "cash-flow-statement"]

# You can add certain parameters that you would like to delete from the data
remove = [
    'generalAndAdministrativeExpenses', 'sellingAndMarketingExpenses',
    'goodwill', 'intangibleAssets', 'goodwillAndIntangibleAssets',
    'otherAssets', 'taxPayables',
    'otherLiabilities', 'capitalLeaseObligations',
    'othertotalStockholdersEquity', 'minorityInterest',
    'effectOfForexChangesOnCash'
]

df_dic = {
    "income-statement": features1,
    "balance-sheet-statement": features2,
    "cash-flow-statement": features3
}

"""
This method will try to put all the relative data into one csv file for python to analyze later.
Obviously, there will be some data that maybe irrelevant to our own choosing so please configure them in the features
strings above this comment.
"""


def removing_parameter():
    for x in remove:
        for features_list in [features, features1, features2, features3]:
            if x in features_list:
                features_list.remove(x)


def add_data(tickers, timely="annual"):
    final_result = pd.DataFrame()

    removing_parameter()

    for stock in tqdm(tickers, desc="Contextualizing", unit="stock"):
        temp = defaultdict(list)

        stock_df = pd.read_csv(f"Historic_Prices/{stock}.csv", index_col="Date", parse_dates=True)

        for statement in statements:
            point = df_dic.get(statement)
            """
            Change the annual to quarter if you want to compare it with quarterly data.
            """
            folder_path = f"Financial_Data/{timely}/{statement}"
            file_name = f"{stock}.json"
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r") as ff:
                ft = json.load(ff)

            # Getting all the relevant data from our downloaded /Financial_Data into one csv file
            for x in range(1, len(ft)):
                values = []
                if statement == "income-statement":
                    for key in point[:2] + [0, 0, 0, 0] + df_dic.get(statement)[8:len(point) - 2]:
                        values.append(ft[x].get(key))
                else:
                    for key in df_dic.get(statement)[8:len(point) - 2]:
                        values.append(ft[x].get(key))

                temp[x].extend(values)

        val_ls = [v for v in temp.values()]
        val_ls.reverse()

        # Parsing all the prices and its changes in each stock and the S&P 500
        for x in range(0, len(val_ls)):
            try:
                time_obj = datetime.strptime(val_ls[x][0], "%Y-%m-%d")
                unix_time = time.mktime(time_obj.timetuple())
            except TypeError:
                continue
            current_date = datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d")
            time_pass = 31536000
            if timely == "quarter":
                time_pass /= 4

            one_year_later = datetime.fromtimestamp(unix_time + time_pass).strftime(
                "%Y-%m-%d"
            )


            try:
                sp500_price = (float(spy.loc[current_date, "Adj Close"]))
                stock_price = (float(stock_df.loc[current_date, "Adj Close"]))

                sp500_1y_price = float(spy.loc[one_year_later, "Adj Close"])
                stock_1y_price = float(stock_df.loc[one_year_later, "Adj Close"])
            except KeyError:
                continue

            sp500_p_change = round(
                ((sp500_1y_price - sp500_price) / sp500_price * 100), 2
            )
            stock_p_change = round(
                ((stock_1y_price - stock_price) / stock_price * 100), 2
            )

            additive = [
                stock_price,
                stock_p_change,
                sp500_price,
                sp500_p_change
            ]

            val_ls[x] = val_ls[x][:2] + additive + val_ls[x][6:]
        for row in val_ls:
            temp_df = pd.DataFrame([row])
            final_result = pd.concat([final_result, temp_df], ignore_index=True)

    final_result.columns = features
    # final_result.fillna(0, inplace=True)
    final_result.dropna(axis=0, subset=["stock_price", "stock_change"], inplace=True)
    final_result.to_csv("fin_data.csv", index=False)


"""
testing is for obviously testing purpose
This function tests only two stocks: MSFT and AAPL
"""


def testing():
    tickers = ["MSFT", "AAPL"]

    add_data(tickers)


if __name__ == "__main__":
    add_data(stocks, "quarter")
    # testing()
