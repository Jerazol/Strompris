#!/usr/bin/python3

import requests, json, postgresql, sys, getopt, os
from datetime import datetime as dt
from datetime import date as d
from random import randint
from time import sleep


from datetime import date, timedelta

TOKEN = os.getenv('ELVIA_TOKEN')
METER = os.getenv('ELVIA_METER')
PG    = os.getenv('PG_CONNECTION_STRING')

start_date = date(2021, 10, 26)
end_date = date(2021, 12, 25)    # perhaps date.now()

delta = end_date - start_date   # returns timedelta

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    day2 = start_date + timedelta(days=i+1)
    url = 'https://elvia.azure-api.net/customer/metervalues/api/v1/metervalues?startTime=' + str(day) + 'T00:00:00+01:00&endTime=' + str(day2) + 'T00:00:00+01:00&meteringPointIds=' + METER
    headers = {'Cache-Control': 'no-cache', 'Authorization': 'Bearer ' + TOKEN}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("HTTP Response: " + str(r.status_code))
        print("Requested: " + r.url)
        print(r.text[:200])
        sys.exit(2)

    json_data = r.json()
    db = postgresql.open(PG))

    save_price = db.prepare("INSERT INTO hourlyusage VALUES ($1, $2, $3)")
    tmp1 = json_data['meteringpoints']
    tmp2 = tmp1[0]['metervalue']['timeSeries']
    for key in tmp2:
        save_price(dt.fromisoformat(key['startTime']), key['value'], dt.fromisoformat(key['endTime']))
        sleep(randint(1,10))
