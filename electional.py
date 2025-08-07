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
    print_chart
    )

from clock import (
        get_now,
        get_here,
        print_asc
        )

def main():
    args = parse_arguments()
    if not vars(args):
        args.print_help()
        args.exit(1)
    if args.command == "chart":
        date_str, time_str = get_moment(args)[0], get_moment(args)[1]
        lat, lng = get_locale(args)
        jd_now, jd_then = get_julian_days(date_str, time_str)
        planets = get_planets(jd_now, jd_then)
        angles = get_angles(jd_now, lat, lng)
        horoscope = build_horoscope(planets, angles)
        print_chart(args, date_str, time_str, horoscope, planets)
    elif args.command == "asc":
        date_str, time_str = get_now()
        lat, lng = get_here(args)
        jd_now = get_julian_days(date_str, time_str)[0]
        angles = get_angles(jd_now, lat, lng)
        print_asc(angles)

if __name__ == '__main__':
    main()
