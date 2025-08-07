from datetime import datetime, timezone
import geocoder

def get_now():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")

def get_here(args):
    if args.command == "fixed":
        return float(args.fixed[0]), float(args.fixed[1])
    else:
        ip = geocoder.ip("me")
        return ip.latlng
