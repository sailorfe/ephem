from .config import load_config_defaults
import argparse
import sys

def add_display_options(parser):
    display = parser.add_argument_group('display options')
    display.add_argument('--node', choices=['true', 'mean'], default='true', help="choose lunar node calculation method")
    display.add_argument('-c', '--classical', action='store_true', help="exclude Uranus through Pluto")
    display.add_argument('-b', '--brief', action='store_true', help="print truncated placements, e.g. 21 Sco 2")
    display.add_argument('-v', '--verbose', action='store_true', help="print planet names instead of glyphs")
    display.add_argument('-z', '--no-angles', action='store_true', help="don't print Ascendant or Midheaven")
    display.add_argument('-p', '--no-coordinates', action='store_true', help="don't print coordinates")
    display.add_argument('-m', '--no-color', action='store_true', help="disable ANSI colors")

def parse_arguments(args=None):
    config_defaults = load_config_defaults()

    parser = argparse.ArgumentParser(
        prog='chart',
        description="chart is a minimal, opinionated and configurable horoscope CLI 🪐🌌",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="subcommand help")

    # -*- now -*-
    now = subparsers.add_parser('now', help="calculate the chart of the moment")
    now.set_defaults(**config_defaults)

    now.add_argument('-y', '--lat', type=float, help="latitude")
    now.add_argument('-x', '--lng', type=float, help="longitude")
    now.add_argument('-s', '--shift', type=str, help="shift time forward or backward, e.g. 2h, -30m, 1.5d, 4w (default is hours)")
    now.add_argument('--save-config', action='store_true', help="save coordinates and display preferences to config")
    add_display_options(now)

    # -*- cast -*-
    cast = subparsers.add_parser('cast', help="calculate an event chart")
    cast.add_argument('--save-config', action='store_true', help="save coordinates and display preferences to config")
    cast.add_argument('event', nargs="*", metavar="DATE [TIME] [TITLE]", help="date, optional time and title, e.g. '2025-08-09 7:54 Aquarius Full Moon'")
    cast.add_argument('-y', '--lat', type=float, help="latitude")
    cast.add_argument('-x', '--lng', type=float, help="longitude")
    add_display_options(cast)

    if args == [] or args is None and len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args(args)

def parse_event(event_args):
    # date_str, time_str, title_str
    if len(event_args) == 0:
        return None, None, None
    elif len(event_args) == 1:
        return event_args[0], None, None
    elif len(event_args) == 2:
        return event_args[0], event_args[1], None
    else:
        return event_args[0], event_args[1], " ".join(event_args[2:])

