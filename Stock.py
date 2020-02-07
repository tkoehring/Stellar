import yfinance as yf

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

class Ticker:
        def __init__(self, name=None):
                self.name = name
                self.tick = yf.Ticker(name)

        def getAvailableDates(self):
                self.tick._download_options(proxy=None)
                dates = self.tick._expirations.keys()
                for date in dates:
                        print(date)

        def getAllCalls(self):
                self.tick._download_options(proxy=None)
                dates = self.tick._expirations.keys()
                options = []
                for date in dates:
                        options.append(self.tick.option_chain(date))
                        print(options[-1].calls)

        def getCall(self, date, val):
                option = self.tick.option_chain(date)
                print(option.calls.loc[option.calls['strike']==val])