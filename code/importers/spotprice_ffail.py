import requests, json, postgresql, sys, getopt, os
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta

def add_ffail_parser(parent, subparsers):
    importer = subparsers.add_parser('ffail_spotprice',
                                      help='Import spotprice',
                                      description='Import spotprice from ffail.win API',
                                      parents=[parent])
    importer.add_argument("-z", "--zone", help="Price zone to fetch data for", default="NO1")
    importer.add_argument("-t", "--token", help="Authentication token. Must be either specified in the environment as FFAILTOKEN or specified as an argument", default=os.getenv('FFAILTOKEN'))
    importer.set_defaults(func=do_import)

def do_import(args):
  PG = os.getenv('PG_CONNECTION_STRING')

  request_date = d.today() + timedelta(days=1)
  if args.date != None:
    request_date = d.fromisoformat(args.date)

  URL = 'https://norway-power.ffail.win/?key=' + args.token + '&zone=' + args.zone + '&date=' + str(request_date)
  if args.verbose:
    print(URL)
  r =requests.get(URL)


  if r.status_code != 200:
    print("HTTP Response: " + str(r.status_code))
    print("Requested: " + r.url)
    print(r.text[:200])
    sys.exit(2)

  json_data = r.json()
  db = postgresql.open(PG)

  save_price = db.prepare("INSERT INTO spotprice VALUES ($1, $2, $3, $4) ON CONFLICT (price_hour) DO UPDATE SET price = EXCLUDED.price")
  if args.verbose:
    print(json.dumps(json_data))

  if not args.dryrun:
    for key in json_data:
      save_price(dt.fromisoformat(key), json_data[key]['NOK_per_kWh'], dt.fromisoformat(json_data[key]['valid_from']), dt.fromisoformat(json_data[key]['valid_to']))
