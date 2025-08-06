from datetime import datetime, timezone
import geocoder


def get_moment(args):
    if args.date is not None and args.time is not None:
        return args.date, args.time
    # if given -a, a date, but no time, use UTC noon
    elif args.date is not None and args.approximate:
        return args.date, "12:00"
    else:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")


def get_locale(args):
    if args.lat is not None and args.lng is not None:
        return args.lat, args.lng
    else:
        ip = geocoder.ip("me")
        if ip.ok:
            return ip.latlng
        else:
            raise RuntimeError("Cannot fetch location from IP. Please input coordinates manually.")

