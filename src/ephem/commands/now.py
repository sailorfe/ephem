from datetime import datetime, timezone
from ephem.utils import get_locale
from ephem.julian import get_julian_days, jd_to_datetime
from ephem.horoscope import get_planets, get_angles, build_horoscope
from ephem.display import format_chart


def get_moment():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), False


def run(args):
    date, time, approx_time = get_moment()
    lat, lng, approx_locale, config_locale = get_locale(args)
    jd_now, jd_then = get_julian_days(date, time, args)
    planets = get_planets(jd_now, jd_then)
    angles = get_angles(jd_now, lat, lng)
    horoscope = build_horoscope(planets, angles)
    dt = jd_to_datetime(jd_now)
    title = "Chart of the Moment"
    output = format_chart(args, title, lat, lng, dt, horoscope, planets, approx_time, approx_locale, config_locale)

    if output is not None:
        for line in output:
            print(line)
    # else: Rich already printed, so do nothing here
