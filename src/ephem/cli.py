import argparse
import calendar
import sys
from datetime import date
from .commands import now, cast, cal, data
from .config import load_config_defaults, run_save, run_show
from .constants import AYANAMSAS


def splash_text():
    return """
                      ,dPYb,
                      IP'`Yb
                      I8  8I
                      I8  8
  ,ggg,   gg,gggg,    I8 dPgg,    ,ggg,    ,ggg,,ggg,,ggg,
 i8" "8i  I8P"  "Yb   I8dP" "8I  i8" "8i  ,8" "8P" "8P "8,
 I8, ,8I  I8'    ,8i  I8P    I8  I8, ,8I  I8   8I   8I   8I
 `YbadP' ,I8 _  ,d8' ,d8     I8, `YbadP' ,dP   8I   8I   Yb,
888P"Y888PI8 YY88888P88P     `Y8888P"Y8888P'   8I   8I   `Y8
          I8
          I8
          I8
          I8
          I8
          I8
"""


class EphemParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(
            2, f"\n❌ Error: {message}\n\nUse -h or --help for more information.\n"
        )


def add_display_options(parser, config_defaults=None):
    """Display options for cast, now, and data load."""
    if config_defaults is None:
        config_defaults = {}

    display = parser.add_argument_group("display options")
    display.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        default=config_defaults.get("ascii", False),
        help="use ASCII text instead of Unicode glyphs",
    )
    display.add_argument(
        "-t",
        "--theme",
        choices=["sect", "mode", "element"],
        default=config_defaults.get("theme", "sect"),
        help="choose colorscheme by planetary sect, or sign mode or element (default: sect)",
    )
    display.add_argument(
        "-C",
        "--no-color",
        action="store_true",
        default=config_defaults.get("no_color", False),
        help="disable ANSI colors",
    )
    display.add_argument(
        "-c",
        "--classical",
        action="store_true",
        default=config_defaults.get("classical", False),
        help="exclude Uranus through Pluto",
    )
    display.add_argument(
        "-n",
        "--node",
        choices=["true", "mean"],
        default=config_defaults.get("node", "true"),
        help="choose lunar node calculation method",
    )
    display.add_argument(
        "-A",
        "--no-angles",
        action="store_true",
        default=config_defaults.get("no_angles", False),
        help="don't print Ascendant or Midheaven",
    )
    display.add_argument(
        "-G",
        "--no-geo",
        action="store_true",
        default=config_defaults.get("no_geo", False),
        help="don't print coordinates",
    )


def add_config_options(parser):
    """Add configuration options to parser (only --save-config now)."""
    config = parser.add_argument_group("configuration")
    config.add_argument(
        "--save-config",
        action="store_true",
        help="save current location settings as defaults",
    )


def handle_save_config_action(args):
    """Handle --save-config action for subcommands that support it."""
    if hasattr(args, "save_config") and args.save_config:
        run_save(args)


def handle_global_actions(args_list):
    """Handle global actions that should exit before subcommand parsing."""
    # Handle --list-offsets
    if "--list-offsets" in args_list:
        print("\nAyanamsa offsets:\n")
        for i, key in enumerate(AYANAMSAS.keys()):
            print(f"{i:2}: {key}")
        sys.exit(0)

    # Handle --list-zones
    if "--list-zones" in args_list:
        import zoneinfo

        print("\nAvailable IANA time zones:\n")
        # Get all available zones, sorted
        zones = sorted(zoneinfo.available_timezones())
        for zone in zones:
            print(zone)
        sys.exit(0)

    # Handle --show-config
    if "--show-config" in args_list:
        # Create a minimal args object for run_show
        class ConfigArgs:
            pass

        run_show(ConfigArgs())
        sys.exit(0)


def offset_type(value):
    """Select ayanamsa from index 0-46; no string support possibly ever."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Offset must be an integer, got '{value}'.")
    if not (0 <= ivalue <= 46):
        raise argparse.ArgumentTypeError(
            f"Offset must be between 0 and 46, got {ivalue}."
        )
    return ivalue


def parse_month(value: str):
    """For cal command"""
    # Try numeric
    try:
        month_num = int(value)
        if 1 <= month_num <= 12:
            return month_num
    except ValueError:
        pass

    # Try name or abbreviation (case-insensitive)
    value = value.lower()
    months = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}
    abbrevs = {name.lower(): i for i, name in enumerate(calendar.month_abbr) if name}

    lookup = {**months, **abbrevs}
    if value in lookup:
        return lookup[value]

    raise ValueError(f"Invalid month: {value}")


def parse_arguments(args=None):
    # load config defaults first
    config_defaults = load_config_defaults()

    if args is None:
        args = sys.argv[1:]

    # Handle global actions BEFORE any parsing
    handle_global_actions(args)

    # global flags for locale and ayanamsa
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-o",
        "--offset",
        type=int,
        default=config_defaults.get("offset"),
        help="sidereal ayanamsa index or None for tropical",
    )

    parser = EphemParser(
        prog="ephem",
        description="""Ephem is a tool for calculating astrological charts and monthly ephemerides.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add global options
    parser.add_argument(
        "--list-offsets",
        action="store_true",
        help="list all ayanamsa offsets as index:key pairs",
    )
    parser.add_argument(
        "--list-zones",
        action="store_true",
        help="list all available IANA time zone identifiers",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="display current configuration and exit",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # now
    now_parser = subparsers.add_parser(
        "now", help="🌌 calculate the chart of the moment", parents=[parent_parser]
    )
    now_parser.set_defaults(func=now.run)
    now_parser.add_argument("--lat", "-y", type=float, help="latitude")
    now_parser.add_argument("--lng", "-x", type=float, help="longitude")
    now_parser.add_argument(
        "-s",
        "--shift",
        type=str,
        help="shift time forward or backward, e.g. 2h, -30m, 1.5d, 4w (default is hours)",
    )
    now_parser.add_argument(
        "-z",
        "--timezone",
        type=str,
        help="IANA time zone name, e.g. 'America/New_York'",
    )
    now_parser.add_argument(
        "--save", action="store_true", help="save to chart database"
    )
    add_display_options(now_parser, config_defaults)
    add_config_options(now_parser)

    # cast
    cast_parser = subparsers.add_parser(
        "cast", help="🎂 calculate an event or birth chart", parents=[parent_parser]
    )
    cast_parser.set_defaults(func=cast.run)
    cast_parser.add_argument(
        "event",
        nargs="*",
        metavar="DATE [TIME] [TITLE]",
        help="date, optional time and chart title, e.g. '2025-08-09 7:54 Aquarius Full Moon'",
    )
    cast_parser.add_argument("--lat", "-y", type=float, help="latitude")
    cast_parser.add_argument("--lng", "-x", type=float, help="longitude")
    cast_parser.add_argument(
        "-z",
        "--timezone",
        type=str,
        help="IANA time zone name, e.g. 'America/New_York'",
    )
    cast_parser.add_argument(
        "--save", action="store_true", help="save to chart database"
    )
    add_display_options(cast_parser, config_defaults)
    add_config_options(cast_parser)

    # cal
    today = date.today()
    cal_parser = subparsers.add_parser(
        "cal",
        help="📅 calculate ephemeris table for a given or the current month",
        parents=[parent_parser],
    )
    cal_parser.add_argument(
        "year", type=int, nargs="?", default=today.year, help="year as an integer"
    )
    cal_parser.add_argument(
        "month",
        type=parse_month,
        nargs="?",
        default=today.month,
        help="month as an integer (1–12) or a string (e.g. 'Aug')",
    )
    cal_parser.add_argument(
        "-a",
        "--ascii",
        action="store_true",
        help="use ASCII text instead of Unicode glyphs",
    )
    cal_parser.set_defaults(func=cal.run)

    # data
    data_parser = subparsers.add_parser("data", help="🗃️ manage chart database")
    data_subparsers = data_parser.add_subparsers(dest="data_cmd", required=True)

    view_parser = data_subparsers.add_parser("view", help="show chart database")
    view_parser.set_defaults(func=data.print_charts)

    load_parser = data_subparsers.add_parser(
        "load", help="load chart from database", parents=[parent_parser]
    )
    load_parser.add_argument("id", type=int, help="chart ID to load")
    add_display_options(load_parser, config_defaults)
    load_parser.set_defaults(func=data.run_loaded_chart)

    delete_parser = data_subparsers.add_parser(
        "delete", help="delete chart from database"
    )
    delete_parser.add_argument("id", type=int, help="delete chart by ID ")
    delete_parser.set_defaults(func=data.delete_chart_cmd)

    sync_parser = data_subparsers.add_parser(
        "sync", help="sync YAML charts with database"
    )
    sync_parser.set_defaults(func=data.yaml_sync_cmd)

    # show splash text and help if no args given
    if len(args) == 0:
        print(splash_text())
        parser.print_help()
        sys.exit(0)

    parsed = parser.parse_args(args)

    # validate offset range
    if (
        hasattr(parsed, "offset")
        and parsed.offset is not None
        and not (0 <= int(parsed.offset) <= 46)
    ):
        print("\n❌ Error: --offset must be between 0 and 46.", file=sys.stderr)
        sys.exit(1)

    # validate 'cast' requires at least 1 event arg (DATE)
    if parsed.command == "cast" and (not parsed.event or len(parsed.event) < 1):
        print(
            "\n❌ Error: `cast` needs at minimum a DATE argument. Type `ephem cast --help` for more info.",
            file=sys.stderr,
        )
        sys.exit(1)

    return parsed


def main():
    args = parse_arguments()

    if hasattr(args, "func"):
        # Handle --save-config BEFORE running the main command
        if args.command in ["now", "cast"]:
            handle_save_config_action(args)

        # Dispatch to the subcommand's run function
        args.func(args)
    else:
        # No subcommand provided; show help and exit with error
        print(splash_text())
        # Re-parse with just help, so you still get the global help text
        EphemParser(prog="ephem").print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
