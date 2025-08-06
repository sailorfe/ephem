from constants import FLAGS
from horoscope import get_julian_days, get_planets, get_angles, build_horoscope

from electional import (
    get_moment,
    get_locale,
    parse_arguments,
    print_chart,
    print_raw_placements,
        )

def main():
    args = parse_arguments()
    date_str, time_str = get_moment(args)[0], get_moment(args)[1]
    lat, lng = get_locale(args)
    jd_now, jd_then = get_julian_days(date_str, time_str)
    planets = get_planets(jd_now, jd_then)
    angles = get_angles(jd_now, lat, lng)
    horoscope = build_horoscope(planets, angles)

    if any(getattr(args, key) for key in FLAGS):
        print_raw_placements(args, horoscope)
    else:
        print_chart(args, date_str, time_str, horoscope, planets)

if __name__ == "__main__":
    main()
