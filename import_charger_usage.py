#!/usr/bin/env python3

import requests, json, postgresql, sys, getopt, os
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta

USER  = os.getenv('EASEE_USER')
PASS = os.getenv('EASEE_PASS')
PG    = os.getenv('PG_CONNECTION_STRING')

def request_error(r, desc):
  if r.status_code != 200:
    print(desc)
    print("HTTP Response: " + str(r.status_code))
    print("Requested: " + r.url)
    print(r.text[:200])
    sys.exit(2)


request_date_from = d.today()
try:
   opts, args = getopt.getopt(sys.argv[1:],"d:")

   for opt, arg in opts:
      if opt == '-d':
         request_date_from = d.fromisoformat(arg)
except getopt.GetoptError:
    #We don't care
    print("")

request_date_to = request_date_from + timedelta(days=1)


# Get bearer token
url = 'https://api.easee.cloud/api/accounts/token'
headers = {
  'Content-Type': 'application/*+json',
  'Accept': 'application/json'
}
payload = {'userName': USER, 'password': PASS}
r = requests.post(url, headers=headers, json=payload)
request_error(r, "Get token")
json_data = r.json()
token = json_data["accessToken"]


# Get Charger ID
url = 'https://api.easee.cloud/api/chargers'
headers = {
  'Authorization': 'Bearer ' + token,
  'Accept': 'application/json'
}
r = requests.get(url, headers=headers)
request_error(r, "Charger ID")
json_data = r.json()
charger = json_data[0]['id']


# Get Usage
url = 'https://api.easee.cloud/api/chargers/'+charger+'/usage/hourly/'+str(request_date_from)+'T00:00:00/'+str(request_date_to)+'T00:00:00'
r = requests.get(url, headers=headers)
request_error(r, "Get usage")
json_data = r.json()
db = postgresql.open(PG)

save_usage = db.prepare("INSERT INTO chargerusage VALUES ($1, $2, $3)")

for key in json_data:
    if key['totalEnergy'] > 0:
        try:
            save_usage(dt.fromisoformat(key['from'].replace('Z', '+00:00')), key['totalEnergy'], dt.fromisoformat(key['to'].replace('Z', '+00:00')))
        except postgresql.exceptions.UniqueError as e:
            print("Duplicate value:")
            print("----------------")
            print('from:' + key['from'])
            print('to:' + key['to'])
            print('totalEnergy:' + str(key['totalEnergy']))
