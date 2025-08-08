from chart import (
    save_config,
    get_moment,
    get_locale,
    parse_arguments,
    get_julian_days,
    jd_to_datetime,
    get_planets,
    get_angles,
    build_horoscope,
    format_chart
    )

def main():
    args = parse_arguments()

    if not vars(args):
        args.print_help()
        args.exit(1)

    if args.save_config:
        save_config(args)
        return

    if args.command in ["cast", "now"]:
        date_str, time_str, approx_time = get_moment(args)
        lat, lng, approx_locale = get_locale(args)
        jd_now, jd_then = get_julian_days(date_str, time_str, args)
        planets = get_planets(jd_now, jd_then)
        angles = get_angles(jd_now, lat, lng)
        horoscope = build_horoscope(planets, angles)
        dt = jd_to_datetime(jd_now)
        output = format_chart(args, lat, lng, dt, horoscope, planets, approx_time, approx_locale)
        for line in output:
            print(line)


if __name__ == '__main__':
    main()
