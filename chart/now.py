from datetime import datetime, timezone
import geocoder


def get_moment(args):
    if args.command == "chart" and args.now is not None:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")

    elif args.command == "chart" and args.event:
        return args.event

    else:
        raise ValueError("Unrecognized command for get_moment.")


def get_locale(args):
    if args.command == "chart" and args.now is not None:
        if len(args.now) == 2:
            return float(args.now[0]), float(args.now[1])
        elif args.now == []:
            ip = geocoder.ip("me")
            if ip.ok:
                return ip.latlng
            else:
                raise RuntimeError("Cannot fetch location from IP. Please input coordinates manually.")
        else:
            raise ValueError("--now takes 0 or 2 arguments: latitude longitude")

    elif args.command == "chart" and args.event:
        return float(args.event[2]), float(args.event[3])

    else:
        raise ValueError("Unrecognized command for get_locale.")
