from ephem.config import load_config_defaults

class InvalidCoordinatesError(ValueError):
    """Raised when coordinates are outside valid ranges."""
    pass


def validate_coordinates(lat, lng):
    """Validate latitude and longitude values.

    Args:
        lat (float): Latitude value to validate (-90 to +90)
        lng (float): Longitude value to validate (-180 to +180)

    Raises:
        InvalidCoordinatesError: If coordinates are outside valid ranges
    """
    if not -90 <= lat <= 90:
        raise InvalidCoordinatesError(f"Latitude must be between -90° and +90°, got {lat}°")
    if not -180 <= lng <= 180:
        raise InvalidCoordinatesError(f"Longitude must be between -180° and +180°, got {lng}°")


def get_locale(args):
    if args.lat is not None and args.lng is not None:
        try:
            lat = float(args.lat)
            lng = float(args.lng)
            validate_coordinates(lat, lng)
            return lat, lng, False, False  # explicit location
        except ValueError as e:
            if isinstance(e, InvalidCoordinatesError):
                raise e
            raise ValueError("Latitude and longitude must be numeric values")

    config = load_config_defaults()
    if args.lat is None and args.lng is None:
        lat = config.get("lat")
        lng = config.get("lng")

        if lat is not None and lng is not None:
            try:
                lat = float(lat)
                lng = float(lng)
                validate_coordinates(lat, lng)
                return lat, lng, False, True  # still explicit!
            except (ValueError, InvalidCoordinatesError):
                pass

        return 0.0, 0.0, True, False  # approximate location
