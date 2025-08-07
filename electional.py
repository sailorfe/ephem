from cli import parse_arguments

from horoscope import (
        get_julian_days,
        get_planets,
        get_angles,
        build_horoscope
        )

from chart import (
    get_moment,
    get_locale,
    jd_to_datetime,
    print_chart
    )

def main():
    args = parse_arguments()
    if not vars(args):
        args.print_help()
        args.exit(1)
    if args.command == "chart" or args.command == "now":
        date_str, time_str = get_moment(args)[0], get_moment(args)[1]
        lat, lng = get_locale(args)
        jd_now, jd_then = get_julian_days(date_str, time_str, args)
        planets = get_planets(jd_now, jd_then)
        angles = get_angles(jd_now, lat, lng)
        horoscope = build_horoscope(planets, angles)
        dt = jd_to_datetime(jd_now)
        print_chart(args, lat, lng, dt, horoscope, planets)

if __name__ == '__main__':
    main()
