import yfinance as yf
import math
import numpy as np

''' Calls DataFrame Types
contractSymbol               object
lastTradeDate        datetime64[ns]
strike                      float64
lastPrice                   float64
bid                         float64
ask                         float64
change                      float64
percentChange               float64
volume                        int64
openInterest                  int64
impliedVolatility           float64
inTheMoney                     bool
contractSize                 object
currency                     object
'''

class Stock:
        def __init__(self, name=None):
                self.name = name
                self.tick = yf.Ticker(name)

        def getAvailableDates(self):
                self.tick._download_options(proxy=None)
                dates = self.tick._expirations.keys()
                return dates

        def getCurrentPrice(self):
                df = self.tick.history(period="5m", interval="1m")
                return df['Close'][-1]

        def getAllCalls(self):
                self.tick._download_options(proxy=None)
                dates = self.tick._expirations.keys()
                options = []
                for date in dates:
                        options.append(self.tick.option_chain(date))
                        print(options[-1].calls)

        def getCall_Date(self, date):
                option_chain = self.tick.option_chain(date)
                return option_chain.calls

        def getCall_StrikePrice(self, date, val):
                option_chain = self.tick.option_chain(date)
                return option_chain.calls.loc[option_chain.calls['strike']==val]

        def annual_std_dev(self):
                data = self.tick.history(period="1y", interval="1d")['Close'].to_numpy()
                sum = 0
                returns = np.empty((data.shape[0] - 1,))
                for i in range(1, data.shape[0]):
                        returns[i - 1] = (data[i] - data[i - 1]) / data[i - 1]

                mean = np.mean(returns)

                sum = np.sum(np.power(returns - mean, 2)) / returns.shape[0]

                return math.sqrt(sum) * math.sqrt(data.shape[0] - 1)

        def annual_log_std_dev(self):
                data = self.tick.history(period="1y", interval="1d")['Close'].to_numpy()
                sum = 0
                returns = np.empty((data.shape[0] - 1,))
                for i in range(1, data.shape[0]):
                        returns[i - 1] = math.log(data[i] / data[i - 1])

                mean = np.mean(returns)

                sum = np.sum(np.power(returns - mean, 2)) / returns.shape[0]

                return math.sqrt(sum) * math.sqrt(data.shape[0] - 1)
