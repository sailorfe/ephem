def build_horoscope(planets, angles, part_of_fortune):
    horoscope = {}
    all_positions = planets + angles + part_of_fortune

    for position in all_positions:
        horoscope[position.obj.key] = position

    return horoscope
