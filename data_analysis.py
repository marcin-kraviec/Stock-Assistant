import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from datetime import date

data = yf.Ticker('TSLA')
price = data.history(period='1y')
'''
In order to calculate the daily returns, we will use the pct_change() function, 
which calculates the percentage change between the current element and a prior one.
Daily returns
'''
x = price['Close'].pct_change()
#x.plot()
'''
After understanding how the returns are distributed, we can calculate the returns from an investment.
For that, we need to calculate the cumulative returns, which can be done using the cumprod() function:
'''
returns = (x + 1).cumprod()
#returns.plot() # The plot shows how a $1 investment would grow.

data = yf.download('AAPL MSFT TSLA', start='2021-01-01')
x = data['Close'].pct_change()
#The code above gets the stock prices for the given stocks and applies to pct_change() function to the Close price

print(x.describe())
#Descriptive statistics include the mean, standard deviation, min, max values, as well as the 25/50/75th% percentiles.

#data['Close'].plot() # Nice idea to plot multiple stocks
x = data['Close'].pct_change()
#x.plot()
#(x + 1).cumprod().plot() # Very nice

corr = x.corr()
print(corr)
#In finance, correlation is a statistic that measures the degree to which two securities move in relation to each other.

#sm.graphics.plot_corr(corr, xnames=list(x.columns)) #SUPER !! - MATRIX OD CORRELATION
'''
The corr() function results in a matrix that includes values for each stock pair.
The values are in the range of -1 to 1.

A positive correlation means that the stocks have returns that are positively correlated and move in the same direction.
+1 means that the returns are perfectly correlated.

A correlation of 0 shows no relationship between the pair.
A negative correlation shows that the returns move in different directions.
'''

stocks = ['AAPL', 'AMZN', 'MSFT', 'TSLA']
weights = [0.3, 0.2, 0.4, 0.1]

data = yf.download(stocks, start='2021-01-01')
x = data['Close'].pct_change()

#portfolio return
ret = (x * weights).sum(axis=1)
cumulative = (ret + 1).cumprod()
#cumulative.plot()


'''
Volatility is also often used to measure risk. If a stock is very volatile, you can expect large changes in its price and therefore a higher risk.
Volatility is calculated using the standard deviation of the portfolio return.
We can also calculate the annual volatility by taking the square root of the number of trading days in a year (252) and multiply it by the daily volatility:
'''
print(np.std(ret))
annual_std = np.std(ret) * np.sqrt(252) #This will return the risk % of our portfolio.
print(annual_std)

'''
Sharpe ratio is the measure of the risk-adjusted return of a portfolio. A portfolio with a higher Sharpe ratio is considered better.
To calculate the Sharpe ratio, we need to take the average return and divide it by the volatility.
'''
sharpe = (np.mean(ret)/np.std(ret)) * np.sqrt(252) #Sharpe ratios greater than 1 are considered optimal.
print('Sharpe: %f' % sharpe)


'''
Portfolio optimization is the technique of allocating assets so that it has the maximum return and minimum risk.
This can be done by finding the allocation that results in the maximum Sharpe ratio.

The simplest way to find the best allocation is to check many random allocations and find the one that has the best Sharpe ratio.
This process of randomly guessing is known as a Monte Carlo Simulation (randomise weights).
'''

stocks = ['AAPL', 'AMZN', 'MSFT', 'TSLA']
data = yf.download(stocks, start='2021-01-01')

data = data['Close']
x = data.pct_change()

p_weights = []
p_returns = []
p_risk = []
p_sharpe = []
'''
We are going to randomly assign a weight to each stock in our portfolio, and then calculate the metrics for that portfolio, including the Sharpe ratio.
We divide the resulting weights by their sum to normalize them, so that the sum of the random weights is always 1.
'''

wts = np.random.uniform(size = len(x.columns))
wts - wts/np.sum(wts)

count = 500
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

'''    
The for loop runs 500 times. During each iteration we calculate the metrics and store them in the corresponding lists using the append() function.
We used 500 to optimize the time to run the code in our Playground. In other scenarios, you could generate thousands of portfolios, to get a better result.
'''

max_ind = np.argmax(p_sharpe)
print('Max sharpe ratio: ')
print(p_sharpe[max_ind])
print(p_weights[max_ind])

s = pd.Series(p_weights[max_ind], index=x.columns)
#s.plot(kind='bar') # this plots weights

'''
We found the best portfolio weights!
As a last step, let's plot all the 500 portfolios.
The chart is called Efficient Frontier and shows the returns on the Y-axis and volatility on the X-axis.

We can create the chart using the scatter() function, providing the volatility and return lists as parameters:
'''

plt.scatter(p_risk, p_returns, c=p_sharpe, cmap='plasma')
plt.colorbar(label='Sharpe Ratio')

plt.scatter(p_risk[max_ind], p_returns[max_ind],color='r', marker='*', s=500)

'''
The Efficient Frontier chart shows the return we can get for the given volatility, or, the volatility that we get for a certain return.
'''

plt.show()

print(type(str(date.today())))