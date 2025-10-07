from datetime import datetime
from zoneinfo import ZoneInfo
from ephem.utils.locale import get_locale, InvalidCoordinatesError
from ephem.utils.year import validate_year
from ephem import sweph
from ephem.display import format_chart
from ephem.db import add_chart, create_tables
import re
import sys

TIME_RE = re.compile(r"^(?P<h>\d{1,2})(:(?P<m>\d{1,2}))?(:(?P<s>\d{1,2}))?$")


def parse_time(time_str):
    """Returns (hour, minute, second) tuple or None if time_str is None."""
    if not time_str:
        return None

    match = TIME_RE.match(time_str.strip())
    if not match:
        raise ValueError(
            f"Time must be in H:MM, HH:MM, or HH:MM:SS format, got '{time_str}'"
        )

    hour = int(match.group("h"))
    minute = int(match.group("m") or 0)
    second = int(match.group("s") or 0)

    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError(f"Time out of range: {hour:02d}:{minute:02d}:{second:02d}")

    return hour, minute, second


def parse_event(event_args):
    """
    Reads event positional arg output based on length.
    Supports DATE [TIME] [TITLE].
    """
    if len(event_args) == 0:
        return None, None, None

    date = event_args[0]

    if len(event_args) == 1:
        return date, None, None

    second = event_args[1]
    # check if second arg is a time
    try:
        time = parse_time(second)
        title = " ".join(event_args[2:]) if len(event_args) > 2 else None
    except ValueError:
        time = None
        title = " ".join(event_args[1:])

    return date, time, title


def get_moment(date_str, time_str=None, tz_str=None):
    approx_time = time_str is None

    # parse time or use noon default
    if time_str:
        hour, minute, second = parse_time(time_str)
    else:
        hour, minute, second = 12, 0, 0

    # parse date
    try:
        year, month, day = map(int, date_str.split("-"))
    except ValueError:
        raise ValueError(f"Date must be in YYYY-MM-DD format, got '{date_str}'")

    validate_year(year)

    # build datetime
    dt_naive = datetime(year, month, day, hour, minute, second)
    tz = ZoneInfo(tz_str) if tz_str else ZoneInfo("UTC")
    dt_local = dt_naive.replace(tzinfo=tz)
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))

    return dt_local, dt_utc, approx_time


def main(args):
    date, time, raw_title = parse_event(args.event)
    time = parse_time(time)  # normalize or default

    # title remains None for display if empty
    title = raw_title.strip() if raw_title else None

    dt_local, dt_utc, approx_time = get_moment(date, time, args.timezone)
    lat, lng, approx_locale, config_locale = get_locale(args)

    jd_now, jd_then, *_ = sweph.get_julian_days(dt_utc, args)
    offset = getattr(args, "offset", None)
    planets = sweph.get_planets(jd_now, jd_then, offset)
    angles = sweph.get_angles(jd_now, lat, lng, offset)
    horoscope = sweph.build_horoscope(planets, angles)

    output = format_chart(
        args,
        title,
        lat,
        lng,
        dt_local,
        dt_utc,
        horoscope,
        planets,
        approx_time,
        approx_locale,
        config_locale,
    )

    if args.save:
        create_tables()
        name_to_save = (
            str(title).strip() if title and title.strip() else "Untitled Chart"
        )
        chart_id = add_chart(
            name=name_to_save,
            timestamp_utc=dt_utc.isoformat(),
            timestamp_input=dt_local.isoformat(),
            latitude=args.lat,
            longitude=args.lng,
        )
        print()
        print(f"Chart saved at index {chart_id}.")

    if output is not None:
        for line in output:
            print(line)


def run(args):
    try:
        main(args)
    except (ValueError, InvalidCoordinatesError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
