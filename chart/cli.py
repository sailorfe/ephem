import argparse
import sys

def add_display_options(parser):
    display = parser.add_argument_group('display options')
    display.add_argument('--node', choices=['true', 'mean'], default='true', help='choose lunar node calculation method')
    display.add_argument('-c', '--classical', action='store_true', help='exclude Uranus through Pluto')
    display.add_argument('-b', '--brief', action='store_true', help='print truncated placements, e.g. 21 Sco 2')
    display.add_argument('-v', '--verbose', action='store_true', help='print planet names instead of glyphs')
    display.add_argument('-m', '--no-color', action='store_true', help='disable ANSI colors')
    display.add_argument('-p', '--no-coordinates', action='store_true', help="don't print coordinates")

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='electional',
        description="A horoscope CLI for electional astrology",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help='subcommand help')

    # -*- now -*-
    now = subparsers.add_parser('now', help='calculate the chart of the moment')
    now.add_argument('-y', '--lat', type=float, help="latitude")
    now.add_argument('-x', '--lng', type=float, help="longitude")
    now.add_argument('-s', '--shift', type=str, help="shift time forward or backward, e.g. 2h, -30m, 1.5d (default is hours)")
    add_display_options(now)

    # -*- chart -*-
    chart = subparsers.add_parser('chart', help='calculate an event chart')
    chart.add_argument('--title', help='e.g. <Your Name>, "Now", "Full Moon"')
    chart.add_argument('-y', '--lat', type=float, help="latitude")
    chart.add_argument('-x', '--lng', type=float, help="longitude")
    chart.add_argument('-d', '--date', help='date of event, format: YYYY-MM-DD')
    chart.add_argument('-t', '--time', help='time of event (24h), format: HH:MM')
    chart.add_argument('--noon', action='store_true', help='use 12:00 UTC and print no angles')
    chart.add_argument('--zero', action='store_true', help='use Null Island (0, 0) and print no angles')
    add_display_options(chart)

    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])
