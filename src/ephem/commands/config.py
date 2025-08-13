import configparser
import os
import subprocess
import sys

def run_save(args):
    config = configparser.ConfigParser()
    config['location'] = {}
    if args.lat is not None:
        config['location']['lat'] = str(args.lat)
    if args.lng is not None:
        config['location']['lng'] = str(args.lng)

    config['display'] = {}
    display_keys = ['theme', 'format', 'node']
    for key in display_keys:
        value = getattr(args, key, None)
        if value is not None:
            config['display'][key.replace('_', '-')] = str(value)

    path = get_config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as configfile:
        config.write(configfile)

    print(f"Saved config to {path}")

def run_show(args):
    path = get_config_path()
    if not os.path.exists(path):
        print(f"No config file found at {path}")
        sys.exit(1)

    with open(path) as f:
        print(f.read())

def run_edit(args):
    path = get_config_path()
    editor = os.environ.get("EDITOR", "vi")

    if not os.path.exists(path):
        print(f"No config file found at {path}, creating new one.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w'):
            pass

    try:
        subprocess.run([editor, path])
    except Exception as e:
        print(f"Failed to open editor '{editor}': {e}")
        sys.exit(1)


def get_config_path():
    config_home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return os.path.join(config_home, "ephem", "ephem.ini")

def load_config_defaults():
    config = configparser.ConfigParser()
    path = get_config_path()
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
    display_keys = ['theme', 'format', 'node']
    for key in display_keys:
        value = getattr(args, key, None)
        if value is not None:
            config['display'][key.replace('_', '-')] = str(value)

    path = get_config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)  # check directory exists

    with open(path, 'w') as configfile:
        config.write(configfile)

    print(f"Saved config to {path}")


def add_subparser(subparsers):
    parser = subparsers.add_parser('config', help="view or modify stored preferences ⚙️")
    config_subparsers = parser.add_subparsers(dest='config_cmd', required=True)

    save_parser = config_subparsers.add_parser('save', help="save current settings as defaults")
    save_parser.add_argument('-y', '--lat', type=float, help="latitude")
    save_parser.add_argument('-x', '--lng', type=float, help="longitude")
    save_parser.add_argument('--theme', choices=['sect', 'element', 'mode'], help="color theme")
    save_parser.add_argument('--format', choices=['glyphs', 'names', 'short'], help="display format")
    save_parser.add_argument('--node', choices=['true', 'mean'], help="lunar node calculation method")
    save_parser.set_defaults(func=run_save)

    show_parser = config_subparsers.add_parser('show', help="display saved configuration")
    show_parser.set_defaults(func=run_show)

    edit_parser = config_subparsers.add_parser('edit', help="edit configuration file")
    edit_parser.set_defaults(func=run_edit)

    return parser
