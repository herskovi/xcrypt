
import json
import os

import jinja2
import webapp2



from xcrypt.app.rest.connectToBigQuery import BiqQueryAdapter

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
    ,extensions=['jinja2.ext.autoescape']
    ,variable_start_string='[['
    ,variable_end_string=']]'
   ,autoescape=True)

JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = '/'


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, XCrypt!')
        #template = JINJA_ENVIRONMENT.get_template('index.html')
        #self.response.out.write(template.render())

        BiqQueryAdapter().processRequest();

class StreamDataHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Schedualer!')
        response = BiqQueryAdapter().processRequest()
        self.response.write(response)

class StreamDataHandler(webapp2.RequestHandler):
    def get(self):
        print(os.path.dirname(__file__))
        resp = BiqQueryAdapter().readDataFromBQ()
        responsetoClient = self.json_list(resp);
        self.response.headers['Content-Type'] = 'application/json'
        #print responsetoClient
        return self.response.write(responsetoClient)
        jsonObj = json.loads(responsetoClient)
        response.json


    def json_list(self,list):
        lst = []
        for row in list:
            json_data = {}
            json_data["timestamp"] = _timestamp_query_param_from_json(row.timestamp)
            json_data["exchange"] = row.exchange
            json_data["last"] = row.last
            json_data["ask"] = row.ask
            json_data["bid"] = row.bid
            lst.append(json_data)

        response = json.dumps(lst)
        return response

    def _timestamp_query_param_from_json(value, field):
        """Coerce 'value' to a datetime, if set or not nullable.

        Args:
            value (str): The timestamp.
            field (.SchemaField): The field corresponding to the value.

        Returns:
            Optional[datetime.datetime]: The parsed datetime object from
            ``value`` if the ``field`` is not null (otherwise it is
            :data:`None`).
        """
        if _not_null(value, field):
            # Canonical formats for timestamps in BigQuery are flexible. See:
            # g.co/cloud/bigquery/docs/reference/standard-sql/data-types#timestamp-type
            # The separator between the date and time can be 'T' or ' '.
            value = value.replace(' ', 'T', 1)
            # The UTC timezone may be formatted as Z or +00:00.
            value = value.replace('Z', '')
            value = value.replace('+00:00', '')

            if '.' in value:
                # YYYY-MM-DDTHH:MM:SS.ffffff
                return datetime.datetime.strptime(
                    value, _RFC3339_MICROS_NO_ZULU).replace(tzinfo=UTC)
            else:
                # YYYY-MM-DDTHH:MM:SS
                return datetime.datetime.strptime(
                    value, _RFC3339_NO_FRACTION).replace(tzinfo=UTC)
        else:
            return None


class ArbitrageHandler(webapp2.RequestHandler):
    def get(self,exchange1, exchange2):
        print(os.path.dirname(__file__))
        resp = BiqQueryAdapter().arbitrage(exchange1, exchange2)
        responsetoClient = self.json_list(resp);
        self.response.headers['Content-Type'] = 'application/json'
        print responsetoClient
        return self.response.write(responsetoClient)
        jsonObj = json.loads(responsetoClient)
        return jsonObj


app = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/rest/uploadtobigquery', MainPage),
        ('/rest/getAllData', StreamDataHandler),
        ('/rest/arbitrage/exchange1/exchange2', ArbitrageHandler)
]
, debug=True)