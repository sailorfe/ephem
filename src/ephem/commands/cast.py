from ephem.utils import get_locale
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


def get_moment(date=None, time=None):
    """Falls back to hypothetical UTC noon if given no date."""
    if date and time:
        return date, time, False  # explicit time
    if date and not time:
        return date, "12:00", True # approximate time
    return None, None, True


def run(args):
    date, time, title = parse_event(args.event)
    date, time, approx_time = get_moment(date, time)
    lat, lng, approx_locale, config_locale = get_locale(args)
    jd_now, jd_then = get_julian_days(date, time, args)
    planets = get_planets(jd_now, jd_then)
    angles = get_angles(jd_now, lat, lng)
    horoscope = build_horoscope(planets, angles)
    dt = jd_to_datetime(jd_now)
    output = format_chart(args, title, lat, lng, dt, horoscope, planets, approx_time, approx_locale, config_locale)

    if output is not None:
        for line in output:
            print(line)
    # else: Rich already printed, so do nothing here
