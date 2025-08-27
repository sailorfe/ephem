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

    return defaults

def run_save(args):
    """Save location settings from command line args."""
    if args.lat is None and args.lng is None:
        print("No location provided. Use --lat and/or --lng to set default location.")
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

    # Ensure location section exists
    if 'location' not in config:
        config['location'] = {}

    # Update location settings
    if args.lat is not None:
        config['location']['lat'] = args.lat
    if args.lng is not None:
        config['location']['lng'] = args.lng

    # Write config file
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, 'wb') as f:
            tomli_w.dump(config, f)
        print(f"Saved location settings to {path}")
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

    if 'location' in config and config['location']:
        print("\nLocation defaults:")
        location = config['location']
        if 'lat' in location:
            print(f"  Latitude:  {location['lat']}")
        if 'lng' in location:
            print(f"  Longitude: {location['lng']}")
    else:
        print("No location defaults set.")
