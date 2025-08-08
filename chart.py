from chart.cli import parse_arguments, parse_event
from chart.intake import get_moment, get_locale
from chart.julian import get_julian_days, jd_to_datetime
from chart.horoscope import get_planets, get_angles, build_horoscope
from chart.display import format_chart
from chart.config import save_config

def main():
    args = parse_arguments()

    if not vars(args):
        args.print_help()
        args.exit(1)

    if args.save_config:
        save_config(args)
        return

    if args.command in ["cast", "now"]:
        date, time, title = parse_event(args.event)
        date_str, time_str, approx_time = get_moment(args, date, time)
        lat, lng, approx_locale, config_locale = get_locale(args)
        jd_now, jd_then = get_julian_days(date_str, time_str, args)
        planets = get_planets(jd_now, jd_then)
        angles = get_angles(jd_now, lat, lng)
        horoscope = build_horoscope(planets, angles)
        dt = jd_to_datetime(jd_now)
        output = format_chart(args, title, lat, lng, dt, horoscope, planets, approx_time, approx_locale, config_locale)
        for line in output:
            print(line)


if __name__ == '__main__':
    main()
