import requests, os, json, postgresql
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta

def add_elvia_usage_parser(parent, subparsers):
    importer = subparsers.add_parser('elvia_usage',
                                      help='Import power usage',
                                      description='Import power usage from Elvia API, for the given date or previous day if no date given.',
                                      parents=[parent])
    importer.add_argument("-m", "--meter", help="Metering point ID", required=True)
    importer.add_argument("-t", "--token", help="Authentication token. Must be either specified in the environment as ELVIA_TOKEN or specified as an argument", default=os.getenv('ELVIA_TOKEN'))
    importer.set_defaults(func=do_elvia_usage_import)

def do_elvia_usage_import(args):
    PG    = os.getenv('PG_CONNECTION_STRING')

    request_date_to = d.today()
    if args.date != None:
      request_date_to = d.fromisoformat(args.date)

    request_date_from = request_date_to - timedelta(days=1)

    url = 'https://elvia.azure-api.net/customer/metervalues/api/v1/metervalues?startTime=' + str(request_date_from) + 'T00:00:00+01:00&endTime=' + str(request_date_to) + 'T00:00:00+01:00&meteringPointIds=' + args.meter
    headers = {'Cache-Control': 'no-cache', 'Authorization': 'Bearer ' + args.token}

    if args.dryrun or args.verbose:
      print("requests.get('" + url + "', headers='" + str(headers) + "')")

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
      print("HTTP Response: " + str(r.status_code))
      print("Requested: " + r.url)
      print(r.text[:200])
      return

    json_data = r.json()
    if not args.dryrun:
      db = postgresql.open(PG)

    if not args.dryrun:
      save_price = db.prepare("INSERT INTO hourlyusage VALUES ($1, $2, $3) ON CONFLICT (start_time) DO UPDATE SET usage = EXCLUDED.usage")

    usage_data = json_data['meteringpoints'][0]['metervalue']['timeSeries']
    for key in usage_data:
      try:
        if args.verbose:
          print(
            '{"start_time": "' +
            str(dt.fromisoformat(key['startTime'])) +
            '", "usage":"' +
            str(key['value']) +
            '", "end_time": "' +
            str(dt.fromisoformat(key['endTime'])) +
            '"}'
          )
        if not args.dryrun:
          save_price(dt.fromisoformat(key['startTime']), key['value'], dt.fromisoformat(key['endTime']))
      except (RuntimeError, postgresql.exceptions.Error) as e:
        print("Failed inserting value:")
        print("----------------")
        print('startTime:' + key['startTime'])
        print('endTime:' + key['endTime'])
        print('value:' + str(key['value']))
