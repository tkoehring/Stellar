from Stock import Stock
from Option import Option, optionType
from datetime import datetime, timedelta
import numpy as np
import math
import time
import pandas as pd
from matplotlib import pyplot as plt



def main():
        name = "MSFT"
        date = "2020-05-14"
        strike = float(220.0)
        data = Stock(name)
        call = data.getCall_StrikePrice(date, strike)
        myOpt = Option(datetime.strptime(date, "%Y-%m-%d"), strike, optionType.call)

        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        T = abs((myOpt.date - today).days)

        print(T)
        for i in range(80):
                p = myOpt.call_price(data.getCurrentPrice(), strike, T, 0.0158, data.annual_log_std_dev())
                print(p)
                T -= 1

        '''
        df = data.tick.history(period="1mo", interval="5m")
        df.drop(columns=['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], inplace=True)
        means = df['Close']
        MA_Range = [5, 10, 20, 50]
        for i in MA_Range:
                df['MA{}'.format(i)] = means.rolling(window=i).mean().round(2)
        df.dropna()
        df2 = df.tail(144)
        df2.to_csv("test.csv")
        df2.reset_index(inplace = True)
        print(df2.keys())
        df2.drop(columns=['Datetime'], inplace=True)
        print(df2.keys())
        plot = df2.plot()
        plot.figure.savefig('test.png')
        '''
if __name__== "__main__":
        main()