import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import date


class DataAnalysis():

    @staticmethod
    def sharpe_ratio(stocks, values):
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
        pairs = corr.abs().unstack().sort_values(kind='quicksort').drop_duplicates()

        #drop self correlation
        pairs = pairs.drop(pairs.idxmax())

        dict = {pairs.idxmax(): pairs.max(), pairs.idxmin(): pairs.min()}

        return corr, dict

    @staticmethod
    def volatility(stocks, values):
        weights = []
        for value in values:
            weights.append(value / sum(values))

        data = yf.download(stocks, start='2021-01-01')
        x = data['Close'].pct_change()
        dates = data['Date']

        ret = (x * weights).sum(axis=1)
        vol = np.std(ret)
        annual_std = vol * np.sqrt(252)
        return annual_std

    @staticmethod
    def cumulative_returns(stocks, values):
        weights = []
        for value in values:
            weights.append(value / sum(values))

        data = yf.download(stocks, start='2021-01-01', interval="1d")
        data.reset_index(inplace=True)
        x = data['Close'].pct_change()
        dates = data['Date']

        # portfolio return
        ret = (x * weights).sum(axis=1)
        cumulative = (ret + 1).cumprod()
        return cumulative, dates