from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def validate_timezone(tz_name):
    if not tz_name:
        return False
    try:
        ZoneInfo(tz_name)
        return True
    except ZoneInfoNotFoundError:
        return False
