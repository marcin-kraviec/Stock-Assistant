import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import date


class DataAnalysis:

    @staticmethod
    def sharpe_ratio(stocks, values):
        weights = []
        for value in values:
            weights.append(value/sum(values))

        data = yf.download(stocks, start='2021-01-01')
        data.reset_index(inplace=True)
        x = data['Close'].pct_change()
        ret = (x * weights).sum(axis=1)
        sharpe = (np.mean(ret) / np.std(ret)) * np.sqrt(252)
        return sharpe

    @staticmethod
    def correlation(stocks):
        data = yf.download(stocks, start='2021-01-01')
        data.reset_index(inplace=True)
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
        data.reset_index(inplace=True)
        x = data['Close'].pct_change()

        ret = (x * weights).sum(axis=1)
        vol = np.std(ret)
        annual_std = vol * np.sqrt(252)
        return annual_std, vol

    @staticmethod
    def cumulative_returns(stocks, values):
        weights = []
        for value in values:
            weights.append(value / sum(values))

        data = yf.download(stocks, start='2021-01-01', interval='1d')
        data.reset_index(inplace=True)
        x = data['Close'].pct_change()
        dates = data['Date']

        # portfolio return
        ret = (x * weights).sum(axis=1)
        cumulative = (ret + 1).cumprod()
        return cumulative, dates

    @staticmethod
    def optimise(stocks, values):

        p_weights = []
        p_returns = []
        p_risk = []
        p_sharpe = []

        for value in values:
            p_weights.append(value / sum(values))

        data = yf.download(stocks, start='2021-01-01', interval='1d')
        data.reset_index(inplace=True)

        x = data['Close'].pct_change()

        wts = np.random.uniform(size=len(x.columns))
        wts - wts / np.sum(wts)

        count = 1000
        for k in range(0, count):
            wts = np.random.uniform(size=len(x.columns))
            wts = wts / np.sum(wts)
            p_weights.append(wts)

            # returns
            mean_ret = (x.mean() * wts).sum() * 252
            p_returns.append(mean_ret)

            # volatility
            ret = (x * wts).sum(axis=1)
            annual_std = np.std(ret) * np.sqrt(252)
            p_risk.append(annual_std)

            # Sharpe ratio
            sharpe = (np.mean(ret) / np.std(ret)) * np.sqrt(252)
            p_sharpe.append(sharpe)

        max_ind = np.argmax(p_sharpe)
        #print('Max sharpe ratio: ')
        #print(p_sharpe[max_ind])
        #print(p_weights[max_ind])
        return p_risk, p_returns, p_sharpe, p_weights, max_ind

        # s = pd.Series(p_weights[max_ind], index=x.columns)
        # s.plot(kind='bar') # this plots weights

        '''
        We found the best portfolio weights!
        As a last step, let's plot all the 500 portfolios.
        The chart is called Efficient Frontier and shows the returns on the Y-axis and volatility on the X-axis.

        We can create the chart using the scatter() function, providing the volatility and return lists as parameters:
        

        plt.scatter(p_risk, p_returns, c=p_sharpe, cmap='plasma')
        plt.colorbar(label='Sharpe Ratio')

        plt.scatter(p_risk[max_ind], p_returns[max_ind],color='r', marker='*', s=500)
        '''



