from datetime import datetime, timezone
import geocoder

def get_moment(args):
    if args.command == "chart" and not args.event:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")

    elif args.command == "chart" and args.event:
        if len(args.event) == 4:
            return args.event[0], args.event[1]
        elif args.approximate:
            if len(args.event) == 3:
                return args.event[0], "12:00"
            elif len(args.event) == 1:
                return args.event[0], "12:00"
            else:
                raise ValueError("Invalid number of arguments with --approximate. Use DATE, DATE LAT LNG, or DATE TIME LAT LNG.")
        else:
            raise ValueError("Missing time or place. Use --approximate to assume noon.")

    else:
        raise ValueError("Unrecognized command or missing data in get_moment()")


def get_locale(args):
    if args.command == "chart":
        if args.event:
            if len(args.event) == 4:
                return float(args.event[2]), float(args.event[3])
            elif len(args.event) == 3 and args.approximate:
                return float(args.event[1]), float(args.event[2])
            elif len(args.event) == 1 and args.approximate:
                ip = geocoder.ip("me")
                if ip.ok:
                    return ip.latlng
                else:
                    raise RuntimeError("Cannot fetch location from IP. Please provide coordinates.")
            else:
                raise ValueError("Invalid event arguments. Use DATE TIME LAT LNG or fewer with --approximate.")
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
