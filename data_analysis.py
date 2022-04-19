import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import date


class DataAnalysis():

    @staticmethod
    def sharpe_ratio(stocks, values):
        #function takes lists as inputs
        weights = []
        for value in values:
            weights.append(value/sum(values))

        data = yf.download(stocks, start='2021-01-01')
        x = data['Close'].pct_change()
        ret = (x * weights).sum(axis=1)
        sharpe = (np.mean(ret) / np.std(ret)) * np.sqrt(252)
        return sharpe

    @staticmethod
    def correlation(stocks):
        data = yf.download(stocks, start='2021-01-01')
        x = data['Close'].pct_change()
        corr = x.corr()
        return(corr)