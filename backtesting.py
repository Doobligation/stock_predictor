# Data Processing
import pandas as pd
import numpy as np

# Modelling
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.svm import SVC
from scipy.stats import randint
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, QuantileTransformer, RobustScaler, MaxAbsScaler

from pmdarima import auto_arima

OUTPERFORMANCE = 20


def outperform(stock_change, sp500_change, outperform):
    return stock_change - sp500_change >= outperform


stock_df = pd.read_csv("fin_data.csv", index_col='date', parse_dates=True)
stock_df.dropna(axis=0, how="any", inplace=True)


# Tree
def backtest():
    features = stock_df.columns[6:]
    X = stock_df[features].values
    y = list(
        outperform(
            stock_df["stock_change"], stock_df["sp500_change"], 10
        )
    )

    z = np.array(stock_df[["stock_change", "sp500_change"]])

    X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(X, y, z, test_size=0.3)

    """
    I have added 3 algorithms below: SVC, RandomForestClassifier, and GradientBoostingClassifier
    Of course, it's up to you to control the parameters.
    """

    # clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    # clf.fit(X_train, y_train)
    #
    # clf = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=250, random_state=0, max_depth=100))
    # clf.fit(X_train, y_train)

    clf = make_pipeline(StandardScaler(), GradientBoostingClassifier(n_estimators=250, max_depth=5))
    clf.fit(X_train, y_train)

    print("Classifier performance\n")
    print(f"Accuracy score: {accuracy_score(X_test, y_test): .2f}")

    y_pred = clf.predict(X_test)

    print(sum(y_pred))


    if sum(y_pred) == 0:
        print("No stocks predicted!")

    else:
        invest_list = z[y_pred].tolist()
        print(
            f"{len(invest_list)} stocks predicted to outperform the S&P500 by more than {OUTPERFORMANCE}%:"
        )
        print(" ".join(invest_list))
        return invest_list


# def testing():

backtest()
# testing()
