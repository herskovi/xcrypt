
import time

from xcrypt.app.rest.connectToBigQuery import BiqQueryAdapter

while 1:

    bqClient = BiqQueryAdapter();
    try:
        json_data = bqClient.processRequest();
        time.sleep(60)
    except Exception as e:
        print e.message, e.args
        time.sleep(60)

    if __name__ == "__main__":
        json_data = BiqQueryAdapter().processRequest();

