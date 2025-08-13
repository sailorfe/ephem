import argparse
import sys
from .commands import now, cast, asc, config
from .commands.config import load_config_defaults


def splash_text():
    return """
                      ,dPYb,                                
                      IP'`Yb                                
                      I8  8I                                
                      I8  8'                                
  ,ggg,   gg,gggg,    I8 dPgg,    ,ggg,    ,ggg,,ggg,,ggg,  
 i8" "8i  I8P"  "Yb   I8dP" "8I  i8" "8i  ,8" "8P" "8P" "8, 
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
        self.exit(2, f"\n❌ Error: {message}\n\nUse -h or --help for more information.\n")


def add_display_options(parser):
    display = parser.add_argument_group('display options')
    display.add_argument('--node', choices=['true', 'mean'], default='true',
                         help="choose lunar node calculation method")
    display.add_argument('--theme', choices=['sect', 'element', 'mode'], default='sect',
                         help="choose ANSI color theme")
    display.add_argument('--format', choices=['glyphs', 'names', 'short'],
                         help="choose display format: all glyphs, full planet and sign names, truncated signs with planetary glyphs. Default mixes planet glyphs with full sign names.")
    display.add_argument('-c', '--classical', action='store_true',
                         help="exclude Uranus through Pluto")
    display.add_argument('-n', '--no-angles', action='store_true',
                         help="don't print Ascendant or Midheaven")
    display.add_argument('-a', '--anonymize', action='store_true',
                         help="don't print coordinates")
    display.add_argument('-b', '--bare', action='store_true',
                         help="disable ANSI colors")


def parse_arguments(args=None):
    load_config_defaults()

    parser = EphemParser(
        prog='ephem',
        description=(
            "ephem is an astrology CLI with clear, readable table output remniscent of print ephemerides."
            ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # now
    now_parser = subparsers.add_parser('now', help="calculate the chart of the moment 🌌")
    now_parser.set_defaults(func=now.run)
    now_parser.add_argument('-y', '--lat', type=float, help="latitude")
    now_parser.add_argument('-x', '--lng', type=float, help="longitude")
    now_parser.add_argument('-s', '--shift', type=str,
                            help="shift time forward or backward, e.g. 2h, -30m, 1.5d, 4w (default is hours)")
    now_parser.add_argument('-z', '--timezone', type=str, help="IANA time zone name, e.g. 'America/New_York'")
    add_display_options(now_parser)

    # cast
    cast_parser = subparsers.add_parser('cast', help="calculate an event or birth chart 🎂")
    cast_parser.set_defaults(func=cast.run)
    cast_parser.add_argument('event', nargs="*", metavar="DATE [TIME] [TITLE]",
                             help="date, optional time and chart title, e.g. '2025-08-09 7:54 Aquarius Full Moon'")
    cast_parser.add_argument('-y', '--lat', type=float, help="latitude")
    cast_parser.add_argument('-x', '--lng', type=float, help="longitude")
    cast_parser.add_argument('-z', '--timezone', type=str, help="IANA time zone name, e.g. 'America/New_York'")

    add_display_options(cast_parser)

    # asc
    asc_parser = subparsers.add_parser('asc', help="print the current local ascendant 🌅")
    asc_parser.set_defaults(func=asc.run)
    asc_parser.add_argument('-y', '--lat', type=float, help="latitude")
    asc_parser.add_argument('-x', '--lng', type=float, help="longitude")
    asc_parser.add_argument('-g', '--glyphs', action='store_true', help='show glyphs instead of truncated sign names')

    # config
    config.add_subparser(subparsers)


    if args is None:
        args = sys.argv[1:]

    # show splash if no args given at all
    if len(args) == 0:
        print(splash_text())
        print("✨ Usage: ephem {now,cast,asc,config} [options]\nType `ephem --help` for more info.")
        sys.exit(0)

    parsed = parser.parse_args(args)

    # validate 'cast' requires at least 1 event arg (DATE)
    if parsed.command == "cast" and (not parsed.event or len(parsed.event) < 1):
        print("\n❌ Error: `cast` needs at minimum a DATE argument. Type `ephem cast --help` for more info.", file=sys.stderr)
        sys.exit(1)

    return parsed


def main():
    args = parse_arguments()

    if not vars(args):
        args.print_help()
        args.exit(1)

    if hasattr(args, "func"):
        # Dispatch to the subcommand's run function
        args.func(args)
    else:
        # No subcommand provided; show help and exit with error
        args.print_help()
        args.exit(1)


if __name__ == "__main__":
    main()
