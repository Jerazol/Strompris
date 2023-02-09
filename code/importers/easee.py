import requests, os, json, postgresql, sys
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta

#from datetime import time, tzinfo, timedelta
#import datetime

def add_easee_parser(parent, subparsers):
  importer = subparsers.add_parser('easee',
                                    help='Import charger usage',
                                    description='Import charger usage from Easee API, for the given date or previous day if no date given.',
                                    parents=[parent])
  importer.add_argument("-u", "--user", help="Easee username", required=True)
  importer.add_argument("-p", "--password", help="Easee password. Must be either specified in the environment as EASEE_PASSWORD or specified as an argument", default=os.getenv('EASEE_PASSWORD'))
  importer.set_defaults(func=do_easee_charger_import)

def do_easee_charger_import(args):
  PG    = os.getenv('PG_CONNECTION_STRING')

  request_date_to = d.today()
  if args.date != None:
    request_date_to = d.fromisoformat(args.date)

  request_date_from = request_date_to - timedelta(days=1)

  url = 'https://api.easee.cloud/api/accounts/login'
  headers = {
    'Content-Type': 'application/*+json',
    'Accept': 'application/json'
  }
  payload = {'userName': args.user, 'password': args.password}
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



def request_error(r, desc):
  if r.status_code != 200:
    print(desc)
    print("HTTP Response: " + str(r.status_code))
    print("Requested: " + r.url)
    print(r.text[:200])
    sys.exit(2)
