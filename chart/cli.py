from .config import load_config_defaults
import argparse
import sys

def add_display_options(parser):
    display = parser.add_argument_group('display options')
    display.add_argument('--node', choices=['true', 'mean'], default='true', help='choose lunar node calculation method')
    display.add_argument('-c', '--classical', action='store_true', help='exclude Uranus through Pluto')
    display.add_argument('-b', '--brief', action='store_true', help='print truncated placements, e.g. 21 Sco 2')
    display.add_argument('-v', '--verbose', action='store_true', help='print planet names instead of glyphs')
    display.add_argument('-p', '--no-coordinates', action='store_true', help="don't print coordinates")
    display.add_argument('-m', '--no-color', action='store_true', help='disable ANSI colors')

def parse_arguments():
    config_defaults = load_config_defaults()

    parser = argparse.ArgumentParser(
        prog='chart',
        description="chart is a minimal, opinionated and configurable horoscope CLI 🪐🌌",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help='subcommand help')

    # -*- now -*-
    now = subparsers.add_parser('now', help='calculate the chart of the moment')
    now.set_defaults(**config_defaults)

    now.add_argument('-y', '--lat', type=float, help="latitude")
    now.add_argument('-x', '--lng', type=float, help="longitude")
    now.add_argument('-s', '--shift', type=str, help="shift time forward or backward, e.g. 2h, -30m, 1.5d (default is hours)")
    now.add_argument('--save-config', action='store_true', help='save coordinates and display preferences to config')
    add_display_options(now)

    # -*- cast -*-
    cast = subparsers.add_parser('cast', help='calculate an event chart')
    cast.add_argument('--save-config', action='store_true', help='save coordinates and display preferences to config')
    cast.add_argument('--title', help='e.g. <Your Name>, "Now", "Full Moon"')
    cast.add_argument('-y', '--lat', type=float, help="latitude")
    cast.add_argument('-x', '--lng', type=float, help="longitude")
    cast.add_argument('-d', '--date', help='date of event, format: YYYY-MM-DD')
    cast.add_argument('-t', '--time', help='time of event (24h), format: HH:MM')
    add_display_options(cast)

    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])
