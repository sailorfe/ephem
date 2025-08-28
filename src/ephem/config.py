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
        for bool_opt in ['bare', 'anonymize', 'no_angles', 'classical']:
            if bool_opt.replace('_', '-') in display:
                defaults[bool_opt] = bool(display[bool_opt.replace('_', '-')])
            elif bool_opt in display:
                defaults[bool_opt] = bool(display[bool_opt])

        # Choice options with validation
        if 'node' in display and display['node'] in ['true', 'mean']:
            defaults['node'] = display['node']

        if 'theme' in display and display['theme'] in ['sect', 'element', 'mode']:
            defaults['theme'] = display['theme']

        if 'format' in display and display['format'] in ['glyphs', 'names', 'short']:
            defaults['format'] = display['format']

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

def run_save(args):
    """Save location settings from command line args."""
    if (args.lat is None and args.lng is None and 
        (not hasattr(args, 'offset') or args.offset is None) and
        not any(hasattr(args, attr) and getattr(args, attr) is not None 
                for attr in ['bare', 'anonymize', 'no_angles', 'classical', 'node', 'theme', 'format'])):
        print("No settings provided. Use location, zodiac, or display options to save configuration.")
        return

    if tomli_w is None:
        print("Error: tomli_w package is required for saving configuration.")
        print("Install it with: pip install tomli_w")
        return

    path = get_config_path()

    # Load existing config or start with empty dict
    config = {}
    if path.exists():
        try:
            with open(path, 'rb') as f:
                config = tomllib.load(f)
        except (tomllib.TOMLDecodeError, OSError):
            # If config is corrupted, start fresh
            config = {}

    # Update location settings
    if args.lat is not None or args.lng is not None:
        if 'location' not in config:
            config['location'] = {}
        if args.lat is not None:
            config['location']['lat'] = args.lat
        if args.lng is not None:
            config['location']['lng'] = args.lng

    # Update zodiac settings
    zodiac_changed = False
    if hasattr(args, 'offset') and args.offset is not None:
        if 'zodiac' not in config:
            config['zodiac'] = {}
        config['zodiac']['offset'] = args.offset
        zodiac_changed = True

    # Update display settings
    display_changed = False
    display_attrs = {
        'bare': 'bare',
        'anonymize': 'anonymize', 
        'no_angles': 'no-angles',
        'classical': 'classical',
        'node': 'node',
        'theme': 'theme',
        'format': 'format'
    }

    for attr, config_key in display_attrs.items():
        if hasattr(args, attr):
            value = getattr(args, attr)
            # Only save if explicitly set (not just default values)
            if value is not None and (
                # For boolean flags, save if True
                (attr in ['bare', 'anonymize', 'no_angles', 'classical'] and value) or
                # For choice options, save if not default
                (attr == 'node' and value != 'true') or
                (attr == 'theme' and value != 'sect') or
                (attr == 'format' and value is not None)
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

def run_show(args):
    """Display current config file contents."""
    path = get_config_path()
    if not path.exists():
        print("No config file found.")
        return

    try:
        with open(path, 'rb') as f:
            config = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError) as e:
        print(f"Error reading config file: {e}")
        return

    has_settings = False

    if 'location' in config and config['location']:
        print("\nLocation defaults:")
        location = config['location']
        if 'lat' in location:
            print(f"  Latitude:  {location['lat']}")
        if 'lng' in location:
            print(f"  Longitude: {location['lng']}")
        has_settings = True

    if 'zodiac' in config and config['zodiac']:
        print("\nZodiac system:")
        zodiac = config['zodiac']
        if 'offset' in zodiac:
            offset_val = zodiac['offset']
            if offset_val is None:
                print(f"  System: Tropical")
            else:
                # Import here to avoid circular imports
                from .constants import AYANAMSAS
                try:
                    ayanamsa_name = list(AYANAMSAS.keys())[offset_val]
                    print(f"  System: Sidereal — {ayanamsa_name} (index {offset_val})")
                except IndexError:
                    print(f"  System: Sidereal — Unknown ayanamsa (index {offset_val})")
        has_settings = True

    if 'display' in config and config['display']:
        print("\nDisplay preferences:")
        display = config['display']
        
        # Boolean flags
        bool_flags = {
            'bare': 'Disable colors',
            'anonymize': 'Hide coordinates', 
            'no-angles': 'Hide angles',
            'classical': 'Classical planets only'
        }
        for key, description in bool_flags.items():
            if key in display and display[key]:
                print(f"  {description}: enabled")
        
        # Choice options
        if 'node' in display:
            print(f"  Node calculation: {display['node']}")
        if 'theme' in display:
            print(f"  Color theme: {display['theme']}")
        if 'format' in display:
            print(f"  Display format: {display['format']}")
        
        has_settings = True
    
    if not has_settings:
        print("No settings configured.")
