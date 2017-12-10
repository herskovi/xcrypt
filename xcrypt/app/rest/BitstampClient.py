import bitstamp.client
import datetime
import time

public_client = bitstamp.client.Public()



class BitstampClient:

    def getTickerLiveData(self, ticker):

        trading_client = bitstamp.client.Trading(
        username='tiup1158', key='nMoaHtxxcsIJdT9WSC8lh26kg6jHZskw', secret='dUcAim3leobugXI4I26q6Csko3aVzVfr')
        #print(trading_client.account_balance()['fee'])
        #bc = bitstamp.BaseClient()
        #for x in range(0, 5):
        #print datetime.datetime.now()
        exchange = {'exchange': 'BITSTAMP'}
        json_data = public_client.ticker(base=ticker)
        json_data.update(exchange)
        return json_data
        #time.sleep(5)






