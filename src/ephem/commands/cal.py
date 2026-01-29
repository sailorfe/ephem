from ephem.display.month import format_calendar
import sys


def main(args):
    format_calendar(args)


def run(args):
    try:
        main(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
