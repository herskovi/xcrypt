import hashlib

import datetime
import time
import requests
import json

from Ticker import Ticker


class CexioClient(object):

    def getTickerLiveData(self,ticker="BTC/USD"):

        exchange = {'exchange': 'CEXIO'}

        #trading_client = bitstamp.client.Trading()
        #print(trading_client.account_balance()['fee'])
        #bc = bitstamp.BaseClient()
        #for x in range(0, 5):
        #print datetime.datetime.now()
        # json_data = public_client.ticker(base=ticker)
        # return json_data
        #time.sleep(5)
        url = "https://cex.io/api/ticker/" + ticker
        username = 'up110426782'
        key = 'c0Ky7Sw2ZRPVmYQDmsxdkk1KC4Q'
        secret = 'S5H5U3WQIKpASd24banLkl0aM8'
        nonce = int(time.time())
        userID = username
        api_key = key
        API_SECRET = secret
        #message = nonce + userID + api_key
        myResponse = requests.get(url)

        # For successful API call, response code will be 200 (OK)
        if (myResponse.ok):

            # Loading the response data into a dict variable
            # json.loads takes in only binary or string variables so using content to fetch binary content
            # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)

            jData = json.loads(myResponse.text)
            jData.update(exchange)
            self.prepareResponse(jData)
            #return self.ticker
            return jData

        else:
            # If response code is not ok (200), print the resulting http error code with description
            myResponse.raise_for_status()

        #signature = hmac.new(API_SECRET, msg=message, digestmod=hashlib.sha256).hexdigest().upper()

    def prepareResponse(self, data):

        volume = data["volume"]
        timestamp = data["timestamp"]
        last = data["last"]
        low = data["low"]
        high = data["high"]
        bid = data["bid"]
        ask = data["ask"]
        self.ticker = Ticker("CexIo", volume, last,bid, "", high, low, ask)
        print volume
        print timestamp
        print last
        print low
        print high
        print bid
        print ask

    def main(args):
       pass

if __name__ == "__main__":
    json_data = CexioClient().getTickerLiveData("BTC/USD")
    print json_data
















