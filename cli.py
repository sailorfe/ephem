import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(prog='electional', description="A horoscope CLI for electional astrology.")
    subparsers = parser.add_subparsers(dest="command", required=True, help='subcommand help')

    chart = subparsers.add_parser('chart', help='calculate the chart of the moment or an event/birth chart')
    group = chart.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', '--now', nargs='*', metavar=('LAT', 'LNG'), help="use current time and location via IP or manualy given coordinates")
    group.add_argument('-e', '--event', nargs=4, metavar=('DATE', 'TIME', 'LAT', 'LNG'), help="calculate chart for specific date/time/place (YYYY-MM-DD HH:MM y x)")

    chart.add_argument('-t', '--title', help='e.g. <Your Name>, "Now", "Full Moon"')
    chart.add_argument('-s', '--short', action='store_true', help='print truncated placements, e.g. 21 Sco 2')
    chart.add_argument('-p', '--plain', action='store_true', help='disable ANSI colors')
    chart.add_argument('-c', '--classical', action='store_true', help='exclude Uranus through Pluto')
    chart.add_argument('-a', '--approximate', action='store_true', help="given a date but no time and/or place, use UTC noon and don't print angles")
    chart.add_argument('--node', choices=['true', 'mean'], default='true', help='choose lunar node calculation method')

    asc = subparsers.add_parser('asc', help='calculate current local ascendant with IP geolocation or given coordinates')
    asc.add_argument('-f', '--fixed', nargs=2, metavar=('LAT', 'LNG'), help="manually provide coordinates")

    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])
