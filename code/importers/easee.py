from datetime import time, tzinfo, timedelta
import datetime

def add_easee_parser(parent, subparsers):
  LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

  print(LOCAL_TIMEZONE)

  t = datetime.datetime.now()
  print(t)
