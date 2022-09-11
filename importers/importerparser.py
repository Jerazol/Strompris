import argparse

from importers.spotprice_ffail import add_ffail_parser
from importers.easee import add_easee_parser
from importers.consumption import add_consumption_parser

def configure_parser():
  """ configure command line argument parser, including command documentation """

  # configure_parser in parser_utils maps every subparser to its function
  parent, parser = configure_importers_parser()
  subparsers = parser.add_subparsers(title='commands', dest='command')
  add_ffail_parser(parent, subparsers)
  add_easee_parser(parent, subparsers)
  add_consumption_parser(parent, subparsers)
  return parser

def configure_importers_parser():
  importers = argparse.ArgumentParser(add_help=False)
  importers.add_argument('--verbose', '-v',
                         dest='verbose',
                         action='store_true',
                         help="Add verbose output")
  importers.add_argument('--dryrun', '--dry-run',
                         required=False,
                         action='store_true',
                         help="Run in dry-run mode, just show what would be done")
  importers.add_argument('--interval', '-i',
                         required=False,
                         action='store_true',
                         help="Interval between timestamps to import data from.")
  importers.add_argument('--date', '-d',
                         required=False,
                         action='store_true',
                         help="End timestamp for import job.")

  parser = argparse.ArgumentParser(
    description='import helper',
    epilog='''\
lorem ipsum dolor sit amet
Please see README.md for details.''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[importers])
  return importers, parser
