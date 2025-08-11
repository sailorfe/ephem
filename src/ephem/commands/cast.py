from datetime import datetime
from zoneinfo import ZoneInfo
from ephem.utils.locale import get_locale
from ephem.julian import get_julian_days, jd_to_datetime
from ephem.horoscope import get_planets, get_angles, build_horoscope
from ephem.display import format_chart


def parse_event(event_args):
    """Reads event positional arg output based on length."""
    if len(event_args) == 0:
        return None, None, None
    elif len(event_args) == 1:
        return event_args[0], None, None
    elif len(event_args) == 2:
        return event_args[0], event_args[1], None
    else:
        return event_args[0], event_args[1], " ".join(event_args[2:])


def get_moment(date_str, time_str=None, tz_str=None):
    approx_time = False

    # default time to noon if missing
    if not time_str:
        time_str = "12:00"
        approx_time = True

    # parse date parts
    year, month, day = map(int, date_str.split("-"))

    # parse time parts, allow 1 or 2 digits for hour, minute
    hour_str, minute_str = time_str.split(":")
    hour = int(hour_str)
    minute = int(minute_str)

    # build naive datetime
    dt_naive = datetime(year, month, day, hour, minute)

    # assign timezone (or UTC default)
    tz = ZoneInfo(tz_str) if tz_str else ZoneInfo("UTC")
    dt_local = dt_naive.replace(tzinfo=tz)

    # convert to UTC
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))

    return dt_local, dt_utc, approx_time


def run(args):
    date, time, title = parse_event(args.event)
    dt_local, dt_utc, approx_time = get_moment(date, time, args.timezone)
    lat, lng, approx_locale, config_locale = get_locale(args)
    jd_now, jd_then, *_ = get_julian_days(dt_utc, args)
    planets = get_planets(jd_now, jd_then)
    angles = get_angles(jd_now, lat, lng)
    horoscope = build_horoscope(planets, angles)

    output = format_chart(
        args, title, lat, lng,
        dt_local, dt_utc,  # pass both local and UTC datetimes
        horoscope, planets,
        approx_time, approx_locale, config_locale
    )

    if output is not None:
        for line in output:
            print(line)
    # else: Rich output already printed directly

