from .config import load_config_defaults
from chart.commands import now, cast, asc
import argparse
import sys

def add_display_options(parser):
    display = parser.add_argument_group('display options')
    display.add_argument('--node', choices=['true', 'mean'], default='true', help="choose lunar node calculation method")
    display.add_argument('--theme', choices=['sect', 'element', 'mode'], default='sect', help="choose ANSI color theme")
    display.add_argument('-c', '--classical', action='store_true', help="exclude Uranus through Pluto")
    display.add_argument('-g', '--glyphs', action='store_true', help="print planet and sign glyphs")
    display.add_argument('-v', '--verbose', action='store_true', help="print planet names and full sign names")
    display.add_argument('-z', '--no-angles', action='store_true', help="don't print Ascendant or Midheaven")
    display.add_argument('-p', '--no-coordinates', action='store_true', help="don't print coordinates")
    display.add_argument('-m', '--no-color', action='store_true', help="disable ANSI colors")


def parse_arguments(args=None):
    config_defaults = load_config_defaults()

    parser = argparse.ArgumentParser(
        prog='chart',
        description="chart is a minimal, opinionated and configurable horoscope CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="subcommand help")

    # -*- now -*-
    now_parser = subparsers.add_parser('now', help="calculate the chart of the moment")
    now_parser.set_defaults(func=now.run)

    now_parser.add_argument('-y', '--lat', type=float, help="latitude")
    now_parser.add_argument('-x', '--lng', type=float, help="longitude")
    now_parser.add_argument('-s', '--shift', type=str, help="shift time forward or backward, e.g. 2h, -30m, 1.5d, 4w (default is hours)")
    now_parser.add_argument('--save-config', action='store_true', help="save coordinates and display preferences to config")
    add_display_options(now_parser)

    # -*- cast -*-
    cast_parser = subparsers.add_parser('cast', help="calculate an event chart")
    cast_parser.set_defaults(func=cast.run)

    cast_parser.add_argument('--save-config', action='store_true', help="save coordinates and display preferences to config")
    cast_parser.add_argument('event', nargs="*", metavar="DATE [TIME] [TITLE]", help="date, optional time and title, e.g. '2025-08-09 7:54 Aquarius Full Moon'")
    cast_parser.add_argument('-y', '--lat', type=float, help="latitude")
    cast_parser.add_argument('-x', '--lng', type=float, help="longitude")
    add_display_options(cast_parser)


    # -*- asc -*-
    asc_parser = subparsers.add_parser('asc', help="print the current local ascendant")
    asc_parser.set_defaults(func=asc.run)
    asc_parser.add_argument('-y', '--lat', type=float, help="latitude")
    asc_parser.add_argument('-x', '--lng', type=float, help="longitude")
    asc_parser.add_argument('--save-config', action='store_true', help="save coordinates to config")
    asc_parser.add_argument('-g', '--glyphs', action='store_true', help='show glyphs instead of truncated sign names')
 

    parsed = parser.parse_args(args)

    if args == [] or args is None and len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if parsed.command == "cast" and (not parsed.event or len(parsed.event) < 1):
        parser.error(
            "`chart cast` needs at minimum a DATE, and optionally a TIME and TITLE. For example:"
            "\n    chart cast 1993-08-16 13:05 \"Debian Linux\""
        )

    return parsed



