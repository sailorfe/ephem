from datetime import datetime, timezone, timedelta
import re
import swisseph as swe


def parse_shift_to_timedelta(shift_str):
    if not shift_str:
        return timedelta(0)

    pattern = r"^\s*(-?\d*\.?\d*)([wdhm]?)\s*$"
    match = re.match(pattern, shift_str.lower())
    if not match:
        raise ValueError(f"Invalid shift format: {shift_str}")

    value_str, unit = match.groups()
    value = float(value_str)

    if unit == "w":
        return timedelta(days=value * 7)
    elif unit == "d":
        return timedelta(days=value)
    elif unit == "h" or unit == "":
        return timedelta(hours=value)
    elif unit == "m":
        return timedelta(minutes=value)
    else:
        raise ValueError(f"Unknown unit in shift: {unit}")


def get_julian_days(dt_utc, args):
    shift_td = timedelta(0)
    if getattr(args, "shift", None):
        shift_td = parse_shift_to_timedelta(args.shift)

    dt_shifted = dt_utc + shift_td

    frac_hour = (
        dt_shifted.hour
        + dt_shifted.minute / 60
        + dt_shifted.second / 3600
        + dt_shifted.microsecond / 3_600_000_000
    )
    jd_now = swe.julday(dt_shifted.year, dt_shifted.month, dt_shifted.day, frac_hour)
    jd_then = jd_now - (1 / 1440)

    return jd_now, jd_then, dt_shifted  # return shifted datetime for display too


def jd_to_datetime(jd_now):
    """Converts astronomical Julian day to a formatted UTC datetime string."""
    y, m, d, h = swe.revjul(jd_now)
    hours = int(h)
    minutes = int((h - hours) * 60)
    seconds = int(((h - hours) * 60 - minutes) * 60)
    dt = datetime(y, m, d, hours, minutes, seconds, tzinfo=timezone.utc)
    return datetime.strftime(dt, "%Y-%m-%d %H:%M")


def sidereal_time(jd_now):
    st = swe.sidtime(jd_now)
    return st
