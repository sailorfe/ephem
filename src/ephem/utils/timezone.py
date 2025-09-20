from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def validate_timezone(tz_name):
    """
    Validates if tz_name is a valid IANA timezone string.
    Returns True if valid, False otherwise.
    """
    if not tz_name:
        return False
    try:
        ZoneInfo(tz_name)
        return True
    except ZoneInfoNotFoundError:
        return False
