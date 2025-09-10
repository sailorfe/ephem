import os
import tomllib
from pathlib import Path

try:
    import tomli_w
except ImportError:
    tomli_w = None

def get_config_path():
    """Get the config file path using XDG spec."""
    config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    return Path(config_home) / "ephem" / "ephem.toml"

def load_config_defaults():
    """Load and return config values as a dict."""
    path = get_config_path()

    if not path.exists():
        return {}

    try:
        with open(path, 'rb') as f:
            config = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError) as e:
        print(f"Warning: Could not load config file {path}: {e}")
        return {}

    defaults = {}

    # Load location settings if they exist
    if 'location' in config:
        location = config['location']
        if 'lat' in location:
            try:
                defaults['lat'] = float(location['lat'])
            except (ValueError, TypeError):
                pass
        if 'lng' in location:
            try:
                defaults['lng'] = float(location['lng'])
            except (ValueError, TypeError):
                pass

    # Load display settings if they exist
    if 'display' in config:
        display = config['display']

        # Boolean options
        for bool_opt in ['no_geo', 'anonymize', 'no_angles', 'classical', 'ascii']:
            if bool_opt.replace('_', '-') in display:
                defaults[bool_opt] = bool(display[bool_opt.replace('_', '-')])
            elif bool_opt in display:
                defaults[bool_opt] = bool(display[bool_opt])

        # Choice options with validation
        if 'node' in display and display['node'] in ['true', 'mean']:
            defaults['node'] = display['node']

    # Load ayanamsa/zodiac settings if they exist
    if 'zodiac' in config:
        zodiac = config['zodiac']
        if 'offset' in zodiac:
            try:
                offset_val = zodiac['offset']
                # Validate offset range (0-46 or None for tropical)
                if offset_val is None or (isinstance(offset_val, int) and 0 <= offset_val <= 46):
                    defaults['offset'] = offset_val
            except (ValueError, TypeError):
                pass

    return defaults

def validate_config_values(lat: float | None, lng: float | None):
    """Raise ValueError if latitude or longitude are out of bounds."""
    if lat is not None and not -90 <= lat <= 90:
        raise ValueError(f"Invalid latitude {lat}, must be between -90 and 90")
    if lng is not None and not -180 <= lng <= 180:
        raise ValueError(f"Invalid longitude {lng}, must be between -180 and 180")


def run_save(args):
    """Save location, zodiac, and display settings from command line args."""
    # No settings? Early exit
    if (args.lat is None and args.lng is None and 
        (not hasattr(args, 'offset') or args.offset is None) and
        not any(hasattr(args, attr) and getattr(args, attr) is not None 
                for attr in ['bare', 'anonymize', 'no_angles', 'classical', 'node', 'theme', 'format'])):
        print("No settings provided. Use location, zodiac, or display options to save configuration.")
        return

    # tomli_w check
    if tomli_w is None:
        print("Error: tomli_w package is required for saving configuration.")
        print("Install it with: pip install tomli_w")
        return

    # Validate coordinates
    if args.lat is not None or args.lng is not None:
        validate_config_values(args.lat, args.lng)

    # Load existing config or start fresh
    path = get_config_path()
    config = {}
    if path.exists():
        try:
            with open(path, 'rb') as f:
                config = tomllib.load(f)
        except (tomllib.TOMLDecodeError, OSError):
            config = {}

    # Update location
    if args.lat is not None or args.lng is not None:
        if 'location' not in config:
            config['location'] = {}
        if args.lat is not None:
            config['location']['lat'] = args.lat
        if args.lng is not None:
            config['location']['lng'] = args.lng

    # Update zodiac
    zodiac_changed = False
    if hasattr(args, 'offset') and args.offset is not None:
        if 'zodiac' not in config:
            config['zodiac'] = {}
        config['zodiac']['offset'] = args.offset
        zodiac_changed = True

    # Update display settings
    display_changed = False
    display_attrs = {
        'no_geo': 'no-geo',
        'anonymize': 'anonymize', 
        'no_angles': 'no-angles',
        'classical': 'classical',
        'ascii': 'ascii',
        'node': 'node'
    }

    for attr, config_key in display_attrs.items():
        if hasattr(args, attr):
            value = getattr(args, attr)
            if value is not None and (
                (attr in ['no_geo', 'anonymize', 'no_angles', 'classical', 'ascii'] and value) or
                (attr == 'node' and value != 'true')
            ):
                if 'display' not in config:
                    config['display'] = {}
                config['display'][config_key] = value
                display_changed = True

    # Write config file
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, 'wb') as f:
            tomli_w.dump(config, f)

        saved_items = []
        if args.lat is not None or args.lng is not None:
            saved_items.append("location settings")
        if zodiac_changed:
            saved_items.append("zodiac preferences")
        if display_changed:
            saved_items.append("display preferences")

        if saved_items:
            print(f"Saved {' and '.join(saved_items)} to {path}")
        else:
            print("No changes to save.")

    except OSError as e:
        print(f"Error saving config file: {e}")

