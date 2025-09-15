from datetime import datetime
from zoneinfo import ZoneInfo
from ephem.utils.locale import get_locale
from ephem import sweph
from ephem.display import format_chart
from ephem.db import add_chart, create_tables

def get_moment(tz_str=None):
    # current time in user's timezone or UTC
    tz = ZoneInfo(tz_str) if tz_str else ZoneInfo("UTC")

    dt_local = datetime.now(tz)
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))

    approx_time = False  # now is exact current time

    return dt_local, dt_utc, approx_time


def run(args):
    dt_local, dt_utc, approx_time = get_moment(args.timezone)
    lat, lng, approx_locale, config_locale = get_locale(args)

    jd_now, jd_then, dt_utc_shifted = sweph.get_julian_days(dt_utc, args)
    offset = getattr(args, 'offset', None)

    dt_local_shifted = dt_utc_shifted.astimezone(dt_local.tzinfo)

    planets = sweph.get_planets(jd_now, jd_then, offset)
    angles = sweph.get_angles(jd_now, lat, lng, offset)
    horoscope = sweph.build_horoscope(planets, angles)
    title = "Chart of the Moment"

    output = format_chart(
        args, title, lat, lng,
        dt_local_shifted, dt_utc_shifted,
        horoscope, planets,
        approx_time, approx_locale, config_locale
    )

    if output is not None:
        for line in output:
            print(line)

    if args.save:
        create_tables()
        add_chart(
            name=title,
            timestamp_utc=dt_utc.isoformat(),
            timestamp_input=dt_local.isoformat(),
            latitude=args.lat,
            longitude=args.lng
        )
