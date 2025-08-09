from .config import load_config_defaults

def get_locale(args):
    if args.lat is not None and args.lng is not None:
        return args.lat, args.lng, False, False  # explicit location

    config = load_config_defaults()
    if args.lat is None and args.lng is None:
        lat = config.get("lat")
        lng = config.get("lng")

        if lat is not None and lng is not None:
            try:
                return float(lat), float(lng), False, True  # still explicit!
            except ValueError:
                pass

        return 0.0, 0.0, True, False  # approximate location
