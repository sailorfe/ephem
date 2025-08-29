from ephem.constants import OBJECTS

def build_horoscope(planets, angles):
    """
    Build horoscope dictionary with data for location in DMS,
    including sign qualities/elements and retrograde info.
    """
    horoscope = {}
    all_bodies = planets + angles

    for body in all_bodies:
        obj_data = OBJECTS[body['obj_key']]

        entry = {
            "obj_name": obj_data['name'],
            "obj_glyph": obj_data['glyph'],
            "deg": body['deg'],
            "mnt": body['mnt'],
            "sec": body['sec'],
            "sign": body['sign'],
            "sign_trunc": body['trunc'],
            "sign_glyph": body['glyph'],
            "trip": body['trip'],
            "quad": body['quad'],
            "rx": body.get('rx', False),
        }

        # pre-rendered strings for display
        entry["full"] = f"{entry['deg']:>2} {entry['sign']} {entry['mnt']} {entry['sec']}{' r' if entry['rx'] else ''}"
        entry["short"] = f"{entry['deg']:>2} {entry['sign_trunc']} {entry['mnt']}{' r' if entry['rx'] else ''}"
        entry["glyph"] = f"{entry['deg']:>2} {entry['sign_glyph']} {entry['mnt']}{' r' if entry['rx'] else ''}"

        horoscope[body['obj_key']] = entry

    return horoscope
