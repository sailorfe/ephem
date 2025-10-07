from ephem.config import load_config_defaults


class InvalidCoordinatesError(ValueError):
    """Raised when coordinates are outside valid ranges."""

    pass


def validate_coordinates(lat, lng):
    """Validate and convert latitude and longitude values.

    Args:
        lat: Latitude value (-90 to +90), can be string or number
        lng: Longitude value (-180 to +180), can be string or number

    Returns:
        tuple: (float(lat), float(lng))

    Raises:
        InvalidCoordinatesError: If coordinates are invalid or out of range
    """
    try:
        lat = float(lat)
        lng = float(lng)
    except (ValueError, TypeError):
        raise InvalidCoordinatesError("Latitude and longitude must be numeric values")

    if not -90 <= lat <= 90:
        raise InvalidCoordinatesError(
            f"Latitude must be between -90° and +90°, got {lat}°"
        )
    if not -180 <= lng <= 180:
        raise InvalidCoordinatesError(
            f"Longitude must be between -180° and +180°, got {lng}°"
        )

    return lat, lng


def get_locale(args):
    # Handle partial coordinates
    if args.lat is not None and args.lng is None:
        args.lat = None
    elif args.lng is not None and args.lat is None:
        args.lng = None

    # Check explicit coordinates
    if args.lat is not None and args.lng is not None:
        lat, lng = validate_coordinates(args.lat, args.lng)
        return lat, lng, False, False

    if args.lat is not None or args.lng is not None:
        raise ValueError("Both latitude and longitude must be provided together")

    # Fall back to config
    config = load_config_defaults()
    lat = config.get("lat")
    lng = config.get("lng")

    if lat is not None and lng is not None:
        try:
            lat, lng = validate_coordinates(lat, lng)
            return lat, lng, False, True
        except InvalidCoordinatesError:
            pass  # fall through to default

    return 0.0, 0.0, True, False  # approximate location
