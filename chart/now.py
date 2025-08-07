from datetime import datetime, timezone
import geocoder

def get_moment(args):
    if args.command in ("asc", "chart") and not args.event:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")

    elif args.command == "chart" and args.event:
        return args.event[0], args.event[1]

    else:
        raise ValueError("Unrecognized command or missing data in get_moment()")


def get_locale(args):
    if args.command == "chart":
        if args.event:
            return float(args.event[2]), float(args.event[3])
        elif args.coordinates:
            if len(args.coordinates) != 2:
                raise ValueError("Please provide both latitude and longitude, or none.")
            return float(args.coordinates[0]), float(args.coordinates[1])
        else:
            ip = geocoder.ip("me")
            if ip.ok:
                return ip.latlng
            else:
                raise RuntimeError("Cannot fetch location from IP. Please provide coordinates.")

    else:
        raise ValueError("Unrecognized command or missing data in get_locale()")
