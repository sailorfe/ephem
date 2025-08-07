import configparser
import os

def load_config_defaults():
    config = configparser.ConfigParser()
    path = os.path.expanduser("~/.config/chart/chart.ini")
    if os.path.exists(path):
        config.read(path)
        defaults = {}
        if 'location' in config:
            if 'lat' in config['location']:
                defaults['lat'] = float(config['location']['lat'])
            if 'lng' in config['location']:
                defaults['lng'] = float(config['location']['lng'])
        if 'display' in config:
            for key, value in config['display'].items():
                # booleans being weird
                if value.lower() in ['true', 'false']:
                    defaults[key.replace('-', '_')] = config['display'].getboolean(key)
                else:
                    defaults[key.replace('-', '_')] = value
        return defaults
    return {}


def save_config(args):
    config = configparser.ConfigParser()

    config['location'] = {}
    if args.lat is not None:
        config['location']['lat'] = str(args.lat)
    if args.lng is not None:
        config['location']['lng'] = str(args.lng)

    config['display'] = {}
    display_keys = ['classical', 'brief', 'verbose', 'no_color', 'node']
    for key in display_keys:
        value = getattr(args, key, None)
        if value is not None:
            config['display'][key.replace('_', '-')] = str(value)

    path = os.path.expanduser("~/.config/chart/chart.ini")
    with open(path, 'w') as configfile:
        config.write(configfile)

    print(f"✅ Saved config to {path}")
