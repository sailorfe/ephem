from datetime import datetime, timezone
import geocoder


def get_moment(args):
    if args.date is not None and args.time is not None:
        return args.date, args.time
    else:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")


def get_locale(args):
    if args.lat is not None and args.lng is not None:
        return args.lat, args.lng
    else:
        ip = geocoder.ip("me")
        return ip.latlng if ip.ok else print (f"Cannot fetch location from IP. Input coordinates manually.")
