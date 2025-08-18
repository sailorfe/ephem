import os
import configparser
from pathlib import Path

def get_config_path():
    """Get the config file path using XDG spec."""
    config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    return Path(config_home) / "ephem" / "ephem.ini"

def load_config_defaults():
    """Load and return config values as a dict."""
    config = configparser.ConfigParser()
    path = get_config_path()

    if not path.exists():
        return {}

    config.read(path)
    defaults = {}

    # Load only location settings
    if 'location' in config:
        if 'lat' in config['location']:
            defaults['lat'] = float(config['location']['lat'])
        if 'lng' in config['location']:
            defaults['lng'] = float(config['location']['lng'])

    return defaults

def run_save(args):
    """Save location settings from command line args."""
    if args.lat is None and args.lng is None:
        print("No location provided. Use --lat and/or --lng to set default location.")
        return

    config = configparser.ConfigParser()
    config.read(get_config_path())

    # Save only location settings
    if 'location' not in config:
        config['location'] = {}
    if args.lat is not None:
        config['location']['lat'] = str(args.lat)
    if args.lng is not None:
        config['location']['lng'] = str(args.lng)

    # Write config file
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as configfile:
        config.write(configfile)

    print(f"Saved location settings to {path}")

def run_show(args):
    """Display current config file contents."""
    path = get_config_path()
    if not path.exists():
        print("No config file found.")
        return

    config = configparser.ConfigParser()
    config.read(path)

    if 'location' in config:
        print("\nLocation defaults:")
        if 'lat' in config['location']:
            print(f"  Latitude:  {config['location']['lat']}")
        if 'lng' in config['location']:
            print(f"  Longitude: {config['location']['lng']}")
    else:
        print("No location defaults set.")
