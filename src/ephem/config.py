import os
import tomllib
from pathlib import Path
from typing import Dict, Any, Optional, Callable

try:
    import tomli_w
except ImportError:
    tomli_w = None


def get_config_path():
    """Get the config file path using XDG spec."""
    config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    return Path(config_home) / "ephem" / "ephem.toml"


# FUNCTIONAL OVERHAUL YEAAAAAAH
def parse_float_field(value: Any) -> Optional[float]:
    """Safely parse a float value."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_bool_field(value: Any) -> bool:
    """Safely parse a bool value."""
    return bool(value)


def validate_choice_field(choices: list) -> Callable[[Any], Optional[str]]:
    """Return a validator function for choice fields."""

    def validator(value: Any) -> Optional[str]:
        return value if value in choices else None

    return validator


def validate_offset_field(value: Any) -> Optional[int]:
    """Validate zodiac offset field (0-46 or None)."""
    if value is None:
        return None
    try:
        offset_val = int(value)
        return offset_val if 0 <= offset_val <= 46 else None
    except (ValueError, TypeError):
        return None


FIELD_PARSERS = {
    ("location", "lat"): parse_float_field,
    ("location", "lng"): parse_float_field,
    ("zodiac", "offset"): validate_offset_field,
    ("display", "node"): validate_choice_field(["true", "mean"]),
    ("display", "theme"): validate_choice_field(["sect", "mode", "element"]),
    ("display", "no-geo"): parse_bool_field,
    ("display", "no-angles"): parse_bool_field,
    ("display", "classical"): parse_bool_field,
    ("display", "ascii"): parse_bool_field,
    ("display", "no-color"): parse_bool_field,
}


CLI_TO_CONFIG_MAPPING = {
    "no_geo": ("display", "no-geo"),
    "no_angles": ("display", "no-angles"),
    "no_color": ("display", "no-color"),
    "classical": ("display", "classical"),
    "ascii": ("display", "ascii"),
    "node": ("display", "node"),
    "theme": ("display", "theme"),
    "lat": ("location", "lat"),
    "lng": ("location", "lng"),
    "offset": ("zodiac", "offset"),
}


def load_config_defaults():
    """Load and return config values as a dict using functional approach."""
    path = get_config_path()

    if not path.exists():
        return {}

    try:
        with open(path, "rb") as f:
            config = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError) as e:
        print(f"Warning: Could not load config file {path}: {e}")
        return {}

    defaults = {}

    # Process all fields using the parser mapping
    for (section, key), parser in FIELD_PARSERS.items():
        if section in config and key in config[section]:
            parsed_value = parser(config[section][key])
            if parsed_value is not None:
                # Convert config key back to CLI arg name
                cli_key = next(
                    (
                        cli_key
                        for cli_key, (sec, k) in CLI_TO_CONFIG_MAPPING.items()
                        if sec == section and k == key
                    ),
                    key.replace("-", "_"),  # fallback
                )
                defaults[cli_key] = parsed_value

    return defaults


def validate_config_values(lat: Optional[float], lng: Optional[float]):
    """Raise ValueError if latitude or longitude are out of bounds."""
    if lat is not None and not -90 <= lat <= 90:
        raise ValueError(f"Invalid latitude {lat}, must be between -90 and 90")
    if lng is not None and not -180 <= lng <= 180:
        raise ValueError(f"Invalid longitude {lng}, must be between -180 and 180")


def should_save_value(attr: str, value: Any) -> bool:
    """Determine if a value should be saved to config."""
    if value is None:
        return False

    # Boolean flags: save if True
    bool_flags = {"no_geo", "no_angles", "classical", "ascii", "no_color"}
    if attr in bool_flags:
        return bool(value)

    # Choice options: save if not default
    choice_defaults = {"node": "true", "theme": "sect"}
    if attr in choice_defaults:
        return value != choice_defaults[attr]

    # Location and zodiac: always save if provided
    return True


def update_config_section(
    config: Dict[str, Any], section: str, updates: Dict[str, Any]
):
    """Functionally update a config section."""
    if updates:
        if section not in config:
            config[section] = {}
        config[section].update(updates)


def run_save(args):
    """Save location settings from command line args using functional approach."""

    # Collect all potential saves
    saves_to_make = {
        attr: getattr(args, attr, None)
        for attr in CLI_TO_CONFIG_MAPPING.keys()
        if hasattr(args, attr)
    }

    # Filter to only values that should be saved
    filtered_saves = {
        attr: value
        for attr, value in saves_to_make.items()
        if should_save_value(attr, value)
    }

    if not filtered_saves:
        print(
            "No settings provided. Use location, zodiac, or display options to save configuration."
        )
        return

    if tomli_w is None:
        print("Error: tomli_w package is required for saving configuration.")
        print("Install it with: pip install tomli_w")
        return

    path = get_config_path()

    # Load existing config
    config = {}
    if path.exists():
        try:
            with open(path, "rb") as f:
                config = tomllib.load(f)
        except (tomllib.TOMLDecodeError, OSError):
            config = {}

    # Group updates by section
    section_updates = {}
    for attr, value in filtered_saves.items():
        section, key = CLI_TO_CONFIG_MAPPING[attr]
        if section not in section_updates:
            section_updates[section] = {}
        section_updates[section][key] = value

    # Apply updates to config
    for section, updates in section_updates.items():
        update_config_section(config, section, updates)

    # Write config file
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "wb") as f:
            tomli_w.dump(config, f)

        saved_sections = list(section_updates.keys())
        section_names = {
            "location": "location settings",
            "zodiac": "zodiac preferences",
            "display": "display preferences",
        }
        saved_items = [section_names[section] for section in saved_sections]

        print(f"Saved {' and '.join(saved_items)} to {path}")

    except OSError as e:
        print(f"Error saving config file: {e}")


def run_show(args):
    """Display current config file contents."""
    path = get_config_path()
    if not path.exists():
        print("No config file found.")
        return

    try:
        with open(path, "rb") as f:
            config = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError) as e:
        print(f"Error reading config file: {e}")
        return

    has_settings = False

    if "location" in config and config["location"]:
        print("\nLocation defaults:")
        location = config["location"]
        if "lat" in location:
            print(f"  Latitude:  {location['lat']}")
        if "lng" in location:
            print(f"  Longitude: {location['lng']}")
        has_settings = True

    if "zodiac" in config and config["zodiac"]:
        print("\nZodiac system:")
        zodiac = config["zodiac"]
        if "offset" in zodiac:
            offset_val = zodiac["offset"]
            if offset_val is None:
                print("  System: Tropical")
            else:
                # Import here to avoid circular imports
                from .constants import AYANAMSAS

                try:
                    ayanamsa_name = list(AYANAMSAS.keys())[offset_val]
                    print(f"  System: Sidereal — {ayanamsa_name} (index {offset_val})")
                except IndexError:
                    print(f"  System: Sidereal — Unknown ayanamsa (index {offset_val})")
        has_settings = True

    if "display" in config and config["display"]:
        print("\nDisplay preferences:")
        display = config["display"]

        # Boolean flags
        bool_flags = {
            "no-geo": "Hide coordinates",
            "no-angles": "Hide angles",
            "no-color": "Disable ANSI colors",
            "classical": "Classical planets only",
            "ascii": "ASCII mode (no Unicode glyphs)",
        }
        for key, description in bool_flags.items():
            if key in display and display[key]:
                print(f"  {description}: enabled")

        # Choice options
        if "node" in display:
            print(f"  Node calculation: {display['node']}")
        if "theme" in display:
            print(f"  Color theme: {display['theme']}")

        has_settings = True

    if not has_settings:
        print("No settings configured.")
