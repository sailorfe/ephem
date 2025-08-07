import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
            prog='electional',
            description="A horoscope CLI for electional astrology",
            formatter_class=argparse.RawDescriptionHelpFormatter
            )
    subparsers = parser.add_subparsers(dest="command", required=True, help='subcommand help')

    now = subparsers.add_parser('now', help='calculate the chart of the moment')
    now.add_argument('-y', '--lat', type=float, help="latitude")
    now.add_argument('-x', '--lng', type=float, help="longitude")
    scrub = now.add_mutually_exclusive_group()
    scrub.add_argument('--fw', type=int, help="move forward N hours")
    scrub.add_argument('--bw', type=int, help="move backward N hours")

    now_display = now.add_argument_group('display options')
    now_display.add_argument('--node', choices=['true', 'mean'], default='true', help='choose lunar node calculation method')
    now_display.add_argument('-c', '--classical', action='store_true', help='exclude Uranus through Pluto')
    now_display.add_argument('-s', '--short', action='store_true', help='print truncated placements, e.g. 21 Sco 2')
    now_display.add_argument('-v', '--verbose', action='store_true', help='print planet names instead of glyphs')
    now_display.add_argument('-m', '--no-color', action='store_true', help='disable ANSI colors')
    now_display.add_argument('-p', '--no-geo', action='store_true', help="don't print coordinates")

    chart = subparsers.add_parser('chart', help='calculate an event chart')
    chart.add_argument('--title', help='e.g. <Your Name>, "Now", "Full Moon"')
    chart.add_argument('-y', '--lat', type=float, help="latitude")
    chart.add_argument('-x', '--lng', type=float, help="longitude")
    chart.add_argument('-d', '--date', help='date of event, format: YYYY-MM-DD')
    chart.add_argument('-t', '--time', help='time of event (24h), format: HH:MM')
    chart.add_argument('--noon', action='store_true', help='use 12:00 UTC and print no angles')
    chart.add_argument('--zero', action='store_true', help='use Null Island (0, 0) and print no angles')

    chart_display = chart.add_argument_group('display options')
    chart_display.add_argument('--node', choices=['true', 'mean'], default='true', help='choose lunar node calculation method')
    chart_display.add_argument('-c', '--classical', action='store_true', help='exclude Uranus through Pluto')
    chart_display.add_argument('-s', '--short', action='store_true', help='print truncated placements, e.g. 21 Sco 2')
    chart_display.add_argument('-v', '--verbose', action='store_true', help='print planet names instead of glyphs')
    chart_display.add_argument('-m', '--no-color', action='store_true', help='disable ANSI colors')
    chart_display.add_argument('-p', '--no-geo', action='store_true', help="don't print coordinates")

    return parser.parse_args(args=None if sys.argv[1:] else ['--help'])
