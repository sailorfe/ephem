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
    # if given -a and a date but no latitude, use Null Island
    # i really don't know how necessary this is when -a hides angles entirely
    elif args.date is not None and args.lat is None and args.approximate:
        return (0, 0)
    else:
        ip = geocoder.ip("me")
        return ip.latlng if ip.ok else print (f"Cannot fetch location from IP. Input coordinates manually.")
