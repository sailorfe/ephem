from datetime import datetime, timezone
import geocoder

def get_moment(args):
    if args.command == "chart":
        if args.date is not None and args.time is not None:
            return args.date, args.time
        if args.date is not None and args.time is None:
            time_str = "12:00"
            return args.date, time_str
    else:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")

def get_locale(args):
    if args.lat is not None and args.lng is not None:
        return args.lat, args.lng
    elif args.command == "chart" and args.zero:
        return 0.0, 0.0
    else:
        ip = geocoder.ip("me")
        if ip.ok:
            return ip.latlng
        else:
            raise RuntimeError("No coordinates provided and IP geoloation failed.")
