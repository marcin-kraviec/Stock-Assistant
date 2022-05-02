import pandas as pd
import yfinance as yf
import numpy as np


# class with static calculations methods
class DataAnalysis:

    @staticmethod
    def sharpe_ratio(stocks, values):

        # calculate stocks weights based on their value
        weights = []
        for value in values:
            weights.append(value/sum(values))

        # downloading data of stock from yfinance
        data = yf.download(stocks, start='2021-01-01')
        data.reset_index(inplace=True)

        # calculate percentage change
        x = data['Close'].pct_change()

        # calculate returns based on the calculated weights
        ret = (x * weights).sum(axis=1)

        # calculate sharpe ratio
        sharpe = (np.mean(ret) / np.std(ret)) * np.sqrt(252)

        return sharpe

    @staticmethod
    def correlation(stocks):

        # downloading data of stock from yfinance
        data = yf.download(stocks, start='2021-01-01')
        data.reset_index(inplace=True)

        # calculate percentage change
        x = data['Close'].pct_change()

        # calculate correlation
        corr = x.corr()

        # drop repetitions
        pairs = corr.abs().unstack().sort_values(kind='quicksort').drop_duplicates()

        # drop self correlation
        pairs = pairs.drop(pairs.idxmax())

        # provide max and min correlation
        dict = {pairs.idxmax(): pairs.max(), pairs.idxmin(): pairs.min()}

        return corr, dict

    @staticmethod
    def volatility(stocks, values):

        # calculate stocks weights based on their value
        weights = []
        for value in values:
            weights.append(value / sum(values))

        # downloading data of stock from yfinance
        data = yf.download(stocks, start='2021-01-01')
        data.reset_index(inplace=True)

        # calculate percentage change
        x = data['Close'].pct_change()

        # calculate returns based on the calculated weights
        ret = (x * weights).sum(axis=1)

        # calculated daily volatility as std
        vol = np.std(ret)

        # calculated annual volatility as std multiplied ny number of trading days
        annual_std = vol * np.sqrt(252)

        return annual_std, vol

    @staticmethod
    def cumulative_returns(stocks, values, date):

        # calculate stocks weights based on their value
        weights = []
        for value in values:
            weights.append(value / sum(values))

        # downloading data of stock from yfinance
        data = yf.download(stocks, start=date, interval='1d')
        data.reset_index(inplace=True)

        # calculate percentage change
        x = data['Close'].pct_change()

        # get dataframe indexes
        dates = data['Date']

        # calculate returns based on the calculated weights
        ret = (x * weights).sum(axis=1)

        # calculate cumulative returns
        cumulative = (ret + 1).cumprod()

        # create pandas Series with dates as indexes and cumulative returns as values
        output = pd.Series(list(cumulative.values), index=dates)

        return output

    @staticmethod
    def optimise(stocks, values):

        # calculate stocks weights based on their value for our portfolio
        current_weights = []
        for value in values:
            current_weights.append(value / sum(values))

        p_weights = []
        p_returns = []
        p_risk = []
        p_sharpe = []

        p_weights.append(current_weights)

        # downloading data of stock from yfinance
        data = yf.download(stocks, start='2021-01-01', interval='1d')
        data.reset_index(inplace=True)

        x = data['Close'].pct_change()

        # use monte carlo method to find weights that provide best sharpe ratio
        COUNT = 1000
        for k in range(0, COUNT):

            # calculate mean returns multiplied by number of trading days
            mean_returns = (x.mean() * p_weights[k]).sum() * 252
            p_returns.append(mean_returns)

            # calculate random stocks weights that sum up to 1
            weights = np.random.uniform(size=len(x.columns))
            weights = weights / np.sum(weights)
            p_weights.append(weights)

            # calculate annual volatility
            ret = (x * p_weights[k]).sum(axis=1)
            annual_std = np.std(ret) * np.sqrt(252)
            p_risk.append(annual_std)

            # calculate sharpe ratio
            sharpe = (np.mean(ret) / np.std(ret)) * np.sqrt(252)
            p_sharpe.append(sharpe)

        # get the best sharpe ratio
        max_ind = np.argmax(p_sharpe)

        return p_risk, p_returns, p_sharpe, p_weights, max_ind

    '''
    We found the best portfolio weights!
    As a last step, let's plot all the 500 portfolios.
    The chart is called Efficient Frontier and shows the returns on the Y-axis and volatility on the X-axis.
    '''

    @staticmethod
    def rsi(df, period=13):

        # calculate net change
        net_change = df['Close'].diff()

        #TODO: Finish comments explanation
        increase = net_change.clip(lower=0)
        decrease = -1 * net_change.clip(upper=0)
        ema_up = increase.ewm(com=period, adjust=False).mean()
        ema_down = decrease.ewm(com=period, adjust=False).mean()
        RS = ema_up / ema_down

        # calculate RSI and add a new column to df
        df['RSI'] = 100 - (100 / (1 + RS))

        return df






