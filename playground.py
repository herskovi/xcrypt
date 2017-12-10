import httplib2
from oauth2client.contrib import gce

credentials = gce.AppAssertionCredentials(
   scope='https://www.googleapis.com/auth/devstorage.full_control')
http = credentials.authorize(httplib2.Http())