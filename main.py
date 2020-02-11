from Stock import Ticker
import pandas as pd
from matplotlib import pyplot as plt

def main():
        name = "MSFT"
        date = "2020-05-14"
        strike = float(220.0)
        data = Ticker(name)
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
if __name__== "__main__":
        main()