#!venv/bin/python

import requests, json, postgresql, sys, getopt, os
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta

TOKEN = os.getenv('ELVIA_TOKEN')
METER = os.getenv('ELVIA_METER')
PG    = os.getenv('PG_CONNECTION_STRING')

request_date_to = d.today()
try:
   opts, args = getopt.getopt(sys.argv[1:],"d:")

   for opt, arg in opts:
      if opt == '-d':
         request_date_to = d.fromisoformat(arg)
except getopt.GetoptError:
    #We don't care
    print("")

request_date_from = request_date_to - timedelta(days=1)

url = 'https://elvia.azure-api.net/customer/metervalues/api/v1/metervalues?startTime=' + str(request_date_from) + 'T00:00:00+01:00&endTime=' + str(request_date_to) + 'T00:00:00+01:00&meteringPointIds=' + METER
headers = {'Cache-Control': 'no-cache', 'Authorization': 'Bearer ' + TOKEN}

r = requests.get(url, headers=headers)

if r.status_code != 200:
    print("HTTP Response: " + str(r.status_code))
    print("Requested: " + r.url)
    print(r.text[:200])
    sys.exit(2)

json_data = r.json()
db = postgresql.open(PG)

save_price = db.prepare("INSERT INTO hourlyusage VALUES ($1, $2, $3)")
tmp1 = json_data['meteringpoints']
tmp2 = tmp1[0]['metervalue']['timeSeries']
for key in tmp2:
    save_price(dt.fromisoformat(key['startTime']), key['value'], dt.fromisoformat(key['endTime']))
