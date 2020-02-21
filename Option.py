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

    def call_price(self, S, K, T, r, d, sigma):
        # S: spot price
        # K: strike price
        # T: time to maturity
        # r: interest rate
        # sigma: volatility of underlying asset
        T /= 252
        sigma=0.223

        print("S: {}".format(S))
        print("K: {}".format(K))
        print("T: {}".format(T))
        print("r: {}".format(r))
        print("d: {}".format(d))
        print("Sigma: {}".format(sigma))
        #sigma = 0.22
        d1 = (np.log(S / K) + (r + d + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call = (S * stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))

        print("Delta: {}".format(stats.norm.cdf(d1, 0.0, 1.0)))
        print("Vega: {}".format(S*stats.norm.pdf(d1) * np.sqrt(T)))
        return call
