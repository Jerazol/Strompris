#!/usr/bin/env python

import requests, json, postgresql, sys, getopt, os
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta


PG = os.getenv('PG_CONNECTION_STRING')
FFAILTOKEN = os.getenv('FFAILTOKEN')

request_date = d.today() + timedelta(days=1)
try:
   opts, args = getopt.getopt(sys.argv[1:],"d:")

   for opt, arg in opts:
      if opt == '-d':
         request_date = arg
except getopt.GetoptError:
    #We don't care
    print("")

r =requests.get('https://norway-power.ffail.win/?key=' + FFAILTOKEN + '&zone=NO1&date=' + str(request_date))

if r.status_code != 200:
    print("HTTP Response: " + str(r.status_code))
    print("Requested: " + r.url)
    print(r.text[:200])
    sys.exit(2)

json_data = r.json()
db = postgresql.open(PG)

save_price = db.prepare("INSERT INTO spotprice VALUES ($1, $2, $3, $4)")
for key in json_data:
    save_price(dt.fromisoformat(key), json_data[key]['NOK_per_kWh'], dt.fromisoformat(json_data[key]['valid_from']), dt.fromisoformat(json_data[key]['valid_to']))
