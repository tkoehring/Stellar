from Stock import Ticker

def main():
        name = "MSFT"
        date = "2020-05-14"
        strike = float(220.0)
        data = Ticker(name)
        data.getCall(date, strike)

if __name__== "__main__":
        main()