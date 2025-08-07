from datetime import datetime, timezone
import configparser
import os
import geocoder

def get_moment(args):
    if args.command == "cast":
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

    if getattr(args, "zero", False):
        return 0.0, 0.0

    config = configparser.ConfigParser()
    path = os.path.expanduser("~/.config/chart/chart.ini")
    config.read(path)

    if "location" in config:
        config_defaults = config["location"]
        lat = config_defaults.get("lat")
        lng = config_defaults.get("lng")

        if lat is not None and lng is not None:
            print(f"📍 Using location from config: {lat}, {lng}")
            return float(lat), float(lng)

    print("🌐 No lat/lng provided or found in config; using IP-based location.")
    ip = geocoder.ip("me")
    if ip.ok and ip.latlng:
        return ip.latlng
    else:
        raise RuntimeError("❌ Geolocation failed and no location was provided.")
