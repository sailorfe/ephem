from datetime import datetime, timezone
import configparser
import os

def get_moment(args):
    if args.command == "cast":
        if args.date and args.time:
            return args.date, args.time, False  # not approximate
        if args.date and not args.time:
            print("🕛 No time provided; using UTC noon and not printing angles.")
            return args.date, "12:00", True  # approximate
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), False


def get_locale(args):
    if args.lat is not None and args.lng is not None:
        return args.lat, args.lng, False  # explicit location

    config_path = os.path.expanduser("~/.config/chart/chart.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    lat = lng = None
    if config.has_section("location"):
        lat = config["location"].get("lat")
        lng = config["location"].get("lng")

    if lat and lng:
        if args.no_coordinates:
            print(f"📍 Using location from config")
        else:
            print(f"📍 Using location from config: {lat}, {lng}")
        try:
            return float(lat), float(lng), True  # approximate
        except ValueError:
            print("⚠️ Invalid config location values; defaulting to 0,0.")

    print("🌐 No coordinates provided or found in config; not printing angles.")
    return 0.0, 0.0, True  # definitely approximate
