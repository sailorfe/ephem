from horoscope import get_julian_days, get_angles

from electional import (
        get_locale,
        )

from clock import (
        get_moment,
        parse_arguments,
        print_asc
        )

def main():
    args = parse_arguments()
    date_str, time_str = get_moment()[0], get_moment()[1]
    lat, lng = get_locale(args)
    jd_now, jd_before = get_julian_days(date_str, time_str)
    angles = get_angles(jd_now, lat, lng)

    print_asc(angles)

if __name__ == "__main__":
    main()
