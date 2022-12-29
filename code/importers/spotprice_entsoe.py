import os
import xml.etree.ElementTree as ET

def add_entsoe_parser(parent, subparsers):
    importer = subparsers.add_parser('entsoe_spotprice',
                                      help='Import spotprice',
                                      description='Import spotprices from Entsoe API for the given date or following day if no date given.',
                                      parents=[parent])
    importer.add_argument("-z", "--zone", help="Price zone to fetch data for", default="10YNO-1--------2")
    importer.add_argument("-t", "--token", help="Authentication token. Must be either specified in the environment as ENTSOETOKEN or specified as an argument", default=os.getenv('ENTSOETOKEN'))
    importer.set_defaults(func=do_entsoe_prices_import)

def do_entsoe_prices_import(args):
    # root = ET.fromstring(country_data_as_string)
    print("Token: " + args.token)
    print("Zone: " + args.zone)
    tree = ET.parse('/home/tommyg/spotprice_2021.xml')
    root = tree.getroot()
    ns = {'urn': 'urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0'}
    ts = root.findall("./urn:TimeSeries", ns)
    timeInterval = ts[0].findall("./urn:Period/urn:timeInterval", ns)
    points = ts[0].findall("./urn:Period/urn:Point", ns)
    print(timeInterval[0][0].text)
    print(timeInterval[0][1].text)
    print(points[0][1].text)
