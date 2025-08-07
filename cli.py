import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
            prog='electional',
            description="A horoscope CLI for electional astrology",
            epilog="""
examples:
    electional chart                                                    # chart of the moment from IP
    electional chart --lat 36 --lng -86                                 # chart of the moment from coordinates
    electional chart -e -d 1989-12-13 -y 40.33 -x -75.95 --noon         # event with unkown time
    electional chart -e -d 1993-08-16 -t 13:05 --zero                   # event with unknown coordinates
    electional chart -e -d 1845-05-19 --noon --zero                     # event with date only
    electional asc                                                      # print the current ascendant from IP
    electional asc --lat 47.95 --lng -124.39                            # print the current ascendant from coordinates
""",
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    subparsers = parser.add_subparsers(dest="command", required=True, help='subcommand help')

    chart = subparsers.add_parser('chart', help='calculate the chart of the moment or an event/birth chart')
    chart.add_argument('-y', '--lat', type=float, help='latitude')
    chart.add_argument('-x', '--lng', type=float, help='longitude')
    chart.add_argument('-e', '--event', action='store_true', help="calculate chart of an event")
    chart.add_argument('-d', '--date', help='date of event, format: YYYY-MM-DD')
    chart.add_argument('-t', '--time', help='time of event (24h), format: HH:MM')
    chart.add_argument('--noon', action='store_true', help='use 12:00 UTC and print no angles')
    chart.add_argument('--zero', action='store_true', help='use Null Island (0, 0) and print no angles')

    chart.add_argument('--title', help='e.g. <Your Name>, "Now", "Full Moon"')
    chart.add_argument('--node', choices=['true', 'mean'], default='true', help='choose lunar node calculation method')
    chart.add_argument('-c', '--classical', action='store_true', help='exclude Uranus through Pluto')
    chart.add_argument('-s', '--short', action='store_true', help='print truncated placements, e.g. 21 Sco 2')
    chart.add_argument('-v', '--verbose', action='store_true', help='print planet names instead of glyphs')
    chart.add_argument('--no-color', action='store_true', help='disable ANSI colors')

    asc = subparsers.add_parser('asc', help='calculate current local ascendant with IP geolocation or given coordinates')
    asc.add_argument('-y', '--lat', type=float, help='latitude')
    asc.add_argument('-x', '--lng', type=float, help='longitude')

    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])
