from datetime import datetime, timezone
from .config import load_config_defaults

def get_moment(args, date=None, time=None):
    if args.command == "cast":
        if date and time:
            return date, time, False  # explicit time
        if date and not time:
            return date, "12:00", True # approximate time
        return None, None, True
    elif args.command == "now":
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
