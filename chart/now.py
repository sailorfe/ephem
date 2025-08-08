from datetime import datetime, timezone
from .config import load_config_defaults

def get_moment(args):
    if args.command == "cast":
        if args.date and args.time:
            return args.date, args.time, False  # explicit time
        if args.date and not args.time:
            return args.date, "12:00", True # approximate time
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), False


def get_locale(args):
    if args.lat is not None and args.lng is not None:
        return args.lat, args.lng, False, False  # explicit location

    config = load_config_defaults()

    if args.lat is None and args.lng is None:
        lat = config.get("lat")
        lng = config.get("lng")

        if lat is not None and lng is not None:
            try:
                return float(lat), float(lng), False, True  # still explicit!
            except ValueError:
                pass

        return 0.0, 0.0, True, False  # approximate location
