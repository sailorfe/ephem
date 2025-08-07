from datetime import datetime, timezone
import re
import swisseph as swe

def parse_shift_to_julian_delta(shift_str):
    if not shift_str:
        return 0.0

    # default unit is hours
    pattern = r"^\s*(-?\d*\.?\d*)([dhm]?)\s*$"
    match = re.match(pattern, shift_str.lower())

    if not match:
        raise ValueError(f"Invalid shift format: {shift_str}")

    value, unit = match.groups()
    value = float(value)

    if unit == "d":    # days
        return value
    elif unit == "h" or unit == "":  # hours (or no unit)
        return value / 24
    elif unit == "m":  # minutes
        return value / 1440
    else:
        raise ValueError(f"Unknown unit in shift: {unit}")


def get_julian_days(date_str, time_str, args):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    jd_now = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)
    jd_then = jd_now - (1 / 1440)

    if args.command == "now" and args.shift:
        jd_now += parse_shift_to_julian_delta(args.shift)

    return jd_now, jd_then


def jd_to_datetime(jd_now):
    y, m, d, h = swe.revjul(jd_now)
    hours = int(h)
    minutes = int((h - hours) * 60)
    seconds = int(((h - hours) * 60 - minutes) * 60)
    dt = datetime(y, m, d, hours, minutes, seconds, tzinfo=timezone.utc)
    return datetime.strftime(dt, "%Y-%m-%d %H:%M")
