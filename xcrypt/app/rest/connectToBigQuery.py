# Imports the Google Cloud client library

from  google.cloud import bigquery
#import bigquery
import os
import httplib2
from oauth2client.contrib import gce

from BitstampClient import BitstampClient
from xcrypt.app.rest.CexIoClient import CexioClient
# import bigquery
import os

import httplib2
from BitstampClient import BitstampClient
from  google.cloud import bigquery
from oauth2client.contrib import gce

from xcrypt.app.rest.CexIoClient import CexioClient


class BiqQueryAdapter:
    table_name = "tickers"
    dataset_name = "xcrypt"

    def setGoogleAuthEnv(self):
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Volumes/partition_2/xcrypt/gcp-key.json"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./gcp-key.json"
        cred = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        print "GOOGLE_APPLICATION_CREDENTIALS"
        print cred

    def initOAuth(self):
         credentials = gce.AppAssertionCredentials(
         scope='https://www.googleapis.com/auth/devstorage.full_control')
         http = credentials.authorize(httplib2.Http())

    # Instantiates a client
    def streamDataIntoBQ(self,dataset_name, table_name, rows ):
        bigquery_client = bigquery.Client()
        dataset_ref = bigquery_client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)
        table = bigquery_client.get_table(table_ref)
        errors = bigquery_client.create_rows(table, rows)

    def readDataFromBQ(self):
        self.setGoogleAuthEnv()
        self.initOAuth()
        bigquery_client = bigquery.Client()
        # dataset_ref = bigquery_client.dataset(dataset_name)
        # table_ref = dataset_ref.table(table_name)
        # table = bigquery_client.get_table(table_ref)
        query_job = bigquery_client.query("""
              #standardSQL
              SELECT timestamp, last, bid, ask, open, exchange, volume 
              FROM xcrypt.tickers
              ORDER BY timestamp DESC
              LIMIT 200000
              """)
        results = query_job.result()  # Waits for job to complete.
        # for row in results:
        #     print("{}: {}: {}: {} :{}".format(row.timestamp, row.exchange, row.last, row.ask, row.bid ))
        return results

    def arbitrage(self, exchange1, exchnage2):
        self.setGoogleAuthEnv()
        self.initOAuth()
        bigquery_client = bigquery.Client()
        query = "SELECT timestamp, last, bid, ask, open, exchange, volume  FROM xcrypt.tickers WHERE exchange =' "  + exchange1 + "OR  exchange = ' " + exchnage2 +  "ORDER BY timestamp"
        query_job = bigquery_client.query("" + query + "")
        results = query_job.result()  # Waits for job to complete.
        # for row in results:
        #     print("{}: {}: {}: {} :{}".format(row.timestamp, row.exchange, row.last, row.ask, row.bid ))
        return results


    def callBitstamp(self):
        bitstampClient = BitstampClient();
        json_data = bitstampClient.getTickerLiveData("btc")
        print json_data
        return json_data

    def callCexIo(self):
        cexioClient = CexioClient();
        cexioClientData = cexioClient.getTickerLiveData("BTC/USD")
        print cexioClientData
        return cexioClientData
        #cexioClientData = json.dumps(cexioClientData)
        #cexioClientData = json.loads(cexioClientData)
        #resp = self.serializeJson(cexioClientData)

        print cexioClientData
        return cexioClientData


    def processRequest(self, table_name = "tickers", dataset_name = "xcrypt"):
        self.setGoogleAuthEnv()
        self.initOAuth()
        bitstampData = self.callBitstamp()
        cexIoData = self.callCexIo()
        rows = [bitstampData,cexIoData]
        #rows = [bitstampData]  # FIXME - Append to Array in more generic way.
        print rows[0]

        # rows = [bitstampData]
        errors = self.streamDataIntoBQ(dataset_name, table_name, rows)
        if not errors:
            print('Loaded '  + str(len(rows)) + ' rows into {}:{}'.format(dataset_name, table_name))
            return rows
        else:
            print('Errors:')
            print(errors)
            print " Rows were created successfully!!!!!"

        def json_repr(obj):
            """Represent instance of a class as JSON.
            Arguments:
            obj -- any object
            Return:
            String that reprent JSON-encoded object.
            """

        def serializeJson(obj):
            """Recursively walk object's hierarchy."""
            if isinstance(obj, (bool, int, long, float, basestring)):
                 return obj
            elif isinstance(obj, dict):
                obj = obj.copy()
                for key in obj:
                    obj[key] = serializeJson(obj[key])
                return obj
            elif isinstance(obj, list):
                return [serializeJson(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(serializeJson([item for item in obj]))
            elif hasattr(obj, '__dict__'):
                return serializeJson(obj.__dict__)
            else:
                return repr(obj)  # Don't know how to handle, convert to string
        #return json.dumps(serialize(obj))




#timestamp	TIMESTAMP	NULLABLE


if __name__ == "__main__":
    json_data = BiqQueryAdapter().processRequest();



