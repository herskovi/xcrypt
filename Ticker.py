import datetime


class Ticker:
    def __init__(self, excange, volume, last,bid, vwap, high, low, ask ):
        self.excahnge = excange
        self.volume = volume
        self.timestamp = datetime.datetime.now()
        self.last = last
        self.bid = bid
        self.vwap = vwap
        self.high = high
        self.low = low
        self.ask = ask





