import scipy.stats as stats
import numpy as np
import enum
from datetime import datetime

class optionType(enum.Enum):
    call = 1
    put = 2

class Option:
    #0.0158
    def __init__(self, Date=None, Strike=None, Type=optionType.call):
        self.date = Date
        self.strike = Strike
        self.type = Type

    def call_price(self, S, K, T, r, sigma):
        # S: spot price
        # K: strike price
        # T: time to maturity
        # r: interest rate
        # sigma: volatility of underlying asset

        #print("S: {}".format(S))
        #print("K: {}".format(K))
        #print("T: {}".format(T))
        #print("r: {}".format(r))
        #print("Sigma: {}".format(sigma))

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        call = (S * stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))

        return call
